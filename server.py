from http.server import BaseHTTPRequestHandler, HTTPServer
import json, os
PORT = int(os.environ.get("PORT", 8083))
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self._json(200, {"ok": True})
            return
        self._json(404, {"error": "not found"})
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length) if length else b"{}")
        if self.path == "/outline":
            topic = body.get("topic", "")
            outline = {
                "topic": topic,
                "sections": ["Introduction", "Key Points", "Analysis", "Conclusion"],
                "keywords": body.get("keywords", []),
            }
            self._json(200, outline)
            return
        if self.path == "/draft":
            outline = body.get("outline", {})
            draft = {
                "title": outline.get("topic", ""),
                "body": "Draft content would be generated here in production.",
                "word_count_estimate": 750,
            }
            self._json(200, draft)
            return
        self._json(404, {"error": "unknown route"})
    def _json(self, code, obj):
        payload = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)
    def log_message(self, *args, **kwargs):
        return
def main():
    HTTPServer(("", PORT), Handler).serve_forever()
if __name__ == "__main__":
    main()
