import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List

from app.config import Config
from app.llm.client import GeminiClient
from app.orchestrator import SessionOrchestrator
from app.database.models import SessionDatabase

app = FastAPI(
    title="SPK-SBCC 3T API",
    description="Sistem Pendukung Keputusan Berbasis AI untuk Perancangan Komunikasi Perubahan Sosial dan Perilaku di Wilayah 3T",
    version="1.0.0"
)

# Aktifkan CORS agar frontend eksternal (jika ada) bisa mengakses
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = SessionOrchestrator()
db = SessionDatabase()
gemini_client = GeminiClient()

# Validasi API key di log saat startup
Config.validate()

# Model Pydantic untuk Request
class Profile3T(BaseModel):
    konektivitas_internet: str  # tidak_ada | lemah | memadai
    listrik: str                 # tidak_stabil | stabil
    bahasa_dominan: str          # Indonesia | Sunda | Jawa | dll
    literasi: str                # rendah | sedang | tinggi
    kanal_terpercaya: List[str]
    akses_layanan: str           # jauh | sedang | dekat
    audience: str                # sasaran spesifik (misal: Remaja Putri)

class AnalyzeRequest(BaseModel):
    topic: str
    user_story: str
    profile_3t: Profile3T

class ClarifyRequest(BaseModel):
    session_id: str
    answers: Dict[str, str]

# API Endpoint
@app.get("/api/topics")
def get_supported_topics():
    """
    Mengambil daftar topik kesehatan terdaftar beserta deskripsinya dari database whitelist.
    """
    try:
        from app.reasoning.composer_sbcc import MessagePlanComposer
        composer = MessagePlanComposer()
        topics = []
        for item in composer.claims_data:
            topics.append({
                "id": item["topic"],
                "title": item["title"],
                "description": item["description"]
            })
        return topics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze")
def analyze_story(req: AnalyzeRequest):
    """
    Memulai analisis kasus kesehatan dan diagnosis perilaku baru.
    """
    try:
        profile_dict = req.profile_3t.dict()
        result = orchestrator.process_new_story(
            topic=req.topic,
            user_story=req.user_story,
            profile_3t=profile_dict
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/clarify")
def clarify_session(req: ClarifyRequest):
    """
    Mengirimkan jawaban pertanyaan klarifikasi untuk melanjutkan diagnosis.
    """
    try:
        result = orchestrator.process_clarification(
            session_id=req.session_id,
            answers=req.answers
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/history")
def get_session_history():
    """
    Mengambil daftar riwayat sesi analisis.
    """
    try:
        return db.list_sessions()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/session/{session_id}")
def get_session_detail(session_id: str):
    """
    Mengambil detail hasil keputusan untuk satu sesi.
    """
    try:
        session = db.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Sesi tidak ditemukan.")
        return session
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Model Pydantic untuk Admin
class AdminLoginRequest(BaseModel):
    username: str
    password: str

class AdminEditRequest(BaseModel):
    topic: str
    user_story: str
    profile_3t: Profile3T

# Endpoint Admin
@app.post("/api/admin/login")
def admin_login(req: AdminLoginRequest):
    """
    Endpoint otentikasi login admin sederhana.
    """
    if req.username == Config.ADMIN_USERNAME and req.password == Config.ADMIN_PASSWORD:
        return {"status": "success", "token": "admin_logged_in_token_spk_sbcc_3t"}
    raise HTTPException(status_code=401, detail="Username atau password admin salah.")

@app.delete("/api/admin/session/{session_id}")
def delete_session_record(session_id: str):
    """
    Menghapus sesi analisis secara permanen dari database.
    """
    try:
        db.delete_session(session_id)
        return {"status": "success", "message": f"Sesi {session_id} berhasil dihapus."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/admin/session/{session_id}")
def edit_session_record(session_id: str, req: AdminEditRequest):
    """
    Mengedit detail cerita/profil dan men-diagnose ulang kasus tersebut.
    """
    try:
        profile_dict = req.profile_3t.dict()
        result = orchestrator.process_edited_session(
            session_id=session_id,
            topic=req.topic,
            user_story=req.user_story,
            profile_3t=profile_dict
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Path untuk file database claims
kb_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../knowledge_base")
claims_path = os.path.join(kb_dir, "kb_claims.json")

@app.get("/api/admin/kb/claims")
def get_kb_claims():
    """
    Mengambil data mentah dari kb_claims.json untuk diedit di UI Admin.
    """
    try:
        import json
        if not os.path.exists(claims_path):
            raise HTTPException(status_code=404, detail="File kb_claims.json tidak ditemukan.")
        with open(claims_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/admin/kb/claims")
def update_kb_claims(new_claims: List[Dict[str, Any]]):
    """
    Memperbarui file kb_claims.json dan me-reload composer di memori backend.
    """
    try:
        import json
        with open(claims_path, "w", encoding="utf-8") as f:
            json.dump(new_claims, f, indent=2, ensure_ascii=False)
        
        # Reload composer agar memuat data terupdate dari disk
        from app.reasoning.composer_sbcc import MessagePlanComposer
        orchestrator.composer = MessagePlanComposer()
        return {"status": "success", "message": "Basis pengetahuan claims berhasil diperbarui."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Model Request Chatbot
class ChatRequest(BaseModel):
    session_id: str
    message: str
    chat_history: List[Dict[str, str]] = []

@app.post("/api/chat")
def chat_consultation(req: ChatRequest):
    """
    Rute obrolan konsultasi AI mengenai hasil keputusan kasus.
    """
    try:
        import json
        session = db.get_session(req.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Sesi tidak ditemukan.")
        
        # Susun konteks data keputusan
        context = f"""
Topik Kesehatan: {session.get('topic', '').replace('_', ' ').title()}
Sasaran Utama Perilaku: {session.get('profile_3t', {}).get('audience', 'Masyarakat')}
Cerita Masalah di Lapangan: {session.get('user_story', '')}

Hasil Diagnosis Perilaku (COM-B): {json.dumps(session.get('diagnosis_result', {}).get('deficits', []))}
Pemetaan Fungsi Intervensi (BCW): {json.dumps([f.get('function') for f in session.get('intervention_result', {}).get('functions', [])])}
Variabel Kedaerahan 3T: {json.dumps(session.get('profile_3t', {}))}
Rancangan Pesan Know-Feel-Do: {json.dumps(session.get('realized_message', {}))}
"""
        
        system_prompt = f"""Anda adalah pakar komunikasi perubahan perilaku sosial dan kesehatan (SBCC) yang mendampingi petugas lapangan di wilayah 3T.
Tugas Anda adalah mendiskusikan, menjelaskan, dan menjawab pertanyaan mengenai perencanaan strategi komunikasi kesehatan berdasarkan konteks kasus berikut:

=== KONTEKS KASUS & DIAGNOSIS ===
{context}

Beri saran taktis yang realistis untuk wilayah 3T, gunakan bahasa Indonesia yang ramah, profesional, dan mudah dipahami. Jangan melanggar klaim medis yang ada di konteks.
"""
        
        # Panggil Gemini API
        response_text = gemini_client.generate(
            prompt=f"Riwayat Obrolan:\n{json.dumps(req.chat_history)}\n\nPertanyaan Petugas: {req.message}",
            system_instruction=system_prompt
        )
        return {"reply": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Setup Static Files untuk menyajikan Frontend UI
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
else:
    # Buat foldernya jika belum ada agar tidak error saat start
    os.makedirs(static_dir, exist_ok=True)
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
