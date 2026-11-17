"""Execute every authored lesson's Python block in isolation from repo root."""
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]


class LessonExamples(unittest.TestCase):
    def test_all_authored_python_blocks(self):
        manifest = json.loads((ROOT / "docs/build-progress.json").read_text())
        count = 0
        for lesson in manifest["lessons"]:
            if lesson["status"] not in {"authored", "validated"}:
                continue
            text = (ROOT / lesson["path"]).read_text(encoding="utf-8")
            for index, code in enumerate(re.findall(r"```python\n(.*?)```", text, re.S), 1):
                count += 1
                with self.subTest(lesson=lesson["id"], block=index):
                    process = subprocess.run([sys.executable, "-c", code], cwd=ROOT,
                                             text=True, capture_output=True, timeout=20)
                    self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
        self.assertGreater(count, 0, "No authored examples were exercised")
