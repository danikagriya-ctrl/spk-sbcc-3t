import sys
import os
import traceback

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.orchestrator import SessionOrchestrator

def main():
    orc = SessionOrchestrator()
    
    topic = "tablet_tambah_darah"
    user_story = "kebanyakan remaja potri masih malu-malu untuk ambil table penambah darah sehingga kadang menjadi pucat dalam belajar di sekolah. mukanya menjadi muram dan pucat"
    profile_3t = {
        "konektivitas_internet": "memadai",
        "listrik": "stabil",
        "bahasa_dominan": "Indonesia",
        "literasi": "tinggi",
        "kanal_terpercaya": ["tenaga_kesehatan", "guru", "peer"],
        "akses_layanan": "dekat",
        "audience": "Remaja Putri"
    }
    
    try:
        print("Mulai memproses kasus baru...")
        result = orc.process_new_story(topic, user_story, profile_3t)
        print("Berhasil!")
        print("Status hasil:", result.get("status"))
        print("Pertanyaan Klarifikasi:", result.get("clarification_questions"))
    except Exception as e:
        print("\n=== TERJADI ERROR ===")
        traceback.print_exc()

if __name__ == "__main__":
    main()
