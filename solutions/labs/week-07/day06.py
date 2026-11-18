def summarize(events):
    if not isinstance(events,list): raise ValueError('events must be list')
    counts={}; failures=[]; status='unknown'
    for event in events:
        if not isinstance(event,dict) or not isinstance(event.get('event'),str): raise ValueError('invalid event')
        name=event['event']; counts[name]=counts.get(name,0)+1
        if name=='failure': failures.append(str(event.get('code','unknown'))[:64])
        if name=='run_end': status=event.get('status','unknown')
    return {'counts':counts,'status':status,'failures':failures}
