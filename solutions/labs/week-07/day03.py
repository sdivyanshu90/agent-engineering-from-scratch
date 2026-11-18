import json
def run(decisions,tools):
    observations=[]
    for raw in decisions:
        try: decision=json.loads(raw)
        except (ValueError,TypeError): return 'failed',observations
        if not isinstance(decision,dict): return 'failed',observations
        if decision.get('type')=='finish' and set(decision)=={'type','answer'} and isinstance(decision['answer'],str): return 'completed',observations
        if decision.get('type')!='calls' or set(decision)!={'type','calls'} or not isinstance(decision['calls'],list): return 'failed',observations
        # preflight all calls before invoking any handler
        prepared=[]
        for call in decision['calls']:
            if not isinstance(call,dict) or set(call)!={'name','arguments'} or call['name'] not in tools: return 'failed',observations
            prepared.append((tools[call['name']],call['arguments']))
        for handler,args in prepared:
            try: observations.append({'ok':True,'result':handler(**args)})
            except (TypeError,ValueError) as e: observations.append({'ok':False,'error':type(e).__name__})
    return 'budget_exhausted',observations
