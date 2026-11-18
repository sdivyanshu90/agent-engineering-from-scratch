"""Verify the optional Bubblewrap backend against a generated, owned fixture."""
import os
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forgeagent.isolation import BubblewrapTests

FIXTURE = """import os
from pathlib import Path
import socket
import unittest

class Boundaries(unittest.TestCase):
    def test_inside_namespace(self):
        self.assertNotIn("FORGE_TEST_SECRET", os.environ)
        self.assertFalse(Path("/etc/passwd").exists())
        self.assertFalse(Path("/home").exists())
        self.assertEqual(socket.if_nameindex(), [(1, "lo")])
        with self.assertRaises(OSError):
            Path("/workspace/out.txt").write_text("blocked")
"""


def main():
    with TemporaryDirectory(prefix="forge-isolation-") as directory:
        root = Path(directory)
        (root / "tests").mkdir()
        (root / "tests/test_boundaries.py").write_text(FIXTURE, encoding="utf-8")
        os.environ["FORGE_TEST_SECRET"] = "disposable-fixture-marker"
        test = BubblewrapTests()
        result = test.run(("python", "-m", "unittest", "discover", "-s", "tests"),
                          cwd=root, timeout=5)
        if result != {"status": "passed", "exit_code": 0}:
            raise SystemExit(f"Isolation smoke failed: {result}")
        print("Isolation smoke passed: environment, mounts, network namespace, read-only workspace.")


if __name__ == "__main__":
    main()
