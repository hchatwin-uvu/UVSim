# Milestone 2 feedback changes

Non-GUI fixes completed September 25, 2026 for inclusion with Milestone 3. These changes are prepared for review on `codex/milestone-2-feedback-fixes`; nothing has been submitted to Canvas.

## Changes made

1. **Separated use cases in the submitted design document.** ADD, SUBTRACT, BRANCH, BRANCHNEG, and BRANCHZERO each have their own use case. The revised PDF now follows the same UC-01 through UC-14 identifiers as the Markdown design and test register.
2. **Reformatted Main Flows.** Every use case now has numbered steps, with explicit preconditions, triggers, alternate/error flows, and postconditions. Updated descriptions to match overflow truncation and current console error behavior.
3. **Corrected WRITE formatting.** Output uses four magnitude digits instead of five positive digits: `1234` stays `1234`, `12` becomes `0012`, and `-5` becomes `-0005`.
4. **Changed arithmetic overflow to truncation.** Higher-order magnitude digits are discarded and the sign is preserved: `12345` becomes `2345`, `-12345` becomes `-2345`, and `10000` becomes `0`. Execution continues using the truncated accumulator value. Division still truncates fractional results toward zero; division by zero remains an error.
5. **Revised console usage documentation.** Explained that any accessible file path works, clarified that samples are included when cloning, and corrected output/overflow examples. The application still launches as a console program.
6. **Updated tests and the spreadsheet.** Replaced overflow-error expectations with truncation checks, added three console regression methods, and aligned the PDF and test register to the existing separate Markdown use-case IDs. The suite contains 36 tests. The three console regression checks are retained in `tests/test_regression.py` (renamed from `test_feedback.py`) to catch future regressions in instructor-program output, WRITE formatting, and malformed-file rejection. The spreadsheet source-file references use the new name.
7. **Added instructor fixtures.** Test3, Test3b, Test4, and Test5 are included unchanged in `programs/`.
8. **Protected binary deliverables.** Git attributes prevent newline conversion for PDF/XLSX files.

GUI code, the session controller, simulator callbacks, and GUI-specific tests have been removed. Console input validation and error-exit behavior are unchanged. GUI retry/recovery is deferred to the later sprint assignment.

## Use-case crosswalk from the old submitted PDF

| Old PDF ID | Revised ID(s) | Subject |
| --- | --- | --- |
| UC-01 | UC-01, UC-02 | File selection/loading and format/capacity validation |
| UC-02 | UC-03 | READ |
| UC-03 | UC-04 | WRITE |
| UC-04 | UC-05 | LOAD |
| UC-05 | UC-06 | STORE |
| UC-06 | UC-07, UC-08 | ADD and SUBTRACT, now separate |
| UC-07 | UC-10 | MULTIPLY |
| UC-08 | UC-09 | DIVIDE |
| UC-09 | UC-11 | BRANCH |
| UC-10 | UC-12, UC-13 | BRANCHNEG and BRANCHZERO, now separate |
| UC-11 | UC-14 | Execution/HALT |
| UC-12 | UC-01/02/03/09/14 alternate flows | File, input, and runtime errors; overflow now continues normally |

## Validation performed

- `python -m unittest discover -s tests -q`: **36 tests passed**.
- Test1 and Test2 produced correct results, including reversed, equal, and negative Test2 inputs.
- Test3 produced `3333, 3, 3332, 1666, 666, -334`; Test3b produced `3333, 3, 1332, 666, -334, -1334`.
- Test4 produced `1111, 2222, 3333, 4444, 5555`; Test5 was rejected by the loader.
- The revised PDF and spreadsheet reflect the console implementation and were rendered for review.

## Deferred to the GUI assignment

- Implement the GUI and its design/class documentation.
- Report invalid READ input through the GUI and allow retry without losing execution state.
- Report file errors through the GUI and allow another selection without restarting.
- Test GUI recovery and usability once those features exist.

The current console application still reports errors and exits. These feedback items are not complete. The SRS documents, meeting reports, final submission checks, and instructor regrade also remain team work.
