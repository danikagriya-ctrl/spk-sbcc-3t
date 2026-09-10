import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.main import app as fastapi_app

async def app(scope, receive, send):
    if scope["type"] == "http":
        path = scope.get("path", "")
        if path in ["/api/index.py", "/api/index", "/api/index.py/"]:
            headers = dict(scope.get("headers", []))
            matched = headers.get(b"x-matched-path", b"").decode("latin1")
            if matched and matched not in ["/api/index.py", "/api/index"]:
                scope["path"] = matched
            else:
                scope["path"] = "/"
    await fastapi_app(scope, receive, send)
