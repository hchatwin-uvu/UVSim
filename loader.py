"""Person 1's proposed area: BasicML file loading and validation."""

from uvsim import check_program_length
from word import Word


def load_program(path: str) -> list[int]:
    """Load and validate a BasicML program from a text file."""

    words = []

    with open(path, "r") as file:
        for line_number, line in enumerate(file, start=1):
            word = line.strip()

            # Ignore blank lines
            if not word:
                continue

            # Word owns the six-digit format and range rules
            try:
                word = Word.parse(word)
            except ValueError as error:
                raise ValueError(
                    f"Invalid BasicML word on line {line_number}: {error}"
                )

            words.append(word.value)

            # 250 memory
            check_program_length(len(words))

    return words