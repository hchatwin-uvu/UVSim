
UVSim - BasicML Simulator (Milestone 5)

INSTALLATION

Requires Python 3.10 or newer with Tcl/Tk (tkinter).
No additional pip packages are needed.

Clone the repository and verify Python:

  git clone https://github.com/hchatwin-uvu/UVSim.git
  cd UVSim
  python --version
  python -m tkinter

The last command should open a Tk demonstration window.
Close it before starting UVSim.

On Windows, enable Tcl/Tk in the Python installer if missing.
On macOS, use a Python distribution that includes Tcl/Tk.
On Linux, install the appropriate Tk package (often python3-tk).

Use python3 or py -3 instead of python where appropriate.


LAUNCH

From the repository root:

  python main.py

Optional: load a program immediately:

  python main.py programs/Test1.txt

The explicit GUI command also works:

  python main.py --gui

Legacy terminal mode is available with:

  python main.py --console

The GUI is recommended for normal operation and grading.


MILESTONE 5 OVERVIEW

Milestone 5 expands UVSim with:

- 250 memory registers (addresses 000-249).
- Signed six-digit BasicML words.
- Three-digit instruction opcodes and operands.
- Multiple program tabs with independent contents.
- Independent file paths and unsaved-change tracking.
- Execution of the currently selected program.
- Updated editor and READ input validation.

Legacy four-digit file conversion is also required for
Milestone 5 but remains pending integration verification.


CONTROLS AND WORKFLOW

1. Open File

   Browse any accessible folder and select a BasicML file.
   Cancel preserves the current session.

   Blank lines are ignored. Malformed words may load for
   correction in the editor.

   Files containing more than 250 entries are rejected
   without replacing the current program.

2. Save

   Save valid editor contents to the current file path.
   If no path exists, choose a filename and destination.

   Failed or canceled saves preserve unsaved edits.

3. Save As

   Choose a new filename or folder.
   Subsequent saves use the selected destination.

4. Run

   Execute the currently selected program from the beginning.

   Each run resets the simulator's memory, CPU state,
   pending input, and output.

   Current editor contents are used, including unsaved
   changes, after validation.

   Invalid or empty programs cannot run.

   After HALT, Stop, or an error, Run can be selected
   again without reopening the file.

5. Stop

   Stop execution or a pending READ operation.
   Stop is not a pause operation.

6. Selected Program

   The active tab identifies the program being edited.
   Each tab maintains its own source, file path, and
   unsaved-change state.

7. Status and Errors

   The status area displays loading, execution, input
   requests, completion, and error messages.

8. READ Input

   Accepts integers from -999999 through 999999.

   Examples: 7, +7, -5, 999999, -999999.

   An explicit sign or leading zeros are not required.

   READ input is enabled when the simulator requests
   a value. Submit or Enter sends the value.

   Invalid input can be corrected and submitted again.

9. Program Editor

   Displays instructions and data at addresses 000-249.
   Each program supports up to 250 entries.

   Editing is restricted during execution and READ waits.

10. Program Output

   Read-only, scrollable output from WRITE operations.

   Six magnitude digits are displayed:

     12 becomes 000012
     -5 becomes -000005

   Starting a new run clears previous output.
   HALT, Stop, and errors retain existing output.

11. Resize and Close

   The interface supports window resizing.
   Closing the application ends active execution.


PROGRAM EDITOR CONTROLS

The editor displays one BasicML instruction or data
word per row, with addresses 000 through 249.

Editor buttons:

  Add:
    Insert +000000 before the selected row, or at
    the end if no row is selected.

  Delete:
    Remove selected rows and shift remaining rows up.

  Cut:
    Copy selected rows and remove them.

  Copy:
    Copy selected rows without removing them.

  Paste:
    Insert clipboard words before the selected row,
    or at the end if no row is selected.

Editing and keyboard shortcuts:

  Double-click or F2: Edit selected word.
  Enter: Accept an edit.
  Escape: Cancel an edit.

  Ctrl+C: Copy.
  Ctrl+X: Cut.
  Ctrl+V: Paste.
  Ctrl+A: Select all.
  Delete: Delete selected rows.
  Insert: Add a row.

Words must contain a + or - sign followed by exactly
six decimal digits.

Examples:

  +010007
  +020005
  -000005
  +043000

Accepted values range from -999999 through 999999.

Invalid words are reported and must be corrected
before saving or execution.

Add and Paste operations that exceed 250 entries
are rejected without modifying the program.

The editor tracks changes since loading or saving.
Execution does not modify the editor source.


MULTIPLE PROGRAM TABS

Milestone 5 supports multiple open program tabs.

Each tab maintains its own:

- Program contents.
- File path.
- Unsaved-change state.

Users can create, open, select, and close program tabs.

Run executes the currently selected program using
the shared simulator engine.

Tab switching is restricted while a program is
executing or waiting for READ input.

Closing a tab with unsaved changes prompts the user
to Save, Discard, or Cancel.

Cancel keeps the tab open without losing changes.
Failed or canceled saves must preserve the program.


COLOR CONFIGURATION

Edit theme.ini beside main.py and restart UVSim:

  [theme]
  primary = #4C721D
  off_color = #FFFFFF

Colors use standard RGB hexadecimal values in
#RRGGBB format.

The default theme uses UVU green and white.

Missing or invalid theme settings restore the
default color configuration.

No reinstallation or compilation is required.


BASICML FILE FORMAT

Milestone 5 uses one signed six-digit word per line.

Examples:

  +010007
  -000005
  +043000

Programs may contain up to 250 words, stored at
addresses 000 through 249.

Blank lines and surrounding whitespace are ignored.
Words load consecutively beginning at address 000.

Unused memory and the accumulator initialize to zero.

Instruction words must be nonnegative.

The first three digits represent the opcode.
The final three digits represent the operand.

Supported operations:

  010 READ          011 WRITE
  020 LOAD          021 STORE
  030 ADD           031 SUBTRACT
  032 DIVIDE        033 MULTIPLY
  040 BRANCH        041 BRANCHNEG
  042 BRANCHZERO    043 HALT

Memory-address operands must be between 000 and 249.

HALT ignores its operand field.

Arithmetic uses six magnitude digits.
Overflow retains the lowest six magnitude digits
and preserves the sign.

Division truncates toward zero.

READ accepts integers from -999999 through 999999.

Division by zero, invalid instructions, and invalid
memory addresses produce errors.

Signed words may represent instructions or data,
depending on their use.


LEGACY FILE CONVERSION

Earlier milestones used signed four-digit words
and 100 memory addresses.

Milestone 5 requires support for converting legacy
four-digit files to the new six-digit format.

Examples:

  +1007 -> +010007
  +4300 -> +043000

Conversion must preserve the original source file
and allow the user to choose an output destination.

Invalid or mixed formats must be rejected.

NOTE:
The legacy converter has not yet been verified in
the current integrated working branch. This section
describes the required behavior, not a completed
implementation.


SAMPLES AND GRADING CHECKS

Sample programs are located in programs/.

Files may be opened from any accessible location.
Quote command-line paths containing spaces.

Earlier sample files may use four-digit words.
Their compatibility with Milestone 5 must be
verified before grading.

Basic Milestone 5 checks:

1. Launch the GUI with python main.py.
2. Confirm multiple program tabs are displayed.
3. Confirm editor addresses use three digits.
4. Enter +043000 and run the program.
5. Confirm the status displays "Program halted."
6. Enter an invalid word such as asdf.
7. Confirm the editor reports a validation error.

Additional conversion tests are required after
the converter is integrated.


TESTS

Run the complete automated test suite:

  python -m unittest discover -s tests -v

Run editor tests separately:

  python -m unittest tests.test_editor -v

GUI tests may create hidden Tk windows.
Tests requiring Tk may skip when no graphical
environment is available.

Local Milestone 5 integration verification:

  136 tests run
  All passed

Manual GUI checks confirmed multiple tabs,
six-digit word validation, three-digit addresses,
and successful execution of +043000.

These results were recorded before final
legacy-converter integration.

The full test suite must be rerun after all
Milestone 5 components are integrated.


MILESTONE 5 DOCUMENTATION

Milestone 5 documentation is located in:

  Milestone 5/

Important files:

  Milestone 5/README.md
  Milestone 5/milestone-5.md
  Milestone 5/class-definitions.md
  Milestone 5/use-cases.md
  Milestone 5/srs/SRS_Milestone_5.md
  Milestone 5/gui-design/README.md
  Milestone 5/verification-task4.md
  Milestone 5/meetings/coordination-log.md

These documents contain requirements, use cases,
class definitions, GUI design, verification,
and team coordination information.


MILESTONE 4 DOCUMENTATION

Milestone 4 documentation remains available as
the historical baseline.

  Milestone 4/README.md
  Milestone 4/srs/SRS_Final_Document.pdf
  Milestone 4/design.pdf
  Milestone 4/class-definitions.pdf
  Milestone 4/UVSim-Milestone-4-Unit-Tests.xlsx
  Milestone 4/verification.md

Earlier milestone documents remain unchanged.


SUBMISSION STATUS

The Milestone 5 GUI and expanded backend have
been integrated and tested locally.

The class definitions and diagram have been
updated to reflect the current GUI architecture.

Legacy conversion remains pending integration
and verification.

Final documentation review, regression testing,
and team submission checks remain.
