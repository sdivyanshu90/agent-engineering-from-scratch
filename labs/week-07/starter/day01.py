"""Lab 1: classify a fixed workflow or an agent loop. Implement route()."""
def route(task, confidence):
    """Return workflow for fixed-format task, agent for underspecified task."""
    if not isinstance(task, str) or not 0 <= confidence <= 1:
        raise ValueError('invalid task or confidence')
    # TODO: choose by task category; low confidence should enter explicit review.
    return {'mode': 'workflow', 'state': 'START'}
