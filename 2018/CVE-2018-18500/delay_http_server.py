#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import time

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        if self.path == '/customelements_poc.html':
            self.wfile.write(open('customelements_poc.html', 'r').read())
        elif self.path == '/delay.xml':
            time.sleep(2)
            self.wfile.write("<xml></xml>")
        else:
            self.wfile.write("<html><body><h1>open /customelements_poc.html</h1></body></html>")

    def do_HEAD(self):
        self._set_headers()
        
def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('127.0.0.1', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
