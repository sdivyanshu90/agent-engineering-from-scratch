from forgeagent.durable import Step,plan,verify_plan
def verify(steps,layers): return verify_plan(steps,layers)
def evaluate(candidate,checks,required,max_revisions=2):
    if type(max_revisions) is not int or max_revisions<0: raise ValueError('invalid revision limit')
    by_name={c['name']:c for c in checks}
    if len(by_name)!=len(checks) or set(by_name)!=set(required): raise ValueError('rubric mismatch')
    if any(type(c.get('passed')) is not bool or not isinstance(c.get('evidence'),str) or not c['evidence'] for c in checks):
        raise ValueError('check evidence required')
    failures=sorted(name for name,c in by_name.items() if not c['passed'])
    return {'candidate':candidate,'status':'accept' if not failures else ('revise' if max_revisions else 'reject'),'failures':failures}
