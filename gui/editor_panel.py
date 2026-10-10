"""WP-2: Program editor panel scaffold.

Implement the contract defined in Milestone 4/milestone-4.md. The editor holds
the single copy of the program the user sees; it does not execute it. No
behavior is implemented here.
"""
from collections.abc import Callable, Sequence

from word import Word

MAX_ENTRIES = 100


class EditorPanel:
    """Embeddable view/edit component for up to MAX_ENTRIES words."""

    def __init__(self, parent, on_change: Callable[[], None]) -> None:
        """Build the editor inside parent, showing address 00-99 per entry.

        on_change is called after every user edit so the window can refresh.
        """
        raise NotImplementedError("WP-2: EditorPanel.__init__")

    def set_words(self, words: Sequence[Word]) -> None:
        """Replace the contents with words and clear the unsaved-changes flag."""
        raise NotImplementedError("WP-2: EditorPanel.set_words")

    def get_words(self) -> list[Word]:
        """Return the current entries; raise ValueError naming an invalid line."""
        raise NotImplementedError("WP-2: EditorPanel.get_words")

    @property
    def is_dirty(self) -> bool:
        """True when edits have been made since set_words() or mark_saved()."""
        raise NotImplementedError("WP-2: EditorPanel.is_dirty")

    def mark_saved(self) -> None:
        """Clear the unsaved-changes flag after a successful save."""
        raise NotImplementedError("WP-2: EditorPanel.mark_saved")

    def set_enabled(self, enabled: bool) -> None:
        """Make the editor read-only while a program runs or awaits input."""
        raise NotImplementedError("WP-2: EditorPanel.set_enabled")

    def add_entry(self) -> None:
        """Insert a new entry at the selection; later entries shift down.

        Rejected with an explanation when the program already has MAX_ENTRIES.
        """
        raise NotImplementedError("WP-2: EditorPanel.add_entry")

    def delete_selected(self) -> None:
        """Remove the selected entries; later entries shift up."""
        raise NotImplementedError("WP-2: EditorPanel.delete_selected")

    def cut(self) -> None:
        """Copy the selected entries to the clipboard, then delete them."""
        raise NotImplementedError("WP-2: EditorPanel.cut")

    def copy(self) -> None:
        """Copy the selected entries to the clipboard, one word per line."""
        raise NotImplementedError("WP-2: EditorPanel.copy")

    def paste(self) -> None:
        """Insert clipboard entries at the selection.

        A paste that would exceed MAX_ENTRIES follows the agreed policy;
        the proposal is to reject it and leave the program unchanged.
        """
        raise NotImplementedError("WP-2: EditorPanel.paste")
