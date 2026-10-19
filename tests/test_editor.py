"""Milestone 4 WP-2 unit tests for the BasicML program editor."""
import tkinter as tk
import unittest
from gui.editor_panel import EditorPanel
from word import Word


class EditorPanelTests(unittest.TestCase):
    def setUp(self):
        try:
            self.root = tk.Tk()
        except tk.TclError as error:
            self.skipTest(f"Tk display unavailable: {error}")
        self.changes = []
        self.editor = EditorPanel(self.root, lambda: self.changes.append(True))
        self.root.update()

    def tearDown(self):
        if hasattr(self, "root"):
            self.root.destroy()

    def test_set_get_round_trip_and_addresses(self):
        words = [Word.parse("+1007"), Word.parse("-0005"), Word.parse("+4300")]
        self.editor.set_words(words)
        self.assertEqual(self.editor.get_words(), words)
        self.assertEqual(self.editor.tree.item("2", "values"), ("02", "+4300"))
        self.assertFalse(self.editor.is_dirty)
        self.assertEqual(len(self.changes), 0)

    def test_add_modify_delete_and_renumber(self):
        self.editor.set_words([Word(1007), Word(4300)])
        self.editor.tree.selection_set("1")
        self.editor.add_entry()
        self.assertEqual([w.format() for w in self.editor.get_words()],
                         ["+1007", "+0000", "+4300"])
        self.editor.modify_entry(1, "+2007")
        self.editor.tree.selection_set("0", "1")
        self.editor.delete_selected()
        self.assertEqual([w.format() for w in self.editor.get_words()], ["+4300"])
        self.assertEqual(self.editor.tree.item("0", "values"), ("00", "+4300"))
        self.assertTrue(self.editor.is_dirty)
        self.assertGreaterEqual(len(self.changes), 3)

    def test_cut_copy_paste_multiple_entries(self):
        self.editor.set_words([Word(1007), Word(2007), Word(3008), Word(4300)])
        self.editor.tree.selection_set("1", "2")
        self.editor.copy()
        self.assertEqual(self.root.clipboard_get(), "+2007\n+3008")
        self.editor.cut()
        self.assertEqual([w.format() for w in self.editor.get_words()],
                         ["+1007", "+4300"])
        self.editor.tree.selection_set("1")
        self.editor.paste()
        self.assertEqual([w.format() for w in self.editor.get_words()],
                         ["+1007", "+2007", "+3008", "+4300"])

    def test_paste_at_limit(self):
        self.editor.set_words([Word(0)] * 99)
        self.root.clipboard_clear()
        self.root.clipboard_append("+4300")
        self.editor.paste()
        self.assertEqual(len(self.editor.get_words()), 100)
        self.assertTrue(self.editor.is_dirty)

    def test_reject_paste_over_limit_without_changes(self):
        self.editor.set_words([Word(0)] * 99)
        self.root.clipboard_clear()
        self.root.clipboard_append("+1007\n+4300")
        self.editor.paste()
        self.assertEqual(len(self.editor.get_words()), 99)
        self.assertFalse(self.editor.is_dirty)
        self.assertIn("exceed 100", self.editor.status.get())

    def test_reject_add_at_limit(self):
        self.editor.set_words([Word(0)] * 100)
        self.editor.add_entry()
        self.assertEqual(len(self.editor.get_words()), 100)
        self.assertFalse(self.editor.is_dirty)

    def test_invalid_manual_edit_reports_address_and_line(self):
        self.editor.set_words([Word(1007), Word(4300)])
        self.editor.modify_entry(1, "abc")
        self.assertIn("Address 01", self.editor.status.get())
        self.assertIn("invalid", self.editor.tree.item("1", "tags"))
        with self.assertRaisesRegex(ValueError, r"address 01 \(line 2\)"):
            self.editor.get_words()
        self.editor.modify_entry(1, "+4300")
        self.assertEqual(self.editor.get_words(), [Word(1007), Word(4300)])

    def test_invalid_paste_does_not_modify_program(self):
        self.editor.set_words([Word(4300)])
        self.root.clipboard_clear()
        self.root.clipboard_append("+1007\nnot-a-word")
        self.editor.paste()
        self.assertEqual(self.editor.get_words(), [Word(4300)])
        self.assertFalse(self.editor.is_dirty)
        self.assertIn("clipboard line 2", self.editor.status.get())

    def test_mark_saved_and_reset_on_load(self):
        self.editor.set_words([Word(4300)])
        self.editor.add_entry()
        self.assertTrue(self.editor.is_dirty)
        self.editor.mark_saved()
        self.assertFalse(self.editor.is_dirty)
        self.editor.modify_entry(0, "+1007")
        self.assertTrue(self.editor.is_dirty)
        self.editor.set_words([Word(4300)])
        self.assertFalse(self.editor.is_dirty)

    def test_read_only_blocks_edits_but_allows_copy(self):
        self.editor.set_words([Word(1007), Word(4300)])
        self.editor.tree.selection_set("0")
        self.editor.set_enabled(False)
        self.editor.add_entry()
        self.editor.delete_selected()
        self.editor.cut()
        self.editor.paste()
        self.editor.modify_entry(0, "+9999")
        self.editor.copy()
        self.assertEqual(self.root.clipboard_get(), "+1007")
        self.assertEqual(self.editor.get_words(), [Word(1007), Word(4300)])
        self.assertFalse(self.editor.is_dirty)
        self.assertTrue(self.editor.add_button.instate(["disabled"]))
        self.editor.set_enabled(True)
        self.editor.modify_entry(0, "+2007")
        self.assertEqual(self.editor.get_words()[0], Word(2007))

    def test_set_words_rejects_more_than_100(self):
        with self.assertRaisesRegex(ValueError, "100 entries"):
            self.editor.set_words([Word(0)] * 101)


if __name__ == "__main__":
    unittest.main()
