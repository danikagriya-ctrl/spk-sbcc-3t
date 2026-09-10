import sqlite3
import json
import os
from datetime import datetime
from app.config import Config

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    psycopg2 = None


class SessionDatabase:
    def __init__(self, db_url=None):
        # Deteksi URL PostgreSQL dari Vercel Storage (POSTGRES_URL / DATABASE_URL)
        raw_url = (
            db_url
            or os.environ.get("POSTGRES_URL")
            or os.environ.get("DATABASE_URL")
            or Config.DATABASE_URL
        )

        self.is_postgres = bool(
            raw_url and (
                raw_url.startswith("postgres://")
                or raw_url.startswith("postgresql://")
            )
        )

        if self.is_postgres:
            # Standarisasi skema URL untuk psycopg2
            if raw_url.startswith("postgres://"):
                raw_url = raw_url.replace("postgres://", "postgresql://", 1)
            self.postgres_url = raw_url
            self.db_path = None
        else:
            self.postgres_url = None
            # Jika di Vercel tapi belum pasang cloud database, fallback aman ke /tmp/
            if os.environ.get("VERCEL"):
                self.db_path = "/tmp/sessions.db"
            else:
                url = Config.DATABASE_URL
                if url.startswith("sqlite:///"):
                    self.db_path = url.replace("sqlite:///", "")
                else:
                    self.db_path = "./sessions.db"

        self._init_db()

    def _get_connection(self):
        if self.is_postgres:
            if psycopg2 is None:
                raise RuntimeError("Pustaka 'psycopg2' belum terpasang. Jalankan: pip install psycopg2-binary")
            conn = psycopg2.connect(self.postgres_url)
            return conn
        else:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn

    def _init_db(self):
        """
        Membuat tabel jika belum ada.
        """
        if not self.is_postgres and self.db_path:
            os.makedirs(os.path.dirname(os.path.abspath(self.db_path)), exist_ok=True)
            
        with self._get_connection() as conn:
            if self.is_postgres:
                with conn.cursor() as cur:
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS sessions (
                            session_id VARCHAR(255) PRIMARY KEY,
                            created_at VARCHAR(100) NOT NULL,
                            topic TEXT,
                            user_story TEXT,
                            profile_3t TEXT,
                            extracted_data TEXT,
                            clarification_questions TEXT,
                            diagnosis_result TEXT,
                            intervention_result TEXT,
                            composed_plan TEXT,
                            realized_message TEXT,
                            status VARCHAR(50) NOT NULL
                        );
                    """)
                conn.commit()
            else:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS sessions (
                        session_id TEXT PRIMARY KEY,
                        created_at TEXT NOT NULL,
                        topic TEXT,
                        user_story TEXT,
                        profile_3t TEXT,
                        extracted_data TEXT,
                        clarification_questions TEXT,
                        diagnosis_result TEXT,
                        intervention_result TEXT,
                        composed_plan TEXT,
                        realized_message TEXT,
                        status TEXT NOT NULL
                    )
                """)
                conn.commit()

    def create_session(self, session_id, topic, user_story, profile_3t):
        now = datetime.now().isoformat()
        ph = "%s" if self.is_postgres else "?"
        profile_json = json.dumps(profile_3t)
        
        query = f"""
            INSERT INTO sessions 
            (session_id, created_at, topic, user_story, profile_3t, status)
            VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph})
            ON CONFLICT (session_id) DO UPDATE SET
                created_at = EXCLUDED.created_at,
                topic = EXCLUDED.topic,
                user_story = EXCLUDED.user_story,
                profile_3t = EXCLUDED.profile_3t,
                status = EXCLUDED.status
        """
        params = (session_id, now, topic, user_story, profile_json, "active")
        
        with self._get_connection() as conn:
            if self.is_postgres:
                with conn.cursor() as cur:
                    cur.execute(query, params)
                conn.commit()
            else:
                conn.execute(query, params)
                conn.commit()

    def update_session(self, session_id, **kwargs):
        """
        Mengupdate kolom-kolom sesi secara dinamis.
        """
        allowed_keys = [
            "topic", "user_story", "profile_3t", "extracted_data", 
            "clarification_questions", "diagnosis_result", 
            "intervention_result", "composed_plan", "realized_message", "status"
        ]
        ph = "%s" if self.is_postgres else "?"
        updates = []
        params = []
        for key, value in kwargs.items():
            if key in allowed_keys:
                updates.append(f"{key} = {ph}")
                if isinstance(value, (dict, list)):
                    params.append(json.dumps(value))
                else:
                    params.append(value)
        
        if not updates:
            return
            
        params.append(session_id)
        query = f"UPDATE sessions SET {', '.join(updates)} WHERE session_id = {ph}"
        
        with self._get_connection() as conn:
            if self.is_postgres:
                with conn.cursor() as cur:
                    cur.execute(query, tuple(params))
                conn.commit()
            else:
                conn.execute(query, tuple(params))
                conn.commit()

    def get_session(self, session_id):
        ph = "%s" if self.is_postgres else "?"
        query = f"SELECT * FROM sessions WHERE session_id = {ph}"
        with self._get_connection() as conn:
            if self.is_postgres:
                cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                cur.execute(query, (session_id,))
                row = cur.fetchone()
                cur.close()
                if not row:
                    return None
                res = dict(row)
            else:
                row = conn.execute(query, (session_id,)).fetchone()
                if not row:
                    return None
                res = dict(row)

            # Parse JSON strings back to dicts
            for key in ["profile_3t", "extracted_data", "clarification_questions", "diagnosis_result", "intervention_result", "composed_plan", "realized_message"]:
                if res.get(key):
                    try:
                        res[key] = json.loads(res[key])
                    except Exception:
                        pass
            return res

    def list_sessions(self, limit=50):
        ph = "%s" if self.is_postgres else "?"
        query = f"SELECT session_id, created_at, topic, status FROM sessions ORDER BY created_at DESC LIMIT {ph}"
        with self._get_connection() as conn:
            if self.is_postgres:
                cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                cur.execute(query, (limit,))
                rows = cur.fetchall()
                cur.close()
                return [dict(row) for row in rows]
            else:
                rows = conn.execute(query, (limit,)).fetchall()
                return [dict(row) for row in rows]

    def delete_session(self, session_id):
        ph = "%s" if self.is_postgres else "?"
        query = f"DELETE FROM sessions WHERE session_id = {ph}"
        with self._get_connection() as conn:
            if self.is_postgres:
                with conn.cursor() as cur:
                    cur.execute(query, (session_id,))
                conn.commit()
            else:
                conn.execute(query, (session_id,))
                conn.commit()
