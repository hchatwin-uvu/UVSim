import tkinter as tk
import unittest
from pathlib import Path
from unittest.mock import patch

from gui.app import UVSimApp
from word import Word

ROOT = Path(__file__).resolve().parents[1]


def close_test_app(app):
    with patch.object(app, "confirm_discard", return_value=True):
        app.close()



class FakePanel:
    """Minimal panel used to assert refresh calls without building a real Tk widget tree."""

    def __init__(self, parent, on_submit, output_parent=None):
        self.parent = parent
        self.on_submit = on_submit
        self.last_state = None
        self.last_outputs = []

    def refresh(self, state, outputs):
        self.last_state = state
        self.last_outputs = list(outputs)


class FakeController:
    """Fake controller used to assert calls from the GUI"""

    def __init__(self, state="empty", message="Open a BasicML file to begin", outputs=None):
        self.state = state
        self.message = message
        self._outputs = list(outputs or [])
        self.loaded_programs = []
        self.last_input = None

    @property
    def outputs(self):
        return list(self._outputs)

    def load_program(self, words):
        self.loaded_programs.append(list(words))
        self.state = "ready"
        self.message = "Program loaded successfully."
        self._outputs = []
        return True

    def start(self):
        if self.state == "ready":
            self.state = "running"
            self.message = "Program running."

    def stop(self):
        if self.state in ("running", "waiting_input"):
            self.state = "stopped"
            self.message = "Program stopped."

    def tick(self):
        if self.state == "running":
            self._outputs.append(42)

    def submit_input(self, text):
        if self.state != "waiting_input":
            return False
        self.last_input = text
        self.state = "running"
        self.message = "Input accepted."
        return True


class TestGUIIntegration(unittest.TestCase):
    def make_app(self, controller=None):
        try:
            root = tk.Tk()
        except tk.TclError as error:
            self.skipTest(f"Tk display unavailable: {error}")
        root.withdraw()
        app = UVSimApp(root, controller or FakeController(), panel_factory=FakePanel)
        self.addCleanup(close_test_app, app)
        return app

    def test_valid_file_load_updates_filename_and_button_state(self):
        app = self.make_app()

        app.load_file(str(ROOT / "programs" / "Test1.txt"))

        self.assertEqual(app._filename, str(ROOT / "programs" / "Test1.txt"))
        self.assertEqual(app.filename.get(), str(ROOT / "programs" / "Test1.txt"))
        self.assertEqual(app.status.get(), "Program loaded successfully.")
        self.assertEqual(str(app.run_button.cget("state")), "normal")
        self.assertEqual(app.panel.last_state, "ready")

    def test_open_file_cancellation_is_a_noop(self):
        controller = FakeController()
        app = self.make_app(controller)

        with patch("gui.app.filedialog.askopenfilename", return_value=""):
            app.open_file()

        self.assertEqual(controller.loaded_programs, [])
        self.assertEqual(app.filename.get(), "No program selected")

    def test_start_and_stop_transition_the_ui_state(self):
        app = self.make_app(FakeController(state="ready", message="Program loaded successfully."))

        app.start()

        self.assertEqual(app.controller.state, "running")
        self.assertEqual(str(app.run_button.cget("state")), "disabled")
        self.assertEqual(str(app.stop_button.cget("state")), "normal")

        app.stop()

        self.assertEqual(app.controller.state, "stopped")
        self.assertEqual(app.status.get(), "Program stopped.")
        self.assertEqual(str(app.run_button.cget("state")), "normal")
        self.assertEqual(str(app.stop_button.cget("state")), "disabled")

    def test_submit_input_forwarded_once_when_waiting(self):
        controller = FakeController(state="waiting_input", message="Input a word(-9999 to 9999)")
        app = self.make_app(controller)

        accepted = app.submit_input("42")

        self.assertTrue(accepted)
        self.assertEqual(controller.last_input, "42")
        self.assertEqual(controller.state, "running")
        self.assertEqual(app.status.get(), "Input accepted.")

    def test_load_failure_keeps_existing_filename_and_sets_local_error(self):
        app = self.make_app(FakeController(state="ready", message="Program loaded successfully."))
        app._filename = "existing.txt"
        app.filename.set("existing.txt")

        with patch("gui.app.load_program", side_effect=ValueError("Malformed program")):
            result = app.load_file("bad.txt")

        self.assertFalse(result)
        self.assertEqual(app._filename, "existing.txt")
        self.assertEqual(app.filename.get(), "existing.txt")
        self.assertEqual(app.status.get(), "Unable to complete operation: Malformed program")


class TestRealWindow(unittest.TestCase):
    def setUp(self):
        from controller import SimulatorController
        try:
            self.root = tk.Tk()
        except tk.TclError as error:
            self.skipTest(str(error))
        self.root.withdraw()
        self.app = UVSimApp(self.root, SimulatorController())
        self.addCleanup(close_test_app, self.app)

    def run_to_end(self, inputs):
        values = iter(inputs)
        self.app.start()
        for _ in range(1000):
            if self.app.controller.state == "waiting_input":
                self.app.submit_input(str(next(values)))
            elif self.app.controller.state == "running":
                self.app.controller.tick()
                self.app.refresh()
            else:
                break
        self.assertEqual(self.app.controller.state, "halted")
        return self.app.panel.output.get("1.0", "end-1c").splitlines()

    def test_instructor_files_and_repeat_without_disk_access(self):
        cases = [
            ("Test1.txt", [7, 5], [12]),
            ("Test2.txt", [7, 5], [7]),
            ("Test3.txt", [], [3333, 3, 3332, 1666, 666, -334]),
            ("Test3b.txt", [], [3333, 3, 1332, 666, -334, -1334]),
            ("Test4.txt", [], [1111, 2222, 3333, 4444, 5555]),
        ]
        for name, inputs, expected in cases:
            with self.subTest(name=name):
                self.assertTrue(self.app.load_file(ROOT / "programs" / name))
                self.assertEqual(list(map(int, self.run_to_end(inputs))), expected)
                self.assertFalse(self.app.run_button.instate(["disabled"]))
                with patch("gui.app.load_program", side_effect=AssertionError("Reread disk")):
                    self.assertEqual(list(map(int, self.run_to_end(inputs))), expected)
        previous = self.app.filename.get()
        self.assertFalse(self.app.load_file(ROOT / "programs/Test5.txt"))
        self.assertEqual(self.app.filename.get(), previous)

    def test_layout_and_filename_label(self):
        self.root.deiconify()
        self.root.update()
        self.root.update_idletasks()
        self.assertEqual(self.app.filename_heading.cget("text"), "Selected File Name")
        status_y = self.app.status_label.winfo_rooty()
        input_y = self.app.panel.input_entry.winfo_rooty()
        output_y = self.app.panel.output.winfo_rooty()
        self.assertLess(status_y, input_y)
        self.assertLess(input_y, output_y)
        self.assertGreater(self.app.panel.output.winfo_height(), 50)

    def test_rerun_after_stop_and_runtime_error(self):
        self.app.load_file(ROOT / "programs/Test1.txt")
        self.app.start()
        self.app.controller.tick()
        self.app.refresh()
        self.app.stop()
        self.assertFalse(self.app.run_button.instate(["disabled"]))
        self.assertEqual(list(map(int, self.run_to_end([2, 3]))), [5])
        self.app.start()
        self.app.controller.machine.memory[0] = Word(9900)
        self.app.controller.tick()
        self.app.refresh()
        self.assertEqual(self.app.controller.state, "error")
        self.assertFalse(self.app.run_button.instate(["disabled"]))
        self.assertEqual(list(map(int, self.run_to_end([4, 5]))), [9])

    def test_unsaved_edits_drive_each_run_and_preserve_source(self):
        from word import Word
        self.app.editor.set_words([Word(1102), Word(4300), Word(7)])
        self.app.editor.modify_entry(2, "+0009")
        self.assertEqual(list(map(int, self.run_to_end([]))), [9])
        self.assertTrue(self.app.editor.is_dirty)
        self.assertEqual(self.app.editor.get_words()[2].value, 9)
        self.app.editor.modify_entry(2, "+0012")
        self.assertEqual(list(map(int, self.run_to_end([]))), [12])

    def test_invalid_and_empty_editor_do_not_run_old_program(self):
        self.app.load_file(ROOT / "programs/Test1.txt")
        original = self.app.controller.machine
        self.app.editor.modify_entry(0, "bad")
        self.app.start()
        self.assertIn("line 1", self.app.status.get())
        self.assertIs(self.app.controller.machine, original)
        self.assertNotEqual(self.app.controller.state, "running")
        self.app.editor.set_words([])
        self.app.start()
        self.assertIn("empty", self.app.status.get().lower())
        self.assertIs(self.app.controller.machine, original)

    def test_editing_disabled_during_read_and_restored_after_stop(self):
        self.app.load_file(ROOT / "programs/Test1.txt")
        words = self.app.editor.get_words()
        self.app.start()
        self.app.controller.tick()
        self.app.refresh()
        self.assertEqual(self.app.controller.state, "waiting_input")
        self.app.editor.modify_entry(0, "+4300")
        self.assertEqual(self.app.editor.get_words(), words)
        self.assertTrue(self.app.editor.add_button.instate(["disabled"]))
        self.assertFalse(self.app.editor.copy_button.instate(["disabled"]))
        self.app.stop()
        self.assertFalse(self.app.editor.add_button.instate(["disabled"]))

    def test_discard_cancel_preserves_edits_on_open_and_close(self):
        self.app.load_file(ROOT / "programs/Test1.txt")
        self.app.editor.modify_entry(0, "+4300")
        previous = self.app.filename.get()
        with patch("gui.app.messagebox.askyesno", return_value=False):
            self.assertFalse(self.app.load_file(ROOT / "programs/Test2.txt"))
            self.app.close()
        self.assertFalse(self.app._closed)
        self.assertEqual(self.app.filename.get(), previous)
        self.assertTrue(self.app.editor.is_dirty)
        with patch("gui.app.messagebox.askyesno", return_value=True):
            self.assertTrue(self.app.load_file(ROOT / "programs/Test2.txt"))
        self.assertFalse(self.app.editor.is_dirty)

    def test_open_edit_is_committed_before_run_and_minimum_layout(self):
        from word import Word
        self.root.deiconify()
        self.root.geometry("1000x620")
        self.root.update()
        self.app.editor.set_words([Word(1102), Word(4300), Word(7)])
        self.root.update_idletasks()
        self.app.editor._begin_edit(2)
        self.app.editor._edit_widget.delete(0, "end")
        self.app.editor._edit_widget.insert(0, "+0015")
        self.assertEqual(list(map(int, self.run_to_end([]))), [15])
        self.root.update_idletasks()
        self.assertLess(self.app.panel.input_entry.winfo_rooty(),
                        self.app.editor.tree.winfo_rooty())
        self.assertLess(self.app.editor.tree.winfo_rootx(),
                        self.app.panel.output.winfo_rootx())
        self.assertGreater(self.app.editor.tree.winfo_height(), 80)
        self.assertGreater(self.app.panel.output.winfo_height(), 80)


if __name__ == "__main__":
    unittest.main()
