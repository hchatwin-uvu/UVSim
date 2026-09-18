UVSim — CS 2450 Milestone 2
===========================

UVSim is a command-line simulator for BasicML programs. It supports all 12
BasicML operations using a 100-word memory and a separate accumulator.

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

PROGRAM FORMAT
Use a text file with one signed four-digit decimal word per line, such as
+1007, -0005, or +4300. Files may contain at most 100 words. Blank lines and
surrounding whitespace are ignored. Words load in order starting at address
00, and unused memory is initialized to zero.

Instruction words must be positive. The first two digits identify the
operation; the last two digits specify a memory address from 00 through 99.
Data words may be positive or negative, from -9999 through 9999.

Supported operations:
10 READ       11 WRITE
20 LOAD       21 STORE
30 ADD        31 SUBTRACT    32 DIVIDE    33 MULTIPLY
40 BRANCH     41 BRANCHNEG  42 BRANCHZERO 43 HALT

RUNNING A PROGRAM
When READ displays "Enter a word (-9999 to 9999):", type an integer and press
Enter. Ordinary integers such as 7 and -5 are accepted; keyboard input does
not require an explicit plus sign or four digits.

WRITE prints the value using a five-character, zero-padded format. For
example, 12 prints as 00012 and -5 prints as -0005. HALT ends execution.

Test1 reads two values and prints their sum. Enter 7 and then 5 at the two
prompts; the expected output is 00012.

Test2 reads two values and prints the larger. Enter 7 and then 5; the expected
output is 00007. Entering 5 and then 7 should also produce 00007.
Run the second supplied program with:
python main.py programs/Test2.txt

ERRORS AND EXITING
File errors, invalid input, invalid instructions, division by zero,
arithmetic overflow, and execution outside memory stop the program with
an error message and exit status 1. Successful execution exits with status 0.
After an error, run the command again to restart the program.

Arithmetic results must remain between -9999 and 9999. Division truncates
toward zero: -7 divided by 3 produces -2.

Press Ctrl+C to interrupt execution, including a program in an infinite loop.
There is no automatic instruction limit; interruption may display a Python
KeyboardInterrupt traceback.

TEST THE PROTOTYPE
Open a terminal in the UVSim repository folder. Run each command below
separately and wait for the program's prompts before entering values.

1. Run the addition program:
   python main.py programs/Test1.txt

   Enter 7 and press Enter.
   Enter 5 and press Enter.
   Expected output: 00012

2. Run the larger-number program:
   python main.py programs/Test2.txt

   Enter 7 and press Enter.
   Enter 5 and press Enter.
   Expected output: 00007

   Run the same command again with 5 followed by 7.
   Expected output: 00007

3. Test the filename prompt:
   python main.py

   At "BasicML program file:", enter programs/Test1.txt and press Enter.
   Enter 7, then 5, at the two word prompts, pressing Enter after each.
   Expected output: 00012

4. Run the existing automated tests:
   python -m unittest discover -s tests -v

   Expected result: 33 tests run, ending with OK.

If python is unavailable, use python3 or, on Windows, py -3 in these commands.

The current suite contains 33 tests covering loading, arithmetic, and
control-flow handlers. A successful run ends with OK. Dedicated I/O/memory
and execution-loop unit tests are not currently included.

The two supplied programs do not exercise every opcode. Additional checks
are needed for operations such as DIVIDE, MULTIPLY, BRANCH, and BRANCHZERO.

BEFORE SUBMISSION
Verify the prototype from a fresh clone using these instructions, and check
test coverage against the requirement for two tests per use case.
Include the design document (2+ user stories, 10–15 use cases), unit tests,
test spreadsheet, sprint meeting reports, and source-control contribution
evidence for all four members. See docs/milestone-2.md for the checklist.
