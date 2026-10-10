"""WP-3: Open, Save, and Save As scaffold.

Owns the file dialogs and the current path; moves words between ProgramStore
and the editor. Implement the contract defined in Milestone 4/milestone-4.md.
No behavior is implemented here.
"""
from collections.abc import Callable

from gui.editor_panel import EditorPanel
from program_store import ProgramStore


class FileActions:
    """File commands the window places on its toolbar."""

    def __init__(self, root, store: ProgramStore, editor: EditorPanel,
                 on_status: Callable[[str], None]) -> None:
        """Keep the collaborators; on_status reports results and errors."""
        raise NotImplementedError("WP-3: FileActions.__init__")

    @property
    def current_path(self) -> str | None:
        """Path last opened or saved, for the Selected File Name field."""
        raise NotImplementedError("WP-3: FileActions.current_path")

    def open(self) -> bool:
        """Pick a file from any directory and load it into the editor.

        Cancel, or a failed load, leaves the editor and current path unchanged.
        """
        raise NotImplementedError("WP-3: FileActions.open")

    def open_path(self, path: str) -> bool:
        """Load path without a dialog, e.g. the optional command-line file."""
        raise NotImplementedError("WP-3: FileActions.open_path")

    def save(self) -> bool:
        """Save the editor to the current path; behaves as save_as() without one."""
        raise NotImplementedError("WP-3: FileActions.save")

    def save_as(self) -> bool:
        """Pick a name and directory, save, and make it the current path."""
        raise NotImplementedError("WP-3: FileActions.save_as")

    def confirm_discard(self) -> bool:
        """Ask before unsaved edits are lost; True when it is safe to proceed."""
        raise NotImplementedError("WP-3: FileActions.confirm_discard")
