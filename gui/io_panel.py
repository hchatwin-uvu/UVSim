"""WP-3: READ input and WRITE output panel scaffold.

TODO: Implement Tkinter/ttk widgets within the supplied parent.
Submit/Enter calls on_submit(raw_text); execution belongs to the controller.
Use operations.io_memory.format_word for display. No window is created here yet.
See Milestone 3/milestone-3.md for input clearing and refresh behavior.
"""

from collections.abc import Callable, Sequence


class IOPanel:
    """Embeddable input/output component owned by WP-3."""

    def __init__(self, parent, on_submit: Callable[[str], bool]) -> None:
        """Build widgets; on_submit returns whether the controller accepted input."""
        raise NotImplementedError("WP-3: build the READ/WRITE panel.")

    def refresh(self, state: str, outputs: Sequence[int]) -> None:
        """Enable input only when waiting; refresh output without duplicate lines."""
        raise NotImplementedError("WP-3: implement panel refresh.")
