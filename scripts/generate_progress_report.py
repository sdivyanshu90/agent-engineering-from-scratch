"""Print build status. Learner mastery is deliberately a separate human record."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
m = json.loads((root / "docs/build-progress.json").read_text())
print(f"Build: {m['status']}; {m['authored_days']}/72 authored; {m['validated_days']}/72 validated")
print(f"Capstone: {m['deliverables']['capstone']['status']}")
print(f"Next: {m['next_pending_step']}")
for pending in m["outstanding_work"]:
    print(f"- {pending}")
