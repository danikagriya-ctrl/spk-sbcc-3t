import os
import json

class DiagnosisEngine:
    def __init__(self, kb_dir=None):
        if not kb_dir:
            # Dapatkan path direktori knowledge_base yang berada sejajar dengan app/
            current_dir = os.path.dirname(os.path.abspath(__file__))
            kb_dir = os.path.join(current_dir, "../../knowledge_base")
        
        self.combo_path = os.path.join(kb_dir, "kb_combo.json")
        self.rules_path = os.path.join(kb_dir, "kb_dx_rules.json")
        
        self.components = self._load_json(self.combo_path).get("components", [])
        self.rules_data = self._load_json(self.rules_path)
        self.rules = self.rules_data.get("rules", [])
        self.clarifications = self.rules_data.get("clarifications", [])

    def _load_json(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"File basis pengetahuan tidak ditemukan: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def diagnose(self, signals, behavior_status=None):
        """
        Melakukan diagnosis komponen COM-B yang defisit berdasarkan sinyal hambatan.
        signals: dict berisi signal key dan value boolean, misal {"tidak_tahu_manfaat": True}
        behavior_status: status perilaku (misal: "tetap_tidak_dilakukan" atau "belum_tuntas")
        """
        deficits = set()
        evidence_map = {}
        matched_rules = []

        # 1. Evaluasi aturan IF-THEN
        for rule in self.rules:
            cond = rule["if"]
            signal_name = cond.get("signal")
            target_value = cond.get("value", True)
            
            # Cek kecocokan sinyal dasar
            is_match = signals.get(signal_name) == target_value

            # Cek kondisi tambahan (seperti behavior_status untuk R-DX-O-Ph-03)
            and_behaviour = cond.get("and_behaviour")
            if is_match and and_behaviour:
                if behavior_status != and_behaviour:
                    is_match = False

            if is_match:
                then_clause = rule["then"]
                matched_rules.append(rule["id"])

                # Handle set_deficit
                if "set_deficit" in then_clause:
                    deficit_targets = then_clause["set_deficit"]
                    if isinstance(deficit_targets, str):
                        deficit_targets = [deficit_targets]
                    
                    for target in deficit_targets:
                        deficits.add(target)
                        if target not in evidence_map:
                            evidence_map[target] = []
                        evidence_map[target].append({
                            "rule_id": rule["id"],
                            "evidence": rule["evidence"],
                            "source": rule["source"]
                        })

                # Handle deprioritize
                if "deprioritize" in then_clause:
                    deprio_target = then_clause["deprioritize"]
                    # Jika ada instruksi deprioritize, hapus jika ada di deficits (kecuali jika ada bukti fisik kuat lain)
                    # Di sini jika sarana_tersedia = True dan tetap_tidak_dilakukan = True, 
                    # maka O-Ph (hambatan fisik akses) dicoret dari prioritas utama
                    if deprio_target in deficits and not signals.get("sarana_tidak_tersedia", False):
                        deficits.remove(deprio_target)
                        evidence_map.pop(deprio_target, None)

        # 2. Check clarification loop
        # Jika status komponen COM-B tertentu belum diketahui (tidak diset True/False dalam input signals),
        # dan belum masuk dalam deficits, kita tanyakan pertanyaannya.
        # Untuk kesederhanaan, jika sinyal terkait komponen tersebut semuanya bernilai null/None, kita anggap "unknown".
        clarifications_needed = []
        
        # Mapping komponen ke sinyal-sinyalnya
        component_signals = {
            "C-Ph": ["hambatan_fisik_keterampilan"],
            "C-Ps": ["tidak_tahu_manfaat", "tidak_tahu_cara"],
            "O-Ph": ["sarana_tidak_tersedia", "akses_jauh_atau_biaya_mahal"],
            "O-So": ["mitos_atau_stigma", "keluarga_tidak_mendukung"],
            "M-Re": ["merasa_tidak_perlu_atau_sehat", "tidak_berniat"],
            "M-Au": ["takut_efek_samping", "malas_atau_lupa_kebiasaan"]
        }

        for clarif in self.clarifications:
            target_comp = clarif["if_unknown"]
            
            # Jika komponen ini belum terbukti defisit
            if target_comp not in deficits:
                # Cek apakah semua sinyal terkait komponen ini bernilai None / tidak ada di input
                signals_for_comp = component_signals.get(target_comp, [])
                is_unknown = all(signals.get(s) is None for s in signals_for_comp)
                
                if is_unknown:
                    clarifications_needed.append({
                        "component": target_comp,
                        "question": clarif["ask"],
                        "id": clarif["id"]
                    })

        return {
            "deficits": list(deficits),
            "evidence": evidence_map,
            "matched_rules": matched_rules,
            "clarifications_needed": clarifications_needed,
            "is_complete": len(clarifications_needed) == 0
        }
