"""WP-3: READ input and WRITE output panel."""

import tkinter as tk
from tkinter import ttk
from collections.abc import Callable, Sequence

from operations.io_memory import format_word


class IOPanel:
    """Embeddable input/output component owned by WP-3."""

    def __init__(self, parent, on_submit: Callable[[str], bool], output_parent=None) -> None:
        """Build the READ/WRITE widgets."""
        self.on_submit = on_submit
        self._displayed_count = 0

        # Main panel
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        # READ input
        ttk.Label(
            self.frame,
            text="READ input (-9999 to 9999)"
        ).pack(anchor="w")

        input_frame = ttk.Frame(self.frame)
        input_frame.pack(fill="x", pady=(4, 12))

        self.input_text = tk.StringVar(master=parent)
        self.input_entry = ttk.Entry(input_frame, textvariable=self.input_text)
        self.input_entry.pack(side="left", fill="x", expand=True)

        self.submit_button = ttk.Button(
            input_frame,
            text="Submit input",
            command=self._submit
        )
        self.submit_button.pack(side="left", padx=(8, 0))

        # Pressing Enter does the same thing as clicking Submit.
        self.input_entry.bind("<Return>", self._submit)

        # READ starts disabled until the controller requests input.
        self.input_entry.configure(state="disabled")
        self.submit_button.configure(state="disabled")

        # WRITE output
        output_parent = self.frame if output_parent is None else output_parent
        ttk.Label(
            output_parent,
            text="Program output"
        ).pack(anchor="w")

        output_frame = ttk.Frame(output_parent)
        output_frame.pack(fill="both", expand=True, pady=(4, 12))

        self.output = tk.Text(
            output_frame,
            height=12,
            wrap="none",
            state="disabled"
        )
        self.output.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            output_frame,
            orient="vertical",
            command=self.output.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.output.configure(yscrollcommand=scrollbar.set)

    def _submit(self, event=None) -> str:
        """Send the current READ text to the controller."""
        if self.input_entry.instate(["disabled"]):
            return "break"
        raw_text = self.input_text.get()

        if self.on_submit(raw_text):
            # The callback refreshes the panel and may disable the entry.
            self.input_text.set("")
        return "break"

    def refresh(self, state: str, outputs: Sequence[int]) -> None:
        """Enable READ when waiting and display new WRITE output."""

        waiting = state == "waiting_input"
        if state == "ready":
            self.input_text.set("")

        self.input_entry.configure(
            state="normal" if waiting else "disabled"
        )
        self.submit_button.configure(
            state="normal" if waiting else "disabled"
        )

        # If output was cleared by loading a new program,
        # reset the display before adding new output.
        if len(outputs) < self._displayed_count:
            self.output.configure(state="normal")
            self.output.delete("1.0", tk.END)
            self.output.configure(state="disabled")
            self._displayed_count = 0

        # Add only outputs that have not already been displayed.
        new_outputs = outputs[self._displayed_count:]

        if new_outputs:
            self.output.configure(state="normal")

            for value in new_outputs:
                self.output.insert(tk.END, format_word(value) + "\n")

            self.output.configure(state="disabled")
            self.output.see(tk.END)

            self._displayed_count = len(outputs)

        if waiting:
            self.input_entry.focus_set()
