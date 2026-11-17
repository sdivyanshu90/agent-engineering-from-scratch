"""Run with python -m forgeagent.cli DIRECTORY QUERY [--limit N]."""
import argparse
import json
import logging
from pathlib import Path
from .documents import load_documents, search


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Search local UTF-8 documents by one token")
    parser.add_argument("root", type=Path)
    parser.add_argument("query")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--max-bytes", type=int, default=1_000_000)
    args = parser.parse_args(argv)
    try:
        hits = search(load_documents(args.root, max_bytes=args.max_bytes), args.query, limit=args.limit)
    except (OSError, UnicodeError, ValueError) as error:
        logging.getLogger(__name__).error("document search failed: %s", error)
        return 2
    print(json.dumps([{"path": hit.path, "count": hit.count} for hit in hits], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
