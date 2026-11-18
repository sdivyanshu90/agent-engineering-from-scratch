"""Root integration checks: real snapshots, restart accounting and effect receipts."""
import asyncio
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import time
import unittest
from forgeagent.models import FakeProvider,Reply,Usage
from forgeagent.runtime import Agent,Registry,Tool,Budgets,Rejected,strict_json,layers,Call
from forgeagent.durable import EventJournal,Conflict


def decision(calls):
    return Reply(json.dumps({'type':'calls','calls':calls}),Usage(2,3))


def finish(answer='done'):
    return Reply(json.dumps({'type':'finish','answer':answer}),Usage(2,3))


def registry(handler):
    output=Registry()
    output.register(Tool('echo','Fixture',{'type':'object','properties':{'text':{'type':'string'}},'required':['text'],'additionalProperties':False},handler))
    return output


class ResumeTests(unittest.IsolatedAsyncioTestCase):
    async def test_decision_ready_restart_preserves_messages_counters_and_deadline(self):
        effects=[];saved=[]
        async def echo(text):effects.append(text);return text
        calls=[{'id':'a','name':'echo','arguments':{'text':'hello'},'after':[]}]
        async def crash(state):
            saved.append(deepcopy(state));raise RuntimeError('power loss before effect')
        first=Agent(FakeProvider([decision(calls)]),registry(echo),{'echo'})
        with self.assertRaises(RuntimeError):await first.run('task',checkpoint=crash)
        self.assertEqual(effects,[])
        self.assertEqual(saved[0]['steps'],1)
        self.assertEqual(saved[0]['tokens'],5)
        second_provider=FakeProvider([finish()])
        snapshots=[]
        async def save(state):snapshots.append(deepcopy(state))
        result=await Agent(second_provider,registry(echo),{'echo'}).run('task',resume=saved[0],checkpoint=save)
        self.assertEqual(result.status,'completed');self.assertEqual(effects,['hello'])
        self.assertEqual((result.steps,result.tool_calls,result.tokens),(2,1,10))
        self.assertEqual(snapshots[-1]['deadline_at'],saved[0]['deadline_at'])
        self.assertTrue(any('untrusted_tool_observations' in message.content for message in second_provider.requests[0].messages))
        empty=FakeProvider([])
        repeated=await Agent(empty,registry(echo),{'echo'}).run('task',resume=snapshots[-1])
        self.assertEqual(repeated.answer,'done');self.assertEqual(empty.requests,[])

    async def test_journal_receipt_prevents_repeated_effect_after_crash(self):
        with tempfile.TemporaryDirectory() as directory:
            journal=EventJournal(Path(directory)/'journal.sqlite3');effects=[];saved=[]
            async def echo(text):
                receipt=journal.intent('owner','session','op-a',{'text':text})
                if not receipt['created']:
                    if receipt['status']=='complete':return receipt['result']
                    raise Rejected('reconcile_required')
                effects.append(text)
                journal.resolve('owner','session','op-a',receipt['digest'],result=text)
                return text
            calls=[{'id':'a','name':'echo','arguments':{'text':'once'},'after':[]}]
            async def checkpoint(state):
                if state['pending_calls']:
                    saved.append(deepcopy(state))
                    journal.checkpoint('owner','session','runtime',state,0)
                else:raise RuntimeError('power loss after effect before checkpoint')
            with self.assertRaises(RuntimeError):
                await Agent(FakeProvider([decision(calls)]),registry(echo),{'echo'}).run('task',checkpoint=checkpoint)
            self.assertEqual(effects,['once'])
            restored=EventJournal(Path(directory)/'journal.sqlite3').resume('owner','session','runtime')['state']
            result=await Agent(FakeProvider([finish()]),registry(echo),{'echo'}).run('task',resume=restored)
            self.assertEqual(result.status,'completed');self.assertEqual(effects,['once'])
            receipt=journal.operation('owner','session','op-a')
            with self.assertRaises(Conflict):journal.resolve('owner','session','op-a',receipt['digest'],result='changed')

    async def test_resume_rejects_identity_or_budget_bypass_and_expired_deadline(self):
        saved=[]
        async def echo(text):return text
        async def crash(state):saved.append(deepcopy(state));raise RuntimeError()
        calls=[{'id':'a','name':'echo','arguments':{'text':'x'},'after':[]}]
        with self.assertRaises(RuntimeError):
            await Agent(FakeProvider([decision(calls)]),registry(echo),{'echo'}).run('task',checkpoint=crash)
        with self.assertRaises(Rejected):await Agent(FakeProvider([]),registry(echo),{'echo'}).run('other task',resume=saved[0])
        for settings in [{'budgets': Budgets(steps=99)}, {'rates': ('2', '8')}]:
            with self.assertRaises(Rejected):
                await Agent(FakeProvider([]), registry(echo), {'echo'}, **settings).run('task', resume=saved[0])
        invalid=deepcopy(saved[0]);invalid['steps']=-1
        with self.assertRaises(Rejected):await Agent(FakeProvider([]),registry(echo),{'echo'}).run('task',resume=invalid)
        expired=deepcopy(saved[0]);expired['deadline_at']=time.time()-1
        result=await Agent(FakeProvider([]),registry(echo),{'echo'}).run('task',resume=expired)
        self.assertEqual(result.status,'timed_out');self.assertEqual(result.tool_calls,0)


class EncodingAndLayersTests(unittest.TestCase):
    def test_unicode_surrogate_rejected_before_tool_dispatch(self):
        with self.assertRaises(Rejected):strict_json('"\\ud800"')
    def test_dense_dag_layering_and_stable_same_layer_order(self):
        calls=[Call(str(i),'echo',{},tuple(str(j) for j in range(i))) for i in range(30)]
        self.assertEqual([[call.identifier for call in level] for level in layers(calls)],[[str(i)] for i in range(30)])
        self.assertEqual([c.identifier for c in layers([Call('b','echo',{}),Call('a','echo',{})])[0]],['b','a'])
        with self.assertRaises(Rejected):layers([Call('a','echo',{}),Call('a','echo',{})])
