# UVSim
UVSim BasicML virtual machine simulator for CS 2450.

## Status
Milestone 2 starter scaffold. The simulator, loader, and opcode handlers are intentionally unimplemented so every teammate can contribute code. This is not the working prototype submission.

## Setup and use
Install Python 3.10 or newer (a project baseline) and Git to clone the repository. No third-party Python packages are required.

```text
git clone https://github.com/hchatwin-uvu/UVSim.git
cd UVSim
python --version
python main.py --help
python main.py
```

Use `python3` on systems where that is the Python 3 command, or `py -3` on Windows. Run commands from the repository root. The private repository requires collaborator access.

The CLI asks for a BasicML filename; enter `programs/Test1.txt` or pass it directly with `python main.py programs/Test1.txt`. **Currently this reports that loading is not implemented and exits with status 1.** After the team implements the prototype, it must load the file at memory address 00, execute it, and use the console for READ/WRITE. Test1 reads two values and prints their sum; Test2 prints the larger value. Example future checks: inputs 7 and 5 produce 12 for Test1 and 7 for Test2.

The supplied files contain one signed four-digit word per line. Input formatting, division rounding, overflow handling, and failure behavior still need team decisions; see docs/design.md.

## Structure
- `main.py`: CLI prompt, orchestration, and user-facing errors.
- `loader.py`: file parsing and word validation contract.
- `uvsim.py`: machine state and load/step/run contracts.
- `operations/`: separate arithmetic, I/O/memory, and control-flow work areas.
- `tests/`: unit tests grouped by implementation area (to be written).
- `programs/Test1.txt`, `programs/Test2.txt`: unchanged instructor-provided programs.
- `docs/design.md`: draft user stories, use-case map, and interface decisions.
- `docs/milestone-2.md`: rubric checklist and proposed task split.
- `docs/test-plan.md`: test spreadsheet requirements and coverage plan.
- `docs/meetings/template.md`: sprint meeting report template.
- `README.txt`: standalone plain-text launch instructions required by the rubric.

## BasicML requirements
Memory contains 100 signed four-digit words (-9999 through +9999), addressed 00–99, plus a separate accumulator. Programs load at 00. Instruction words are positive: the first two digits are the opcode and the last two are the operand address. Memory may contain instructions, data, or unused words.

| Code | Operation | Effect |
| --- | --- | --- |
| 10 | READ | Console input to memory |
| 11 | WRITE | Memory value to console |
| 20 | LOAD | Memory value to accumulator |
| 21 | STORE | Accumulator to memory |
| 30 | ADD | Accumulator + memory |
| 31 | SUBTRACT | Accumulator - memory |
| 32 | DIVIDE | Accumulator / memory |
| 33 | MULTIPLY | Accumulator * memory |
| 40 | BRANCH | Jump to operand address |
| 41 | BRANCHNEG | Jump if accumulator < 0 |
| 42 | BRANCHZERO | Jump if accumulator == 0 |
| 43 | HALT | Stop execution |

Arithmetic results remain in the accumulator. All 12 operations must work; the two supplied programs do not cover everything.

## Testing
Use standard-library unittest:
```text
python -m unittest discover -s tests -v
```
The initial scaffold contains no unit tests, so this currently discovers zero tests; that is not milestone coverage. Add at least two tests per approved use case (approximately 20–30 total, more as needed), including success and failure/boundary conditions. Record each in the required spreadsheet. See docs/test-plan.md.

## Team workflow
Proposed ownership, pending team confirmation: Person 1—CLI/loader and memory initialization; Person 2—arithmetic; Person 3—I/O and load/store; Person 4—control flow. The group integrates the execution loop and reviews documentation.

Branch from updated main, for example `git switch -c feature/arithmetic`. Commit your own code and tests under your own account, push the branch, and open a pull request. Have one teammate review before merging. Keep shared interface changes coordinated through Jira and the sprint meeting.

## Submission
Complete the checklist in docs/milestone-2.md. Keep README.txt and these launch instructions synchronized as behavior changes. Verify a fresh clone using only README instructions before submission.
