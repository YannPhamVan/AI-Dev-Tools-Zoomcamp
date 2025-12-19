from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse
import threading

HOST = '127.0.0.1'
PORT = 9000

HTML = b"""
<!doctype html>
<html>
<head><meta charset="utf-8"><title>MCP Test UI</title></head>
<body>
  <h3>MCP Test UI (calls local function)</h3>
  <label>URL: <input id="url" size="60" value="https://datatalks.club"></label><br>
  <label>Word: <input id="word" value="data"></label><br>
  <button id="run">Run</button>
  <pre id="out"></pre>
  <script>
    document.getElementById('run').onclick = async () => {
      const url = document.getElementById('url').value;
      const word = document.getElementById('word').value;
      const res = await fetch('/run', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({url, word})});
      const j = await res.json();
      document.getElementById('out').textContent = JSON.stringify(j, null, 2);
    }
  </script>
</body>
</html>
"""

class Handler(BaseHTTPRequestHandler):
    def _set_json(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()

    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/run':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                payload = json.loads(body)
                url = payload.get('url')
                word = payload.get('word')
                # import the function from main and call it
                from main import count_word_on_page
                result = count_word_on_page(url, word)
                self._set_json()
                self.wfile.write(json.dumps({'ok': True, 'count': result}).encode('utf-8'))
            except Exception as e:
                self._set_json()
                self.wfile.write(json.dumps({'ok': False, 'error': str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run():
    server = HTTPServer((HOST, PORT), Handler)
    print(f"UI server running at http://{HOST}:{PORT}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()

if __name__ == '__main__':
    run()
