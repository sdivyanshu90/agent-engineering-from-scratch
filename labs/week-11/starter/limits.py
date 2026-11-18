"""D65 starter: deterministic admission and honest cost estimates."""


class Bucket:
    def __init__(self, rate_per_second, capacity):
        raise NotImplementedError

    def take(self, now):
        raise NotImplementedError


def capacity(worker_count, mean_seconds):
    raise NotImplementedError


def estimate_cost(input_tokens, output_tokens, input_rate, output_rate):
    """Rates are USD per million tokens; return None if a rate is unknown."""
    raise NotImplementedError
