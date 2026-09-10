import json
from app.llm.client import GeminiClient

class OutputRealizer:
    def __init__(self):
        self.client = GeminiClient()

    def realize(self, composed_plan, profile_3t):
        """
        Mengubah slot isi pesan terstruktur menjadi kalimat narasi pesan dan rencana komunikasi yang natural.
        composed_plan: dict hasil dari MessagePlanComposer.compose_plan
        profile_3t: dict berisi profil 3T (bahasa_dominan, literasi, dll)
        """
        language = profile_3t.get("bahasa_dominan", "Indonesia")
        literacy = profile_3t.get("literasi", "tinggi")
        
        system_instruction = (
            "Anda adalah ahli komunikasi perubahan perilaku sosial (SBCC) terkemuka dari UNICEF. "
            "Tugas Anda adalah menarasikan rancangan pesan dan rencana komunikasi terstruktur yang diberikan "
            "menjadi bahasa yang sangat natural, menyentuh, mudah dipahami, dan sesuai konteks lokal. "
            "DILARANG keras menambahkan klaim medis baru di luar apa yang terdaftar di bagian slot 'Know'. "
            "Patuhi prinsip kreatif: bersikap positif (anjuran bukan larangan), spesifik, dan aspiratif."
        )

        prompt = f"""
Berikut adalah rancangan pesan dan rencana komunikasi terstruktur untuk program kesehatan:
Topik: {composed_plan['topic_title']} ({composed_plan['topic_description']})
Sasaran Utama: {profile_3t.get('audience', 'Sasaran Utama')}

Rancangan Slot Isi Pesan:
- KNOW (Pengetahuan): {json.dumps(composed_plan['message_slots']['know'])}
- FEEL (Afektif/Sikap): {json.dumps(composed_plan['message_slots']['feel'])}
- DO (Tindakan): "{composed_plan['message_slots']['do']}"

Struktur Rencana 4Ms:
- Mobilizers (Siapa yang menggerakkan): {json.dumps(composed_plan['four_ms']['mobilizers'])}
- Multipliers (Kanal penyebaran): {json.dumps(composed_plan['four_ms']['multipliers'])}
- Motivators (Faktor pendorong): {json.dumps(composed_plan['four_ms']['motivators'])}

Konteks Daerah 3T:
- Bahasa Dominan: "{language}" (Bila bukan Indonesia, harap sediakan versi Bahasa Indonesia DAN terjemahan versi Bahasa Daerah setempat yang natural menggunakan dialek khas)
- Tingkat Literasi: "{literacy}" (Bila "rendah", buat kalimat yang sangat sederhana, hindari istilah teknis medis yang rumit, dan berikan panduan visualisasi gambar yang harus digambar)

Format Output yang Diharapkan (Kembalikan dalam JSON dengan kunci berikut):
{{
  "headline_message": "Kalimat slogan/pesan utama yang singkat dan menarik perhatian (catchy)",
  "narrative_know_feel_do": {{
    "know": "Kalimat penjelas bagian KNOW yang natural berbasis fakta whitelist di atas",
    "feel": "Kalimat penyentuh bagian FEEL yang mengurangi rasa khawatir atau menepis stigma",
    "do": "Kalimat ajakan bertindak bagian DO yang sangat spesifik dan mudah dipraktikkan"
  }},
  "local_language_version": {{
    "language": "{language}",
    "headline": "headline dalam bahasa daerah (jika bahasa daerah, jika tidak samakan dengan Indonesia)",
    "message": "versi lengkap pesan Know-Feel-Do yang digabung secara natural dalam bahasa daerah"
  }},
  "visual_guide": "Panduan visual/ilustrasi gambar apa yang harus dipasang di poster/media cetak agar mudah dipahami sasaran (khususnya untuk literasi rendah/sedang)",
  "plan_4ms_narrative": "Penjelasan singkat bagaimana rencana 4Ms dijalankan di lapangan (misal: bagaimana guru mengedukasi di kelas, bagaimana tokoh agama menyampaikan di rumah ibadah)"
}}
"""

        response_text = self.client.generate(prompt, system_instruction=system_instruction, json_mode=True)
        
        try:
            data = json.loads(response_text)
            return data
        except Exception as e:
            print(f"[ERROR] Gagal memparsing JSON hasil realizer LLM: {e}")
            print(f"Konten asli: {response_text}")
            return {
                "headline_message": "Ayo Hidup Sehat!",
                "narrative_know_feel_do": {
                    "know": "Penting bagi kita untuk menjaga kesehatan.",
                    "feel": "Jangan takut dan ragu, ini aman demi kebaikan kita bersama.",
                    "do": composed_plan['message_slots']['do']
                },
                "local_language_version": {
                    "language": language,
                    "headline": "Ayo Hidup Sehat!",
                    "message": "Penting bagi kita untuk menjaga kesehatan."
                },
                "visual_guide": "Gambar ilustrasi sederhana yang menunjukkan tindakan sehat.",
                "plan_4ms_narrative": "Menggunakan kader posyandu untuk menyampaikan pesan secara langsung ke rumah-rumah warga."
            }
        
