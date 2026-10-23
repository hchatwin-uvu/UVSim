"""Tests for the GUI file-command boundary."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from gui.file_actions import FileActions
from program_store import ProgramStore
from word import Word


class FakeEditor:
    def __init__(self):
        self.words = []
        self.is_dirty = False

    def set_words(self, words):
        self.words = list(words)
        self.is_dirty = False

    def set_entries(self, entries):
        self.set_words([Word.parse(entry) for entry in entries])

    def get_words(self):
        return list(self.words)

    def mark_saved(self):
        self.is_dirty = False


class FileActionsTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.editor = FakeEditor()
        self.status = Mock()
        self.actions = FileActions(None, ProgramStore(), self.editor, self.status)

    def test_open_path_loads_and_tracks_file_from_another_directory(self):
        path = Path(self.temp_dir.name) / "program.txt"
        path.write_text("+1007\n+4300\n", encoding="utf-8")
        self.assertTrue(self.actions.open_path(str(path)))
        self.assertEqual(self.editor.words, [Word(1007), Word(4300)])
        self.assertEqual(self.actions.current_path, str(path))

    def test_open_dialog_cancel_does_not_change_state(self):
        self.editor.words = [Word(4300)]
        with patch("gui.file_actions.filedialog.askopenfilename", return_value=""):
            self.assertFalse(self.actions.open())
        self.assertEqual(self.editor.words, [Word(4300)])
        self.assertIsNone(self.actions.current_path)

    def test_failed_open_preserves_editor_and_path(self):
        previous = Path(self.temp_dir.name) / "previous.txt"
        previous.write_text("+4300\n", encoding="utf-8")
        self.assertTrue(self.actions.open_path(str(previous)))
        self.editor.words = [Word(1007)]
        self.editor.is_dirty = True
        with patch("gui.file_actions.messagebox.askyesnocancel", return_value=False):
            self.assertFalse(self.actions.open_path(str(Path(self.temp_dir.name) / "missing.txt")))
        self.assertEqual(self.editor.words, [Word(1007)])
        self.assertEqual(self.actions.current_path, str(previous))

    def test_open_dirty_editor_requires_confirmation(self):
        path = Path(self.temp_dir.name) / "program.txt"
        path.write_text("+4300\n", encoding="utf-8")
        self.editor.words = [Word(1007)]
        self.editor.is_dirty = True
        with patch("gui.file_actions.messagebox.askyesnocancel", return_value=None):
            self.assertFalse(self.actions.open_path(str(path)))
        self.assertEqual(self.editor.words, [Word(1007)])
        self.assertIsNone(self.actions.current_path)

    def test_save_without_path_uses_save_as_and_marks_saved(self):
        path = Path(self.temp_dir.name) / "saved.txt"
        self.editor.words = [Word(1007), Word(-5)]
        self.editor.is_dirty = True
        with patch("gui.file_actions.filedialog.asksaveasfilename",
                   return_value=str(path)):
            self.assertTrue(self.actions.save())
        self.assertEqual(self.actions.current_path, str(path))
        self.assertEqual(ProgramStore().load(str(path)), self.editor.words)
        self.assertFalse(self.editor.is_dirty)

    def test_save_existing_path_writes_edits(self):
        path = Path(self.temp_dir.name) / "program.txt"
        path.write_text("+0000\n", encoding="utf-8")
        self.assertTrue(self.actions.open_path(str(path)))
        self.editor.words = [Word(4300)]
        self.editor.is_dirty = True
        self.assertTrue(self.actions.save())
        self.assertEqual(ProgramStore().load(str(path)), [Word(4300)])
        self.assertFalse(self.editor.is_dirty)

    def test_save_as_cancel_is_noop(self):
        self.editor.words = [Word(4300)]
        self.editor.is_dirty = True
        with patch("gui.file_actions.filedialog.asksaveasfilename", return_value=""):
            self.assertFalse(self.actions.save_as())
        self.assertIsNone(self.actions.current_path)
        self.assertTrue(self.editor.is_dirty)

    def test_failed_save_preserves_editor_and_current_path(self):
        path = Path(self.temp_dir.name) / "program.txt"
        self.actions._current_path = str(path)
        self.editor.words = [Word(4300)]
        self.editor.is_dirty = True
        with patch.object(self.actions.store, "save", side_effect=OSError("disk full")):
            self.assertFalse(self.actions.save())
        self.assertEqual(self.editor.words, [Word(4300)])
        self.assertTrue(self.editor.is_dirty)
        self.assertEqual(self.actions.current_path, str(path))
        self.status.assert_called_with("Unable to save program: disk full")


if __name__ == "__main__":
    unittest.main()
