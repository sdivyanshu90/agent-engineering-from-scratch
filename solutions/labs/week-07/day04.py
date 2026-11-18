def layers(calls):
    ids=[call_id for call_id,_ in calls]
    if len(set(ids))!=len(ids): raise ValueError('duplicate id')
    known=set(ids)
    if any(not set(deps)<=known for _,deps in calls): raise ValueError('missing dependency')
    pending=list(calls);done=set();result=[]
    while pending:
        ready=[item for item in pending if set(item[1])<=done]
        if not ready: raise ValueError('cycle')
        result.append([item[0] for item in ready]); done.update(item[0] for item in ready)
        pending=[item for item in pending if item not in ready]
    return result
