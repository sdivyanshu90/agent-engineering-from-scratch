"""Public contract checks. These are useful minimums, not quality certification."""
import argparse
import asyncio
import importlib.util
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
REFERENCE = ROOT / "solutions/labs/week-11"
NAMES = {1: "ownership", 2: "worker", 3: "leases", 4: "telemetry",
         5: "limits", 6: "deployment"}


def load(day, path=None):
    source = Path(path) if path else REFERENCE / f"{NAMES[day]}.py"
    spec = importlib.util.spec_from_file_location(f"week11_day{day}", source)
    if spec is None or spec.loader is None:
        raise ValueError(f"cannot load module: {source}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check(day, path=None):
    module = load(day, path)
    if day == 1:
        assert module.authenticate("Bearer token-a", {"token-a": "alice"}) == "alice"
        assert module.authenticate("Bearer alice", {"token-a": "alice"}) is None
        rows = {"j1": {"owner": "alice", "status": "queued"}}
        assert module.lookup("alice", "j1", rows)["status"] == "queued"
        assert module.lookup("bob", "j1", rows) is None
        assert module.validate_submission("s", "x") == ("s", "x")
        for session, text in [("", "x"), ("s", ""), ("s", "x" * 4001)]:
            try:
                module.validate_submission(session, text)
            except ValueError:
                pass
            else:
                raise AssertionError("invalid submission accepted")
    elif day == 2:
        async def scenario():
            active = peak = 0
            lock = asyncio.Lock()
            async def handler(value):
                nonlocal active, peak
                async with lock:
                    active += 1
                    peak = max(peak, active)
                await asyncio.sleep(0.002)
                async with lock:
                    active -= 1
                return value * 2
            result = await module.run_many([1, 2, 3, 4], handler, 2)
            assert result == [2, 4, 6, 8]
            assert peak <= 2 and peak > 1
        asyncio.run(scenario())
    elif day == 3:
        rows = {"a": {"job_id": "a", "state": "queued", "created_at": 1,
                      "attempts": 0, "lease_until": None, "lease_token": None}}
        claimed = module.claim(rows, 10, 5, "token-1")
        assert claimed["state"] == "running" and claimed["attempts"] == 1
        assert module.finish(rows, "a", "stale", {"x": 1}) is False
        assert module.finish(rows, "a", "token-1", {"x": 1}) is True
        assert rows["a"]["result"] == {"x": 1}
    elif day == 4:
        event = module.safe_event({"event": "job_finished", "state": "succeeded",
                                   "prompt": "secret", "job_id": "secret-id"})
        assert event == {"event": "job_finished", "state": "succeeded"}
        assert module.durations(2, 5, 9) == {"queue": 3, "execution": 4,
                                             "end_to_end": 7}
        assert module.histogram_bucket(5, [1, 5, 10]) == 5
        assert module.histogram_bucket(11, [1, 5, 10]) == "+Inf"
    elif day == 5:
        bucket = module.Bucket(1 / 30, 2)
        assert bucket.take(0) and bucket.take(0) and not bucket.take(0)
        assert bucket.take(30)
        assert module.capacity(4, 10) == 0.4
        estimate = module.estimate_cost(2000, 500, 0.5, 2.0)
        assert abs(estimate - 0.002) < 1e-12
        assert module.estimate_cost(10, 2, None, 1.0) is None
    elif day == 6:
        result = module.deployment_contract({"FORGEAGENT_TOKEN": "disposable",
                                             "FORGEAGENT_DATABASE": "/data/jobs.sqlite3"})
        assert result["token_configured"] is True
        assert result["database"] == "/data/jobs.sqlite3"
        assert result["topology"] == "single_host_sqlite"
        assert "disposable" not in repr(result)
        for env in ({}, {"FORGEAGENT_TOKEN": "x", "FORGEAGENT_DATABASE": "jobs.sqlite3"}):
            try:
                module.deployment_contract(env)
            except ValueError:
                pass
            else:
                raise AssertionError("unsafe config accepted")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--day", type=int, required=True, choices=range(1, 7))
    parser.add_argument("--module", help="path to learner implementation")
    args = parser.parse_args()
    try:
        check(args.day, args.module)
    except Exception as error:
        print(f"D{60 + args.day}: FAIL: {type(error).__name__}: {error}")
        raise SystemExit(1)
    print(f"D{60 + args.day}: public contract checks passed")
