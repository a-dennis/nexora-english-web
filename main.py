import os, json, base64, time, urllib.request, urllib.error
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

BASE = os.path.dirname(os.path.abspath(__file__))
ICON192 = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAMAAAADACAIAAADdvvtQAAADQklEQVR42u3dsUodQRiG4R3xCtLkJiRNqiRlsLZKK4K1FxDIpYhVbkDIHSgiaHqDxamENBIhRC2EtfJUAd3dw47/P897ATJnnPN+35/ZNeXbx+sOGMt61/V2AeMPULEHYCAwEBgIDAQMPUAMhPGs2QKIMCjRYCAo0YASjVkNVBgIDAQlGsZ4MBBgjIcSDQYCAwEMBFMYRBhEGMBAWLGB3MaDgaADwRgPEQaIMDAQGAhKNPDcAfJMNBgIDAQGgjEeGGogt/EQYVCiwUBgIICB4ABBhIGBAAYCA72EjS9vPuy9jbLauz8P37cuGehV0VswA42nWHCdA5TmMjXaLyTHznucAyJMhCnRSjQD+UK3WaL9Q2K1A6REQ4lOY6BwH4SBALfx9Rq0MR7GeGO8BSvRQb/QOXZ+XZAs+bFzcbO4tw8DDVTSjPGTf0LpvehtjIcOVKlSlCy9xBRmMhJhEGHtRVgvwhgIDFTPYXaDgcBAOpAxPugMbzdEGETYWH9MRoQxEOY2UJ534yeXaLfxLZfo6R9k8+DdDOv8fXpz8vVXngPkmega5NlzBrJUBgr2te4ZCAxkjMeKDOQubG79FBEGEWaM1/cZyBjPQMZ4BsLQEp1pCit5fjFhlproBCnR0laEKdEM1NjXmoEycrz78+/iHwPpQAZsBqr0tebjEQdIB1qeHm9lDMbjHBBhK0ofb6Yq0Uo0A1V1mN1ot0T76xxKNCIayKvNyx9QOq82MxCU6EpjfKdEG+ON8QxUTR7G+KbHeHdhSjQYKHaEMRADgYF0IFNYyAh7v/9p5jWfbx/dXd2KMIgwVIrd6PvPQJhooDT/7XfAD5LgT5szEHSgwJNj+A5kjK+85uj7L8Igwp7iIKaBlGgwUAoiGkiJVqLbLtGeia5uTQZCY+LMaqA+5ppj7385+3xIAzDGo1YH8jY4lGgo0WAgMBDAQHCAIMLAQAADgYHAQGAg4D8HyGUqJuBxDogwKNFgIDR6gBgISjQYCAwEJRowxoOBoERDiQaeM5DbeDAQdCCYwiDCABEGBgIDgYEABoIxHiIMIgxgIKzaQG7joUSj2gHyTDQYCAwEBoIxHhhsIBEGEQYlGgwEBgIYCLPxCAdsxU5ky+MbAAAAAElFTkSuQmCC")
ICON512 = base64.b64decode("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")
TTS_CACHE = {}
MANIFEST = json.dumps({
    "name": "Nexora English", "short_name": "Nexora English",
    "description": "Learn English step by step with an AI teacher. Kannada + English.",
    "start_url": "/", "scope": "/", "display": "standalone",
    "background_color": "#ffffff", "theme_color": "#7c3aed",
    "icons": [
        {"src": "/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
        {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"}]})
SW = """self.addEventListener('install',e=>self.skipWaiting());
self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));
self.addEventListener('fetch',e=>{});"""
MODELS = ["gemini-flash-lite-latest", "gemini-flash-latest", "gemini-2.0-flash"]
RATE = {}

SYSTEM = ("You are a kind English teacher for Indian learners whose first language is Kannada or Hindi. "
          "Use very simple English (short sentences). When useful, add one short explanation in the learner language named below, and do not use any other language. "
          "If the learner writes a sentence with mistakes, show the corrected sentence first, then explain the mistake in one or two lines. "
          "Keep answers under 90 words. Only talk about learning English. Never ask for personal details.")

def ask_ai(persona, text, level, lang='Kannada'):
    key = os.environ.get("GEMINI_API_KEY", "")
    if not key:
        return None
    body = {"system_instruction": {"parts": [{"text": SYSTEM + " Your name is " + persona + ". Learner level: " + level + ". Add the short explanation in " + lang + " script."}]},
            "contents": [{"role": "user", "parts": [{"text": text[:600]}]}]}
    for m in MODELS:
        try:
            req = urllib.request.Request(
                "https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent?key=%s" % (m, key),
                data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=25) as r:
                j = json.loads(r.read())
            return j["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            continue
    return ""

class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass
    def send(self, code, ctype, data, cache="no-cache"):
        if isinstance(data, str):
            data = data.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", cache)
        self.end_headers()
        self.wfile.write(data)
    def do_HEAD(self):
        self.do_GET()
    def do_GET(self):
        p = self.path.split("?")[0]
        if p != "/health":
            self.send_response(302)
            self.send_header("Location", "https://nexora-web-q7rn.onrender.com/english")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        if p in ("/", "/index.html"):
            with open(os.path.join(BASE, "index.html"), "rb") as f:
                return self.send(200, "text/html; charset=utf-8", f.read())
        if p == "/health":
            return self.send(200, "text/plain", "ok")
        if p == "/manifest.webmanifest":
            return self.send(200, "application/manifest+json", MANIFEST)
        if p == "/sw.js":
            return self.send(200, "application/javascript", SW)
        if p == "/icon-192.png":
            return self.send(200, "image/png", ICON192, "public, max-age=86400")
        if p == "/icon-512.png":
            return self.send(200, "image/png", ICON512, "public, max-age=86400")
        if p == "/api/status":
            return self.send(200, "application/json", json.dumps({"ai": bool(os.environ.get("GEMINI_API_KEY"))}))
        if p == "/api/tts":
            from urllib.parse import urlparse, parse_qs, quote
            q = parse_qs(urlparse(self.path).query)
            lang = (q.get("lang", ["kn"])[0])
            text = (q.get("text", [""])[0])[:200]
            if lang not in ("kn", "hi", "en") or not text.strip():
                return self.send(400, "text/plain", "bad")
            key = (lang, text)
            if key in TTS_CACHE:
                return self.send(200, "audio/mpeg", TTS_CACHE[key], "public, max-age=86400")
            try:
                u = "https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=%s&q=%s" % (lang, quote(text))
                rq = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0", "Referer": "https://translate.google.com/"})
                data = urllib.request.urlopen(rq, timeout=10).read()
                if len(TTS_CACHE) > 300:
                    TTS_CACHE.clear()
                TTS_CACHE[key] = data
                return self.send(200, "audio/mpeg", data, "public, max-age=86400")
            except Exception:
                return self.send(502, "text/plain", "tts unavailable")
        if p == "/robots.txt":
            return self.send(200, "text/plain", "User-agent: *\nAllow: /\n")
        return self.send(404, "text/plain", "Not found")
    def do_POST(self):
        if self.path.split("?")[0] != "/api/ask":
            return self.send(404, "text/plain", "Not found")
        ip = self.headers.get("X-Forwarded-For", self.client_address[0]).split(",")[0].strip()
        now = time.time()
        hits = [t for t in RATE.get(ip, []) if now - t < 3600]
        if len(hits) >= 40:
            return self.send(429, "application/json", json.dumps({"reply": "Too many questions this hour. Please come back later."}))
        hits.append(now); RATE[ip] = hits
        try:
            n = int(self.headers.get("Content-Length", "0"))
            d = json.loads(self.rfile.read(min(n, 4000)))
            text = str(d.get("text", ""))[:600]
            persona = "Anaya" if d.get("persona") == "Anaya" else "Arjun"
            level = str(d.get("level", "Beginner"))[:20]
            lang = "Hindi" if d.get("lang") == "hi" else "Kannada"
        except Exception:
            return self.send(400, "application/json", json.dumps({"reply": "Bad request."}))
        out = ask_ai(persona, text, level, lang)
        if out is None:
            out = "My smart answers are switching on soon. Meanwhile, do the lessons and quizzes."
        elif out == "":
            out = "I am busy right now. Please try again in a minute."
        return self.send(200, "application/json", json.dumps({"reply": out}))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    ThreadingHTTPServer(("0.0.0.0", port), H).serve_forever()
