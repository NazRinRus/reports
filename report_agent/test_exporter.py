import http.server
from prometheus_client import start_http_server, Counter

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        REQUESTS.inc()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello World")

REQUESTS = Counter('hello_worlds_total', 'Hello Worlds requested.')

if __name__ == "__main__":
    
    start_http_server(8000)
    server = http.server.HTTPServer(('192.168.0.140', 8001), MyHandler)
    server.serve_forever()
