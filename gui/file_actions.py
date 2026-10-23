"""Open, Save, and Save As commands for the program editor."""
import os
import tkinter as tk
from collections.abc import Callable
from tkinter import filedialog, messagebox

from gui.editor_panel import EditorPanel
from program_store import ProgramStore


class FileActions:
    """File commands the window places on its toolbar."""

    def __init__(self, root, store: ProgramStore, editor: EditorPanel,
                 on_status: Callable[[str], None]) -> None:
        self.root = root
        self.store = store
        self.editor = editor
        self.on_status = on_status
        self._current_path: str | None = None

    @property
    def current_path(self) -> str | None:
        """Path last opened or saved, for the Selected File Name field."""
        return self._current_path

    def open(self) -> bool:
        """Choose a program file and open it, preserving state on cancellation."""
        try:
            path = filedialog.askopenfilename(
                parent=self.root,
                title="Open BasicML program",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            )
        except tk.TclError as error:
            self.on_status(f"Cannot open file picker: {error}")
            return False
        return self.open_path(path) if path else False

    def open_path(self, path: str) -> bool:
        """Load path without a dialog, e.g. the optional command-line file."""
        try:
            entries = self.store.load_source(path)
            if not self.confirm_discard():
                return False
            # Saving during confirmation may have changed the selected file.
            entries = self.store.load_source(path)
            self.editor.set_entries(entries)
        except (OSError, ValueError, tk.TclError) as error:
            self.on_status(f"Unable to open program: {error}")
            return False

        self._current_path = os.fspath(path)
        self.on_status(f"Opened {self._current_path}")
        return True

    def save(self) -> bool:
        """Save to the current path, or prompt for one if not set."""
        if self._current_path is None:
            return self.save_as()
        try:
            self.store.save(self._current_path, self.editor.get_words())
        except (OSError, ValueError) as error:
            self.on_status(f"Unable to save program: {error}")
            return False
        self.editor.mark_saved()
        self.on_status(f"Saved {self._current_path}")
        return True

    def save_as(self) -> bool:
        """Choose a destination and save the editor there."""
        try:
            path = filedialog.asksaveasfilename(
                parent=self.root,
                title="Save BasicML program",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            )
        except tk.TclError as error:
            self.on_status(f"Cannot open save dialog: {error}")
            return False
        if not path:
            return False
        try:
            self.store.save(path, self.editor.get_words())
        except (OSError, ValueError) as error:
            self.on_status(f"Unable to save program: {error}")
            return False

        self._current_path = os.fspath(path)
        self.editor.mark_saved()
        self.on_status(f"Saved {self._current_path}")
        return True

    def confirm_discard(self) -> bool:
        """Ask before dirty editor contents are replaced or discarded."""
        if not self.editor.is_dirty:
            return True
        answer = messagebox.askyesnocancel(
            "Save unsaved edits?",
            "Save your changes before continuing?\n"
            "Yes: Save   No: Discard   Cancel: Keep editing",
            parent=self.root,
            default="cancel",
        )
        if answer is None:
            return False
        return self.save() if answer else True
