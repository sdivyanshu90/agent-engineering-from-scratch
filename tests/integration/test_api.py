import asyncio
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from forgeagent.api import DocumentAPI, decode_document
from forgeagent.http_demo import handle, parse_head
from forgeagent.storage import DocumentStore


class StorageTests(unittest.TestCase):
    def test_rollback_and_parameterized_text(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data.sqlite3"
            store = DocumentStore(path)
            text = "'); DROP TABLE documents; --"
            store.put("alice", "id", text)
            self.assertEqual(DocumentStore(path).get("alice", "id"), text)
            connection = sqlite3.connect(path, autocommit=False)
            try:
                with self.assertRaises(RuntimeError):
                    with connection:
                        connection.execute("INSERT INTO documents VALUES (?, ?, ?)", ("alice", "rolled-back", "text"))
                        raise RuntimeError("injected before commit")
            finally:
                connection.close()
            self.assertIsNone(store.get("alice", "rolled-back"))
            with self.assertRaises(ValueError):
                DocumentStore(":memory:")


class APITests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = DocumentStore(Path(self.temp.name) / "data.sqlite3")
        self.api = DocumentAPI(self.store, {"alice-secret": "alice", "bob-secret": "bob"})
        self.alice = {"authorization": "Bearer alice-secret", "content-type": "application/json"}
        self.bob = {"authorization": "Bearer bob-secret", "content-type": "application/json"}

    async def test_authenticated_write_read_empty_and_ownership(self):
        put = await self.api.dispatch("PUT", "/documents/note", self.alice, b'{"text":"hello"}')
        self.assertEqual(put.status, 200)
        own = await self.api.dispatch("GET", "/documents/note", self.alice, b"")
        self.assertEqual(own.payload["text"], "hello")
        other = await self.api.dispatch("GET", "/documents/note", self.bob, b"")
        self.assertEqual(other.status, 404)
        for _ in range(2):
            self.assertEqual((await self.api.dispatch("PUT", "/documents/note", self.alice, b'{"text":""}')).status, 200)
        self.assertEqual((await self.api.dispatch("GET", "/documents/note", self.alice, b"")).payload["text"], "")
        reopened = DocumentStore(Path(self.temp.name) / "data.sqlite3")
        self.assertEqual(reopened.get("alice", "note"), "")

    async def test_invalid_requests_never_write(self):
        for body in [b"[]", b'{"text":4}', b'{"text":"a","owner":"bob"}', b'{"text":"a","text":"b"}', b"\xff"]:
            with self.subTest(body=body):
                response = await self.api.dispatch("PUT", "/documents/no", self.alice, body)
                self.assertEqual(response.status, 400)
        self.assertIsNone(self.store.get("alice", "no"))
        self.assertEqual((await self.api.dispatch("PUT", "/documents/note", {}, b'{"text":"x"}')).status, 401)
        self.assertEqual((await self.api.dispatch("PUT", "/documents/../secret", self.alice, b'{}')).status, 404)
        self.assertEqual((await self.api.dispatch("POST", "/documents/note", self.alice, b'{}')).status, 405)
        self.assertEqual((await self.api.dispatch("GET", "/documents/note", self.alice, b'{}')).status, 400)
        headers = {"authorization": "Bearer alice-secret", "content-type": "text/plain"}
        self.assertEqual((await self.api.dispatch("PUT", "/documents/no", headers, b'{}')).status, 415)

    async def test_storage_fault_maps_to_service_error(self):
        with patch.object(self.store, "get", side_effect=sqlite3.OperationalError("locked")):
            response = await self.api.dispatch("GET", "/documents/note", self.alice, b"")
        self.assertEqual(response.status, 503)
        self.assertNotIn("locked", str(response.payload))

    async def test_transport_with_in_memory_stream_fixture(self):
        class Writer:
            def __init__(self):
                self.data = b""
                self.closed = False
            def write(self, data):
                self.data += data
            async def drain(self):
                pass
            def close(self):
                self.closed = True
            async def wait_closed(self):
                pass
        for request, expected in [
            (b"GET /documents/missing HTTP/1.1\r\nHost: local\r\nAuthorization: Bearer alice-secret\r\n\r\n", 404),
            (b"GET /documents/x HTTP/1.1\r\nHost: local\r\n\r\n", 401),
            (b"GET / HTTP/1.1\r\nHost: local\r\nContent-Length: -1\r\n\r\n", 400),
        ]:
            reader = asyncio.StreamReader()
            reader.feed_data(request)
            reader.feed_eof()
            writer = Writer()
            await handle(reader, writer, self.api)
            self.assertTrue(writer.data.startswith(f"HTTP/1.1 {expected}".encode()))
            self.assertTrue(writer.closed)
            head, body = writer.data.split(b"\r\n\r\n", 1)
            self.assertIn(f"Content-Length: {len(body)}".encode(), head)


class InputBoundaryTests(unittest.TestCase):
    def test_size_finite_and_duplicate_json(self):
        for body in [b"x" * 4097, b'{"text":NaN}', b'{"text":"a","text":"b"}',
                     ('{"text":"' + 'x' * 2001 + '"}').encode()]:
            with self.subTest(body=body[:40]), self.assertRaises(ValueError):
                decode_document(body)
        self.assertEqual(decode_document(b'{"text":""}'), "")

    def test_framing_rejects_ambiguous_requests(self):
        cases = [b"GET / HTTP/1.1\r\nHost: x\r\nContent-Length: 1\r\nContent-Length: 2",
                 b"GET / HTTP/1.1\r\nHost: x\r\nTransfer-Encoding: chunked",
                 b"GET / HTTP/1.1", b"PUT / HTTP/1.1\r\nHost: x\r\nContent-Length: 4097",
                 b"GET / HTTP/2\r\nHost: x", b"GET / HTTP/1.1\r\n Bad: x\r\nHost: x"]
        for head in cases:
            with self.subTest(head=head), self.assertRaises(ValueError):
                parse_head(head)


class LocalSocketTests(unittest.IsolatedAsyncioTestCase):
    async def test_real_loopback_put_get_and_owner_denial(self):
        with tempfile.TemporaryDirectory() as directory:
            api = DocumentAPI(DocumentStore(Path(directory) / "http.sqlite3"), {"token-a": "alice", "token-b": "bob"})
            async def handler(reader, writer):
                await handle(reader, writer, api)
            server = await asyncio.start_server(handler, "127.0.0.1", 0, limit=8192)
            port = server.sockets[0].getsockname()[1]
            async with server:
                async def request(method, token, body=b""):
                    reader, writer = await asyncio.open_connection("127.0.0.1", port)
                    try:
                        head = (f"{method} /documents/example HTTP/1.1\r\nHost: localhost\r\n"
                                f"Authorization: Bearer {token}\r\nContent-Type: application/json\r\n"
                                f"Content-Length: {len(body)}\r\n\r\n").encode()
                        writer.write(head + body)
                        await writer.drain()
                        response = await asyncio.wait_for(reader.read(), 3)
                    finally:
                        writer.close()
                        await writer.wait_closed()
                    return response
                write = await request("PUT", "token-a", b'{"text":"persisted over a socket"}')
                self.assertTrue(write.startswith(b"HTTP/1.1 200"))
                own = await request("GET", "token-a")
                self.assertIn(b"persisted over a socket", own)
                other = await request("GET", "token-b")
                self.assertTrue(other.startswith(b"HTTP/1.1 404"))
                absent = await request("GET", "wrong-token")
                self.assertTrue(absent.startswith(b"HTTP/1.1 401"))
