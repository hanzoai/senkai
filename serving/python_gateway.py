"""Loopback gateway to an alpha API deployment. Contains no Sekai model."""
import json
import os
import re
import secrets
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.error import HTTPError
from sekai_cookbook import Worlds

key = os.environ["GATEWAY_API_KEY"]
upstream = Worlds()  # HANZO_API_KEY remains server-side.
route = re.compile(r"^/v1/worlds(?:/[a-zA-Z0-9_-]+(?:/(?:events|plans|beliefs/[a-zA-Z0-9_-]+))?)?$")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self): self.forward("GET")
    def do_POST(self): self.forward("POST")
    def log_message(self, *args): pass
    def forward(self, method):
        code, result = 400, {"error": "invalid request"}
        if not secrets.compare_digest(self.headers.get("Authorization", ""), "Bearer "+key):
            code, result = 401, {"error": "unauthorized"}
        elif not route.fullmatch(self.path):
            code, result = 404, {"error": "unknown route"}
        else:
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if not 0 <= size <= 1024*1024: raise ValueError("size")
                self.connection.settimeout(5)
                body = json.loads(self.rfile.read(size)) if size else None
                result = upstream.request(method, self.path[3:], body)
                code = 200
            except HTTPError as error:
                code, result = error.code, {"error": "upstream refused request"}
            except Exception:
                code, result = 502, {"error": "upstream unavailable or invalid request"}
        raw = json.dumps(result).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", int(os.getenv("PORT", "8050"))), Handler).serve_forever()
