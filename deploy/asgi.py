"""Authenticated service with a default drill and an opt-in read-only agent."""
import json
import os
from pathlib import Path

from forgeagent.coding import CodingSession
from forgeagent.models import Reply, Usage
from forgeagent.policy import Workspace
from forgeagent.service import create_app


async def demo_handler(owner: str, session_id: str, text: str) -> dict:
    return {"accepted_characters": len(text), "mode": "demonstration"}


class EvidenceFixtureProvider:
    """Script one read-only tool call followed by a fixed completion."""
    def __init__(self, query):
        self.query = query

    async def complete(self, request):
        if len(request.messages) == 2:
            decision = {"type": "calls", "calls": [
                {"id": "evidence", "name": "retrieve_evidence",
                 "arguments": {"query": self.query}, "after": []}]}
        else:
            decision = {"type": "finish", "answer": "Evidence collection finished."}
        return Reply(json.dumps(decision), Usage(20, 20), "offline-evidence")


def coding_handler(configured_owner, authorized_root):
    """Create fresh read-only sessions rooted in an operator-selected workspace."""
    root = Path(authorized_root)
    if not root.is_absolute():
        raise RuntimeError("FORGEAGENT_WORKSPACE must be absolute")
    root = Workspace(root).root

    async def run(owner, session_id, text):
        if owner != configured_owner:
            raise PermissionError("workspace owner mismatch")
        session = CodingSession(EvidenceFixtureProvider(text[:128]), Workspace(root),
                                owner=owner, session_id=session_id, read_only=True)
        result = await session.run(text)
        if result.status != "completed" or not result.observations:
            raise RuntimeError("repository evidence request failed")
        return {"status": result.status, "evidence": result.observations[0].result}

    return run


def create_application():
    token = os.environ.get("FORGEAGENT_TOKEN", "")
    database = os.environ.get("FORGEAGENT_DATABASE", "")
    owner = os.environ.get("FORGEAGENT_OWNER", "")
    root = os.environ.get("FORGEAGENT_WORKSPACE", "")
    if not token or not owner or not database or not Path(database).is_absolute():
        raise RuntimeError("Set FORGEAGENT_TOKEN, FORGEAGENT_OWNER and an absolute FORGEAGENT_DATABASE")
    handler = coding_handler(owner, root) if root else demo_handler
    return create_app(database_path=database, tokens={token: owner}, run_handler=handler)
