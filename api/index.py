import sys
import os
from urllib.parse import parse_qs

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.main import app as fastapi_app

# Handler ASGI untuk memastikan rute rewrite Vercel mengarah ke rute FastAPI yang benar
class VercelPathHandler:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            query_str = scope.get("query_string", b"").decode("utf-8")
            # Jika rewrite menyertakan parameter _path (misal: /api/topics)
            if "_path=" in query_str:
                qs = parse_qs(query_str)
                if "_path" in qs and qs["_path"]:
                    scope["path"] = qs["_path"][0]
            else:
                path = scope.get("path", "")
                if path in ["/api/index.py", "/api/index", ""]:
                    headers = dict(scope.get("headers", []))
                    matched = headers.get(b"x-matched-path", b"").decode("utf-8")
                    if matched and matched not in ["/api/index.py", "/api/index", "/"]:
                        scope["path"] = matched
                    else:
                        scope["path"] = "/"
        await self.app(scope, receive, send)

app = VercelPathHandler(fastapi_app)
