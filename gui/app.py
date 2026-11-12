"""WP-1: Tkinter window composed against the shared controller contract."""
import os
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog
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
        self.documents = {}
        self._active_tab = None
        self._untitled_count = 0
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
        self.new_button = ttk.Button(toolbar, text="New", command=self.new_document)
        self.new_button.pack(side="left", padx=(0, 8))
        self.close_tab_button = ttk.Button(toolbar, text="Close tab", command=self.close_document)
        self.close_tab_button.pack(side="left", padx=(0, 8))
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
        self.notebook = ttk.Notebook(editor_parent)
        self.notebook.pack(fill="both", expand=True)
        self._create_document()
        self.notebook.bind("<<NotebookTabChanged>>", self._tab_changed)
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

    @property
    def execution_active(self):
        return self.controller.state in ("running", "waiting_input")

    def _create_document(self, entries=(), path=None):
        frame = ttk.Frame(self.notebook)
        tab = str(frame)
        editor = EditorPanel(frame, self._editor_changed)
        editor.set_entries(entries)
        self._untitled_count += 1
        name = f"Untitled {self._untitled_count}"
        actions = FileActions(
            self.root, ProgramStore(), editor, self._file_status_changed,
            path=path, document_name=name,
            validate_destination=lambda destination: self._validate_destination(tab, destination))
        self.documents[tab] = (frame, editor, actions, name)
        self.notebook.add(frame, text=Path(path).name if path else self.documents[tab][3])
        self._select_document(tab)
        return tab

    def _select_document(self, tab):
        if self._active_tab == tab:
            return
        if self.execution_active and self._active_tab is not None:
            self.notebook.select(self._active_tab)
            return
        if self._active_tab in self.documents:
            # Commit a pending cell edit before hiding its document.
            self.editor.finish_edit()
        self._active_tab = tab
        _, self.editor, self.file_actions, _ = self.documents[tab]
        self.notebook.select(tab)
        if hasattr(self, "panel"):
            self.controller.clear()
            self.panel.refresh("empty", [])
            if hasattr(self.panel, "input_text"):
                self.panel.input_text.set("")
            self._local_error = None
            self.refresh()

    def _tab_changed(self, event=None):
        tab = self.notebook.select()
        if tab in self.documents:
            self._select_document(tab)

    @staticmethod
    def _path_key(path):
        return os.path.normcase(os.path.realpath(path))

    def _validate_destination(self, owner, path):
        key = self._path_key(path)
        for tab, (_, _, actions, _) in self.documents.items():
            if tab != owner and actions.current_path and self._path_key(actions.current_path) == key:
                raise ValueError("That file is open in another tab. Choose a different filename.")

    def new_document(self):
        if not self.execution_active:
            self._create_document()
            self.refresh()

    def close_document(self):
        if self.execution_active:
            return False
        if not self.confirm_discard():
            self.refresh()
            return False
        tab = self._active_tab
        frame = self.documents.pop(tab)[0]
        self.notebook.forget(tab)
        frame.destroy()
        self._active_tab = None
        if self.documents:
            self._select_document(next(iter(self.documents)))
        else:
            self._create_document()
        self.refresh()
        return True

    def open_file(self):
        if self.execution_active:
            return
        try:
            path = filedialog.askopenfilename(
                parent=self.root, title="Open BasicML program",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if path:
                self.load_file(path)
        except tk.TclError as error:
            self._file_status_changed(f"Cannot open file picker: {error}")
            self.refresh()

    def load_file(self, path):
        if self.execution_active:
            return False
        # Reopening an existing path focuses its unsaved document, never reloads it.
        key = self._path_key(path)
        for tab, (_, _, actions, _) in self.documents.items():
            if actions.current_path and self._path_key(actions.current_path) == key:
                self._select_document(tab)
                self.refresh()
                return True
        try:
            entries = self.file_actions.store.load_source(path)
        except (OSError, ValueError) as error:
            self._file_status_changed(f"Unable to open program: {error}")
            self.refresh()
            return False
        self._create_document(entries, path)
        self._file_status_changed(f"Opened {path}")
        self.refresh()
        return True

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
        self._update_tab_titles()

    def _file_status_changed(self, message):
        self._local_error = message

    def confirm_discard(self, all_documents=False):
        if all_documents:
            return all(actions.confirm_discard()
                       for _, _, actions, _ in self.documents.values())
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

    def _update_tab_titles(self):
        for tab, (_, editor, actions, untitled) in self.documents.items():
            name = Path(actions.current_path).name if actions.current_path else untitled
            # Do not finish edits here: on_change may be called by an active edit.
            dirty = editor.has_changes
            self.notebook.tab(tab, text=name + (" *" if dirty else ""))

    def refresh(self):
        state = self.controller.state
        active = state in ("running", "waiting_input")
        self.open_button.configure(state="disabled" if active else "normal")
        self.save_button.configure(state="disabled" if active else "normal")
        self.save_as_button.configure(state="disabled" if active else "normal")
        self.new_button.configure(state="disabled" if active else "normal")
        self.close_tab_button.configure(state="disabled" if active else "normal")
        for tab in self.documents:
            self.notebook.tab(tab, state="disabled" if active and tab != self._active_tab else "normal")
        self._update_tab_titles()
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
        # Keep every tab intact until all prompts have succeeded.
        # During execution the active editor is read-only, but can still be saved.
        if not self.confirm_discard(all_documents=True):
            self.refresh()
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
