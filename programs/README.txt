UVSim sample program checks
==========================

Run these commands from the repository root with Python 3.10 or newer.
Use python3 or py -3 instead of python if required by your system.
These programs require the implemented UVSim.step/run execution loop.

MULTIPLY (opcode 33)
python main.py programs/Multiply.txt
Enter 7, then 5, pressing Enter after each: expected output 00035.
Run again with -7 and 5: expected output -0035.
Run again with 7 and 0: expected output 00000.
Run again with 9999 and 2: expected arithmetic range error and exit status 1.

DIVIDE (opcode 32)
python main.py programs/Divide.txt
Enter 12, then 3: expected output 00004.
Run again with 7 and 3: expected output 00002.
Run again with -7 and 3: expected output -0002 (truncation toward zero).
Run again with 7 and 0: expected division-by-zero error and exit status 1.

BRANCH (opcode 40)
python main.py programs/Branch.txt
No input is required. Expected output: one line containing 01234.
The branch jumps from address 00 to 02, skipping a WRITE of unused memory.
An extra 00000 line means the instruction was not skipped correctly.

BRANCHZERO (opcode 42)
python main.py programs/BranchZero.txt
Enter 0: expected output 00001, indicating the zero branch was taken.
Run again with 7: expected output -0001, indicating it was not taken.
Run again with -7: expected output -0001.
Each run should print exactly one result and halt.

EXISTING SUPPLIED PROGRAMS
python main.py programs/Test1.txt
Enter 7, then 5: expected output 00012 (addition).

python main.py programs/Test2.txt
Enter 7, then 5: expected output 00007.
Run again with 5 and 7: expected output 00007 (negative branch taken).
Run again with 7 and 7: expected output 00007.
Test2 uses subtraction to compare the numbers and prints the larger input.

OPCODE COVERAGE
Test1: READ 10, WRITE 11, LOAD 20, STORE 21, ADD 30, HALT 43.
Test2: READ 10, WRITE 11, LOAD 20, SUBTRACT 31, BRANCHNEG 41, HALT 43.
Multiply: READ 10, WRITE 11, LOAD 20, STORE 21, MULTIPLY 33, HALT 43.
Divide: READ 10, WRITE 11, LOAD 20, STORE 21, DIVIDE 32, HALT 43.
Branch: BRANCH 40, WRITE 11, HALT 43.
BranchZero: READ 10, LOAD 20, BRANCHZERO 42, WRITE 11, BRANCH 40, HALT 43.
Together these programs exercise all 12 BasicML opcodes. They are manual
program checks, separate from the automated unit tests in tests/.
