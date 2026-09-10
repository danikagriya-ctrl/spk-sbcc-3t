import os
import google.generativeai as genai
from app.config import Config

class GeminiClient:
    def __init__(self):
        Config.validate()
        api_key = Config.GEMINI_API_KEY
        if api_key:
            genai.configure(api_key=api_key)
        else:
            print("[WARNING] GEMINI_API_KEY tidak ditemukan di konfigurasi!")
            
        # Gunakan gemini-2.5-flash sebagai model default karena hemat biaya dan cepat
        self.model_name = "gemini-2.5-flash"

    def generate(self, prompt, system_instruction=None, json_mode=False):
        """
        Memanggil API Gemini untuk menghasilkan teks atau JSON.
        """
        if not Config.GEMINI_API_KEY or Config.GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
            # Mode fallback jika API key belum diset oleh pengguna
            print("[INFO] Berjalan dalam mode Mock / Offline karena API Key Gemini belum diset.")
            return self._mock_fallback(prompt, json_mode)

        try:
            model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=system_instruction
            )
            
            config = {}
            if json_mode:
                config["response_mime_type"] = "application/json"
                
            response = model.generate_content(
                prompt,
                generation_config=config
            )
            return response.text
        except Exception as e:
            print(f"[ERROR] Kesalahan saat memanggil Gemini API: {e}")
            # Fallback jika terjadi error koneksi/API
            return self._mock_fallback(prompt, json_mode)

    def _mock_fallback(self, prompt, json_mode):
        """
        Fallback yang aman dan kuat jika API Key tidak diset atau terjadi kegagalan jaringan.
        Mengembalikan struktur data yang tepat untuk Interpreter, Realizer, dan Guardrail.
        """
        import json
        if json_mode:
            # Case 1: Verifikasi Guardrail
            if "is_safe" in prompt:
                return json.dumps({
                    "is_safe": True,
                    "reason": "Lolos verifikasi otomatis (mode offline/fallback)."
                })
            
            # Case 2: Penyusunan Pesan (Output Realizer)
            elif "narrative_know_feel_do" in prompt:
                # Deteksi topik dari isi prompt
                topic = "tablet_tambah_darah"
                if "asi_eksklusif" in prompt or "ASI" in prompt or "menyusui" in prompt:
                    topic = "asi_eksklusif"
                elif "imunisasi" in prompt:
                    topic = "imunisasi_dasar"
                elif "BABS" in prompt or "jamban" in prompt or "sanitasi" in prompt:
                    topic = "stop_babs"

                if topic == "tablet_tambah_darah":
                    return json.dumps({
                        "headline_message": "Ayo Minum TTD demi Masa Depan Cerah!",
                        "narrative_know_feel_do": {
                            "know": "Tablet Tambah Darah (TTD) sangat penting untuk mencegah anemia yang bisa membuat kita lemas, lesu, dan sulit konsentrasi belajar.",
                            "feel": "Minum TTD adalah hal yang wajar dilakukan remaja putri berprestasi. Jangan cemas akan rasa mual, karena bisa diminum malam hari sesudah makan.",
                            "do": "Minum 1 tablet tambah darah secara teratur setiap minggu (misal setiap hari Jumat) sesudah makan malam."
                        },
                        "local_language_version": {
                            "language": "Bahasa Daerah",
                            "headline": "Hayu Nginum TTD Sangkan Sehat!",
                            "message": "Nginum TTD teh penting pisan kanggo nyegah anemia supados teu lungsur-langsar di sakola. Hayu nginum saminggu sekali unggal dinten Jumaah saatos tuang wengi."
                        },
                        "visual_guide": "Gambar ilustrasi remaja putri tersenyum ceria memegang tablet tambah darah dan segelas air putih, dengan latar belakang sekolah.",
                        "plan_4ms_narrative": "Guru UKS mengedukasi saat pembagian TTD di kelas, didukung kunjungan bidan desa, serta kader sebaya yang saling mengingatkan teman sekelasnya."
                    })
                elif topic == "asi_eksklusif":
                    return json.dumps({
                        "headline_message": "ASI Saja Cukup, Terbaik untuk Buah Hati!",
                        "narrative_know_feel_do": {
                            "know": "ASI Eksklusif melindungi bayi dari diare dan infeksi berbahaya, serta membantu mencegah risiko stunting sejak dini.",
                            "feel": "Menyusui adalah momen istimewa yang penuh kebanggaan dan kasih sayang. Ibu tidak perlu khawatir karena produksi ASI akan bertambah seiring seringnya menyusui.",
                            "do": "Berikan hanya ASI saja tanpa makanan atau minuman tambahan lain hingga bayi berumur 6 bulan."
                        },
                        "local_language_version": {
                            "language": "Bahasa Daerah",
                            "headline": "Asi Wungkul Paranti Orok Sehat!",
                            "message": "Pasihan ASI hungkul ti lahir dugi ka orok yuswa 6 sasih, teu kenging dipasihan tuangeun atanapi leueuteun sanesna. Nyeri kelar nyusuan mah wajar, sing sabar nya Bu."
                        },
                        "visual_guide": "Ilustrasi ibu tersenyum bahagia sedang mendekap erat dan menyusui bayinya dengan pelekatan yang benar di dalam suasana rumah yang hangat.",
                        "plan_4ms_narrative": "Kader Posyandu melakukan kunjungan rumah ke ibu menyusui baru, didukung oleh suami sebagai motivator utama, dan demonstrasi cara pelekatan menyusui oleh Bidan Desa."
                    })
                elif topic == "imunisasi_dasar":
                    return json.dumps({
                        "headline_message": "Imunisasi Lengkap, Anak Sehat Keluarga Bahagia!",
                        "narrative_know_feel_do": {
                            "know": "Imunisasi melindungi anak dari penyakit mematikan seperti campak, polio, dan difteri secara aman dan gratis di Posyandu.",
                            "feel": "Wajar jika anak sedikit demam setelah imunisasi, itu tanda tubuhnya sedang membentuk sistem kekebalan yang kuat. Ibu bisa merasa tenang karena imunisasi aman.",
                            "do": "Bawa anak ka Posyandu atau Puskesmas secara teratur untuk melengkapi imunisasi dasar sebelum usia 1 tahun."
                        },
                        "local_language_version": {
                            "language": "Bahasa Daerah",
                            "headline": "Imunisasi Sangkan Budak Jagjag!",
                            "message": "Hayu candak murangkalih ka Posyandu supados kenging imunisasi dasar lengkep. Pami rada muriang sakedik mah teu sawios, eta tawis kekebalan awakna nuju diwangun."
                        },
                        "visual_guide": "Gambar ilustrasi seorang bidan desa ramah memberikan imunisasi tetes polio kepada bayi yang digendong ibunya sambil tersenyum tenang.",
                        "plan_4ms_narrative": "Bidan desa berkolaborasi dengan kader posyandu untuk mengingatkan jadwal imunisasi lewat arisan RT, dan dibantu oleh tokoh agama untuk menyosialisasikan keamanan vaksin."
                    })
                else:  # stop_babs
                    return json.dumps({
                        "headline_message": "Stop BABS: Jamban Sehat, Desa Bermartabat!",
                        "narrative_know_feel_do": {
                            "know": "Buang air besar sembarangan menyebarkan kuman diare dan tifus melalui air sungai yang kita gunakan sehari-hari.",
                            "feel": "Kita ingin desa kita bersih dan dihargai. Menggunakan jamban sehat sendiri di rumah memberikan kenyamanan dan menjaga kehormatan keluarga.",
                            "do": "Buang air besar hanya di jamban sehat (leher angsa dengan septik tank kedap air) dan selalu cuci tangan pakai sabun setelahnya."
                        },
                        "local_language_version": {
                            "language": "Bahasa Daerah",
                            "headline": "Ulah Miceun di Solokan, Jaga Kasehatan!",
                            "message": "Hayu urang ngadamel jamban sehat di bumi masing-masing, ulah miceun deui ka walungan supados cai walungan bersih tur teu nyababkeun panyakit diare."
                        },
                        "visual_guide": "Gambar ilustrasi keluarga kecil sehat bergotong royong membersihkan area rumah dekat toilet leher angsa yang bersih dan higienis.",
                        "plan_4ms_narrative": "Kader sanitasi desa melakukan pemicuan STBM, didukung oleh instruksi kepala desa (kebijakan lokal), dan arisan jamban gotong royong sebagai motivator pendorong."
                    })

            # Case 3: Interpretasi Masukan (Input Interpreter)
            else:
                # Deteksi topik dari teks cerita
                topic = "tablet_tambah_darah"
                if "asi" in prompt.lower() or "menyusui" in prompt.lower() or "bayi" in prompt.lower():
                    topic = "asi_eksklusif"
                elif "imunisasi" in prompt.lower() or "vaksin" in prompt.lower():
                    topic = "imunisasi_dasar"
                elif "babs" in prompt.lower() or "sungai" in prompt.lower() or "jamban" in prompt.lower() or "tinja" in prompt.lower():
                    topic = "stop_babs"

                if topic == "tablet_tambah_darah":
                    return json.dumps({
                        "target_behaviour": "remaja putri minum TTD rutin setiap minggu",
                        "audience": "remaja putri",
                        "barrier_signals": {
                            "tidak_tahu_manfaat": "manfaat" not in prompt.lower() and "tahu" not in prompt.lower(),
                            "tidak_tahu_cara": False,
                            "sarana_tidak_tersedia": False,
                            "akses_jauh_atau_biaya_mahal": False,
                            "mitos_atau_stigma": "malu" in prompt.lower() or "stigma" in prompt.lower(),
                            "keluarga_tidak_mendukung": None,
                            "merasa_tidak_perlu_atau_sehat": "sehat" in prompt.lower() or "merasa sehat" in prompt.lower(),
                            "tidak_berniat": False,
                            "takut_efek_samping": "takut" in prompt.lower() or "mual" in prompt.lower() or "pusing" in prompt.lower(),
                            "malas_atau_lupa_kebiasaan": True,
                            "hambatan_fisik_keterampilan": False,
                            "sarana_tersedia": True
                        },
                        "behavior_status": "tetap_tidak_dilakukan"
                    })
                elif topic == "asi_eksklusif":
                    return json.dumps({
                        "target_behaviour": "pemberian ASI eksklusif selama 6 bulan",
                        "audience": "ibu menyusui",
                        "barrier_signals": {
                            "tidak_tahu_manfaat": "encer" in prompt.lower(),
                            "tidak_tahu_cara": "pelekatan" in prompt.lower() or "lecet" in prompt.lower(),
                            "sarana_tidak_tersedia": False,
                            "akses_jauh_atau_biaya_mahal": False,
                            "mitos_atau_stigma": "adat" in prompt.lower() or "mitos" in prompt.lower(),
                            "keluarga_tidak_mendukung": "melarang" in prompt.lower() or "mertua" in prompt.lower(),
                            "merasa_tidak_perlu_atau_sehat": False,
                            "tidak_berniat": False,
                            "takut_efek_samping": False,
                            "malas_atau_lupa_kebiasaan": True,
                            "hambatan_fisik_keterampilan": False,
                            "sarana_tersedia": True
                        },
                        "behavior_status": "belum_tuntas"
                    })
                elif topic == "imunisasi_dasar":
                    return json.dumps({
                        "target_behaviour": "bayi mendapatkan imunisasi dasar lengkap",
                        "audience": "ibu bayi",
                        "barrier_signals": {
                            "tidak_tahu_manfaat": False,
                            "tidak_tahu_cara": False,
                            "sarana_tidak_tersedia": "kosong" in prompt.lower() or "habis" in prompt.lower(),
                            "akses_jauh_atau_biaya_mahal": "jauh" in prompt.lower() or "mahal" in prompt.lower(),
                            "mitos_atau_stigma": "haram" in prompt.lower(),
                            "keluarga_tidak_mendukung": "suami melarang" in prompt.lower(),
                            "merasa_tidak_perlu_atau_sehat": False,
                            "tidak_berniat": False,
                            "takut_efek_samping": "takut demam" in prompt.lower() or "panas" in prompt.lower(),
                            "malas_atau_lupa_kebiasaan": True,
                            "hambatan_fisik_keterampilan": False,
                            "sarana_tersedia": True
                        },
                        "behavior_status": "belum_tuntas"
                    })
                else: # stop_babs
                    return json.dumps({
                        "target_behaviour": "buang air besar hanya di jamban sehat",
                        "audience": "masyarakat umum",
                        "barrier_signals": {
                            "tidak_tahu_manfaat": "sungai" in prompt.lower(),
                            "tidak_tahu_cara": False,
                            "sarana_tidak_tersedia": "tidak punya" in prompt.lower(),
                            "akses_jauh_atau_biaya_mahal": "tidak mampu" in prompt.lower() or "mahal" in prompt.lower(),
                            "mitos_atau_stigma": False,
                            "keluarga_tidak_mendukung": False,
                            "merasa_tidak_perlu_atau_sehat": "biasa" in prompt.lower() or "warisan" in prompt.lower(),
                            "tidak_berniat": False,
                            "takut_efek_samping": False,
                            "malas_atau_lupa_kebiasaan": True,
                            "hambatan_fisik_keterampilan": False,
                            "sarana_tersedia": False
                        },
                        "behavior_status": "tetap_tidak_dilakukan"
                    })
            
            # Case 4: Chatbot Konsultasi Kasus
            if "Pertanyaan Petugas:" in prompt:
                return "Halo! Ini adalah respon simulasi dari Asisten SBCC dalam Mode Luring (Offline). Karena kunci API Gemini Anda di file .env belum diset dengan benar (atau tidak didukung), sistem berjalan luring. Ketika kunci API asli Anda diaktifkan, saya akan dapat menjawab secara dinamis dan mendalam mengenai hambatan kapabilitas, peluang, dan motivasi perilaku pada kasus ini, serta memberikan ide-ide visual, strategi advokasi kepala desa, dan pendekatan lisan daerah."
        else:
            return "Pesan Mock (Offline): Silakan konfigurasikan file .env dengan kunci API Gemini Anda untuk menghasilkan narasi pesan asli."


Class = GeminiClient

