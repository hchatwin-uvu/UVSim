"""Configuration behavior and real-widget branding checks."""
from pathlib import Path
from tempfile import TemporaryDirectory
import tkinter as tk
from tkinter import ttk
import unittest
from theme_config import Theme, load_theme, THEME_FILE
from gui.theme import apply_theme

class ThemeTests(unittest.TestCase):
    def test_configuration_cases(self):
        cases = [
            ("[theme]\nprimary=#123abc\noff_color=#eeeeee", Theme("#123ABC", "#EEEEEE")),
            ("[theme]\nprimary=green\noff_color=#FFFFFF", Theme()),
            ("[theme]\nprimary=#123456", Theme()),
            ("not an ini file", Theme()),
            ("[theme]\nprimary=#123456\nprimary=#654321", Theme()),
            ("[theme]\nprimary=#12345G\noff_color=#FFFFFF", Theme()),
        ]
        with TemporaryDirectory() as folder:
            path = Path(folder) / "theme.ini"
            self.assertEqual(load_theme(path), Theme())
            self.assertEqual(load_theme(folder), Theme())
            for text, expected in cases:
                with self.subTest(text=text):
                    path.write_text(text, encoding="utf-8")
                    self.assertEqual(load_theme(path), expected)
            path.write_bytes(b"\xff\xfe\xfa")
            self.assertEqual(load_theme(path), Theme())

    def test_default_path_is_beside_module(self):
        self.assertTrue(THEME_FILE.is_absolute())
        self.assertEqual(THEME_FILE.parent, Path(__file__).resolve().parents[1])
        self.assertEqual(load_theme(), Theme())

    def test_custom_palette_reaches_real_widgets(self):
        try:
            root = tk.Tk()
        except tk.TclError as error:
            self.skipTest(str(error))
        self.addCleanup(root.destroy)
        root.withdraw()
        panel = ttk.Frame(root)
        output = tk.Text(panel)
        palette = Theme("#123456", "#F0F0F0")
        apply_theme(root, palette)
        style = ttk.Style(root)
        self.assertEqual(style.lookup("TButton", "background"), palette.primary)
        self.assertEqual(style.lookup("Brand.TLabel", "foreground"), palette.off_color)
        self.assertEqual(output.cget("background"), palette.off_color)
        self.assertEqual(output.cget("selectbackground"), palette.primary)
