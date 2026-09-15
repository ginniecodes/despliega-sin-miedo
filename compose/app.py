import os
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer


REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
APP_MESSAGE = os.getenv("APP_MESSAGE", "Hello, World!")


def increment_visits():
    with socket.create_connection((REDIS_HOST, REDIS_PORT), timeout=2) as redis:
        redis.sendall(b"*2\r\n$4\r\nINCR\r\n$6\r\nvisits\r\n")
        return redis.recv(1024).decode().strip().lstrip(":")


class HelloWorldHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            visits = increment_visits()
            body = f"{APP_MESSAGE} Redis visit count: {visits}\n".encode()
            self.send_response(200)
        except OSError:
            body = b"Redis is unavailable.\n"
            self.send_response(503)

        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8000), HelloWorldHandler).serve_forever()
