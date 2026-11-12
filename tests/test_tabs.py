"""Milestone 5 program tabs: isolation, storage, and execution integration."""
import tempfile
import tkinter as tk
import unittest
from pathlib import Path
from unittest.mock import patch

from controller import SimulatorController
from gui.app import UVSimApp
from program_store import ProgramStore
from word import Word


class TabTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        try:
            self.root = tk.Tk()
        except tk.TclError as error:
            self.skipTest(str(error))
        self.root.withdraw()
        self.app = UVSimApp(self.root, SimulatorController())
        self.addCleanup(self.cleanup_app)

    def cleanup_app(self):
        with patch.object(self.app, "confirm_discard", return_value=True):
            self.app.close()

    def file(self, name, text):
        path = Path(self.folder.name) / name
        path.write_text(text, encoding="utf-8")
        return path

    def run_program(self):
        self.app.start()
        self.app.controller.tick(20)
        self.app.refresh()
        self.assertEqual(self.app.controller.state, "halted")
        return self.app.panel.output.get("1.0", "end-1c").strip()

    def test_switch_edit_run_and_save_documents_independently(self):
        a = self.file("a.txt", "+011002\n+043000\n+000007\n")
        b = self.file("b.txt", "+011002\n+043000\n+000008\n")
        self.assertTrue(self.app.load_file(a))
        first = self.app._active_tab
        self.app.editor.modify_entry(2, "+000009")
        self.assertTrue(self.app.load_file(b))
        second = self.app._active_tab
        self.assertEqual(self.run_program(), "000008")
        self.app._select_document(first)
        self.assertTrue(self.app.editor.is_dirty)
        self.assertEqual(self.run_program(), "000009")
        self.app.save_file()
        self.assertFalse(self.app.editor.is_dirty)
        self.assertIn("+000009", a.read_text())
        self.assertIn("+000008", b.read_text())
        self.app._select_document(second)
        self.assertEqual(self.run_program(), "000008")

    def test_reopen_focuses_unsaved_document_without_reloading(self):
        path = self.file("a.txt", "+043000\n")
        self.app.load_file(path)
        first = self.app._active_tab
        self.app.editor.modify_entry(0, "+000001")
        self.app.new_document()
        count = len(self.app.documents)
        self.app.load_file(path)
        self.assertEqual(self.app._active_tab, first)
        self.assertEqual(len(self.app.documents), count)
        self.assertEqual(self.app.editor.get_words(), [Word(1)])
        self.assertTrue(self.app.editor.is_dirty)

    def test_save_as_cannot_overwrite_another_open_document(self):
        path = self.file("a.txt", "+043000\n")
        self.app.load_file(path)
        self.app.new_document()
        self.app.editor.add_entry()
        with patch("gui.file_actions.filedialog.asksaveasfilename", return_value=str(path)):
            self.app.save_file_as()
        self.assertIsNone(self.app.file_actions.current_path)
        self.assertTrue(self.app.editor.is_dirty)
        self.assertEqual(path.read_text(), "+043000\n")
        self.assertIn("another tab", self.app.status.get())

    def test_notebook_selection_event_activates_document(self):
        first = self.app._active_tab
        self.app.editor.set_words([Word(43000)])
        self.app.new_document()
        self.app.notebook.select(first)
        self.root.update()
        self.assertEqual(self.app._active_tab, first)
        self.assertEqual(self.app.editor.get_words(), [Word(43000)])

    def test_running_and_waiting_lock_tabs_until_stop(self):
        other = self.app._active_tab
        self.app.new_document()
        active = self.app._active_tab
        self.app.editor.set_words([Word(10249), Word(43000)])
        self.app.start()
        self.app._select_document(other)
        self.assertEqual(self.app._active_tab, active)
        self.assertEqual(str(self.app.notebook.tab(other, "state")), "disabled")
        self.app.controller.tick()
        self.app.refresh()
        self.assertEqual(self.app.controller.state, "waiting_input")
        self.assertFalse(self.app.close_document())
        self.app.new_document()
        self.assertEqual(len(self.app.documents), 2)
        self.app.editor.modify_entry(0, "+043000")
        self.assertEqual(self.app.editor.get_words()[0], Word(10249))
        self.app.stop()
        self.app._select_document(other)
        self.assertEqual(self.app._active_tab, other)
        self.assertEqual(self.app.controller.state, "empty")

    def test_input_and_output_use_six_digits_and_last_register(self):
        self.app.editor.set_words([Word(10249), Word(11249), Word(43000)])
        self.app.start()
        self.app.controller.tick()
        self.app.refresh()
        self.assertIn("999999", self.app.status.get())
        self.assertTrue(self.app.submit_input("-999999"))
        self.app.controller.tick()
        self.app.refresh()
        self.assertEqual(self.app.controller.outputs, [-999999])
        self.assertEqual(self.app.panel.output.get("1.0", "end-1c").strip(), "-999999")

    def test_cancel_and_failed_save_keep_dirty_tab(self):
        self.app.editor.add_entry()
        original = self.app._active_tab
        with patch("gui.file_actions.messagebox.askyesnocancel", return_value=None):
            self.assertFalse(self.app.close_document())
        with patch("gui.file_actions.messagebox.askyesnocancel", return_value=True):
            with patch("gui.file_actions.filedialog.asksaveasfilename", return_value=""):
                self.assertFalse(self.app.close_document())
            with patch("gui.file_actions.filedialog.asksaveasfilename", return_value=str(Path(self.folder.name)/"x.txt")):
                with patch.object(self.app.file_actions.store, "save", side_effect=OSError("disk full")):
                    self.assertFalse(self.app.close_document())
        self.assertEqual(self.app._active_tab, original)
        self.assertTrue(self.app.editor.is_dirty)
        with patch("gui.file_actions.messagebox.askyesnocancel", return_value=False):
            self.assertTrue(self.app.close_document())
        self.assertEqual(len(self.app.documents), 1)
        self.assertFalse(self.app.editor.is_dirty)

    def test_close_application_checks_inactive_dirty_tabs(self):
        self.app.editor.add_entry()
        self.app.new_document()
        self.app.editor.add_entry()
        with patch("gui.file_actions.messagebox.askyesnocancel", side_effect=[False, None]) as ask:
            self.app.close()
        self.assertEqual(ask.call_count, 2)
        self.assertFalse(self.app._closed)
        self.assertEqual(len(self.app.documents), 2)
        self.assertTrue(all(editor.is_dirty for _, editor, _, _ in self.app.documents.values()))

    def test_250_word_save_load_and_oversized_open(self):
        words = [Word(43000)] + [Word(999999)] * 249
        path = self.file("full.txt", "")
        store = ProgramStore()
        store.save(path, words)
        self.assertEqual(store.load(path), words)
        self.assertTrue(self.app.load_file(path))
        self.assertEqual(self.app.editor.tree.item("249", "values"), ("249", "+999999"))
        self.app.editor.add_entry()
        self.assertEqual(len(self.app.editor.get_words()), 250)
        before = self.app._active_tab
        oversized = self.file("large.txt", "+000000\n" * 251)
        self.assertFalse(self.app.load_file(oversized))
        self.assertEqual(self.app._active_tab, before)
        with self.assertRaises(ValueError):
            store.save(path, words + [Word(0)])
        self.assertEqual(store.load(path), words)

    def test_pending_cell_edit_survives_switch(self):
        first = self.app._active_tab
        self.app.editor.set_words([Word(43000)])
        self.app.new_document()
        second = self.app._active_tab
        self.app._select_document(first)
        self.root.deiconify()
        self.root.update_idletasks()
        self.app.editor._begin_edit(0)
        self.app.editor._edit_widget.delete(0, "end")
        self.app.editor._edit_widget.insert(0, "+011249")
        self.app._select_document(second)
        self.app._select_document(first)
        self.assertEqual(self.app.editor.get_words(), [Word(11249)])
        self.assertTrue(self.app.editor.is_dirty)


if __name__ == "__main__":
    unittest.main()
