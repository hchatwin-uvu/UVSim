UVSim — CS 2450 Milestone 2
===========================

STATUS: Starter scaffold only. File loading and instruction execution are
not implemented yet. This is not the completed milestone prototype.

PREREQUISITES
Install Python 3.10 or newer. No third-party Python packages are required.
Install Git if cloning. Obtain collaborator access to this private repository.

GET STARTED
git clone https://github.com/hchatwin-uvu/UVSim.git
cd UVSim
python --version
python main.py --help
python main.py

Use python3 instead of python if your system requires it, or py -3 on Windows.
Run all commands from the UVSim repository root.

When prompted for the BasicML file, enter:
programs/Test1.txt

You may also specify the file directly:
python main.py programs/Test1.txt

CURRENT RESULT
The scaffold reports "File loading is not implemented yet." and exits with
status 1. The team must implement the loader and simulator before programs run.

INTENDED COMPLETED BEHAVIOR
Load one signed four-digit word per line into memory starting at address 00.
Execute BasicML instructions and enter integer values when READ requests them.
WRITE prints results. HALT ends the program.
Test1 reads two values and prints their sum (7 and 5 -> 12).
Test2 reads two values and prints the larger (7 and 5 -> 7).
Run the second supplied program with:
python main.py programs/Test2.txt

TESTS
python -m unittest discover -s tests -v
No tests have been written in this starter; zero discovered tests does not
satisfy the milestone. Add two tests per approved use case and a test spreadsheet.

BEFORE SUBMISSION
Finish all 12 opcodes, loading, console interaction, and error handling.
Update this README to describe actual behavior and any prerequisites.
Include the design document (2+ user stories, 10–15 use cases), unit tests,
test spreadsheet, sprint meeting reports, and source-control contribution
evidence for all four members. See docs/milestone-2.md for the checklist.
