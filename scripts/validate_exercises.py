"""Run public contracts against references for both authored weeks."""
import importlib.util
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main():
    for week in (1, 2):
        path = ROOT / f"labs/week-{week:02}/checks.py"
        spec = importlib.util.spec_from_file_location(f"week{week}_checks", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for day in range(1, 7):
            module.check(day)
            print(f"Week {week} day {day}: reference contract passed")


if __name__ == "__main__":
    main()
