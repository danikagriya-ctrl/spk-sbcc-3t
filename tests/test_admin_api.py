import os
import sys
import unittest
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

class TestAdminAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_admin_login(self):
        # 1. Login dengan password salah (harus gagal)
        response = self.client.post("/api/admin/login", json={
            "username": "admin",
            "password": "wrongpassword"
        })
        self.assertEqual(response.status_code, 401)
        
        # 2. Login dengan data benar (harus sukses)
        response = self.client.post("/api/admin/login", json={
            "username": "admin",
            "password": "admin123"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")
        self.assertIn("token", response.json())

    def test_kb_claims_endpoints(self):
        response = self.client.get("/api/admin/kb/claims")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) > 0)
        self.assertIn("topic", data[0])

    def test_session_lifecycle(self):
        # 1. Buat sesi analisis baru
        response = self.client.post("/api/analyze", json={
            "topic": "tablet_tambah_darah",
            "user_story": "Remaja putri tidak mau minum obat tambah darah di sekolah.",
            "profile_3t": {
                "konektivitas_internet": "memadai",
                "listrik": "stabil",
                "bahasa_dominan": "Indonesia",
                "literasi": "tinggi",
                "kanal_terpercaya": ["tenaga_kesehatan"],
                "akses_layanan": "dekat",
                "audience": "Remaja Putri"
            }
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        session_id = data["session_id"]
        
        # 2. Edit/Proses ulang sesi
        response = self.client.put(f"/api/admin/session/{session_id}", json={
            "topic": "tablet_tambah_darah",
            "user_story": "Banyak anak lemas di sekolah dan takut minum TTD karena rasanya mual.",
            "profile_3t": {
                "konektivitas_internet": "memadai",
                "listrik": "stabil",
                "bahasa_dominan": "Indonesia",
                "literasi": "tinggi",
                "kanal_terpercaya": ["tenaga_kesehatan", "guru"],
                "akses_layanan": "dekat",
                "audience": "Remaja Putri"
            }
        })
        self.assertEqual(response.status_code, 200)
        
        # 3. Hapus sesi
        response = self.client.delete(f"/api/admin/session/{session_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")

    def test_clarification_with_ragu_answers(self):
        # 1. Buat sesi analisis baru dengan cerita singkat agar memicu pertanyaan klarifikasi
        response = self.client.post("/api/analyze", json={
            "topic": "tablet_tambah_darah",
            "user_story": "Ada masalah anemia pada remaja putri.",
            "profile_3t": {
                "konektivitas_internet": "lemah",
                "listrik": "tidak_stabil",
                "bahasa_dominan": "Indonesia",
                "literasi": "sedang",
                "kanal_terpercaya": ["guru"],
                "akses_layanan": "sedang",
                "audience": "Remaja Putri"
            }
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Jika statusnya pending_clarification, maka jawab semua pertanyaan dengan 'ragu'
        if data.get("status") == "pending_clarification":
            session_id = data["session_id"]
            questions = data["clarification_questions"]
            self.assertTrue(len(questions) > 0)
            
            # Buat jawaban 'ragu' untuk setiap pertanyaan
            answers = {q["id"]: "ragu" for q in questions}
            
            # Kirim jawaban ke API clarify
            response_clarify = self.client.post("/api/clarify", json={
                "session_id": session_id,
                "answers": answers
            })
            self.assertEqual(response_clarify.status_code, 200)
            data_clarify = response_clarify.json()
            
            # Status harus selesai (completed) dan tidak meminta klarifikasi lagi
            self.assertEqual(data_clarify.get("status"), "completed")
            self.assertIn("composed_plan", data_clarify)
            
            # Hapus sesi setelah tes selesai
            self.client.delete(f"/api/admin/session/{session_id}")

if __name__ == "__main__":
    unittest.main()
