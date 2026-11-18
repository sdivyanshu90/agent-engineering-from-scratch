"""Fail-closed demonstration deployment; the handler does not run agent tools."""
import os
from pathlib import Path

from forgeagent.service import create_app


async def demo_handler(owner: str, session_id: str, text: str) -> dict:
    # A deployment must explicitly replace this with an authorized agent runner.
    return {"accepted_characters": len(text), "mode": "demonstration"}


def create_application():
    token = os.environ.get("FORGEAGENT_TOKEN", "")
    database = os.environ.get("FORGEAGENT_DATABASE", "")
    owner = os.environ.get("FORGEAGENT_OWNER", "")
    if not token or not owner or not database or not Path(database).is_absolute():
        raise RuntimeError("Set FORGEAGENT_TOKEN, FORGEAGENT_OWNER and an absolute FORGEAGENT_DATABASE")
    return create_app(database_path=database, tokens={token: owner}, run_handler=demo_handler)
