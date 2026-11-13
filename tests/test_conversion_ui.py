"""Legacy conversion dialogs, document preservation, and execution."""
import tempfile
import tkinter as tk
import unittest
from pathlib import Path
from unittest.mock import patch

from controller import SimulatorController
from gui.app import UVSimApp
from program_store import ProgramStore
from word import Word

ROOT = Path(__file__).resolve().parents[1]


class ConversionUITests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.directory = Path(self.folder.name)
        try:
            self.root = tk.Tk()
        except tk.TclError as error:
            self.skipTest(str(error))
        self.root.withdraw()
        self.app = UVSimApp(self.root, SimulatorController())
        self.addCleanup(self.close_app)

    def close_app(self):
        with patch.object(self.app, "confirm_discard", return_value=True):
            self.app.close()

    def convert(self, source, destination):
        with patch("gui.file_actions.filedialog.askopenfilename", return_value=str(source)):
            with patch("gui.file_actions.filedialog.asksaveasfilename", return_value=str(destination)):
                return self.app.convert_legacy_file()

    def run_program(self, inputs=()):
        values = iter(inputs)
        self.app.start()
        for _ in range(1000):
            if self.app.controller.state == "waiting_input":
                self.assertTrue(self.app.submit_input(str(next(values))))
            elif self.app.controller.state == "running":
                self.app.controller.tick()
            else:
                break
        self.app.refresh()
        self.assertEqual(self.app.controller.state, "halted")
        return self.app.controller.outputs

    def test_instructor_files_convert_save_reload_and_run(self):
        # Old data beginning with an opcode is converted as an instruction,
        # per the milestone's explicit ambiguity rule (e.g. 1111 -> 011011).
        cases = [
            ("Test1", [7, 5], [12]),
            ("Test2", [5, 7], [7]),
            ("Test3", [], [13233, 1, 4444, 2222, -7778, -17778]),
            ("Test3b", [], [13233, 1, 444, 222, -9778, -19778]),
            ("Test4", [], [11011, 2222, 33033, 4444, 5555]),
        ]
        for name, inputs, expected in cases:
            with self.subTest(name=name):
                source = ROOT / "programs" / f"{name}.txt"
                original = source.read_bytes()
                destination = self.directory / f"{name}-converted.txt"
                self.assertTrue(self.convert(source, destination))
                self.assertEqual(source.read_bytes(), original)
                self.assertFalse(self.app.editor.is_dirty)
                self.assertEqual(ProgramStore().load(destination), self.app.editor.get_words())
                self.assertTrue(self.app.close_document())
                self.assertTrue(self.app.load_file(destination))
                self.assertEqual(self.run_program(inputs), expected)

    def test_conversion_preserves_other_tabs_and_unsaved_edits(self):
        source = self.directory / "legacy.txt"
        source.write_text("+4300\n-5555\n")
        self.app.load_file(source)
        original_tab = self.app._active_tab
        self.app.editor.modify_entry(1, "unfinished edit")
        self.assertTrue(self.convert(source, self.directory / "converted.txt"))
        self.assertEqual(self.app.editor.get_words(), [Word(43000), Word(-5555)])
        self.app._select_document(original_tab)
        self.assertTrue(self.app.editor.is_dirty)
        self.assertEqual(self.app.editor.tree.item("1", "values")[1], "unfinished edit")
        self.assertEqual(source.read_text(), "+4300\n-5555\n")

    def test_cancel_at_either_dialog_preserves_session(self):
        self.app.editor.add_entry()
        active = self.app._active_tab
        with patch("gui.file_actions.filedialog.askopenfilename", return_value=""):
            with patch("gui.file_actions.filedialog.asksaveasfilename") as save:
                self.assertFalse(self.app.convert_legacy_file())
                save.assert_not_called()
        self.assertFalse(self.convert(ROOT / "programs/Test1.txt", ""))
        self.assertEqual(self.app._active_tab, active)
        self.assertEqual(len(self.app.documents), 1)
        self.assertTrue(self.app.editor.is_dirty)

    def test_invalid_sources_fail_before_destination_dialog(self):
        for text in ("+4300\n+043000\n", "+10AB\n", "", "+0000\n" * 251, "+043000\n"):
            with self.subTest(text=text[:20]):
                source = self.directory / "bad.txt"
                source.write_text(text)
                with patch("gui.file_actions.filedialog.askopenfilename", return_value=str(source)):
                    with patch("gui.file_actions.filedialog.asksaveasfilename") as save:
                        self.assertFalse(self.app.convert_legacy_file())
                        save.assert_not_called()
                self.assertIn("Unable to convert", self.app.status.get())
                self.assertEqual(len(self.app.documents), 1)
        self.assertFalse(self.convert(ROOT / "programs/Test5.txt", self.directory / "unused.txt"))
        self.assertFalse((self.directory / "unused.txt").exists())

    def test_source_and_all_open_destinations_are_protected(self):
        source = self.directory / "legacy.txt"
        source.write_text("+4300\n")
        self.assertFalse(self.convert(source, source))
        self.assertEqual(source.read_text(), "+4300\n")
        destination = self.directory / "open.txt"
        destination.write_text("+043000\n")
        self.app.load_file(destination)
        self.app.editor.add_entry()
        self.assertFalse(self.convert(source, destination))
        self.assertTrue(self.app.editor.is_dirty)
        self.app.new_document()
        self.assertFalse(self.convert(source, destination))
        self.assertEqual(destination.read_text(), "+043000\n")
        self.assertIn("another tab", self.app.status.get())

    def test_write_failure_preserves_destination_source_and_tabs(self):
        source = self.directory / "legacy.txt"
        source.write_text("+4300\n")
        destination = self.directory / "existing.txt"
        destination.write_text("original destination")
        with patch("program_store.os.replace", side_effect=OSError("disk full")):
            self.assertFalse(self.convert(source, destination))
        self.assertEqual(source.read_text(), "+4300\n")
        self.assertEqual(destination.read_text(), "original destination")
        self.assertEqual(len(self.app.documents), 1)
        self.assertIn("disk full", self.app.status.get())
        self.assertEqual(list(self.directory.glob(".uvsim-*")), [])

    def test_file_and_dialog_errors_are_reported(self):
        self.assertFalse(self.convert(self.directory / "missing.txt", self.directory / "out.txt"))
        with patch("gui.file_actions.filedialog.askopenfilename", side_effect=tk.TclError("dialog unavailable")):
            self.assertFalse(self.app.convert_legacy_file())
        self.assertIn("dialog unavailable", self.app.status.get())
        self.assertEqual(len(self.app.documents), 1)

    def test_conversion_disabled_running_and_waiting_for_input(self):
        self.app.editor.set_words([Word(10249), Word(43000)])
        self.app.start()
        for expected in ("running", "waiting_input"):
            self.app.refresh()
            self.assertEqual(self.app.controller.state, expected)
            self.assertTrue(self.app.convert_button.instate(["disabled"]))
            with patch("gui.file_actions.filedialog.askopenfilename") as dialog:
                self.assertFalse(self.app.convert_legacy_file())
                dialog.assert_not_called()
            self.app.controller.tick()
        self.app.stop()
        self.assertFalse(self.app.convert_button.instate(["disabled"]))

    def test_converts_250_entries_and_toolbar_fits_minimum_window(self):
        source = self.directory / "full.txt"
        source.write_text("+4300\n" + "+5555\n" * 249)
        self.assertTrue(self.convert(source, self.directory / "full-six.txt"))
        self.assertEqual(len(self.app.editor.get_words()), 250)
        self.root.deiconify()
        self.root.geometry("1000x720")
        self.root.update()
        self.root.update_idletasks()
        for button in (self.app.new_button, self.app.close_tab_button,
                       self.app.open_button, self.app.convert_button,
                       self.app.save_button, self.app.save_as_button,
                       self.app.run_button, self.app.stop_button):
            self.assertTrue(button.winfo_ismapped(), button.cget("text"))
            self.assertLessEqual(button.winfo_rootx() + button.winfo_width(),
                                 self.root.winfo_rootx() + self.root.winfo_width())


if __name__ == "__main__":
    unittest.main()
