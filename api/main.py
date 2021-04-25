import json
import socket
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

from data import load


host = "0"
port = 8000


class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(DataLoader.data.encode("utf_8"))


def main():
    with open("results.json", "w") as outfile:
        outfile.write(json.dumps(load(), indent=2))

    return
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
