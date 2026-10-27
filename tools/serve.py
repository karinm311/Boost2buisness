#!/usr/bin/env python3
"""Tiny static server that behaves like Netlify, for QA and Lighthouse.

It serves HTTP/1.1 with gzip and Netlify-style long caching. Pretty URLs
work: /team/chani serves /team/chani.html, and /x/ serves /x/index.html.

usage:  python3 tools/serve.py site/dist 8765
        (then open http://127.0.0.1:8765/)
Run it in the background, and stop it later by its PID, not with `pkill -f`,
which can kill your own shell.
"""
import gzip
import http.server
import os
import sys

ROOT = os.path.realpath(sys.argv[1] if len(sys.argv) > 1 else "site/dist")
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8765

TYPES = {
    ".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8", ".mjs": "text/javascript; charset=utf-8",
    ".json": "application/json", ".svg": "image/svg+xml", ".xml": "application/xml",
    ".txt": "text/plain; charset=utf-8", ".webmanifest": "application/manifest+json",
    ".woff2": "font/woff2", ".woff": "font/woff", ".ttf": "font/ttf",
    ".webp": "image/webp", ".avif": "image/avif", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".png": "image/png", ".gif": "image/gif", ".ico": "image/x-icon",
    ".mp4": "video/mp4", ".webm": "video/webm", ".pdf": "application/pdf",
}
COMPRESS = {".html", ".css", ".js", ".mjs", ".json", ".svg", ".xml", ".txt", ".webmanifest"}
LONG_CACHE = {".woff2", ".woff", ".ttf", ".webp", ".avif", ".jpg", ".jpeg", ".png", ".gif", ".mp4", ".webm"}


def resolve(url_path):
    """Map a URL path to a file inside ROOT, or return None."""
    path = url_path.split("?")[0].split("#")[0]
    from urllib.parse import unquote
    path = unquote(path)
    candidates = []
    if path.endswith("/"):
        candidates.append(path + "index.html")
    else:
        candidates += [path, path + ".html", path + "/index.html"]
    for cand in candidates:
        fp = os.path.realpath(os.path.join(ROOT, cand.lstrip("/")))
        if (fp == ROOT or fp.startswith(ROOT + os.sep)) and os.path.isfile(fp):
            return fp
    return None


class Handler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *args):
        pass

    def _send(self, code, data, ctype, extra=None):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(data)

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        fp = resolve(self.path)
        if not fp:
            nf = os.path.join(ROOT, "404.html")
            body = open(nf, "rb").read() if os.path.isfile(nf) else b"not found"
            self._send(404, body, "text/html; charset=utf-8" if os.path.isfile(nf) else "text/plain")
            return
        ext = os.path.splitext(fp)[1].lower()
        data = open(fp, "rb").read()
        headers = {"Cache-Control": "public, max-age=31536000, immutable" if ext in LONG_CACHE else "no-cache"}
        if ext in COMPRESS and "gzip" in self.headers.get("Accept-Encoding", ""):
            data = gzip.compress(data, 9)
            headers["Content-Encoding"] = "gzip"
            headers["Vary"] = "Accept-Encoding"
        self._send(200, data, TYPES.get(ext, "application/octet-stream"), headers)


if __name__ == "__main__":
    if not os.path.isdir(ROOT):
        sys.exit(f"no such folder: {ROOT}")
    print(f"serving {ROOT} at http://127.0.0.1:{PORT}/  (pid {os.getpid()})", flush=True)
    http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
