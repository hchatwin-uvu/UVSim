"""WP-3: Data-layer scaffold for reading and writing BasicML program files.

Replaces loader.py once implemented; no Tkinter imports. The controller must
not import this module (TODO-4). Implement the contract defined in
Milestone 4/milestone-4.md. No behavior is implemented here.
"""
from word import Word

MAX_PROGRAM_WORDS = 100


class ProgramStore:
    """Load and save programs as one formatted word per line."""

    def load(self, path: str) -> list[Word]:
        """Return the validated words in the file at path.

        Keep loader.load_program's rules and line-numbered messages: blank
        lines ignored, at most MAX_PROGRAM_WORDS. Raise OSError or ValueError.
        """
        raise NotImplementedError("WP-3: ProgramStore.load")

    def save(self, path: str, words: list[Word]) -> None:
        """Write words to path so that load(path) returns them unchanged.

        Raise OSError or ValueError. A failed save must not leave a partly
        written file in place of the original.
        """
        raise NotImplementedError("WP-3: ProgramStore.save")
