"""Check local Markdown file links/images; no network or anchor validation.

Conventions: inline Markdown links, no spaces in paths, external HTTPS links.
External URLs and #fragment targets require a separate resource/content audit.
"""
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"!?\[[^\]\n]*\]\(([^)]+)\)")


def validate(root=ROOT):
    failures = []
    for source in root.rglob("*.md"):
        if any(part in {".git", ".venv", "learner-work"} for part in source.relative_to(root).parts):
            continue
        # Code examples may contain literal Markdown; don't treat it as navigation.
        text = re.sub(r"```.*?```", "", source.read_text(encoding="utf-8"), flags=re.S)
        for match in LINK.finditer(text):
            target = match.group(1).strip().strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith("#"):
                continue
            path = source.parent / unquote(parsed.path)
            if not path.exists():
                failures.append(f"{source.relative_to(root)} -> {target}")
    return failures


if __name__ == "__main__":
    failures = validate()
    for failure in failures:
        print(failure)
    print(f"Local Markdown path check: {len(failures)} broken links (anchors and external URLs not checked)")
    raise SystemExit(bool(failures))
