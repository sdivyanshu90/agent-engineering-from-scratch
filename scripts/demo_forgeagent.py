"""Offline contract demo for a generated repository fixture."""
import argparse
import asyncio
import json
from pathlib import Path
import tempfile

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forgeagent.coding import CodingSession
from forgeagent.models import Reply, Usage
from forgeagent.policy import Workspace


class ScriptedProvider:
    """Deterministically reads a fixture, proposes a known patch, then stops."""
    def __init__(self): self.index=0
    async def complete(self,request):
        self.index+=1
        if self.index==1:
            text={"type":"calls","calls":[{"id":"read-1","name":"read_file",
                "arguments":{"path":"src/math.py"},"after":[]}]}
        elif self.index==2:
            observation=json.loads(request.messages[-1].content)["untrusted_tool_observations"][0]["result"]
            text={"type":"calls","calls":[{"id":"proposal-1","name":"propose_patch",
                "arguments":{"path":"src/math.py","expected_sha256":observation["sha256"],
                    "replacement_text":"def add(left, right):\n    return left + right\n"},"after":[]}]}
        else:
            text={"type":"finish","answer":"The exact patch is proposed and awaits human approval."}
        return Reply(json.dumps(text),Usage(40,20),f"offline-{self.index}")


class FixtureBackend:
    """Checks one known fixture predicate without executing the submitted code."""
    def run(self,argv,*,cwd,timeout):
        expected=("def add(left, right):\n    return left + right\n")
        actual=(Path(cwd)/"src/math.py").read_text(encoding="utf-8")
        if actual!=expected: return {"status":"failed","executed":False,"evidence":"fixture predicate mismatch"}
        return {"status":"passed","executed":False,"evidence":"known fixture text predicate; no code executed"}


async def main(*, isolated=False, interactive=False):
    with tempfile.TemporaryDirectory(prefix="forgeagent-demo-") as directory:
        root=Path(directory);(root/"src").mkdir()
        (root/"src/math.py").write_text("def add(left, right):\n    return left - right\n",encoding="utf-8")
        backend = FixtureBackend()
        if isolated:
            from forgeagent.isolation import BubblewrapTests
            (root / "tests").mkdir()
            (root / "tests/test_add.py").write_text(
                "import unittest\nfrom src.math import add\n\n"
                "class AddTest(unittest.TestCase):\n"
                "    def test_add(self):\n"
                "        self.assertEqual(add(2, 3), 5)\n",
                encoding="utf-8",
            )
            backend = BubblewrapTests()
        session=CodingSession(ScriptedProvider(),Workspace(root),session_id="demo-1",test_backend=backend)
        result=await session.run("Repair the add function in src/math.py. Propose an exact change; stop for review.")
        proposal=next(o.result for o in result.observations if o.name=="propose_patch")
        print("agent status:",result.status)
        print("review this exact file: src/math.py")
        print("before SHA-256:",proposal["before_sha256"])
        print("after SHA-256:",proposal["after_sha256"])
        print("review digest:",proposal["review_sha256"])
        print("replacement:\ndef add(left, right):\n    return left + right")
        if interactive and input("Type 'approve' to apply this fixture replacement: ") != "approve":
            print("Proposal declined.")
            return 0
        if not interactive:
            print("Simulated approval of the generated fixture.")
        applied=session.repo.approve_and_apply(proposal["proposal_id"],proposal["review_sha256"])
        print("human-approved apply SHA-256:",applied)
        outcome=session.repo.run_tests()
        print("test adapter result:",json.dumps(outcome,sort_keys=True))
        if isolated:
            print("Scope: scripted provider and generated tests in Linux namespaces.")
        else:
            print("Scope: scripted provider and fixture text predicate.")
        return 0 if outcome["status"] == "passed" else 1


if __name__=="__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--isolated", action="store_true", help="run the generated test using Linux Bubblewrap")
    parser.add_argument("--interactive", action="store_true", help="pause for human review")
    args = parser.parse_args()
    raise SystemExit(asyncio.run(main(isolated=args.isolated, interactive=args.interactive)))
