"""Bounded local HTTP/1.1 subset for learning, not an Internet-facing server.

PUT/GET only, one request per connection, no transfer encodings or TLS. Use a
maintained HTTP server for production. Bind loopback only; token from environment.
"""
import asyncio
import json
import os
from pathlib import Path
import re

from .api import DocumentAPI, Response
from .storage import DocumentStore

MAX_BODY = 4096
MAX_HEADER = 8192


def parse_head(head: bytes):
    if len(head) > MAX_HEADER:
        raise ValueError("headers too large")
    lines = head.decode("ascii").split("\r\n")
    if not lines or not lines[0]:
        raise ValueError("missing request line")
    method, path, version = lines[0].split(" ")
    if version != "HTTP/1.1" or method not in {"PUT", "GET"}:
        raise ValueError("unsupported request")
    headers = {}
    for line in lines[1:]:
        if not line:
            continue
        name, value = line.split(":", 1)
        if not re.fullmatch(r"[!#$%&'*+.^_`|~0-9A-Za-z-]+", name):
            raise ValueError("invalid header name")
        name = name.lower()
        if name in headers or any(ord(c) < 32 or ord(c) == 127 for c in value):
            raise ValueError("duplicate or invalid header")
        headers[name] = value.strip()
    if "transfer-encoding" in headers or not headers.get("host"):
        raise ValueError("transfer encoding unsupported or Host missing")
    length = headers.get("content-length", "0")
    if not re.fullmatch(r"[0-9]{1,5}", length) or int(length) > MAX_BODY:
        raise ValueError("invalid content length")
    return method, path, headers, int(length)


async def handle(reader, writer, api):
    try:
        try:
            async with asyncio.timeout(2.0):
                head = await reader.readuntil(b"\r\n\r\n")
                method, path, headers, size = parse_head(head[:-4])
                body = await reader.readexactly(size)
                response = await api.dispatch(method, path, headers, body)
        except TimeoutError:
            response = Response(408, {"error": "request timeout"})
        except (ValueError, UnicodeError, asyncio.IncompleteReadError, asyncio.LimitOverrunError):
            response = Response(400, {"error": "malformed or oversized request"})
        payload = json.dumps(response.payload, ensure_ascii=False).encode("utf-8")
        labels = {200: "OK", 400: "Bad Request", 401: "Unauthorized", 404: "Not Found",
                  405: "Method Not Allowed", 408: "Request Timeout", 415: "Unsupported Media Type",
                  503: "Service Unavailable"}
        fields = [f"HTTP/1.1 {response.status} {labels[response.status]}",
                  "Content-Type: application/json", f"Content-Length: {len(payload)}", "Connection: close"]
        if response.status == 401:
            fields.append('WWW-Authenticate: Bearer realm="local-demo"')
        if response.status == 405:
            fields.append("Allow: GET, PUT")
        writer.write(("\r\n".join(fields) + "\r\n\r\n").encode("ascii") + payload)
        await asyncio.wait_for(writer.drain(), timeout=2.0)
    finally:
        writer.close()
        await writer.wait_closed()


async def serve(database: Path, token: str):
    api = DocumentAPI(DocumentStore(database), {token: "learner"})
    server = await asyncio.start_server(lambda r, w: handle(r, w, api), "127.0.0.1", 8765, limit=MAX_HEADER)
    async with server:
        print("Local teaching server at http://127.0.0.1:8765; Ctrl+C to stop")
        await server.serve_forever()


if __name__ == "__main__":
    token = os.environ.get("FORGE_DEMO_TOKEN")
    if not token:
        raise SystemExit("Set FORGE_DEMO_TOKEN to a local disposable secret before starting.")
    try:
        asyncio.run(serve(Path("forge-demo.sqlite3"), token))
    except KeyboardInterrupt:
        pass
