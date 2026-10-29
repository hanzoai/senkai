import json
import os
from urllib.parse import quote, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("API redirect refused")


class Worlds:
    def __init__(self, base=None, key=None):
        self.base = (base or os.environ.get("HANZO_BASE_URL", "https://api.hanzo.ai/v1")).rstrip("/")
        self.key = key or os.environ.get("HANZO_API_KEY")
        parts = urlsplit(self.base)
        if parts.scheme != "https" and not (parts.scheme == "http" and parts.hostname in ("127.0.0.1", "localhost", "::1")):
            raise ValueError("HTTPS required except on loopback")
        if parts.username or parts.password or parts.query or parts.fragment or not self.base.endswith("/v1"):
            raise ValueError("base must end in /v1 and contain no credentials/query/fragment")
        if not self.key:
            raise ValueError("Set HANZO_API_KEY for your enabled alpha deployment")
        self.opener = build_opener(NoRedirect)

    def request(self, method, path, body=None):
        if path != "/worlds" and not path.startswith("/worlds/"):
            raise ValueError("worlds routes only")
        req = Request(self.base+path, json.dumps(body, allow_nan=False).encode() if body is not None else None,
                      {"Authorization": "Bearer "+self.key, "Content-Type": "application/json"}, method=method)
        with self.opener.open(req, timeout=30) as response:
            raw = response.read(1024*1024+1)
        if len(raw) > 1024*1024:
            raise ValueError("response too large")
        return json.loads(raw)

    def create(self, domain="simulation"):
        return self.request("POST", "/worlds", {"model": "sekai-1-alpha", "domain": domain})

    def event(self, world, body):
        return self.request("POST", f"/worlds/{quote(world, safe='')}/events", body)

    def belief(self, world, entity):
        return self.request("GET", f"/worlds/{quote(world, safe='')}/beliefs/{quote(entity, safe='')}")

    def plan(self, world, body):
        return self.request("POST", f"/worlds/{quote(world, safe='')}/plans", body)
