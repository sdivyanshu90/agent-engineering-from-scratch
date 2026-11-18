"""D64 starter: avoid raw inputs, identifiers, and unbounded labels."""


def safe_event(event):
    """Return only event/state/attempt/seconds/status fields."""
    raise NotImplementedError


def durations(accepted, started, finished):
    """Return queue, execution, and end-to-end seconds after validation."""
    raise NotImplementedError


def histogram_bucket(value, bounds):
    """Return the first inclusive upper bound or '+Inf'."""
    raise NotImplementedError
