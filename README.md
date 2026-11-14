# UVSim

UVSim is a Tkinter GUI for executing BasicML programs. Requires Python 3.10+
with Tcl/Tk; no third-party Python packages are needed.

```sh
python main.py
```

See [README.txt](README.txt) for installation, every GUI control, file format,
error recovery, sample outputs, and test instructions.

- [Milestone 5 deliverables](Milestone%205/README.md)
- [Current class definitions](Milestone%205/class-definitions.md)
- [Current GUI design](Milestone%205/gui-design/README.md)
- [Current verification](Milestone%205/verification-task4.md)

Run tests with `python -m unittest discover -s tests -v`.

## Milestone 4

The interface starts with green (`#4C721D`) and white (`#FFFFFF`). Edit
[theme.ini](theme.ini) and restart to change both colors using standard RGB hexadecimal values (`#RRGGBB`). Missing or invalid
configuration restores the default green-and-white colors. Run again after HALT, Stop, or an error
without reopening the file.

- [Current GUI design](Milestone%205/gui-design/README.md)
- [Integrated verification](Milestone%205/verification-task4.md)
- [Milestone 4 deliverables](Milestone%204/README.md)
- [Milestone 4 plan and implementation history](Milestone%204/milestone-4.md)

The program editor is now integrated beside output. Run uses current editor
contents, including unsaved changes, and locks editing until execution stops.
Open adds a tab; closing modified tabs offers Save, Discard, or Cancel. Save/Save As are connected, and
malformed words load for correction before execution or saving.

## Milestone 5 conversion

Click **Convert legacy file** to select a saved four-digit program and save a
six-digit copy. The result opens in a new tab. Cancellation and errors preserve
your open documents; the source and files open in other tabs cannot be
overwritten. Conversion uses the file on disk, not unsaved editor edits.

The assignment treats any legacy word starting with a valid opcode as an
instruction. For example, `+1111` becomes `+011011`; numeric `+5555` becomes
`+005555`. This means some older sample data produce different outputs after
conversion. See README.txt for details.

Run conversion integration tests with
`python -m unittest tests.test_conversion_ui -v`.
