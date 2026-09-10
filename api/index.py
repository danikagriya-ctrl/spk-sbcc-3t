import sys
import os

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
            path = scope.get("path", "")
            # Jika request diteruskan oleh rewrite Vercel sebagai /api/index.py atau /api/index
            if path in ["/api/index.py", "/api/index"]:
                headers = dict(scope.get("headers", []))
                # Ambil original path dari header Vercel
                matched = headers.get(b"x-matched-path", b"").decode("utf-8")
                if matched and matched not in ["/api/index.py", "/api/index"]:
                    scope["path"] = matched
                else:
                    scope["path"] = "/"
        await self.app(scope, receive, send)

app = VercelPathHandler(fastapi_app)
