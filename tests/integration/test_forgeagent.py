"""Offline integration tests for the bounded coding-agent fixture."""
import asyncio
import json
from pathlib import Path

import tempfile
import unittest

from forgeagent.coding import CodingSession, sha256_text
from forgeagent.context import ContextItem
from forgeagent.durable import EventJournal
from forgeagent.policy import PolicyDenied, Workspace
from scripts.demo_forgeagent import ScriptedProvider, FixtureBackend


def fixture(tmp_path):
    (tmp_path / 'src').mkdir()
    (tmp_path / 'src/math.py').write_text('def add(left, right):\n    return left - right\n')
    return Workspace(tmp_path)


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.tmp_path = Path(directory.name)

    def test_full_proposal_approval_and_fixture_validation(self):
        tmp_path = self.tmp_path
        async def run():
            session = CodingSession(ScriptedProvider(), fixture(tmp_path), test_backend=FixtureBackend())
            result = await session.run('Repair the owned fixture.')
            assert result.status == 'completed'
            proposal = next(x.result for x in result.observations if x.name == 'propose_patch')
            assert (tmp_path / 'src/math.py').read_text().endswith('left - right\n')
            with self.assertRaises(PolicyDenied):
                session.repo.approve_and_apply(proposal['proposal_id'], 'wrong')
            assert session.repo.approve_and_apply(proposal['proposal_id'], proposal['review_sha256']) == proposal['after_sha256']
            assert session.repo.run_tests()['status'] == 'passed'
        asyncio.run(run())

    def test_journal_resume_after_approval_event(self):
        tmp_path = self.tmp_path
        async def run():
            workspace = fixture(tmp_path)
            journal = EventJournal(tmp_path / 'events.db')
            session = CodingSession(ScriptedProvider(), workspace, journal=journal)
            result = await session.run('Repair fixture')
            proposal = next(x.result for x in result.observations if x.name == 'propose_patch')
            session.repo.approve_and_apply(proposal['proposal_id'], proposal['review_sha256'])
            restored = CodingSession(ScriptedProvider(), Workspace(tmp_path), journal=journal)
            resumed = await restored.run('Repair fixture', resume=True)
            assert resumed.status == 'completed'
            assert (tmp_path / 'src/math.py').read_text().endswith('left + right\n')
        asyncio.run(run())

    def test_missing_isolation_backend_fails_closed(self):
        tmp_path = self.tmp_path
        session = CodingSession(ScriptedProvider(), fixture(tmp_path))
        with self.assertRaises(PolicyDenied):
            session.repo.run_tests()


    def test_compacted_context_preserves_provenance_across_resume(self):
        async def run():
            journal = EventJournal(self.tmp_path / "events.db")
            workspace = fixture(self.tmp_path)
            provider = ScriptedProvider()
            session = CodingSession(provider, workspace, journal=journal)
            session.save_context([ContextItem("note", "old evidence", "tool",
                                             "fixture", "untrusted", "rev-1", 1)])
            first = await session.run("Repair fixture")
            self.assertEqual(first.status, "completed")
            new_session = CodingSession(ScriptedProvider(), Workspace(self.tmp_path), journal=journal)
            restored = await new_session.run("Repair fixture", resume=True)
            self.assertEqual(restored.status, "completed")
            saved = journal.resume("local", "coding", "agent")["state"]
            initial = json.loads(saved["messages"][1]["content"])
            self.assertEqual(initial["untrusted_compacted_context"], new_session.context)
            self.assertIn("rev-1", new_session.context[0]["source_revisions"])
            self.assertIn("untrusted", new_session.context[0]["authority"])
        asyncio.run(run())

    def test_grounded_evidence_and_scope(self):
        session = CodingSession(ScriptedProvider(), fixture(self.tmp_path), read_only=True)
        (self.tmp_path / ".env.development").write_text("private_marker=hidden")
        answer = session.repo.evidence("add")
        citation = answer["citations"][0]
        self.assertEqual(citation["path"], "src/math.py")
        self.assertEqual(citation["revision"], sha256_text(session.repo.read(citation["path"])["text"]))
        self.assertTrue(session.repo.evidence("private_marker")["abstained"])
        self.assertNotIn("propose_patch", session.agent.allowed)
        self.assertNotIn("run_tests", session.agent.allowed)
