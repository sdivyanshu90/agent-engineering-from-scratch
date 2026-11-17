import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class IntegrityTests(unittest.TestCase):
    def test_checkpoint_passes_and_completion_fails(self):
        validator = load("validate_curriculum")
        failures, authored = validator.validate()
        self.assertEqual(failures, [])
        self.assertGreater(authored, 0)
        failures, _ = validator.validate(require_complete=True)
        self.assertTrue(any("planned" in failure for failure in failures))
        self.assertIn("ForgeAgent capstone is not validated", failures)

    def test_local_links(self):
        validator = load("validate_links")
        self.assertEqual(validator.validate(), [])
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a.md").write_text("[broken](missing.md)", encoding="utf-8")
            self.assertEqual(validator.validate(root), ["a.md -> missing.md"])

    def test_reference_labs(self):
        import sys
        sys.path.insert(0, str(ROOT / "labs/week-01"))
        from checks import check
        for day in range(1, 7):
            with self.subTest(day=day):
                self.assertTrue(check(day))
