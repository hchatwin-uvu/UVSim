"""Startup branding settings, independent of Tkinter and launch directory."""
from configparser import ConfigParser, Error
from dataclasses import dataclass
from pathlib import Path
import re

THEME_FILE = Path(__file__).resolve().with_name("theme.ini")
UVU_PRIMARY = "#4C721D"
UVU_OFF_COLOR = "#FFFFFF"

@dataclass(frozen=True)
class Theme:
    """Primary and off-color in #RRGGBB format."""
    primary: str = UVU_PRIMARY
    off_color: str = UVU_OFF_COLOR

def load_theme(path=THEME_FILE) -> Theme:
    """Load both [theme] keys; unreadable, incomplete or invalid files use defaults."""
    config = ConfigParser(interpolation=None)
    try:
        with open(path, encoding="utf-8-sig") as source:
            config.read_file(source)
        colors = [config.get("theme", key) for key in ("primary", "off_color")]
        if all(re.fullmatch(r"#[0-9a-fA-F]{6}", color) for color in colors):
            return Theme(*(color.upper() for color in colors))
    except (OSError, UnicodeError, Error):
        pass
    return Theme()
