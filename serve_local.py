from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import os
ROOT=Path(__file__).resolve().parent
os.chdir(ROOT)
class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        path=self.path.split('?',1)[0]
        target=ROOT/path.lstrip('/')
        if path!='/' and not target.exists() and '.' not in Path(path).name:
            self.path='/index.html'
        return super().do_GET()
print('QA Lab Brasil 3.0 local: http://localhost:8000')
ThreadingHTTPServer(('127.0.0.1',8000),Handler).serve_forever()
