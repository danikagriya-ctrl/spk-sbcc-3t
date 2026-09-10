import json
from app.llm.client import GeminiClient

class InputInterpreter:
    def __init__(self):
        self.client = GeminiClient()

    def interpret(self, user_story):
        """
        Mengekstrak variabel terstruktur dari cerita bebas petugas menggunakan Gemini.
        """
        system_instruction = (
            "Anda adalah asisten AI ekstraksi informasi untuk Sistem Pendukung Keputusan kesehatan. "
            "Tugas Anda HANYA mengekstrak informasi dari teks bebas yang diberikan oleh pengguna ke dalam skema JSON. "
            "DILARANG keras melakukan diagnosis sendiri atau menyimpulkan intervensi. Cukup petakan teks bebas "
            "menjadi kunci-kunci sinyal hambatan yang disediakan. Jika suatu hambatan tidak disinggung sama sekali "
            "dalam teks, berikan nilai null (tidak diketahui). Jika disinggung dan merupakan hambatan, berikan nilai true. "
            "Jika disinggung dan dinyatakan aman/bukan hambatan, berikan nilai false."
        )

        prompt = f"""
Bacalah cerita masalah lapangan berikut:
"{user_story}"

Ekstrak informasi di atas ke dalam format JSON berikut dengan kunci-kunci yang persis sama:
{{
  "target_behaviour": "tuliskan secara ringkas perilaku apa yang ingin dicapai (misal: minum tablet tambah darah setiap minggu)",
  "audience": "tuliskan kelompok sasaran utama (misal: remaja putri, ibu hamil, bayi)",
  "barrier_signals": {{
    "tidak_tahu_manfaat": true/false/null,
    "tidak_tahu_cara": true/false/null,
    "sarana_tidak_tersedia": true/false/null,
    "akses_jauh_atau_biaya_mahal": true/false/null,
    "mitos_atau_stigma": true/false/null,
    "keluarga_tidak_mendukung": true/false/null,
    "merasa_tidak_perlu_atau_sehat": true/false/null,
    "tidak_berniat": true/false/null,
    "takut_efek_samping": true/false/null,
    "malas_atau_lupa_kebiasaan": true/false/null,
    "hambatan_fisik_keterampilan": true/false/null,
    "sarana_tersedia": true/false/null
  }},
  "behavior_status": "tetap_tidak_dilakukan" atau "belum_tuntas" atau null
}}

Catatan penting:
- "sarana_tersedia" bernilai true jika sarana kesehatan (seperti obat, tablet, jamban) sebenarnya sudah ada/tersedia di puskesmas atau desa.
- "behavior_status" diset menjadi "tetap_tidak_dilakukan" jika sarana sudah ada namun perilaku tetap sama sekali tidak terjadi, jika tidak berikan null.
"""

        response_text = self.client.generate(prompt, system_instruction=system_instruction, json_mode=True)
        
        try:
            data = json.loads(response_text)
            return data
        except Exception as e:
            print(f"[ERROR] Gagal memparsing JSON hasil interpreter LLM: {e}")
            print(f"Konten asli: {response_text}")
            # Kembalikan struktur default kosong
            return {
                "target_behaviour": "Tidak teridentifikasi",
                "audience": "Masyarakat umum",
                "barrier_signals": {},
                "behavior_status": None
            }
