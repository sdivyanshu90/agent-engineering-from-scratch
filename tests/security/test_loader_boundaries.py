"""Boundary tests for owned workspaces; these do not establish OS isolation."""
from pathlib import Path
import tempfile
import unittest
from forgeagent.documents import load_documents


class LoaderBoundaryTests(unittest.TestCase):
    def test_exact_and_exceeded_byte_bound(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            file = root / "a.txt"
            file.write_bytes(b"abcd")
            self.assertEqual(load_documents(root, max_bytes=4)[0].text, "abcd")
            with self.assertRaises(ValueError):
                load_documents(root, max_bytes=3)
            for invalid in [0, -1, True, 2.5]:
                with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                    load_documents(root, max_bytes=invalid)

    def test_invalid_utf8_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "bad.md").write_bytes(b"\xff")
            with self.assertRaises(UnicodeDecodeError):
                load_documents(root)

    def test_file_and_directory_symlinks_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "workspace"
            root.mkdir()
            outside = base / "outside"
            outside.mkdir()
            (outside / "secret.txt").write_text("secret", encoding="utf-8")
            try:
                (root / "link.txt").symlink_to(outside / "secret.txt")
            except (OSError, NotImplementedError) as error:
                self.skipTest(f"symlinks unavailable: {error}")
            with self.assertRaisesRegex(ValueError, "symbolic links"):
                load_documents(root)
            (root / "link.txt").unlink()
            (root / "linked-directory").symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "symbolic links"):
                load_documents(root)
