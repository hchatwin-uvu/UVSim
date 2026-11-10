"""BasicML word; the only module that knows the digit layout.

Milestone 5 format: a sign followed by six digits. The first three digits are
the operation code and the last three are the memory address, so READ (010)
into address 007 is written +010007. WP-2 and WP-3 depend on parse() and
format().
"""

WORD_DIGITS = 6
OPCODE_DIGITS = 3
ADDRESS_DIGITS = WORD_DIGITS - OPCODE_DIGITS

MAX_WORD = 10 ** WORD_DIGITS - 1  # 999999
MIN_WORD = -MAX_WORD               # -999999

# Splits a magnitude into its operation code and address fields
_ADDRESS_BASE = 10 ** ADDRESS_DIGITS


class Word:
    """One signed six-digit memory word."""

    def __init__(self, value: int) -> None:
        """Store value; raise ValueError outside MIN_WORD,MAX_WORD."""

        # A BasicML word can only be from -999999 to +999999
        if value < MIN_WORD or value > MAX_WORD:
            raise ValueError(
                f"Word out of range: {value} "
                f"(must be {MIN_WORD} to {MAX_WORD})."
            )

        self._value = value

    @classmethod
    def parse(cls, text: str) -> "Word":
        """Build a Word from file-format text such as +010007 or -000005.

        Raise ValueError with a user-readable explanation for anything else.
        """

        word = text.strip()

        # BasicML words must be signed and exactly six digits. isdecimal()
        if (len(word) != WORD_DIGITS + 1 or word[0] not in "+-"
                or not word[1:].isdecimal() or not word[1:].isascii()):
            raise ValueError(
                f"Invalid BasicML word '{word}': expected a sign (+ or -) "
                "followed by six digits, such as +010007."
            )

        return cls(int(word))

    @property
    def value(self) -> int:
        return self._value

    @property
    def opcode(self) -> int:
        """Operation code, the first three digits"""
        return abs(self._value) // _ADDRESS_BASE

    @property
    def operand(self) -> int:
        """Memory address 000-999, the last three digits."""
        return abs(self._value) % _ADDRESS_BASE

    def format(self) -> str:
        """Return the file format: sign plus six digits, e.g. +010007."""

        # + forces the sign, 05 pads to seven characters with zeros
        return f"{self._value:+0{WORD_DIGITS + 1}d}"

    def __eq__(self, other) -> bool:
        """Two words are equal when they hold the same value."""
        return isinstance(other, Word) and self._value == other._value
