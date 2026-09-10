import sys
import os
from urllib.parse import parse_qs, urlencode, urlparse

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.main import app as fastapi_app

async def app(scope, receive, send):
    if scope["type"] == "http":
        headers = dict(scope.get("headers", []))
        
        # 1. Coba ambil dari header reverse-proxy Vercel
        raw_forwarded = (
            headers.get(b"x-forwarded-uri")
            or headers.get(b"x-matched-path")
            or headers.get(b"x-vercel-matched-path")
            or b""
        ).decode("latin1")
        
        target_path = ""
        if raw_forwarded:
            target_path = urlparse(raw_forwarded).path
            
        # 2. Coba ambil dari parameter query __api_path jika ada
        query_bytes = scope.get("query_string", b"")
        query_str = query_bytes.decode("latin1")
        if "__api_path=" in query_str:
            qs = parse_qs(query_str)
            if "__api_path" in qs and qs["__api_path"]:
                sub = qs.pop("__api_path")[0]
                target_path = "/api" + (sub if sub.startswith("/") else "/" + sub)
                scope["query_string"] = urlencode(qs, doseq=True).encode("latin1")

        # 3. Terapkan target_path ke scope
        current_path = scope.get("path", "")
        if target_path and target_path not in ["/api/index.py", "/api/index"]:
            scope["path"] = target_path
            scope["raw_path"] = target_path.encode("latin1")
            
    await fastapi_app(scope, receive, send)
