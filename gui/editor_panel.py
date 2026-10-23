"""Milestone 4 WP-2: editable BasicML program panel (no file I/O or execution)."""
import tkinter as tk
from tkinter import ttk
from collections.abc import Callable, Sequence
from word import Word

MAX_ENTRIES = 100


class EditorPanel:
    """Display and edit up to 100 BasicML words, at addresses 00-99."""

    def __init__(self, parent, on_change: Callable[[], None]) -> None:
        self.on_change = on_change
        self._entries = []
        self._saved_entries = []
        self._enabled = True
        self._clipboard = ""
        self._edit_widget = None
        self._edit_index = None

        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True)
        ttk.Label(self.frame, text="Program editor (addresses 00-99)").pack(anchor="w")
        toolbar = ttk.Frame(self.frame)
        toolbar.pack(fill="x", pady=5)
        self.add_button = ttk.Button(toolbar, text="Add", command=self.add_entry)
        self.delete_button = ttk.Button(toolbar, text="Delete", command=self.delete_selected)
        self.cut_button = ttk.Button(toolbar, text="Cut", command=self.cut)
        self.copy_button = ttk.Button(toolbar, text="Copy", command=self.copy)
        self.paste_button = ttk.Button(toolbar, text="Paste", command=self.paste)
        for button in (self.add_button, self.delete_button, self.cut_button,
                       self.copy_button, self.paste_button):
            button.pack(side="left", padx=(0, 4))

        table = ttk.Frame(self.frame)
        table.pack(fill="both", expand=True)
        self.tree = ttk.Treeview(table, columns=("address", "word"),
                                 show="headings", selectmode="extended", height=12)
        self.tree.heading("address", text="Address")
        self.tree.heading("word", text="Instruction / data")
        self.tree.column("address", width=75, minwidth=65, stretch=False)
        self.tree.column("word", width=175, minwidth=110, stretch=True)
        self.tree.tag_configure("invalid", foreground="#B00020")
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(table, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.status = tk.StringVar(master=self.frame,
                                   value="Double-click a word to edit it.")
        ttk.Label(self.frame, textvariable=self.status, wraplength=450).pack(
            fill="x", pady=(6, 0))

        self.tree.bind("<Double-1>", self._on_double_click)
        self.tree.bind("<F2>", self._on_edit_key)
        self.tree.bind("<Return>", self._on_edit_key)
        self.tree.bind("<Control-c>", lambda e: self._key(self.copy))
        self.tree.bind("<Control-x>", lambda e: self._key(self.cut))
        self.tree.bind("<Control-v>", lambda e: self._key(self.paste))
        self.tree.bind("<Control-a>", self._select_all)
        self.tree.bind("<Delete>", lambda e: self._key(self.delete_selected))
        self.tree.bind("<Insert>", lambda e: self._key(self.add_entry))
        self._update_buttons()

    def set_words(self, words: Sequence[Word]) -> None:
        """Replace editor content, clear unsaved flag, and renumber addresses."""
        words = list(words)
        if len(words) > MAX_ENTRIES:
            raise ValueError("Program cannot exceed 100 entries (00-99).")
        if any(not isinstance(w, Word) for w in words):
            raise TypeError("set_words expects Word objects.")
        self.set_entries([w.format() for w in words])

    def set_entries(self, entries: Sequence[str]) -> None:
        """Load editable source, including invalid words, without marking dirty.

        Validation uses editor row numbers after blank file lines are ignored.
        Run and Save continue to validate through get_words().
        """
        entries = list(entries)
        if len(entries) > MAX_ENTRIES:
            raise ValueError("Program cannot exceed 100 entries (00-99).")
        if any(not isinstance(entry, str) for entry in entries):
            raise TypeError("set_entries expects strings.")
        self._cancel_edit()
        self._entries = entries.copy()
        self._saved_entries = self._entries.copy()
        self._refresh_tree([])
        self.status.set("Program loaded. Double-click a word to edit it.")
        for index, entry in enumerate(entries):
            try:
                Word.parse(entry)
            except ValueError as error:
                self.status.set(f"Address {index:02d} (line {index+1}): {error}")
                break

    def get_words(self) -> list[Word]:
        """Return current words; report the first invalid address and line."""
        self._finish_edit()
        result = []
        for i, text in enumerate(self._entries):
            try:
                result.append(Word.parse(text))
            except ValueError as error:
                raise ValueError(f"Invalid entry at address {i:02d} "
                                 f"(line {i+1}): {error}") from error
        return result

    @property
    def is_dirty(self) -> bool:
        self._finish_edit()
        return self._entries != self._saved_entries

    def mark_saved(self) -> None:
        self._finish_edit()
        self._saved_entries = self._entries.copy()

    def set_enabled(self, enabled: bool) -> None:
        if not enabled:
            self._finish_edit()
        self._enabled = bool(enabled)
        self._update_buttons()

    def add_entry(self) -> None:
        if not self._enabled:
            return
        if len(self._entries) >= MAX_ENTRIES:
            self.status.set("Cannot add: program already has 100 entries.")
            return
        selected = self._selected_indices()
        index = selected[0] if selected else len(self._entries)
        self._entries.insert(index, "+0000")
        self._changed([index])

    def delete_selected(self) -> None:
        if not self._enabled:
            return
        selected = self._selected_indices()
        if not selected:
            self.status.set("Select one or more entries to delete.")
            return
        for i in reversed(selected):
            del self._entries[i]
        self._changed([min(selected[0], len(self._entries) - 1)])

    def cut(self) -> None:
        if self._enabled and self._selected_indices():
            self.copy()
            self.delete_selected()

    def copy(self) -> None:
        selected = self._selected_indices()
        if not selected:
            self.status.set("Select one or more entries to copy.")
            return
        self._clipboard = "\n".join(self._entries[i] for i in selected)
        try:
            self.frame.clipboard_clear()
            self.frame.clipboard_append(self._clipboard)
        except tk.TclError:
            pass
        self.status.set(f"Copied {len(selected)} entries.")

    def paste(self) -> None:
        if not self._enabled:
            return
        try:
            content = self.frame.clipboard_get()
        except tk.TclError:
            content = self._clipboard
        if not content.strip():
            self.status.set("Clipboard is empty.")
            return
        lines = [line.strip() for line in content.splitlines()]
        if len(self._entries) + len(lines) > MAX_ENTRIES:
            self.status.set("Cannot paste: result would exceed 100 entries (00-99).")
            return
        for n, line in enumerate(lines, 1):
            try:
                Word.parse(line)
            except ValueError as error:
                self.status.set(f"Cannot paste: clipboard line {n}: {error}")
                return
        selected = self._selected_indices()
        index = selected[0] if selected else len(self._entries)
        self._entries[index:index] = lines
        self._changed(list(range(index, index + len(lines))))

    def modify_entry(self, index: int, text: str) -> None:
        """Update one word; highlight invalid text until the user fixes it."""
        if not self._enabled:
            return
        if not 0 <= index < len(self._entries):
            raise IndexError(f"No entry at address {index}.")
        if text.strip() != self._entries[index]:
            self._entries[index] = text.strip()
            self._changed([index])

    def _selected_indices(self) -> list[int]:
        return sorted(int(item) for item in self.tree.selection())

    def _changed(self, selected=None) -> None:
        self._refresh_tree(selected)
        self._report_validation()
        self.on_change()

    def _refresh_tree(self, selected=None) -> None:
        if selected is None:
            selected = self._selected_indices()
        children = self.tree.get_children()
        if children:
            self.tree.delete(*children)
        for i, text in enumerate(self._entries):
            try:
                Word.parse(text)
                tags = ()
            except ValueError:
                tags = ("invalid",)
            self.tree.insert("", "end", iid=str(i),
                             values=(f"{i:02d}", text), tags=tags)
        kept = [str(i) for i in selected if 0 <= i < len(self._entries)]
        if kept:
            self.tree.selection_set(kept)
            self.tree.focus(kept[0])
            self.tree.see(kept[0])
        self._update_buttons()

    def _report_validation(self) -> None:
        for i, text in enumerate(self._entries):
            try:
                Word.parse(text)
            except ValueError as error:
                self.status.set(f"Address {i:02d} (line {i+1}): {error}")
                return
        self.status.set(f"{len(self._entries)}/100 entries. Unsaved edits.")

    def _update_buttons(self) -> None:
        state = "normal" if self._enabled else "disabled"
        for button in (self.add_button, self.delete_button,
                       self.cut_button, self.paste_button):
            button.configure(state=state)
        self.copy_button.configure(state="normal")

    def _on_double_click(self, event) -> None:
        if not self._enabled or self.tree.identify_region(event.x, event.y) != "cell":
            return
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self._begin_edit(int(item))

    def _on_edit_key(self, event=None) -> str:
        selected = self._selected_indices()
        if self._enabled and selected:
            self._begin_edit(selected[0])
        return "break"

    def _begin_edit(self, index: int) -> None:
        self._finish_edit()
        item = str(index)
        self.tree.see(item)
        self.tree.update_idletasks()
        bounds = self.tree.bbox(item, "#2")
        if not bounds:
            return
        x, y, width, height = bounds
        self._edit_index = index
        self._edit_widget = ttk.Entry(self.tree)
        self._edit_widget.insert(0, self._entries[index])
        self._edit_widget.place(x=x, y=y, width=width, height=height)
        self._edit_widget.focus_set()
        self._edit_widget.select_range(0, "end")
        self._edit_widget.bind("<Return>", self._commit_edit_key)
        self._edit_widget.bind("<Escape>", self._cancel_edit_key)
        self._edit_widget.bind("<FocusOut>", lambda e: self._finish_edit())

    def _finish_edit(self) -> None:
        if self._edit_widget is None:
            return
        widget, index = self._edit_widget, self._edit_index
        value = widget.get()
        self._edit_widget = None
        self._edit_index = None
        widget.destroy()
        if self._enabled and index is not None:
            self.modify_entry(index, value)

    def _cancel_edit(self) -> None:
        if self._edit_widget is not None:
            widget = self._edit_widget
            self._edit_widget = None
            self._edit_index = None
            widget.destroy()

    def _commit_edit_key(self, event=None) -> str:
        self._finish_edit()
        self.tree.focus_set()
        return "break"

    def _cancel_edit_key(self, event=None) -> str:
        self._cancel_edit()
        self.tree.focus_set()
        return "break"

    def _key(self, action) -> str:
        action()
        return "break"

    def _select_all(self, event=None) -> str:
        self.tree.selection_set(self.tree.get_children())
        return "break"
