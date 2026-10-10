"""WP-1: Color configuration scaffold; no Tkinter imports.

Reads the user's color scheme at startup so it can change without touching
source code. Implement the contract defined in Milestone 4/milestone-4.md.
The file name and format below are proposals. No behavior is implemented here.
"""
from dataclasses import dataclass

THEME_FILE = "theme.ini"
UVU_PRIMARY = "#4C721D"
UVU_OFF_COLOR = "#FFFFFF"


@dataclass(frozen=True)
class Theme:
    """One primary color and one off-color, as #RRGGBB hex strings."""

    primary: str = UVU_PRIMARY
    off_color: str = UVU_OFF_COLOR


def load_theme(path: str = THEME_FILE) -> Theme:
    """Return the configured Theme.

    A missing file, missing key, or invalid color falls back to the UVU
    defaults; this function must not raise for bad configuration.
    """
    raise NotImplementedError("WP-1: load_theme")


def save_theme(theme: Theme, path: str = THEME_FILE) -> None:
    """Write theme to path. Only needed if the optional in-app picker is built."""
    raise NotImplementedError("WP-1: save_theme")
