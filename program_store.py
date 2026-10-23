"""WP-3: Data-layer scaffold for reading and writing BasicML program files.

Replaces loader.py once implemented; no Tkinter imports. The controller must
not import this module (TODO-4). Implement the contract defined in
Milestone 4/milestone-4.md.
"""
import os
import tempfile

from word import Word

MAX_PROGRAM_WORDS = 100


class ProgramStore:
    """Load and save programs as one formatted word per line."""

    def load(self, path: str) -> list[Word]:
        """Return the validated words in the file at path.

        Keep loader.load_program's rules and line-numbered messages: blank
        lines ignored, at most MAX_PROGRAM_WORDS. Raise OSError or ValueError.
        """
        words = []
        with open(path, "r", encoding="utf-8") as source:
            for line_number, line in enumerate(source, start=1):
                text = line.strip()
                if not text:
                    continue
                if (len(text) != 5 or text[0] not in "+-"
                        or not text[1:].isdigit()):
                    raise ValueError(
                        f"Invalid BasicML word on line {line_number}: {text}"
                    )

                value = int(text)
                if not -9999 <= value <= 9999:
                    raise ValueError(
                        f"BasicML word out of range on line {line_number}: {text}"
                    )
                words.append(Word(value))
                if len(words) > MAX_PROGRAM_WORDS:
                    raise ValueError("Program contains more than 100 words.")
        return words

    def save(self, path: str, words: list[Word]) -> None:
        """Write words to path so that load(path) returns them unchanged.

        Raise OSError or ValueError. A failed save must not leave a partly
        written file in place of the original.
        """
        if len(words) > MAX_PROGRAM_WORDS:
            raise ValueError("Program contains more than 100 words.")
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
