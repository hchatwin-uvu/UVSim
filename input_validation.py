"""WP-3: Reusable READ validation, independent of Tkinter and machine state."""


def parse_word(text: str) -> int:
    """Return a valid signed integer in -9999..9999."""

    text = text.strip()

    if not text:
        raise ValueError("Input cannot be blank.")

    try:
        value = int(text)
    except ValueError:
        raise ValueError("Input must be a whole number.") from None

    if value < -9999 or value > 9999:
        raise ValueError("Input must be between -9999 and 9999.")

    return value