"""Lab 4: compute topological execution layers for (id, dependency_ids)."""
def layers(calls):
    ids={call_id for call_id,_ in calls}
    if len(ids)!=len(calls): raise ValueError('duplicate id')
    # TODO: reject missing parents and cycles; preserve input order within layers.
    return [[call_id for call_id,_ in calls]] if calls else []
