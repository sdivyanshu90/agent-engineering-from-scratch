"""No installation or network access is needed for the foundation checkpoint."""
import sqlite3
import sys
from pathlib import Path


def main():
    if not (3, 12) <= sys.version_info[:2] < (3, 15):
        raise SystemExit("Use Python 3.12, 3.13, or 3.14; 3.12 is the teaching default.")
    assert Path("pyproject.toml").is_file(), "Run from the repository root."
    assert sqlite3.connect(":memory:").execute("SELECT 1").fetchone() == (1,)
    print(f"Python {sys.version_info.major}.{sys.version_info.minor}: ready; no API key required")


if __name__ == "__main__":
    main()
