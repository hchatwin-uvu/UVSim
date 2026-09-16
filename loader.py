"""Person 1's proposed area: BasicML file loading and validation."""


def load_program(path: str) -> list[int]:
    """Load and validate a BasicML program from a text file."""

    words = []

    with open(path, "r") as file:
        for line_number, line in enumerate(file, start=1):
            word = line.strip()

            # Ignore blank lines
            if not word:
                continue

            # BasicML words must be signed and exactly four digits
            if len(word) != 5 or word[0] not in "+-" or not word[1:].isdigit():
                raise ValueError(
                    f"Invalid BasicML word on line {line_number}: {word}"
                )

            value = int(word)

            # A BasicML word can only be from -9999 to +9999
            if value < -9999 or value > 9999:
                raise ValueError(
                    f"BasicML word out of range on line {line_number}: {word}"
                )

            words.append(value)

            # UVSim only has 100 memory locations
            if len(words) > 100:
                raise ValueError("Program contains more than 100 words.")

    return words