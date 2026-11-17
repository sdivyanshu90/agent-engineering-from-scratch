"""Week 2 async application boundary. No third-party API framework is used."""
import asyncio
from dataclasses import dataclass
import json
import re
import sqlite3

from .storage import DocumentStore


@dataclass(frozen=True)
class Response:
    status: int
    payload: dict


def decode_document(body: bytes) -> str:
    if len(body) > 4096:
        raise ValueError("body exceeds 4096 bytes")

    def reject_constant(value):
        raise ValueError("non-finite JSON number")

    def unique_keys(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate JSON key")
            result[key] = value
        return result

    value = json.loads(body.decode("utf-8"), parse_constant=reject_constant, object_pairs_hook=unique_keys)
    if not isinstance(value, dict) or set(value) != {"text"} or not isinstance(value["text"], str):
        raise ValueError("expected exactly one string field: text")
    if len(value["text"]) > 2000:
        raise ValueError("text exceeds 2000 code points")
    return value["text"]


class DocumentAPI:
    def __init__(self, store: DocumentStore, tokens: dict[str, str]):
        if not tokens or any(not token or not owner for token, owner in tokens.items()):
            raise ValueError("nonempty token-to-owner configuration required")
        self.store = store
        self.tokens = dict(tokens)

    async def dispatch(self, method: str, path: str, headers: dict[str, str], body: bytes) -> Response:
        # Headers in this internal interface must already have lowercase names.
        authorization = headers.get("authorization", "")
        token = authorization.removeprefix("Bearer ") if authorization.startswith("Bearer ") else ""
        owner = self.tokens.get(token)
        if owner is None:
            return Response(401, {"error": "authentication required"})
        match = re.fullmatch(r"/documents/([A-Za-z0-9_-]{1,64})", path)
        if not match:
            return Response(404, {"error": "route not found"})
        identifier = match.group(1)
        try:
            if method == "PUT":
                if headers.get("content-type") != "application/json":
                    return Response(415, {"error": "use application/json"})
                try:
                    text = decode_document(body)
                except (ValueError, UnicodeError, RecursionError):
                    return Response(400, {"error": "invalid document JSON"})
                await asyncio.to_thread(self.store.put, owner, identifier, text)
                return Response(200, {"id": identifier})
            if method == "GET":
                if body:
                    return Response(400, {"error": "GET body not accepted"})
                text = await asyncio.to_thread(self.store.get, owner, identifier)
                if text is None:
                    return Response(404, {"error": "document not found"})
                return Response(200, {"id": identifier, "text": text})
            return Response(405, {"error": "method not allowed"})
        except sqlite3.OperationalError:
            return Response(503, {"error": "storage unavailable"})
