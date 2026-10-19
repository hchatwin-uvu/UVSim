# UVSim

UVSim is a Tkinter GUI for executing BasicML programs. Requires Python 3.10+
with Tcl/Tk; no third-party Python packages are needed.

```sh
python main.py
```

See [README.txt](README.txt) for installation, every GUI control, file format,
error recovery, sample outputs, and test instructions.

- [Milestone 3 deliverables](Milestone%203/submission-checklist.md)
- [Class definitions](Milestone%203/class-definitions.md)
- [GUI design](Milestone%203/gui-design/README.md)
- [Verification](Milestone%203/verification.md)

Run tests with `python -m unittest discover -s tests -v`.

## Milestone 4 WP-1

The interface starts with UVU green (`#4C721D`) and white (`#FFFFFF`). Edit
[theme.ini](theme.ini) and restart to change both colors. Missing or invalid
configuration restores UVU defaults. Run again after HALT, Stop, or an error
without reopening the file.

- [Current GUI design](Milestone%204/gui-design/README.md)
- [WP-1 verification and pending integration](Milestone%204/verification.md)
- [Milestone 4 plan](Milestone%204/milestone-4.md)
