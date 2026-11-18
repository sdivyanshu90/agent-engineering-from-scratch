"""Reference: deterministic refill with explicit estimated-cost units."""
import math


class Bucket:
    def __init__(self, rate_per_second, capacity):
        if not math.isfinite(rate_per_second) or rate_per_second <= 0:
            raise ValueError("rate must be finite and positive")
        if type(capacity) is not int or capacity < 1:
            raise ValueError("capacity must be a positive integer")
        self.rate = rate_per_second
        self.capacity = float(capacity)
        self.tokens = float(capacity)
        self.updated = None

    def take(self, now):
        if not math.isfinite(now):
            raise ValueError("time must be finite")
        if self.updated is None:
            self.updated = now
        if now < self.updated:
            raise ValueError("clock moved backward")
        self.tokens = min(self.capacity, self.tokens + (now - self.updated) * self.rate)
        self.updated = now
        if self.tokens < 1:
            return False
        self.tokens -= 1
        return True


def capacity(worker_count, mean_seconds):
    if type(worker_count) is not int or worker_count < 1:
        raise ValueError("worker count must be positive")
    if not math.isfinite(mean_seconds) or mean_seconds <= 0:
        raise ValueError("duration must be finite and positive")
    return worker_count / mean_seconds


def estimate_cost(input_tokens, output_tokens, input_rate, output_rate):
    if input_rate is None or output_rate is None:
        return None
    if any(type(count) is not int or count < 0 for count in (input_tokens, output_tokens)):
        raise ValueError("token counts must be nonnegative integers")
    if any(not math.isfinite(rate) or rate < 0 for rate in (input_rate, output_rate)):
        raise ValueError("rates must be finite and nonnegative")
    return (input_tokens * input_rate + output_tokens * output_rate) / 1_000_000
