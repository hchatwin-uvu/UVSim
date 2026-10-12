"""WP-4: BasicML word; the only module that knows the digit layout.

Implements the contract defined in Milestone 4/milestone-4.md. WP-2 and WP-3
depend on parse() and format().
"""

MIN_WORD = -9999
MAX_WORD = 9999


class Word:
    """One signed four-digit memory word."""

    def __init__(self, value: int) -> None:
        """Store value; raise ValueError outside MIN_WORD,MAX_WORD."""

        # A BasicML word can only be from -9999 to +9999
        if value < MIN_WORD or value > MAX_WORD:
            raise ValueError(
                f"Word out of range: {value} "
                f"(must be {MIN_WORD} to {MAX_WORD})."
            )

        self._value = value

    @classmethod
    def parse(cls, text: str) -> "Word":
        """Build a Word from file-format text such as +1007 or -0005.

        Raise ValueError with a user-readable explanation for anything else.
        """

        word = text.strip()

        # BasicML words must be signed and exactly four digits
        if len(word) != 5 or word[0] not in "+-" or not word[1:].isdigit():
            raise ValueError(
                f"Invalid BasicML word '{word}': expected a sign (+ or -) "
                "followed by four digits, such as +1007."
            )

        return cls(int(word))

    @property
    def value(self) -> int:
        return self._value

    @property
    def opcode(self) -> int:
        """Function code, currently the first two digits."""
        return abs(self._value) // 100

    @property
    def operand(self) -> int:
        """Memory address 00-99, currently the last two digits."""
        return abs(self._value) % 100

    def format(self) -> str:
        """Return the file format: sign plus four digits, e.g. +1007."""

        # + forces the sign, 05 pads to five characters with zeros
        return f"{self._value:+05d}"

    def __eq__(self, other) -> bool:
        """Two words are equal when they hold the same value."""
        return isinstance(other, Word) and self._value == other._value
