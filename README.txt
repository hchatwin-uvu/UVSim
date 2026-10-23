UVSim - Milestone 4 (WP-1 and WP-2 program documentation)

INSTALLATION
Requires Python 3.10 or newer with Tcl/Tk (tkinter). No pip packages are needed.
Obtain access to the repository, then run:
  git clone https://github.com/hchatwin-uvu/UVSim.git
  cd UVSim
  python --version
  python -m tkinter
The last command should open a Tk demonstration window; close it before starting
UVSim. On Windows, enable Tcl/Tk in the Python installer if it is missing. On
macOS, use a Python distribution that includes Tcl/Tk. On Linux, install your
Python distribution's Tk package (commonly python3-tk) and use a graphical desktop.
Use python3 or py -3 instead of python where appropriate.

LAUNCH
From the repository root:
  python main.py
Optional: load a program immediately:
  python main.py programs/Test1.txt
The explicit python main.py --gui form also works. A desktop display is required.
A legacy terminal mode remains available with --console for compatibility; use
the default GUI for grading and normal operation.

CONTROLS AND WORKFLOW
1. Open file: browse any accessible folder and select a BasicML text file.
   Cancel preserves the session. A failed load preserves the previous program.
   Malformed words load for correction. Blank lines are ignored; validation line
   numbers refer to editor rows. Files over 100 entries are rejected intact.
2. Save: write valid editor contents to the current path. Without a path,
   choose a name and folder. Failed saves preserve edits and the existing file.
3. Save As: choose a new name/folder; subsequent Save uses that destination.
4. Run: execute the loaded program from the beginning. After HALT, Stop, or an
   error, click Run again without reopening the file. Each run resets memory,
   CPU state, pending input, and output using current editor contents.
   Unsaved edits run too; invalid or empty programs show an error without running.
   Open file and Run are disabled while running or waiting for READ input.
5. Stop: abandon execution or a pending READ; retain output. This is not pause.
6. Selected File Name: displays the last successfully loaded path.
7. Status/error area: above READ and output; shows loading, execution, input
   requests, completion, and errors. Correct invalid READ input and retry.
8. READ input (-9999 to 9999): enabled only when input is requested. Enter an
   integer such as 7, +7, or -5; four digits and an explicit sign are not required.
   Submit input or Enter sends it once. Accepted input clears; invalid input
   remains available for correction without losing prior execution state.
9. Program editor (left): edit instructions/data using the controls below.
   Editing is disabled during execution and READ waits; Copy stays available.
10. Program output (right): read-only scrollable WRITE results. Four magnitude digits
   are shown: 12 becomes 0012 and -5 becomes -0005. HALT, Stop, and errors retain
   output; starting a fresh run clears it. Opening another source retains prior
   results until Run starts its new execution.
11. Resize/close: controls expand with the window. Closing cancels execution.

COLOR CONFIGURATION
Edit theme.ini beside main.py, save the file, and restart UVSim:
  [theme]
  primary = #4C721D
  off_color = #FFFFFF
Both colors must use # followed by six hexadecimal digits (0-9, A-F).
Primary colors the header, buttons, separators, and selections; off_color colors
surfaces and button/header text. Body text stays dark. These defaults are the
supplied UVU green and white. No reinstall or compilation is needed.
The file is located beside the application even when launched from another
working directory. Missing/unreadable files, malformed INI, missing keys, or
invalid colors restore the entire UVU default palette without crashing.
Native file dialogs keep operating-system styling. Custom contrast is the
user's choice. Open, Save, Save As, and Run are disabled during execution.

PROGRAM EDITOR (MILESTONE 4 WP-2)
The program editor displays one BasicML instruction or data value per row, with
its address in the range 00-99. The editor supports up to 100 entries. The
editor is integrated beside output below the shared READ input controls.

Editor buttons:
  Add: Insert +0000 before the first selected row, or at the end if no row is
       selected. Following entries shift down and addresses are renumbered.
  Delete: Remove the selected row(s). Remaining rows shift up.
  Cut: Copy selected row(s) to the clipboard and delete them.
  Copy: Copy selected row(s) without deleting them.
  Paste: Insert clipboard words before the first selected row, or at the end
         when no row is selected. Multiple lines can be pasted together.

Editing and keyboard shortcuts (with focus on the editor):
  Double-click a word, or select a row and press F2 or Enter, to edit it.
  Press Enter to accept an edit, or Escape to cancel it.
  Ctrl+C: Copy selected rows.
  Ctrl+X: Cut selected rows.
  Ctrl+V: Paste clipboard rows.
  Ctrl+A: Select all rows.
  Delete: Delete selected rows.
  Insert: Add a new row.

Words must contain a + or - sign followed by exactly four digits, for example
+1007, +2005, -0005, or +4300. Values must be within -9999 through 9999.
Invalid words are highlighted and the editor reports the affected address and
line. Invalid entries must be corrected before the editor's program can be
accepted for saving or execution.

If an Add or Paste operation would exceed 100 entries, the operation is rejected
without changing the program. Invalid clipboard words are also rejected without
changing the program. Cut, Copy, Paste, and Delete support multiple selections.

The editor tracks changes since loading or saving. Open and Close offer Yes
(Save), No (Discard), and Cancel (Keep editing). Canceling or failing a requested
save prevents Open/Close from proceeding. Canceling the
file picker or failing to load a file preserves edits without discarding them.
While a program is running or waiting for READ input, modifying the editor is
disabled; Copy remains available. Run validates the current editor words and
starts fresh without reopening the file. Execution never changes editor source.
You may also build a program with Add before opening any file.

BASICML FILE FORMAT
One signed four-digit word per line, e.g. +1007, -0005, +4300. Maximum 100 words.
Blank lines and surrounding whitespace are ignored. Words load consecutively
starting at address 00. Unused memory and the accumulator reset to zero.
Instruction words must be nonnegative; the opcode is the first two digits and
the operand is an address from 00 to 99. Supported operations:
  10 READ   11 WRITE   20 LOAD   21 STORE
  30 ADD    31 SUBTRACT   32 DIVIDE   33 MULTIPLY
  40 BRANCH   41 BRANCHNEG   42 BRANCHZERO   43 HALT
Arithmetic overflow retains the lowest four magnitude digits and the sign:
12345 becomes 2345; -12345 becomes -2345. Division truncates toward zero.
Division by zero and invalid instructions produce a GUI error. READ rejects
values outside -9999 to 9999. No register display or step mode is provided.

SAMPLES AND GRADING CHECKS
Included programs are in programs/, but files may be opened from any accessible
location. Relative command-line paths use the current directory; quote paths
containing spaces. Use Open file for selection without typing a path.
  Test1.txt: enter 7, then 5; output 0012.
  Test2.txt: enter 7, then 5 (or 5, then 7); output 0007.
  Test3.txt: 3333, 0003, 3332, 1666, 0666, -0334.
  Test3b.txt: 3333, 0003, 1332, 0666, -0334, -1334.
  Test4.txt: 1111, 2222, 3333, 4444, 5555.
  Test5.txt: opens for correction; Run and Save reject its invalid entries.
  Correct the highlighted entries before running or saving.
For input recovery, try abc or 10000 at READ, then correct the value.

TESTS
  python -m unittest discover -s tests -v
To run the WP-2 editor tests separately:
  python -m unittest tests.test_editor -v
GUI tests create hidden real Tk windows. They skip only if Tk cannot initialize;
skips mean GUI behavior was not verified on that machine. See tests/README.md
and Milestone 4/verification.md for coverage and recorded results.

SUBMISSION CONTENTS
See Milestone 4/milestone-4.md for the team plan and outstanding integration.
Milestone 4/gui-design/README.md describes the implemented WP-1 interface.
Save integration is complete. Final team document audit and submission review remain.

MILESTONE 4 DOCUMENTATION
Current submission index: Milestone 4/README.md
Final SRS: Milestone 4/srs/SRS_Final_Document.pdf
Use cases/design: Milestone 4/design.pdf
Class definitions/diagram: Milestone 4/class-definitions.pdf
Test register: Milestone 4/UVSim-Milestone-4-Unit-Tests.xlsx
Verification and remaining manual acceptance: Milestone 4/verification.md
Earlier milestone folders are historical records.
