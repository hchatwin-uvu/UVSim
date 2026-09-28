"""WP-1: Tkinter window composed against the shared controller contract."""
import tkinter as tk
from tkinter import filedialog, ttk
from controller import SimulatorController
from gui.io_panel import IOPanel


class UVSimApp:
    """Own the window and one timer; delegate execution to the controller.

    Inject controller/panel_factory to test WP-1 independently. The panel
    builds inside the supplied parent and exposes refresh(state, outputs).
    """
    def __init__(self, root, controller, panel_factory=IOPanel):
        self.root = root
        self.controller = controller
        self._timer = None
        self._closed = False
        self._local_error = None
        self._filename = "No program selected"
        root.title("UVSim | BasicML simulator")
        root.geometry("780x600")
        root.minsize(600, 480)
        root.protocol("WM_DELETE_WINDOW", self.close)
        frame = ttk.Frame(root, padding=20)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="UVSim", font=("Segoe UI", 22, "bold")).pack(anchor="w")
        ttk.Label(frame, text="Open a BasicML file, then run its instructions.").pack(anchor="w", pady=(0, 16))
        toolbar = ttk.Frame(frame)
        toolbar.pack(fill="x")
        self.open_button = ttk.Button(toolbar, text="Open file", command=self.open_file)
        self.open_button.pack(side="left")
        self.run_button = ttk.Button(toolbar, text="Run", command=self.start)
        self.run_button.pack(side="left", padx=8)
        self.stop_button = ttk.Button(toolbar, text="Stop", command=self.stop)
        self.stop_button.pack(side="left")
        self.filename = tk.StringVar(value=self._filename)
        self.file_label = ttk.Label(frame, textvariable=self.filename, wraplength=700)
        self.file_label.pack(fill="x", pady=(12, 16))
        panel_parent = ttk.Frame(frame)
        panel_parent.pack(fill="both", expand=True)
        self.panel = panel_factory(panel_parent, self.submit_input)
        ttk.Separator(frame).pack(fill="x", pady=(16, 10))
        self.status = tk.StringVar()
        self.status_label = ttk.Label(frame, textvariable=self.status, wraplength=700)
        self.status_label.pack(fill="x")
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
        try:
            path = filedialog.askopenfilename(
                parent=self.root, title="Open BasicML program",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        except tk.TclError as error:
            self._local_error = f"Cannot open file picker: {error}. Try Open file again."
            self.refresh()
            return
        if path:
            self.load_file(path)

    def load_file(self, path):
        if self.controller.state in ("running", "waiting_input"):
            return False
        accepted = self._invoke(self.controller.load_file, path)
        if accepted:
            self._filename = str(path)
        self.refresh()
        return bool(accepted)

    def start(self):
        if self.controller.state == "ready":
            self._invoke(self.controller.start)
            self.refresh()

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
        self.run_button.configure(state="normal" if state == "ready" else "disabled")
        self.stop_button.configure(state="normal" if active else "disabled")
        self.filename.set(self._filename)
        self.status.set(self._local_error or self.controller.message)
        self.panel.refresh(state, self.controller.outputs)

    def close(self):
        if self._closed:
            return
        self._closed = True
        if self._timer is not None:
            self.root.after_cancel(self._timer)
            self._timer = None
        self.root.destroy()


def launch(path=None):
    """Launch the GUI, showing an explicit notice for unfinished dependencies."""
    root = tk.Tk()
    try:
        app = UVSimApp(root, SimulatorController())
    except NotImplementedError:
        for widget in root.winfo_children():
            widget.destroy()
        root.title("UVSim | Integration pending")
        frame = ttk.Frame(root, padding=24)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="GUI integration is not ready", font=("Segoe UI", 16, "bold")).pack(anchor="w")
        ttk.Label(frame, text="WP-1 is implemented. WP-2's controller and WP-3's I/O panel must be implemented before programs can run here. The console application remains available with python main.py.", wraplength=480).pack(pady=16)
        ttk.Button(frame, text="Close", command=root.destroy).pack(anchor="e")
    else:
        if path:
            app.load_file(path)
    root.mainloop()
