import os
import uuid
from app.database.models import SessionDatabase
from app.llm.interpreter import InputInterpreter
from app.llm.realizer import OutputRealizer
from app.llm.guardrail import SafetyGuardrail
from app.reasoning.diagnosis_combo import DiagnosisEngine
from app.reasoning.intervention_bcw import InterventionMapper
from app.reasoning.context_3t import Context3TFilter
from app.reasoning.composer_sbcc import MessagePlanComposer

class SessionOrchestrator:
    def __init__(self):
        self.db = SessionDatabase()
        self.interpreter = InputInterpreter()
        self.realizer = OutputRealizer()
        self.guardrail = SafetyGuardrail()
        
        self.diagnosis_engine = DiagnosisEngine()
        self.intervention_mapper = InterventionMapper()
        self.context_filter = Context3TFilter()
        self.composer = MessagePlanComposer()

    def process_new_story(self, topic, user_story, profile_3t):
        """
        Memulai sesi baru, mengekstrak cerita bebas, dan menjalankan diagnosis awal.
        """
        session_id = str(uuid.uuid4())
        self.db.create_session(session_id, topic, user_story, profile_3t)

        # 1. Stasiun 1: Interpretasi Input (LLM)
        extracted = self.interpreter.interpret(user_story)
        self.db.update_session(session_id, extracted_data=extracted)

        # Gabungkan signals
        signals = {}
        # Isi sinyal awal dari ekstraksi LLM
        raw_signals = extracted.get("barrier_signals", {})
        for k, v in raw_signals.items():
            if v is not None:
                signals[k] = v

        # Jalankan diagnosis
        return self._run_evaluation_pipeline(session_id, signals, extracted.get("behavior_status"))

    def process_clarification(self, session_id, answers):
        """
        Menerima jawaban dari pertanyaan klarifikasi, memperbarui sinyal,
        dan melanjutkan alur keputusan.
        answers: dict berisi {"R-CLR-C-Ps": "ya"/"tidak"/"ragu", ...}
        """
        session = self.db.get_session(session_id)
        if not session:
            raise ValueError(f"Sesi {session_id} tidak ditemukan.")

        extracted = session.get("extracted_data", {})
        signals = extracted.get("barrier_signals", {})
        if not signals:
            signals = {}

        # Terjemahkan jawaban klarifikasi ke sinyal diagnosis
        for clarif_id, ans in answers.items():
            ans = ans.lower().strip()
            if clarif_id == "R-CLR-C-Ps":
                if ans == "tidak":
                    signals["tidak_tahu_manfaat"] = True
                    signals["tidak_tahu_cara"] = True
                elif ans == "ya":
                    signals["tidak_tahu_manfaat"] = False
                    signals["tidak_tahu_cara"] = False
                elif ans == "ragu":
                    # Ragu-ragu dianggap berpotensi ada hambatan pengetahuan
                    signals["tidak_tahu_manfaat"] = True
                    signals["tidak_tahu_cara"] = True
            elif clarif_id == "R-CLR-O-So":
                if ans == "ya":
                    signals["mitos_atau_stigma"] = True
                    signals["keluarga_tidak_mendukung"] = True
                elif ans == "tidak":
                    signals["mitos_atau_stigma"] = False
                    signals["keluarga_tidak_mendukung"] = False
                elif ans == "ragu":
                    # Ragu-ragu dianggap berpotensi ada hambatan sosial/mitos
                    signals["mitos_atau_stigma"] = True
                    signals["keluarga_tidak_mendukung"] = True
            elif clarif_id == "R-CLR-M-Au":
                if ans == "ya":
                    signals["takut_efek_samping"] = True
                    signals["malas_atau_lupa_kebiasaan"] = True
                elif ans == "tidak":
                    signals["takut_efek_samping"] = False
                    signals["malas_atau_lupa_kebiasaan"] = False
                elif ans == "ragu":
                    # Ragu-ragu dianggap berpotensi ada hambatan motivasi
                    signals["takut_efek_samping"] = True
                    signals["malas_atau_lupa_kebiasaan"] = True

        # Update database dengan sinyal baru
        extracted["barrier_signals"] = signals
        self.db.update_session(session_id, extracted_data=extracted)

        return self._run_evaluation_pipeline(session_id, signals, extracted.get("behavior_status"))

    def _run_evaluation_pipeline(self, session_id, signals, behavior_status):
        """
        Menjalankan stasiun 2 (diagnosis) hingga stasiun 5 (realisasi pesan)
        jika tidak ada lagi pertanyaan klarifikasi yang tersisa.
        """
        session = self.db.get_session(session_id)
        topic = session["topic"]
        profile_3t = session["profile_3t"]

        # 2. Stasiun 2: Diagnosis COM-B (Rule-based)
        dx_result = self.diagnosis_engine.diagnose(signals, behavior_status)
        self.db.update_session(session_id, diagnosis_result=dx_result)

        # Jika masih butuh klarifikasi, hentikan dan kembalikan pertanyaan balik ke UI
        if not dx_result["is_complete"]:
            self.db.update_session(
                session_id, 
                status="pending_clarification", 
                clarification_questions=dx_result["clarifications_needed"]
            )
            return {
                "session_id": session_id,
                "status": "pending_clarification",
                "clarification_questions": dx_result["clarifications_needed"],
                "diagnosis_so_far": dx_result["deficits"]
            }

        # 3. Stasiun 3: Pemetaan Intervensi (Rule-based BCW)
        deficits = dx_result["deficits"]
        # Kasus khusus jika deficits kosong (karena input tidak memiliki hambatan/masalah)
        if not deficits:
            # Berikan default kapabilitas psikologis atau motivasi reflektif agar sistem tetap memberikan edukasi pencegahan
            deficits = ["C-Ps"] 
            dx_result["deficits"] = deficits
            self.db.update_session(session_id, diagnosis_result=dx_result)

        bcw_result = self.intervention_mapper.map_interventions(deficits)
        self.db.update_session(session_id, intervention_result=bcw_result)

        # 4. Stasiun 4: Penyaringan Konteks 3T
        filter_result = self.context_filter.apply_filter(bcw_result["functions"], profile_3t)

        # 5. Stasiun 5: Message & Plan Composer (Rule-based)
        composed = self.composer.compose_plan(
            topic=topic,
            audience=profile_3t.get("audience", "Sasaran Utama"),
            functions=bcw_result["functions"],
            filter_3t_result=filter_result
        )
        self.db.update_session(session_id, composed_plan=composed)

        # 6. Realisasi Output (LLM) + Guardrail
        realized = self.realizer.realize(composed, profile_3t)
        
        # Jalankan audit guardrail klaim whitelist
        # Audit teks know dan teks bahasa daerah
        text_to_audit = f"{realized['narrative_know_feel_do']['know']}. {realized['local_language_version']['message']}"
        is_safe, audit_reason = self.guardrail.verify_claims(
            text_to_audit, 
            composed["message_slots"]["know"], 
            composed["prohibited_claims_guard"]
        )

        realized["safety_audit"] = {
            "is_safe": is_safe,
            "reason": audit_reason
        }
        
        # Update sesi akhir
        self.db.update_session(
            session_id, 
            realized_message=realized, 
            status="completed"
        )

        # Gabungkan semua data untuk dikembalikan ke UI
        return {
            "session_id": session_id,
            "status": "completed",
            "diagnosis": dx_result,
            "intervention": bcw_result,
            "context_3t": filter_result,
            "composed_plan": composed,
            "realized_output": realized
        }

    def process_edited_session(self, session_id, topic, user_story, profile_3t):
        """
        Mengedit sesi yang sudah ada, mengekstrak ulang cerita baru, dan menjalankan diagnosis ulang.
        """
        session = self.db.get_session(session_id)
        if not session:
            raise ValueError(f"Sesi {session_id} tidak ditemukan.")

        # Update data dasar sesi di database
        self.db.update_session(
            session_id, 
            topic=topic, 
            user_story=user_story, 
            profile_3t=profile_3t,
            status="active" # Kembalikan ke active untuk diproses ulang
        )

        # Jalankan ulang ekstraksi Interpreter (LLM)
        extracted = self.interpreter.interpret(user_story)
        self.db.update_session(session_id, extracted_data=extracted)

        # Gabungkan signals
        signals = {}
        raw_signals = extracted.get("barrier_signals", {})
        for k, v in raw_signals.items():
            if v is not None:
                signals[k] = v

        # Jalankan ulang pipa evaluasi
        return self._run_evaluation_pipeline(session_id, signals, extracted.get("behavior_status"))

