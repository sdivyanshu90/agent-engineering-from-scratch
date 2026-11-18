"""Deterministic evaluation harness for the bounded Agent interface.

Fixtures provide model decisions, while graders inspect the resulting Agent
trace and side effects. This measures protocol execution, not model intelligence.
"""
from __future__ import annotations

import asyncio
from collections import Counter
from pathlib import Path
import json
import math
import statistics
import time

from .models import FakeProvider, Reply, Usage
from .runtime import Agent, Budgets, Registry, Tool


def load_fixture(path):
    value=json.loads(Path(path).read_text(encoding='utf-8'))
    if value.get('schema_version')!=1 or not isinstance(value.get('cases'),list):
        raise ValueError('unsupported fixture schema')
    return value


def _registry(case,side_effects):
    registry=Registry()
    async def lookup(key):
        if key=='fail':raise ValueError('fixture failure')
        if key=='slow':await asyncio.sleep(.05)
        return case.get('lookup',{}).get(key,'missing')
    async def mutate(value):
        side_effects.append(value);return {'stored':value}
    registry.register(Tool('lookup','Look up a fixture value',{'type':'object','properties':{'key':{'type':'string','maxLength':32}},'required':['key'],'additionalProperties':False},lookup))
    registry.register(Tool('store','Store a fixture value',{'type':'object','properties':{'value':{'type':'string','maxLength':32}},'required':['value'],'additionalProperties':False},mutate,'write'))
    return registry


def _replies(case):
    return [Reply(step['text'],Usage(step.get('input_tokens',8),step.get('output_tokens',4))) for step in case['steps']]


def grade(case,result,side_effects,provider):
    """Exact, per-case deterministic checks; no fuzzy/model grader involved."""
    expected=case['expected']
    calls=[o.name for o in result.observations]
    checks={
        'status':result.status==expected.get('status','completed'),
        'answer':result.answer==expected.get('answer',''),
        'tool_sequence':calls==expected.get('tool_sequence',[]),
        'side_effects':side_effects==expected.get('side_effects',[]),
        'steps':result.steps<=expected.get('max_steps',99),
        'budget':result.tokens<=case.get('budgets',{}).get('tokens',8192),
    }
    if 'observation_ok' in expected:
        checks['observation_ok']=[o.ok for o in result.observations]==expected['observation_ok']
    if 'error' in expected:
        checks['error']=[o.error for o in result.observations]==expected['error']
    return {'id':case['id'],'passed':all(checks.values()),'checks':checks,
            'status':result.status,'answer':result.answer,'tool_calls':result.tool_calls,
            'steps':result.steps,'tokens':result.tokens,'known_cost_usd':float(result.known_cost),
            'latency_seconds':sum(e.get('seconds',0) for e in result.events if e.get('event')=='run_end'),
            'event_names':[e.get('event') for e in result.events],
            'fixture_requests':len(provider.requests)}


async def _evaluate_case(case):
    if case.get('mode')=='cancellation':return await _evaluate_cancellation(case)
    effects=[];provider=FakeProvider(_replies(case));registry=_registry(case,effects)
    raw=case.get('budgets',{})
    budgets=Budgets(steps=raw.get('steps',6),tools=raw.get('tools',12),tokens=raw.get('tokens',8192),
        seconds=raw.get('seconds',2),tool_seconds=raw.get('tool_seconds',.1))
    agent=Agent(provider,registry,case.get('allowed',['lookup']),budgets=budgets,
        rates=tuple(case.get('rates_usd_per_million',['0','0'])))
    began=time.perf_counter();result=await agent.run(case['task'],allow_write=case.get('allow_write',False))
    row=grade(case,result,effects,provider);row['wall_seconds']=time.perf_counter()-began
    return row


async def _evaluate_cancellation(case):
    """Cancel a real Agent while it awaits its provider; assert no tool effect."""
    started=asyncio.Event();effects=[];registry=_registry(case,effects)
    class WaitingProvider:
        async def complete(self,request):started.set();await asyncio.Event().wait()
    agent=Agent(WaitingProvider(),registry,case.get('allowed',['lookup']))
    events=[];began=time.perf_counter();task=asyncio.create_task(agent.run(case['task'],events=events))
    await started.wait();task.cancel()
    try:await task
    except asyncio.CancelledError:cancelled=True
    else:cancelled=False
    checks={'cancelled':cancelled,'event_recorded':any(e.get('event')=='cancelled' for e in events),
            'no_side_effect':not effects}
    elapsed=time.perf_counter()-began
    return {'id':case['id'],'passed':all(checks.values()),'checks':checks,'status':'cancelled' if cancelled else 'not_cancelled',
        'answer':'','tool_calls':0,'steps':1,'tokens':0,'known_cost_usd':0.0,'latency_seconds':elapsed,
        'event_names':[e.get('event') for e in events],'fixture_requests':1,'wall_seconds':elapsed}


def evaluate(fixture,*,split):
    """Run a named frozen split. Split label is explicit in all output."""
    if split not in {'dev','heldout'}:raise ValueError('split must be dev or heldout')
    if fixture.get('split')!=split:raise ValueError('fixture split mismatch')
    rows=asyncio.run(_evaluate_all(fixture['cases']))
    latency=[r['wall_seconds'] for r in rows]
    costs=[r['known_cost_usd'] for r in rows]
    return {'split':split,'case_count':len(rows),'passed':sum(r['passed'] for r in rows),
        'pass_rate':sum(r['passed'] for r in rows)/len(rows) if rows else 0,
        'latency_seconds':{'p50':_percentile(latency,.5),'p95':_percentile(latency,.95),'unit':'seconds; local wall clock'},
        'known_cost_usd':{'mean':statistics.fmean(costs) if costs else 0,'unit':'USD; supplied fixture rates only'},
        'cases':rows,'interpretation':'Deterministic protocol/fixture regression. Not a live model quality estimate; timing is machine-dependent.'}


async def _evaluate_all(cases):
    return [await _evaluate_case(case) for case in cases]


def _percentile(values,p):
    if not values:return 0.0
    ordered=sorted(values);return ordered[min(len(ordered)-1,math.ceil(p*len(ordered))-1)]


def wilson(successes,n,z=1.96):
    """Wilson interval for binomial proportion; small fixtures remain uncertain."""
    if type(n) is not int or n<=0 or type(successes) is not int or not 0<=successes<=n:raise ValueError('invalid counts')
    p=successes/n;d=1+z*z/n;c=(p+z*z/(2*n))/d
    h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return [max(0,c-h),min(1,c+h)]
