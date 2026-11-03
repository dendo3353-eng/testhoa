import http.server
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PORT = 8080

class GardenHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def guess_type(self, path):
        if path.endswith('.js') or path.endswith('.mjs'):
            return 'application/javascript; charset=utf-8'
        elif path.endswith('.css'):
            return 'text/css; charset=utf-8'
        elif path.endswith('.json'):
            return 'application/json; charset=utf-8'
        elif path.endswith('.webp'):
            return 'image/webp'
        elif path.endswith('.png'):
            return 'image/png'
        elif path.endswith('.ttf'):
            return 'font/ttf'
        elif path.endswith('.mp3'):
            return 'audio/mpeg'
        return super().guess_type(path)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, must-revalidate')
        super().end_headers()

    def do_GET(self):
        clean_path = self.path.split('?')[0]
        if clean_path.startswith('/access/'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            data_file = os.path.join(BASE_DIR, 'garden_data_local.json')
            with open(data_file, 'rb') as f:
                self.wfile.write(f.read())
            return
        
        # When request is / or /?..., serve /index.html
        if clean_path == '/' or clean_path == '':
            self.path = '/index.html'
        elif clean_path == '/vuon.html':
            self.path = '/vuon.html'

        return super().do_GET()

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    # Use ThreadingHTTPServer for fast concurrent handling
    http.server.ThreadingHTTPServer.allow_reuse_address = True
    with http.server.ThreadingHTTPServer(("", port), GardenHandler) as httpd:
        print(f"Flower Garden Server running at: http://localhost:{port}/")
        print(f"Directory: {BASE_DIR}")
        sys.stdout.flush()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
