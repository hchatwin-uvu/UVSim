"""Tests for validated BasicML program-file storage."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from program_store import ProgramStore
from word import Word


class ProgramStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.store = ProgramStore()

    def make_file(self, content):
        path = Path(self.temp_dir.name) / "program.txt"
        path.write_text(content, encoding="utf-8")
        return path

    def test_load_skips_blank_lines_and_returns_words(self):
        path = self.make_file("\n+1007\n  \n-0005\n+4300\n")
        self.assertEqual(
            self.store.load(str(path)),
            [Word(1007), Word(-5), Word(4300)],
        )

    def test_load_preserves_line_numbered_validation_errors(self):
        path = self.make_file("\n1007\n")
        with self.assertRaisesRegex(ValueError, "line 2: 1007"):
            self.store.load(str(path))

    def test_load_rejects_more_than_100_nonblank_words(self):
        path = self.make_file("+0000\n" * 101)
        with self.assertRaisesRegex(ValueError, "more than 100"):
            self.store.load(str(path))

    def test_load_missing_file_raises_os_error(self):
        with self.assertRaises(OSError):
            self.store.load(str(Path(self.temp_dir.name) / "missing.txt"))

    def test_save_and_load_round_trip(self):
        path = Path(self.temp_dir.name) / "nested" / "program.txt"
        path.parent.mkdir()
        words = [Word(1007), Word(-5), Word(4300)]
        self.store.save(str(path), words)
        self.assertEqual(path.read_text(encoding="utf-8"), "+1007\n-0005\n+4300\n")
        self.assertEqual(self.store.load(str(path)), words)

    def test_save_rejects_too_many_words_and_invalid_entries(self):
        path = Path(self.temp_dir.name) / "program.txt"
        with self.assertRaisesRegex(ValueError, "more than 100"):
            self.store.save(str(path), [Word(0)] * 101)
        with self.assertRaisesRegex(ValueError, "Word objects"):
            self.store.save(str(path), [1007])
        self.assertFalse(path.exists())

    def test_failed_replace_preserves_original_and_cleans_temporary_file(self):
        path = self.make_file("original contents\n")
        with patch("program_store.os.replace", side_effect=OSError("replace failed")):
            with self.assertRaisesRegex(OSError, "replace failed"):
                self.store.save(str(path), [Word(4300)])
        self.assertEqual(path.read_text(encoding="utf-8"), "original contents\n")
        self.assertEqual(list(Path(self.temp_dir.name).glob(".uvsim-*.tmp")), [])

    def test_unwritable_destination_raises_os_error(self):
        path = Path(self.temp_dir.name) / "missing" / "program.txt"
        with self.assertRaises(OSError):
            self.store.save(str(path), [Word(4300)])


if __name__ == "__main__":
    unittest.main()
