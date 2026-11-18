import asyncio
import json
from pathlib import Path
import unittest

from forgeagent.evaluation import evaluate,load_fixture,wilson
from forgeagent.telemetry import redact_event

ROOT=Path(__file__).resolve().parents[2]

class AgentEvaluationTests(unittest.TestCase):
    def test_development_fixture_runs_actual_agent(self):
        fixture=load_fixture(ROOT/'datasets/evaluation-fixtures/agent-development.json')
        report=evaluate(fixture,split='dev')
        self.assertEqual(report['case_count'],11)
        self.assertEqual(report['passed'],11)
        self.assertTrue(all(row['fixture_requests']>=1 for row in report['cases']))
        self.assertTrue(all('wall_seconds' in row for row in report['cases']))

    def test_split_mismatch_and_interval(self):
        fixture=load_fixture(ROOT/'datasets/evaluation-fixtures/agent-development.json')
        with self.assertRaises(ValueError):evaluate(fixture,split='heldout')
        lo,hi=wilson(4,4)
        self.assertLess(lo,1);self.assertEqual(hi,1)

    def test_telemetry_allowlist_drops_payload_and_untrusted_values(self):
        safe=redact_event({'event':'tool_start','step':2,'tool':'send_email','arguments':'secret','status':'prompt secret'})
        self.assertEqual(safe,{'event':'tool_start','step':2})
