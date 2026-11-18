"""Small privacy-conscious trace summaries for the local agent runtime.

Raw prompts, answers, tool arguments/results, identifiers, and exception text are
never copied into the exported record. Durations are seconds; costs are USD.
"""
from collections import Counter
import math


_SAFE_FIELDS={'event','step','calls','ok','status','seconds','code'}
_EVENTS={'model_start','model_end','tool_start','tool_end','failure','cancelled','run_end'}
_STATUSES={'running','completed','failed','timed_out','budget_exhausted','cancelled'}
_CODES={'tool_timeout','tool_failed','tool_denied','write_denied','cancelled'}


def redact_event(event):
    """Keep only explicitly reviewed low-cardinality runtime metadata."""
    if not isinstance(event,dict):return {}
    out={}
    for key,value in event.items():
        if key not in _SAFE_FIELDS:continue
        if key=='event' and value in _EVENTS:out[key]=value
        elif key=='status' and value in _STATUSES:out[key]=value
        elif key=='code' and value in _CODES:out[key]=value
        elif key in {'step','calls'} and type(value) is int and 0<=value<=100000:out[key]=value
        elif key=='ok' and type(value) is bool:out[key]=value
        elif key=='seconds' and type(value) in {int,float} and math.isfinite(value) and value>=0:out[key]=value
    return out


def percentile(values,p):
    if not values:return 0.0
    ordered=sorted(values)
    return ordered[max(0,min(len(ordered)-1,math.ceil(p*len(ordered))-1))]


def summarize(runs):
    """Aggregate completed Agent results without recording conversational data.

    `runs` may contain RunResult objects. Latency percentiles use each run's
    `run_end.seconds`; token counts include only provider-reported counts. Cost
    is known-cost accounting from caller-supplied rates, not a provider invoice.
    """
    runs=list(runs);latencies=[];statuses=Counter();event_counts=Counter();tokens=[];costs=[]
    redacted=[]
    for result in runs:
        statuses[result.status]+=1;tokens.append(result.tokens);costs.append(float(result.known_cost))
        for event in result.events:
            safe=redact_event(event);redacted.append(safe)
            if safe.get('event'):event_counts[safe['event']]+=1
            if safe.get('event')=='run_end' and isinstance(safe.get('seconds'),(int,float)):
                latencies.append(float(safe['seconds']))
    mean=lambda values:sum(values)/len(values) if values else 0.0
    return {'run_count':len(runs),'statuses':dict(sorted(statuses.items())),
        'events':dict(sorted(event_counts.items())),
        'latency_seconds':{'p50':percentile(latencies,.5),'p95':percentile(latencies,.95),'unit':'seconds'},
        'reported_tokens':{'mean':mean(tokens),'unit':'provider-reported tokens'},
        'known_cost_usd':{'mean':mean(costs),'unit':'USD from caller-supplied rates'},
        'redacted_events':redacted,
        'privacy':'Prompts, answers, tool names/arguments/results, call IDs, model IDs, and raw errors excluded.'}


def compare_routes(rows):
    """Summarize already-graded route observations; does not infer causality."""
    output={}
    for row in rows:
        name=row['route'];bucket=output.setdefault(name,{'n':0,'pass':0,'seconds':[],'cost_usd':[]})
        bucket['n']+=1;bucket['pass']+=bool(row['passed'])
        bucket['seconds'].append(float(row['seconds']));bucket['cost_usd'].append(float(row['cost_usd']))
    return {name:{'n':b['n'],'pass_rate':b['pass']/b['n'],'latency_seconds_p50':percentile(b['seconds'],.5),
        'known_cost_usd_mean':sum(b['cost_usd'])/b['n'],'cost_unit':'USD'} for name,b in sorted(output.items())}
