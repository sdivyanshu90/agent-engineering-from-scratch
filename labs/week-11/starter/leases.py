"""D63 starter: model durable claim generations and stale-finish rejection."""


def claim(rows, now, lease_seconds, token):
    """Claim oldest queued/expired row; return updated copy or None."""
    raise NotImplementedError


def finish(rows, job_id, token, result):
    """Finish only a running row whose current lease token matches."""
    raise NotImplementedError
