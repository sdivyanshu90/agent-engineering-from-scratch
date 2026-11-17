"""Validate authored checkpoint separately from the complete 72-day product.

Length is a rejection heuristic, never proof of instructional depth. Human
content review remains required. Planned lessons need no placeholder files.
"""
import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = ["Learning objectives", "Required prerequisites", "Problem motivation",
            "Intuitive explanation", "Deep technical explanation", "Mathematical foundations",
            "Architecture and execution diagrams", "Implementation from first principles",
            "Worked execution walkthrough", "Independent laboratory", "Experiments",
            "Failure analysis", "Engineering tradeoffs", "Real-world connection",
            "Common misconceptions", "Technical examination", "Daily mastery gate",
            "Resources", "Revision and retention", "Next lesson connection"]
AUTHORED = {"authored", "validated"}


def validate(root=ROOT, require_complete=False):
    manifest = json.loads((root / "docs/build-progress.json").read_text())
    failures = []
    lessons = manifest["lessons"]
    if len(lessons) != manifest["planned_instructional_days"] or len(lessons) != 72:
        failures.append("Schedule must contain exactly 72 lessons")
    if len({lesson["id"] for lesson in lessons}) != len(lessons):
        failures.append("Duplicate lesson identifier")
    if len({lesson["path"] for lesson in lessons}) != len(lessons):
        failures.append("Duplicate lesson path")
    known = set()
    authored = 0
    for index, lesson in enumerate(lessons, 1):
        identifier = lesson["id"]
        if identifier != f"D{index:02}":
            failures.append(f"Out-of-order identifier: {identifier}")
        if (lesson["week"], lesson["day"]) != ((index-1)//6+1, (index-1)%6+1):
            failures.append(f"Wrong week/day: {identifier}")
        if not set(lesson["prerequisites"]) <= known:
            failures.append(f"Unknown or future prerequisite: {identifier}")
        known.add(identifier)
        if lesson["status"] not in {"planned", "in_progress", *AUTHORED}:
            failures.append(f"Unknown status: {identifier}")
        if lesson["status"] not in AUTHORED:
            if require_complete:
                failures.append(f"{identifier} is {lesson['status']}")
            continue
        authored += 1
        source = root / lesson["path"]
        if not source.is_file():
            failures.append(f"Missing authored chapter: {identifier}")
            continue
        text = source.read_text(encoding="utf-8")
        headings = re.findall(r"^## (\d+)\. (.+)$", text, re.M)
        if headings != [(str(i), section) for i, section in enumerate(SECTIONS, 1)]:
            failures.append(f"{identifier} must have all 20 exact sections in order")
        if len(text.split()) < 1200:
            failures.append(f"{identifier} too short for chapter review")
        if "```mermaid" not in text or "```python" not in text:
            failures.append(f"{identifier} missing diagram or implementation")
        for ref in [lesson.get("assessment"), lesson.get("lab"), lesson.get("solution")]:
            if not ref or not (root / ref).is_file():
                failures.append(f"{identifier} missing lab, solution, or assessment mapping")
        if not lesson.get("concepts"):
            failures.append(f"{identifier} missing concept coverage")
    actual = {p.relative_to(root).as_posix() for p in (root / "curriculum").glob("week-*/day-*/README.md")}
    scheduled = {lesson["path"] for lesson in lessons}
    if actual - scheduled:
        failures.append(f"Orphaned chapters: {sorted(actual-scheduled)}")
    if manifest["authored_days"] != authored:
        failures.append("Authored count does not match lesson states")
    validated = sum(lesson["status"] == "validated" for lesson in lessons)
    if manifest["validated_days"] != validated:
        failures.append("Validated count does not match lesson states")
    for week in range(1, 13):
        if any(lesson["week"] == week and lesson["status"] in AUTHORED for lesson in lessons):
            for path in [f"curriculum/week-{week:02}/README.md", f"curriculum/week-{week:02}/weekly-review.md", f"assessments/weekly/week-{week:02}.md"]:
                if not (root / path).is_file():
                    failures.append(f"Missing week resource: {path}")
    if require_complete:
        for item in manifest["deliverables"].values():
            if "planned" in item and item["planned"] != item["complete"]:
                failures.append("Incomplete assessment deliverable")
        if manifest["deliverables"]["capstone"]["status"] != "validated":
            failures.append("ForgeAgent capstone is not validated")
        if manifest["outstanding_work"]:
            failures.append("Outstanding work remains")
    return failures, authored


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    failures, authored = validate(require_complete=args.require_complete)
    for failure in failures:
        print(failure)
    print(f"{authored}/72 chapters authored; {len(failures)} integrity failures; mode="
          + ("full completion" if args.require_complete else "checkpoint"))
    raise SystemExit(bool(failures))
