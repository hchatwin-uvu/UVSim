# Design document starter — draft
Expand and approve this document before submission. These are proposed outlines,
not completed use cases or agreed architecture.

## Draft user stories
1. As a CS student, I want to load and execute a BasicML file so I can observe how machine instructions manipulate data.
2. As a CS student, I want console input/output and understandable errors so I can test and correct my programs.

## Proposed use-case map
Expand every row with actor, preconditions, trigger, main flow, alternate/error
flows, and postconditions. Keep 10–15 use cases and at least two tests per case.

| ID | Use case |
| --- | --- |
| UC-01 | Select and load a BasicML file |
| UC-02 | Validate words and program capacity |
| UC-03 | READ console input into memory |
| UC-04 | WRITE memory to console |
| UC-05 | LOAD accumulator |
| UC-06 | STORE accumulator |
| UC-07 | ADD |
| UC-08 | SUBTRACT |
| UC-09 | DIVIDE |
| UC-10 | MULTIPLY |
| UC-11 | BRANCH |
| UC-12 | BRANCHNEG |
| UC-13 | BRANCHZERO |
| UC-14 | Execute a program and HALT |

## Starter contracts
- main.py owns filename selection and user-facing error reporting.
- load_program(path) returns a list of validated integer words.
- UVSim owns memory, accumulator, instruction counter/register, and halted state.
- UVSim.load(words) will reset state and load at address 00.
- UVSim.step() will execute one instruction; run() will repeat until HALT.
- operations modules are separate work areas; handler signatures are not yet fixed.

## Decisions to settle before parallel implementation
- Handler signature and opcode dispatch mechanism.
- Exactly one owner for instruction-counter advancement and branch targets.
- Input/output injection for deterministic tests.
- Signed word parsing, whitespace, blank lines, empty files, and leading signs.
- Integer division rounding (especially negative results), division by zero,
  accumulator overflow, and numeric READ validation.
- Invalid opcode/negative instruction, running past address 99, missing HALT,
  and any optional execution limit.
- Error types and messages; what state remains after failed load/execution.

Separate assignment requirements from chosen policies when documenting decisions.

## Arithmetic implementation choices (UC-07 through UC-10)
The arithmetic module exposes `add(machine, operand)`, `subtract(machine, operand)`,
`divide(machine, operand)`, and `multiply(machine, operand)`. Each accepts the
existing UVSim instance and an integer memory address, and returns None.
`ARITHMETIC_HANDLERS` maps opcodes 30–33 to these functions for the future
execution dispatcher. Handlers change only the accumulator; the execution loop
owns instruction-counter advancement. The shared step/run scaffold is unchanged.

These are local implementation choices for team integration, not previously
agreed assignment requirements: division truncates toward zero, and accumulator
results must fit MIN_WORD through MAX_WORD (-9999 through 9999). Division by zero,
out-of-range results, and addresses outside 00–99 raise ValueError, matching the
CLI's existing error reporting. Failures leave machine state unchanged. Handlers
expect integer accumulator and memory values validated by the loader or other
instruction handlers. Tests are in tests/test_arithmetic.py.
