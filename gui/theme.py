"""Apply configurable branding to ttk and classic text widgets."""
import tkinter as tk
from tkinter import ttk
from theme_config import Theme


def apply_theme(root, theme: Theme) -> None:
    """Style the assembled tree. Reapply after adding classic Tk text widgets.

    Clam allows custom button colors on Windows. New ttk widgets inherit styles.
    """
    style = ttk.Style(root)
    style.theme_use("clam")
    primary, paper = theme.primary, theme.off_color
    ink = "#182113"
    root.configure(background=paper)
    style.configure(".", background=paper, foreground=ink, font=("Segoe UI", 10))
    style.configure("TFrame", background=paper)
    style.configure("TLabel", background=paper, foreground=ink)
    style.configure("Brand.TFrame", background=primary)
    style.configure("Brand.TLabel", background=primary, foreground=paper)
    style.configure("TButton", background=primary, foreground=paper,
                    padding=(14, 8), borderwidth=0)
    style.map("TButton", background=[("disabled", paper), ("active", primary)],
              foreground=[("disabled", "#595959"), ("active", paper)])
    style.configure("TEntry", fieldbackground=paper, foreground=ink, padding=6)
    style.configure("TSeparator", background=primary)
    style.configure("Treeview", background=paper, fieldbackground=paper, foreground=ink)
    style.map("Treeview", background=[("selected", primary)], foreground=[("selected", paper)])

    def visit(widget):
        if isinstance(widget, tk.Text):
            widget.configure(background=paper, foreground=ink, insertbackground=ink,
                             selectbackground=primary, selectforeground=paper,
                             highlightbackground=primary, highlightcolor=primary,
                             highlightthickness=1, relief="flat", padx=12, pady=10)
        for child in widget.winfo_children():
            visit(child)
    visit(root)
