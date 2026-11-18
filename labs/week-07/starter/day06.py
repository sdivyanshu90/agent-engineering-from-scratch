"""Lab 6: summarize a trace without storing prompt or tool payloads."""
def summarize(events):
    # TODO: retain lifecycle counts, terminal status and stable failure category.
    return {'events':len(events),'status':'unknown','failures':0}
