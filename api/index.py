import sys
import os
from urllib.parse import parse_qs, urlencode

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.main import app as fastapi_app

async def app(scope, receive, send):
    if scope["type"] == "http":
        query_bytes = scope.get("query_string", b"")
        query_str = query_bytes.decode("latin1")
        if "__api_path=" in query_str:
            qs = parse_qs(query_str)
            if "__api_path" in qs and qs["__api_path"]:
                subpath = qs.pop("__api_path")[0]
                if not subpath.startswith("/"):
                    subpath = "/" + subpath
                scope["path"] = "/api" + subpath
                scope["raw_path"] = scope["path"].encode("latin1")
                scope["query_string"] = urlencode(qs, doseq=True).encode("latin1")
        else:
            path = scope.get("path", "")
            if path in ["/api/index.py", "/api/index", "/api/index.py/"]:
                headers = dict(scope.get("headers", []))
                matched = headers.get(b"x-matched-path", b"").decode("latin1")
                if matched and matched not in ["/api/index.py", "/api/index"]:
                    scope["path"] = matched
                else:
                    scope["path"] = "/"
    await fastapi_app(scope, receive, send)
