"""WP-4: BasicML word scaffold; the only module that knows the digit layout.

Implement the contract defined in Milestone 4/milestone-4.md. WP-2 and WP-3
depend on parse() and format(), so deliver this first. No behavior is
implemented here.
"""

MIN_WORD = -9999
MAX_WORD = 9999


class Word:
    """One signed four-digit memory word."""

    def __init__(self, value: int) -> None:
        """Store value; raise ValueError outside MIN_WORD..MAX_WORD."""
        raise NotImplementedError("WP-4: Word.__init__")

    @classmethod
    def parse(cls, text: str) -> "Word":
        """Build a Word from file-format text such as +1007 or -0005.

        Raise ValueError with a user-readable explanation for anything else.
        """
        raise NotImplementedError("WP-4: Word.parse")

    @property
    def value(self) -> int:
        """Raw signed integer."""
        raise NotImplementedError("WP-4: Word.value")

    @property
    def opcode(self) -> int:
        """Function code, currently the first two digits."""
        raise NotImplementedError("WP-4: Word.opcode")

    @property
    def operand(self) -> int:
        """Memory address 00-99, currently the last two digits."""
        raise NotImplementedError("WP-4: Word.operand")

    def format(self) -> str:
        """Return the file format: sign plus four digits, e.g. +1007."""
        raise NotImplementedError("WP-4: Word.format")
