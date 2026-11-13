"""WP-3: Data-layer scaffold for reading and writing BasicML program files.

Replaces loader.py once implemented; no Tkinter imports. The controller must
not import this module (TODO-4). Implement the contract defined in
Milestone 4/milestone-4.md.
"""
import os
import tempfile

from uvsim import MEMORY_SIZE, check_program_length
from word import Word

MAX_PROGRAM_WORDS = MEMORY_SIZE


class ProgramStore:
    """Load and save programs as one formatted word per line."""

    def load_source(self, path: str) -> list[str]:
        """Read editable entries without rejecting malformed BasicML words.

        Blank lines are ignored as in load(). Reject oversized files without
        truncation so the existing editor is never partially replaced.
        """
        with open(path, encoding="utf-8-sig") as source:
            entries = [line.strip() for line in source if line.strip()]
        check_program_length(len(entries))
        return entries

    def load(self, path: str) -> list[Word]:
        """Return the validated words in the file at path.

        Blank lines are ignored and errors include source line numbers.
        Raise OSError or ValueError.
        """
        words = []
        with open(path, "r", encoding="utf-8-sig") as source:
            for line_number, line in enumerate(source, start=1):
                text = line.strip()
                if not text:
                    continue
                try:
                    word = Word.parse(text)
                except ValueError as error:
                    raise ValueError(
                        f"Invalid BasicML word on line {line_number}: {text}: {error}"
                    ) from error
                words.append(word)
                check_program_length(len(words))
        return words

    def save(self, path: str, words: list[Word]) -> None:
        """Write words to path so that load(path) returns them unchanged.

        Raise OSError or ValueError. A failed save must not leave a partly
        written file in place of the original.
        """
        check_program_length(len(words))
        if any(not isinstance(word, Word) for word in words):
            raise ValueError("ProgramStore.save expects Word objects.")

        destination = os.path.abspath(os.fspath(path))
        directory = os.path.dirname(destination)
        temporary_path = None
        try:
            with tempfile.NamedTemporaryFile(
                    mode="w", encoding="utf-8", newline="\n",
                    dir=directory, prefix=".uvsim-", suffix=".tmp",
                    delete=False) as temporary:
                temporary_path = temporary.name
                for word in words:
                    temporary.write(word.format() + "\n")
            os.replace(temporary_path, destination)
        except OSError:
            if temporary_path is not None:
                try:
                    os.remove(temporary_path)
                except FileNotFoundError:
                    pass
            raise
