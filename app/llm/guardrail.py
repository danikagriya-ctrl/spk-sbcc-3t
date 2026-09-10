import json
from app.llm.client import GeminiClient

class SafetyGuardrail:
    def __init__(self):
        self.client = GeminiClient()

    def verify_claims(self, realized_text, approved_claims, prohibited_claims):
        """
        Memverifikasi secara semantik apakah teks hasil narasi LLM melanggar batasan medis
        atau menambahkan klaim kesehatan di luar whitelist.
        Mengembalikan tuple: (is_safe: bool, reason: str)
        """
        # Jika API key tidak ada, langsung anggap aman untuk mock/offline
        from app.config import Config
        if not Config.GEMINI_API_KEY or Config.GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
            return True, "Mode offline: Lolos verifikasi otomatis."

        system_instruction = (
            "Anda adalah auditor medis independen yang sangat ketat untuk Kementerian Kesehatan. "
            "Tugas Anda adalah memeriksa apakah pesan promosi kesehatan di bawah ini AMAN secara medis "
            "dan TIDAK menambahkan klaim baru di luar daftar fakta ilmiah terverifikasi yang diberikan."
        )

        prompt = f"""
Daftar Klaim Kesehatan Terverifikasi (WHITELIST):
{json.dumps(approved_claims, indent=2)}

Daftar Klaim/Topik yang DILARANG:
{json.dumps(prohibited_claims, indent=2)}

Teks Pesan Promosi Kesehatan yang Diperiksa:
"{realized_text}"

Lakukan analisis kepatuhan:
1. Apakah teks pesan memuat fakta medis baru yang TIDAK ADA dalam daftar WHITELIST? (Penting: Implikasi gaya bahasa yang natural tidak dianggap fakta medis baru selama maknanya sama).
2. Apakah teks pesan melanggar daftar hal yang DILARANG?

Kembalikan jawaban Anda dalam format JSON berikut:
{{
  "is_safe": true/false,
  "reason": "jelaskan alasan keputusan Anda secara ringkas dan objektif"
}}
"""

        response_text = self.client.generate(prompt, system_instruction=system_instruction, json_mode=True)
        
        try:
            data = json.loads(response_text)
            return data.get("is_safe", True), data.get("reason", "Lolos audit.")
        except Exception as e:
            print(f"[ERROR] Gagal memparsing JSON hasil guardrail: {e}")
            return True, "Lolos (Error parsing guardrail: diloloskan secara default)."
