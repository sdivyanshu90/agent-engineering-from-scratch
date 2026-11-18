"""Integration contracts for the bounded Week 7 runtime."""
import asyncio
import json
import unittest
from decimal import Decimal

from forgeagent.models import FakeProvider, Reply, Usage, ProviderError
from forgeagent.runtime import (
    Agent, Budgets, Call, Observation, Registry, Rejected, Tool,
    dispatch, layers, parse_decision, strict_json, validate_arguments,
)


def reply(text, inp=5, out=3):
    return Reply(text, Usage(inp, out))


def schema(properties=None, required=()):
    return {'type':'object','properties':properties or {},'required':list(required),'additionalProperties':False}


class RuntimeTests(unittest.TestCase):
    def test_json_and_schema_are_closed_and_noncoercing(self):
        self.assertEqual(strict_json('{"x":1}'), {'x':1})
        for text in ('{"x":1,"x":2}', 'NaN', '[', ' ' * 200):
            with self.subTest(text=text[:8]), self.assertRaises(Rejected): strict_json(text, 100)
        spec=schema({'n':{'type':'integer','minimum':1,'maximum':4},'b':{'type':'boolean'}}, ['n'])
        self.assertEqual(validate_arguments({'n':2,'b':True}, spec), {'n':2,'b':True})
        for args in ({'n':True}, {'n':0}, {'n':2,'unknown':1}, {}):
            with self.subTest(args=args), self.assertRaises(Rejected): validate_arguments(args,spec)

    def test_tool_denial_and_invalid_arguments_preflight_without_effects(self):
        async def scenario():
            effects=[]; registry=Registry()
            async def write(value): effects.append(value); return 'changed'
            registry.register(Tool('write','Change a value',schema({'value':{'type':'string'}}),write,'write'))
            with self.assertRaises(Rejected):
                await dispatch([Call('a','write',{'value':'x'})],registry,{'other'},allow_write=True)
            with self.assertRaises(Rejected):
                await dispatch([Call('a','write',{'value':'x','extra':1})],registry,{'write'},allow_write=True)
            with self.assertRaises(Rejected):
                await dispatch([Call('a','write',{'value':'x'})],registry,{'write'})
            self.assertEqual(effects,[])
        asyncio.run(scenario())

    def test_dependency_graph_rejects_cycle_and_missing_before_side_effect(self):
        async def scenario():
            effects=[]; registry=Registry()
            async def write(): effects.append('ran'); return 1
            registry.register(Tool('write','Write',schema(),write,'write'))
            for calls in ([Call('a','write',{},('absent',))],
                          [Call('a','write',{},('b',)),Call('b','write',{},('a',))]):
                with self.assertRaises(Rejected): await dispatch(calls,registry,{'write'},allow_write=True)
            self.assertEqual(effects,[])
        asyncio.run(scenario())

    def test_dense_dag_layers_are_linear_contract_and_stable_with_duplicates_rejected(self):
        # Four complete bipartite layers exercise many edges while input order
        # deliberately interleaves nodes from distinct depths.
        calls=[]
        for level in range(4):
            for index in range(6):
                identifier=f'l{level}n{index}'
                parents=[] if level==0 else [f'l{level-1}n{p}' for p in range(6)]
                calls.append(Call(identifier,'read',{},tuple(parents)))
        calls.reverse()
        result=layers(calls)
        expected=[[f'l{level}n{index}' for index in reversed(range(6))] for level in range(4)]
        self.assertEqual([[call.identifier for call in group] for group in result],expected)
        with self.assertRaises(Rejected): layers([Call('dup','read',{}),Call('dup','read',{})])
        duplicated='{"type":"calls","calls":[' \
            '{"id":"dup","name":"read","arguments":{},"after":[]},' \
            '{"id":"dup","name":"read","arguments":{},"after":[]}]} '
        with self.assertRaises(Rejected): parse_decision(duplicated)

    def test_dependent_calls_use_stable_layers_and_skip_on_failure(self):
        async def scenario():
            effects=[]; registry=Registry()
            async def bad(): effects.append('bad'); raise ValueError('secret detail')
            async def downstream(): effects.append('downstream'); return 'unexpected'
            async def independent(): effects.append('independent'); return 'ok'
            registry.register(Tool('bad','Fail safely',schema(),bad,'read'))
            registry.register(Tool('downstream','Dependent',schema(),downstream,'read'))
            registry.register(Tool('independent','Independent',schema(),independent,'read'))
            calls=[Call('a','bad',{}),Call('b','downstream',{},('a',)),Call('c','independent',{})]
            self.assertEqual([[c.identifier for c in layer] for layer in layers(calls)],[['a','c'],['b']])
            obs=await dispatch(calls,registry,{'bad','downstream','independent'})
            self.assertEqual([o.error for o in obs],['tool_failed','dependency_failed',None])
            self.assertNotIn('downstream',effects)
        asyncio.run(scenario())

    def test_read_only_calls_overlap_and_results_keep_request_order(self):
        async def scenario():
            active=0; peak=0; registry=Registry()
            async def read(value):
                nonlocal active,peak
                active+=1; peak=max(active,peak); await asyncio.sleep(.03); active-=1; return value
            registry.register(Tool('read','Read',schema({'value':{'type':'integer'}}),read,'read'))
            result=await dispatch([Call('one','read',{'value':1}),Call('two','read',{'value':2})],registry,{'read'})
            self.assertGreaterEqual(peak,2)
            self.assertEqual([x.result for x in result],[1,2])
        asyncio.run(scenario())

    def test_writes_in_batch_are_serialized(self):
        async def scenario():
            active=0; peak=0; registry=Registry()
            async def write():
                nonlocal active,peak
                active+=1; peak=max(active,peak); await asyncio.sleep(.01); active-=1; return True
            registry.register(Tool('write','Write',schema(),write,'write'))
            await dispatch([Call('a','write',{}),Call('b','write',{})],registry,{'write'},allow_write=True)
            self.assertEqual(peak,1)
        asyncio.run(scenario())

    def test_timeout_and_tool_output_bounds_are_observations(self):
        async def scenario():
            registry=Registry()
            async def slow(): await asyncio.sleep(.05); return 'late'
            async def huge(): return 'x'*5000
            registry.register(Tool('slow','Slow',schema(),slow)); registry.register(Tool('huge','Huge',schema(),huge))
            obs=await dispatch([Call('s','slow',{}),Call('h','huge',{})],registry,{'slow','huge'},timeout=.005)
            self.assertEqual([o.error for o in obs],['tool_timeout','tool_failed'])
        asyncio.run(scenario())

    def test_unexpected_programming_error_propagates(self):
        async def scenario():
            registry=Registry()
            async def broken(): raise RuntimeError('programmer defect')
            registry.register(Tool('broken','Broken',schema(),broken))
            with self.assertRaises(ExceptionGroup):
                await dispatch([Call('x','broken',{})],registry,{'broken'})
        asyncio.run(scenario())

    def test_completed_model_usage_can_overshoot_and_blocks_effects(self):
        async def scenario():
            effects=[]; registry=Registry()
            async def write(): effects.append(1); return 1
            registry.register(Tool('write','Write',schema(),write,'write'))
            p=FakeProvider([reply('{"type":"calls","calls":[{"id":"x","name":"write","arguments":{},"after":[]}]}',9,2)])
            result=await Agent(p,registry,{'write'},budgets=Budgets(tokens=10),rates=('2','2')).run('change')
            self.assertEqual(result.status,'budget_exhausted'); self.assertEqual(result.tokens,11)
            self.assertEqual(effects,[]); self.assertEqual(len(p.requests),1)
        asyncio.run(scenario())

    def test_tool_count_budget_prevents_batch(self):
        async def scenario():
            effects=[]; registry=Registry()
            async def read(): effects.append(1); return 1
            registry.register(Tool('read','Read',schema(),read))
            p=FakeProvider([reply('{"type":"calls","calls":[{"id":"a","name":"read","arguments":{},"after":[]},{"id":"b","name":"read","arguments":{},"after":[]}]}')])
            result=await Agent(p,registry,{'read'},budgets=Budgets(tools=1)).run('read')
            self.assertEqual(result.status,'budget_exhausted'); self.assertEqual(effects,[])
        asyncio.run(scenario())

    def test_caller_cancellation_reraises_and_records_terminal_trace(self):
        async def scenario():
            class WaitingProvider:
                async def complete(self, request): await asyncio.Event().wait()
            agent=Agent(WaitingProvider(),Registry(),[],budgets=Budgets(seconds=2))
            events=[]
            task=asyncio.create_task(agent.run('cancel',events=events))
            await asyncio.sleep(.01); task.cancel()
            with self.assertRaises(asyncio.CancelledError): await task
            self.assertEqual(events[-1]['status'],'cancelled')
            self.assertIn({'event':'cancelled'},events)
        asyncio.run(scenario())

    def test_agent_records_and_propagates_unexpected_programming_error(self):
        async def scenario():
            registry=Registry()
            async def broken(): raise RuntimeError('bug')
            registry.register(Tool('broken','Broken',schema(),broken))
            p=FakeProvider([reply('{"type":"calls","calls":[{"id":"x","name":"broken","arguments":{},"after":[]}]}')])
            events=[]
            with self.assertRaises(ExceptionGroup):
                await Agent(p,registry,{'broken'}).run('run',events=events)
            self.assertEqual(events[-1]['status'],'failed')
            self.assertIn({'event':'internal_error'},events)
        asyncio.run(scenario())

    def test_outer_deadline_and_provider_error_have_distinct_statuses(self):
        async def scenario():
            class Slow:
                async def complete(self, request): await asyncio.sleep(.1)
            timed=await Agent(Slow(),Registry(),[],budgets=Budgets(seconds=.01)).run('slow')
            self.assertEqual(timed.status,'timed_out')
            failed=await Agent(FakeProvider([ProviderError('offline')]),Registry(),[]).run('offline')
            self.assertEqual(failed.status,'failed')
            self.assertIn({'event':'failure','code':'offline'},failed.events)
        asyncio.run(scenario())

    def test_write_requires_per_call_grant_even_when_discovered(self):
        async def scenario():
            calls=[]; registry=Registry()
            async def write(): calls.append('ran'); return 1
            registry.register(Tool('write','Write',schema(),write,'write'))
            p=FakeProvider([reply('{"type":"calls","calls":[{"id":"a","name":"write","arguments":{},"after":[]}]}')])
            result=await Agent(p,registry,{'write'}).run('write')
            self.assertEqual(result.status,'failed'); self.assertEqual(calls,[])
        asyncio.run(scenario())
