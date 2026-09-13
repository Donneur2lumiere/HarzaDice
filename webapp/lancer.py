#!/usr/bin/env python3
"""Lanceur HarzaDice — serveur HTTP local + ouverture du navigateur.
Interopérable Windows, Linux, macOS (Python 3.7+ requis)."""
import http.server
import socketserver
import webbrowser
import threading
import os

PORT = 8000
WEB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'www')


class HarzaDiceHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def do_GET(self):
        if self.path == '/quit':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Serveur arrete')
            threading.Thread(target=self.server.shutdown, daemon=True).start()
        else:
            super().do_GET()

    def log_message(self, *args):
        pass


class HarzaDiceServer(socketserver.TCPServer):
    allow_reuse_address = True


if __name__ == '__main__':
    httpd = HarzaDiceServer(('', PORT), HarzaDiceHandler)
    url = f'http://localhost:{PORT}'
    print(f'HarzaDice — serveur local sur {url}')
    print('Ctrl+C pour arreter')
    webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('Serveur arrete. A bientot !')
