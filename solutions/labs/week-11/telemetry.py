"""Reference: finite fields and explicit temporal measurements."""
import math

SAFE = {"event", "state", "attempt", "seconds", "status"}


def safe_event(event):
    return {key: value for key, value in event.items() if key in SAFE}


def durations(accepted, started, finished):
    values = (accepted, started, finished)
    if any(not isinstance(value, (int, float)) or not math.isfinite(value)
           for value in values):
        raise ValueError("timestamps must be finite numbers")
    queue = started - accepted
    execution = finished - started
    total = finished - accepted
    if min(queue, execution, total) < 0:
        raise ValueError("timestamps must be ordered")
    return {"queue": queue, "execution": execution, "end_to_end": total}


def histogram_bucket(value, bounds):
    ordered = list(bounds)
    if any(not isinstance(bound, (int, float)) or not math.isfinite(bound)
           for bound in ordered) or ordered != sorted(set(ordered)):
        raise ValueError("bounds must be unique increasing finite numbers")
    if not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError("value must be finite")
    for bound in ordered:
        if value <= bound:
            return bound
    return "+Inf"
