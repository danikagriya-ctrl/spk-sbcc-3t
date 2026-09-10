import sys
import os
from urllib.parse import parse_qs

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.main import app as fastapi_app

class VercelPathHandler:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            query_str = scope.get("query_string", b"").decode("utf-8")
            if "__path=" in query_str:
                qs = parse_qs(query_str)
                if "__path" in qs and qs["__path"]:
                    target_path = qs["__path"][0]
                    if not target_path.startswith("/"):
                        target_path = "/" + target_path
                    scope["path"] = target_path
        await self.app(scope, receive, send)

app = VercelPathHandler(fastapi_app)
