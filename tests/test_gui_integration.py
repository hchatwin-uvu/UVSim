import os
import tkinter as tk
import unittest
from pathlib import Path
from unittest.mock import patch

from gui.app import UVSimApp

ROOT = Path(__file__).resolve().parents[1]


class FakePanel:
    """Minimal panel used to assert refresh calls without building a real Tk widget tree."""

    def __init__(self, parent, on_submit):
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
        self.loaded_paths = []
        self.last_input = None

    @property
    def outputs(self):
        return list(self._outputs)

    def load_file(self, path):
        self.loaded_paths.append(path)
        if path.endswith("bad.txt"):
            raise ValueError("Malformed program")
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


@unittest.skipUnless(os.environ.get("DISPLAY"), "Tkinter requires a display")
class TestGUIIntegration(unittest.TestCase):
    def make_app(self, controller=None):
        root = tk.Tk()
        root.withdraw()
        app = UVSimApp(root, controller or FakeController(), panel_factory=FakePanel)
        self.addCleanup(root.destroy)
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

        self.assertEqual(controller.loaded_paths, [])
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
        self.assertEqual(str(app.run_button.cget("state")), "disabled")
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

        result = app.load_file("bad.txt")

        self.assertFalse(result)
        self.assertEqual(app._filename, "existing.txt")
        self.assertEqual(app.filename.get(), "existing.txt")
        self.assertEqual(app.status.get(), "Unable to complete operation: Malformed program")


if __name__ == "__main__":
    unittest.main()
