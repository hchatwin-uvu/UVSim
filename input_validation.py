"""WP-3: Reusable READ validation, independent of Tkinter and machine state."""


def parse_word(text: str) -> int:
    """Return a valid signed integer in -9999..9999.

    TODO: Reject blank, invalid, and out-of-range input with a ValueError
    containing a user-readable explanation. Both widgets and controller can
    use this function; it must not modify simulator state or display messages.
    """
    raise NotImplementedError("WP-3: implement READ input validation.")
