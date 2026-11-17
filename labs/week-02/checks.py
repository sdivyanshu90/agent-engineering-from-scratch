"""Public Week 2 contracts; --module selects an independent learner file."""
import argparse
import asyncio
import importlib.util
import math
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
NAMES = {1: "validation", 2: "storage", 3: "concurrent", 4: "recovery", 5: "vectors", 6: "optimization"}


def load_module(path):
    spec = importlib.util.spec_from_file_location("week02_submission", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def rejects(operation, kinds=(ValueError, UnicodeError)):
    try:
        operation()
    except kinds:
        return
    raise AssertionError("invalid input accepted")


async def async_check(day, module):
    if day == 3:
        started = 0
        both_started = asyncio.Event()

        async def operation(value):
            nonlocal started
            started += 1
            if started == 2:
                both_started.set()
            await both_started.wait()
            return value

        result = await asyncio.wait_for(module.collect([lambda: operation("a"), lambda: operation("b")]), 2)
        assert result == ["a", "b"]
        assert await module.collect([]) == []
    else:
        calls = 0
        delays = []

        async def operation():
            nonlocal calls
            calls += 1
            if calls < 3:
                raise module.TransientError("fixture")
            return "ok"

        async def fake_sleep(delay):
            delays.append(delay)

        assert await module.retry(operation, attempts=3, base_delay=0.1, sleep=fake_sleep) == "ok"
        assert calls == 3 and delays == [0.1, 0.2]
        async def permanent():
            raise ValueError("permanent")
        try:
            await module.retry(permanent, sleep=fake_sleep)
        except ValueError:
            pass
        else:
            raise AssertionError("permanent failure hidden")


def check(day, path=None):
    path = path or ROOT / "solutions/labs/week-02" / (NAMES[day] + ".py")
    module = load_module(path)
    if day == 1:
        assert module.validate_document(b'{"text":"ok"}') == "ok"
        assert module.validate_document(b'{"text":""}') == ""
        for body in [b"", b"[]", b'{"text": 4}', b'{"text":"a","text":"b"}', b'{"text":"a","owner":"x"}', b"\xff", b'{"text":NaN}', b'x' * 4097]:
            rejects(lambda body=body: module.validate_document(body))
    elif day == 2:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.sqlite3"
            store = module.Store(path)
            store.put("a", "id", "hello ' world")
            assert module.Store(path).get("a", "id") == "hello ' world"
            assert store.get("b", "id") is None
            store.put("a", "id", "")
            assert store.get("a", "id") == ""
    elif day in {3, 4}:
        asyncio.run(async_check(day, module))
    elif day == 5:
        assert module.dot([1, 2], [3, 4]) == 11
        assert math.isclose(module.cosine([3, 4], [0, 5]), 0.8)
        assert module.matvec([[1, 2], [3, 4]], [2, 1]) == [4, 10]
        rejects(lambda: module.dot([1, 2], [3]))
        rejects(lambda: module.cosine([0, 0], [1, 0]))
    else:
        assert math.isclose(module.derivative(lambda x: (3*x+1)**2, 2), 42, rel_tol=1e-6)
        result = module.softmax([1000, 1000])
        assert result == [0.5, 0.5]
        assert module.descend_square(2, steps=0) == [2]
        assert math.isclose(module.descend_square(2, steps=1)[1], 1.6)
        rejects(lambda: module.softmax([]))
        rejects(lambda: module.softmax([float("nan")]))
        rejects(lambda: module.derivative(lambda x: x, 0, h=0))
    return True


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    parser = argparse.ArgumentParser()
    parser.add_argument("--day", type=int, choices=NAMES, required=True)
    parser.add_argument("--module", type=Path)
    args = parser.parse_args()
    check(args.day, args.module)
    print(f"Week 2 day {args.day}: public contract passed")
