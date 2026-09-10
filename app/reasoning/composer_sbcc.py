import os
import json

class MessagePlanComposer:
    def __init__(self, kb_dir=None):
        if not kb_dir:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            kb_dir = os.path.join(current_dir, "../../knowledge_base")
        
        self.sem_path = os.path.join(kb_dir, "kb_sem_msg.json")
        self.claims_path = os.path.join(kb_dir, "kb_claims.json")
        
        self.sem_data = self._load_json(self.sem_path)
        self.claims_data = self._load_json(self.claims_path)

    def _load_json(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"File basis pengetahuan tidak ditemukan: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def compose_plan(self, topic, audience, functions, filter_3t_result, custom_do_action=None):
        """
        Menyusun rancangan pesan know-feel-do dan struktur rencana 4Ms.
        topic: string, e.g. "tablet_tambah_darah" | "asi_eksklusif"
        audience: string, e.g. "remaja putri"
        functions: list of dict dari InterventionMapper.map_interventions
        filter_3t_result: dict dari Context3TFilter.apply_filter
        custom_do_action: string aksi opsional yang dimasukkan petugas
        """
        # 1. Ambil whitelist claims berdasarkan topik
        topic_claims = None
        for item in self.claims_data:
            if item["topic"] == topic:
                topic_claims = item
                break
        
        if not topic_claims:
            raise ValueError(f"Topik kesehatan '{topic}' tidak ditemukan di database kb_claims.json.")

        approved_claims = topic_claims["approved_claims"]
        prohibited_claims = topic_claims["prohibited_claims"]

        # 2. Tentukan Level SEM yang Relevan
        # Kita bisa memetakan secara dinamis berdasarkan sasaran utama
        sem_levels = self.sem_data.get("sem_levels", [])
        active_sem = []
        
        # Secara umum, SBCC menargetkan 3 level pertama untuk aksi dasar
        # Kita sertakan level sesuai profil intervensi
        for sl in sem_levels:
            if sl["level"] in ["individual", "interpersonal", "community"]:
                active_sem.append(sl)

        # 3. Tentukan kerangka isi Slot Pesan (Know - Feel - Do)
        function_names = [f["function"] for f in functions]
        
        # Slot KNOW diisi dengan rekomendasi klaim dari database
        know_slots = approved_claims[:3] # Default ambil 3 klaim pertama untuk diproses
        
        # Slot FEEL bergantung pada fungsi Persuasion atau Modelling
        feel_slots = []
        if "Persuasion" in function_names or "Modelling" in function_names:
            feel_slots.append("Membangun rasa percaya diri dan menepis ketakutan akan efek samping atau mitos.")
            feel_slots.append("Menunjukkan kebanggaan sosial bahwa banyak orang/teman lain melakukannya.")
        else:
            feel_slots.append("Mendorong rasa nyaman dan kebiasaan sehat baru.")

        # Slot DO berupa tindakan spesifik. Jika ada custom_do_action dari user, pakai itu.
        # Jika tidak, berikan default berdasarkan topik.
        do_action = custom_do_action
        if not do_action:
            if topic == "tablet_tambah_darah":
                do_action = "Minum 1 tablet tambah darah secara rutin setiap minggu (misal setiap hari Jumat) sesudah makan malam."
            elif topic == "asi_eksklusif":
                do_action = "Berikan hanya ASI saja secara eksklusif sesering mungkin (minimal 8-12 kali sehari) tanpa tambahan makanan/minuman lain hingga bayi berumur 6 bulan."
            elif topic == "imunisasi_dasar":
                do_action = "Bawa bayi ke Posyandu atau Puskesmas sesuai jadwal untuk mendapatkan 5 jenis imunisasi dasar lengkap sebelum berusia 1 tahun."
            elif topic == "stop_babs":
                do_action = "Buang air besar hanya di jamban sehat (leher angsa dengan septik tank kedap air) dan selalu cuci tangan pakai sabun setelahnya."
            elif topic == "pencegahan_stunting":
                do_action = "Ibu hamil meminum Tablet Tambah Darah (TTD) secara rutin, serta berikan makanan tambahan (PMT) kaya protein hewani seperti telur atau ikan setiap hari kepada balita."
            elif topic == "pencegahan_malaria":
                do_action = "Tidur menggunakan kelambu berinsektisida secara rutin setiap malam dan segera periksakan darah ke Puskesmas/Pos Malaria Desa jika mengalami gejala demam."
            elif topic == "pencegahan_dbd":
                do_action = "Lakukan gerakan 3M Plus minimal sekali seminggu (menguras, menutup, mendaur ulang wadah air) serta gunakan losion anti nyamuk untuk pencegahan tambahan."
            elif topic == "pencegahan_tbc":
                do_action = "Lakukan pemeriksaan dahak (TCM) jika mengalami batuk lebih dari 2 minggu dan pastikan meminum Obat Anti Tuberkulosis (OAT) secara tuntas selama 6 bulan tanpa putus."
            else:
                do_action = "Lakukan perilaku hidup bersih dan sehat sesuai instruksi petugas."

        # 4. Tentukan Pilar 4Ms
        # Mobilizers dari filter 3T
        mobilizers = filter_3t_result.get("mobilizers", ["Kader Posyandu"])
        
        # Multipliers dari filter 3T
        multipliers = filter_3t_result.get("eligible_channels", ["tatap_muka"])
        
        # Motivators dari fungsi BCW (Incentivisation / Modelling)
        motivators = []
        if "Incentivisation" in function_names:
            motivators.append("Apresiasi/penghargaan sosial bagi yang patuh (misal: penghargaan kelas terpatuh, pemberian PMT).")
        if "Modelling" in function_names:
            mobilizer_examples = ", ".join(mobilizers[:2])
            motivators.append(f"Demonstrasi langsung dan testimoni keberhasilan dari {mobilizer_examples}.")
        if not motivators:
            motivators.append("Pemberian dukungan emosional keluarga dan penjelasan mengenai masa depan sehat berprestasi.")

        return {
            "topic_title": topic_claims["title"],
            "topic_description": topic_claims["description"],
            "sem_levels": active_sem,
            "message_slots": {
                "know": know_slots,
                "feel": feel_slots,
                "do": do_action
            },
            "four_ms": {
                "mobilizers": mobilizers,
                "multipliers": multipliers,
                "motivators": motivators
            },
            "prohibited_claims_guard": prohibited_claims,
            "creative_principles": self.sem_data.get("creative_principles", [])
        }
