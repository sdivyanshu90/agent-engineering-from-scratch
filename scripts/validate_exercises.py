"""Run public contracts against references for authored weeks."""
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main():
    manifest=json.loads((ROOT / "docs/build-progress.json").read_text())
    weeks=sorted({lesson["week"] for lesson in manifest["lessons"] if lesson["status"] in {"authored","validated"}})
    for week in weeks:
        path = ROOT / f"labs/week-{week:02}/checks.py"
        spec = importlib.util.spec_from_file_location(f"week{week}_checks", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for day in range(1, 7):
            module.check(day)
            print(f"Week {week} day {day}: reference contract passed")


if __name__ == "__main__":
    main()
