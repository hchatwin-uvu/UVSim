"""WP-1: Tkinter window composed against the shared controller contract."""
import tkinter as tk
from tkinter import ttk
from controller import SimulatorController
from gui.io_panel import IOPanel
from gui.editor_panel import EditorPanel
from gui.file_actions import FileActions
from gui.theme import apply_theme
from theme_config import load_theme
from program_store import ProgramStore


class UVSimApp:
    """Own the window and one timer; delegate execution to the controller.

    Inject controller/panel_factory to test WP-1 independently. The panel
    builds inside the supplied parent and exposes refresh(state, outputs).
    """
    def __init__(self, root, controller, panel_factory=IOPanel, theme=None):
        self.root = root
        self.controller = controller
        self._timer = None
        self._closed = False
        self._local_error = None
        self.theme = theme if theme is not None else load_theme()
        root.title("UVSim | BasicML simulator")
        root.geometry("1100x720")
        root.minsize(1000, 620)
        root.protocol("WM_DELETE_WINDOW", self.close)
        frame = ttk.Frame(root, padding=20)
        frame.pack(fill="both", expand=True)
        header = ttk.Frame(frame, style="Brand.TFrame", padding=16)
        header.pack(fill="x", pady=(0, 16))
        ttk.Label(header, text="UVSim", style="Brand.TLabel", font=("Segoe UI", 24, "bold")).pack(anchor="w")
        ttk.Label(header, text="BasicML simulator", style="Brand.TLabel").pack(anchor="w")
        toolbar = ttk.Frame(frame)
        toolbar.pack(fill="x")
        self.open_button = ttk.Button(toolbar, text="Open file", command=self.open_file)
        self.open_button.pack(side="left")
        self.save_button = ttk.Button(toolbar, text="Save", command=self.save_file)
        self.save_button.pack(side="left", padx=(8, 0))
        self.save_as_button = ttk.Button(toolbar, text="Save As", command=self.save_file_as)
        self.save_as_button.pack(side="left", padx=(8, 0))
        self.run_button = ttk.Button(toolbar, text="Run", command=self.start)
        self.run_button.pack(side="left", padx=8)
        self.stop_button = ttk.Button(toolbar, text="Stop", command=self.stop)
        self.stop_button.pack(side="left")
        self.filename = tk.StringVar(value="No program selected")
        self.filename_heading = ttk.Label(frame, text="Selected File Name", font=("Segoe UI", 10, "bold"))
        self.filename_heading.pack(anchor="w", pady=(14, 4))
        self.file_label = ttk.Label(frame, textvariable=self.filename, wraplength=700)
        self.file_label.pack(fill="x", pady=(0, 10))
        ttk.Separator(frame).pack(fill="x", pady=(0, 10))
        self.status = tk.StringVar()
        self.status_label = ttk.Label(frame, textvariable=self.status, wraplength=700)
        self.status_label.pack(fill="x", pady=(0, 12))
        panel_parent = ttk.Frame(frame)
        panel_parent.pack(fill="x")
        workspace = ttk.Frame(frame)
        workspace.pack(fill="both", expand=True)
        workspace.columnconfigure(0, weight=1, uniform="panels")
        workspace.columnconfigure(1, weight=1, uniform="panels")
        workspace.rowconfigure(0, weight=1)
        editor_parent = ttk.Frame(workspace, padding=(0, 0, 12, 0))
        editor_parent.grid(row=0, column=0, sticky="nsew")
        output_parent = ttk.Frame(workspace)
        output_parent.grid(row=0, column=1, sticky="nsew")
        self.editor = EditorPanel(editor_parent, self._editor_changed)
        self.file_actions = FileActions(
            root, ProgramStore(), self.editor, self._file_status_changed)
        self.panel = panel_factory(panel_parent, self.submit_input, output_parent=output_parent)
        apply_theme(root, self.theme)
        frame.bind("<Configure>", self._resize_labels)
        self.refresh()
        self._schedule()

    def _resize_labels(self, event):
        width = max(200, event.width - 8)
        self.file_label.configure(wraplength=width)
        self.status_label.configure(wraplength=width)

    def _schedule(self):
        if not self._closed and self._timer is None:
            self._timer = self.root.after(20, self._pump)

    def _pump(self):
        self._timer = None
        if self._closed:
            return
        if self.controller.state == "running" and self._local_error is None:
            self._invoke(self.controller.tick)
        self.refresh()
        self._schedule()

    def _invoke(self, action, *args):
        """Display boundary failures; suppress repeat ticks until user action."""
        self._local_error = None
        try:
            return action(*args)
        except (OSError, ValueError, EOFError, NotImplementedError) as error:
            self._local_error = f"Unable to complete operation: {error}"
            return False

    def open_file(self):
        if self.controller.state in ("running", "waiting_input"):
            return
        self.file_actions.open()
        self.refresh()

    def load_file(self, path):
        if self.controller.state in ("running", "waiting_input"):
            return False
        accepted = self.file_actions.open_path(path)
        self.refresh()
        return accepted

    def save_file(self):
        if self.controller.state in ("running", "waiting_input"):
            return
        self.file_actions.save()
        self.refresh()

    def save_file_as(self):
        if self.controller.state in ("running", "waiting_input"):
            return
        self.file_actions.save_as()
        self.refresh()

    def start(self):
        if self.controller.state not in ("running", "waiting_input"):
            def prepare():
                return self.controller.load_program(self.editor.get_words())
            if not self._invoke(prepare):
                self.refresh()
                return
            self.panel.refresh(self.controller.state, self.controller.outputs)
            self._invoke(self.controller.start)
            self.refresh()

    def _editor_changed(self):
        """Keep stale execution errors from hiding the editor's current feedback."""
        self._local_error = None
        self.status.set("Program edited. Run uses the current editor contents.")

    def _file_status_changed(self, message):
        self._local_error = message

    def confirm_discard(self):
        return self.file_actions.confirm_discard()

    def stop(self):
        if self.controller.state in ("running", "waiting_input"):
            self._invoke(self.controller.stop)
            self.refresh()

    def submit_input(self, text):
        if self.controller.state != "waiting_input":
            return False
        accepted = self._invoke(self.controller.submit_input, text)
        self.refresh()
        return bool(accepted)

    def refresh(self):
        state = self.controller.state
        active = state in ("running", "waiting_input")
        self.open_button.configure(state="disabled" if active else "normal")
        self.save_button.configure(state="disabled" if active else "normal")
        self.save_as_button.configure(state="disabled" if active else "normal")
        can_run = not active
        self.run_button.configure(state="normal" if can_run else "disabled")
        self.stop_button.configure(state="normal" if active else "disabled")
        self.editor.set_enabled(not active)
        self.filename.set(self.file_actions.current_path or "No program selected")
        self.status.set(self._local_error or self.controller.message)
        self.panel.refresh(state, self.controller.outputs)

    def close(self):
        if self._closed:
            return
        if not self.confirm_discard():
            return
        self._closed = True
        if self._timer is not None:
            self.root.after_cancel(self._timer)
            self._timer = None
        self.root.destroy()


def launch(path=None):
    """Launch the editor, simulator controls, and configured branding."""
    root = tk.Tk()
    app = UVSimApp(root, SimulatorController())
    if path:
        app.load_file(path)
    root.mainloop()
