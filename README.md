# UVSim

UVSim is a Tkinter GUI for executing BasicML programs. Requires Python 3.10+
with Tcl/Tk; no third-party Python packages are needed.

```sh
python main.py
```

See [README.txt](README.txt) for installation, every GUI control, file format,
error recovery, sample outputs, and test instructions.

- [Milestone 3 deliverables](Milestone%203/submission-checklist.md)
- [Current class definitions](Milestone%204/class-definitions.md)
- [Current GUI design](Milestone%204/gui-design/README.md)
- [Current verification](Milestone%204/verification.md)

Run tests with `python -m unittest discover -s tests -v`.

## Milestone 4

The interface starts with UVU green (`#4C721D`) and white (`#FFFFFF`). Edit
[theme.ini](theme.ini) and restart to change both colors. Missing or invalid
configuration restores UVU defaults. Run again after HALT, Stop, or an error
without reopening the file.

- [Current GUI design](Milestone%204/gui-design/README.md)
- [Integrated verification](Milestone%204/verification.md)
- [Milestone 4 deliverables](Milestone%204/README.md)
- [Milestone 4 plan and implementation history](Milestone%204/milestone-4.md)

The program editor is now integrated beside output. Run uses current editor
contents, including unsaved changes, and locks editing until execution stops.
Open/Close offer Save, Discard, or Cancel. Save/Save As are connected, and
malformed words load for correction before execution or saving.
