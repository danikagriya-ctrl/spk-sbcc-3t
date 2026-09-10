import sys
import os
import json

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.main import app as fastapi_app

async def app(scope, receive, send):
    if scope["type"] == "http":
        headers = {k.decode('latin1'): v.decode('latin1') for k, v in scope.get("headers", [])}
        body = json.dumps({
            "scope_path": scope.get("path"),
            "scope_raw_path": scope.get("raw_path", b"").decode("latin1", "ignore"),
            "scope_query_string": scope.get("query_string", b"").decode("latin1"),
            "headers": headers
        }, indent=2).encode("utf-8")
        await send({
            "type": "http.response.start",
            "status": 200,
            "headers": [[b"content-type", b"application/json"]]
        })
        await send({
            "type": "http.response.body",
            "body": body
        })
        return
