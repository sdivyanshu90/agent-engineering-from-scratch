def recover_snapshot(saved_state,saved_revision,events):
    if type(saved_revision) is not int or saved_revision<0: raise ValueError("bad revision")
    state=saved_state;revision=saved_revision
    for event in events:
        if type(event.get("revision")) is not int or event["revision"]<=revision: continue
        if event.get("kind")!="agent_snapshot": continue
        payload=event.get("payload")
        if not isinstance(payload,dict) or not isinstance(payload.get("snapshot"),dict):
            raise ValueError("full snapshot event required")
        state=payload["snapshot"];revision=event["revision"]
    if state is None: raise ValueError("no recoverable snapshot")
    return {"revision":revision,"state":state}
