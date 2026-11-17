import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from forgeagent.documents import Document, frequencies, load_documents, search, tokenize

ROOT = Path(__file__).resolve().parents[2]


class DocumentTests(unittest.TestCase):
    def test_unicode_policy_and_empty(self):
        self.assertEqual(tokenize("Straße STRASSE a_b café!"), ["strasse", "strasse", "a", "b", "café"])
        self.assertEqual(frequencies(""), {})
        self.assertEqual(frequencies("A a B"), {"a": 2, "b": 1})
        with self.assertRaises(TypeError):
            tokenize(None)

    def test_sort_ties_zero_missing_and_nonmutation(self):
        docs = [Document("b", "a a"), Document("a", "a a"), Document("c", "b")]
        self.assertEqual([hit.path for hit in search(docs, "A")], ["a", "b"])
        self.assertEqual(search(docs, "missing"), [])
        self.assertEqual(search(docs, "a", limit=0), [])
        self.assertEqual([doc.path for doc in docs], ["b", "a", "c"])
        self.assertEqual(search([], "a"), [])

    def test_invalid_query_and_limit(self):
        for query in ["", "!", "two words"]:
            with self.subTest(query=query), self.assertRaises(ValueError):
                search([], query)
        for limit in [-1, True, 1.5]:
            with self.subTest(limit=limit), self.assertRaises(ValueError):
                search([], "a", limit=limit)

    def test_loading_nested_sorted_empty_and_extensions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "nested").mkdir()
            (root / "nested/z.md").write_text("café", encoding="utf-8")
            (root / "a.txt").write_text("", encoding="utf-8")
            (root / "ignore.bin").write_bytes(b"\xff")
            docs = load_documents(root)
            self.assertEqual(docs, [Document("a.txt", ""), Document("nested/z.md", "café")])
            with self.assertRaises(NotADirectoryError):
                load_documents(root / "a.txt")
        with self.assertRaises(FileNotFoundError):
            load_documents(root)

    def test_cli_process_contracts(self):
        def run(*args):
            return subprocess.run([sys.executable, "-m", "forgeagent.cli", *args], cwd=ROOT,
                                  text=True, capture_output=True, timeout=10)
        ok = run("datasets/sample-data", "agents")
        self.assertEqual(ok.returncode, 0, ok.stderr)
        self.assertEqual(json.loads(ok.stdout), [{"path": "agents.txt", "count": 2}])
        self.assertEqual(ok.stderr, "")
        absent = run("datasets/sample-data", "nonexistent")
        self.assertEqual(absent.returncode, 0)
        self.assertEqual(json.loads(absent.stdout), [])
        invalid = run("datasets/sample-data", "two words")
        self.assertEqual(invalid.returncode, 2)
        self.assertEqual(invalid.stdout, "")
        self.assertIn("exactly one token", invalid.stderr)
        missing = run("datasets/definitely-missing", "agents")
        self.assertEqual(missing.returncode, 2)
        self.assertEqual(missing.stdout, "")
        malformed = run("datasets/sample-data", "agents", "--limit", "abc")
        self.assertEqual(malformed.returncode, 2)
        self.assertEqual(malformed.stdout, "")
