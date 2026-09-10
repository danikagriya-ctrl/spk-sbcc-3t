import sqlite3
import json

conn = sqlite3.connect("sessions.db")
conn.row_factory = sqlite3.Row
rows = conn.execute("SELECT * FROM sessions").fetchall()

print(f"Total sessions: {len(rows)}")
for r in rows:
    d = dict(r)
    print(f"Session: {d['session_id']}")
    print(f"  Topic: {d['topic']}")
    print(f"  Status: {d['status']}")
    print(f"  Clarification questions: {d['clarification_questions']}")
    print(f"  Profile 3T: {d['profile_3t']}")
    print("-" * 50)
conn.close()
