"""Public lab contracts; reference is default, --module selects learner file."""
import argparse
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
NAMES = {1: "summary", 2: "normalize", 3: "counts", 4: "loader", 5: "rank", 6: "cli"}


def load_module(path):
    spec = importlib.util.spec_from_file_location("learner_submission", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def check(day, path=None):
    path = path or ROOT / "solutions/labs/week-01" / (NAMES[day] + ".py")
    module = load_module(path)
    if day == 1:
        assert module.summarize("") == {"characters": 0, "words": 0}
        assert module.summarize("A  b\n") == {"characters": 5, "words": 2}
    elif day == 2:
        assert module.normalize(" AGENT,  tool! ... a-b ") == ["agent", "tool", "a-b"]
        assert module.normalize("") == []
    elif day == 3:
        tokens = ["a", "b", "a"]
        assert module.count_tokens(tokens) == {"a": 2, "b": 1}
        assert tokens == ["a", "b", "a"]
        first = module.count_tokens([])
        first["bad"] = 1
        assert module.count_tokens([]) == {}
    elif day == 4:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "b.txt").write_text("é", encoding="utf-8")
            (root / "a.txt").write_text("", encoding="utf-8")
            (root / "ignored.md").write_text("hidden", encoding="utf-8")
            assert module.load_texts(root) == [("a.txt", ""), ("b.txt", "é")]
            (root / "bad.txt").write_bytes(b"\xff")
            try:
                module.load_texts(root)
            except UnicodeDecodeError:
                pass
            else:
                raise AssertionError("invalid UTF-8 must fail visibly")
        try:
            module.load_texts(root)
        except OSError:
            pass
        else:
            raise AssertionError("missing directory must fail visibly")
    elif day == 5:
        hits = [module.Hit("b", 2), module.Hit("z", 0), module.Hit("a", 2)]
        assert [hit.path for hit in module.rank(hits, 1)] == ["a"]
        assert module.rank(hits, 0) == []
        for bad in [-1, True, 1.2]:
            try:
                module.rank(hits, bad)
            except ValueError:
                pass
            else:
                raise AssertionError("invalid limit accepted")
    else:
        import contextlib
        import io
        import json
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = module.main([str(ROOT / "datasets/sample-data"), "agents"])
        assert code == 0
        assert json.loads(stdout.getvalue()) == [{"path": "agents.txt", "count": 2}]
    return True


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    parser = argparse.ArgumentParser()
    parser.add_argument("--day", type=int, choices=NAMES, required=True)
    parser.add_argument("--module", type=Path)
    args = parser.parse_args()
    check(args.day, args.module)
    print(f"Day {args.day}: public contract passed")
