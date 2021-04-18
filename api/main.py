import socket
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

from data import parseAll


host = "0"
port = 8000
global results


class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        global results
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(results.encode("utf_8"))


def main():
    global results
    results = parseAll()
    server = HTTPServer((host, port), Server)

    try:
        print(f"Server started at {host}:{port}")
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()
    print("Server stopped")


if __name__ == "__main__":
    main()
