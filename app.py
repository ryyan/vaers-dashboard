import json
import socket
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from data import load


host = "0"
port = 8000


class RequestHandler(SimpleHTTPRequestHandler):
    valid_paths = [
        "/index.html",
        "/results.json",
    ]

    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"

        if self.path in RequestHandler.valid_paths:
            return SimpleHTTPRequestHandler.do_GET(self)

        self.send_response(404)
        self.end_headers()


def main():
    results = load()
    with open("results.json", "w") as outfile:
        outfile.write(json.dumps(results, indent=2))

    server = ThreadingHTTPServer((host, port), RequestHandler)

    try:
        print(f"Server started at {host}:{port}")
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()
    print("Server stopped")


if __name__ == "__main__":
    main()
