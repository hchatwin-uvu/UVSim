"""WP-3: Reusable READ validation, independent of Tkinter and machine state."""

from word import MAX_WORD, MIN_WORD

def parse_word(text: str) -> int:
    """Return a valid signed integer in -999999..999999."""

    text = text.strip()

    if not text:
        raise ValueError("Input cannot be blank.")

    try:
        value = int(text)
    except ValueError:
        raise ValueError("Input must be a whole number.") from None

    if value < MIN_WORD or value > MAX_WORD:
        raise ValueError(f"Input must be between {MIN_WORD} and {MAX_WORD}.")

    return value