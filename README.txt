UVSim - Milestone 3

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
the default GUI for Milestone 3 grading and normal operation.

CONTROLS AND WORKFLOW
1. Open file: opens the native file picker. Navigate to any accessible folder,
   select a BasicML text file, then choose Open. Text files and All files filters
   are available. Cancel preserves the existing session. Loading does not run it.
2. Selected filename: shows the last successfully loaded path. Failed loading
   leaves the previous filename, program, and output intact.
3. Run: enabled after successful loading. Starts executing the loaded program.
   Open file and Run are disabled during execution or while awaiting READ input.
4. READ input (-9999 to 9999): enabled only when the program requests input.
   Enter an integer such as 7, +7, or -5; an explicit sign or four digits is not
   required for interactive input.
5. Submit input / Enter: submits the value once. Accepted input clears and the
   program continues. Invalid input stays visible; correct it and submit again.
6. Program output: read-only, scrollable WRITE results in execution order.
   Four magnitude digits are shown: 12 becomes 0012 and -5 becomes -0005.
   Output remains after HALT, Stop, or an execution error. A successful new load
   clears it. Use the vertical scrollbar to review earlier results.
7. Stop: abandons a running program or pending READ and retains output. Reload a
   file to begin another run; Stop does not provide pause/resume.
8. Status/error area: shows loading, running, input requests, completion, Stop,
   and error messages. File errors allow another selection. READ errors allow
   correction without losing earlier inputs. Runtime errors stop execution;
   open a valid program to recover without restarting the application.
9. Window resize/close: resize normally; controls expand with the window. Close
   using the title-bar close control. Closing cancels scheduled execution.

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
values outside -9999 to 9999. No editor, register display, or step mode is provided.

SAMPLES AND GRADING CHECKS
Included programs are in programs/, but files may be opened from any accessible
location. Relative command-line paths use the current directory; quote paths
containing spaces. Use Open file for selection without typing a path.
  Test1.txt: enter 7, then 5; output 0012.
  Test2.txt: enter 7, then 5 (or 5, then 7); output 0007.
  Test3.txt: 3333, 0003, 3332, 1666, 0666, -0334.
  Test3b.txt: 3333, 0003, 1332, 0666, -0334, -1334.
  Test4.txt: 1111, 2222, 3333, 4444, 5555.
  Test5.txt: deliberately malformed; expect a load error. Select Test1 afterward.
For input recovery, try abc or 10000 at READ, then correct the value.

TESTS
  python -m unittest discover -s tests -v
GUI tests create hidden real Tk windows. They skip only if Tk cannot initialize;
skips mean GUI behavior was not verified on that machine. See tests/README.md
and Milestone 3/verification.md for coverage and recorded results.

SUBMISSION CONTENTS
See Milestone 3/submission-checklist.md for the deliverable index. Include source,
program samples, tests, revised Milestone 2 documents, the annotated GUI design,
class definitions, all seven SRS documents, this README.txt, and sprint reports.
