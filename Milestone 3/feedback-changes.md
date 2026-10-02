# Milestone 2 feedback changes

Initial non-GUI fixes completed September 25; GUI integration and final documentation verified October 2, 2026. Include these revised deliverables with Milestone 3 for regrade consideration. No Canvas upload is claimed here.

## Changes made

1. **Separated use cases in the submitted design document.** ADD, SUBTRACT, BRANCH, BRANCHNEG, and BRANCHZERO each have their own use case. The revised PDF now follows the same UC-01 through UC-14 identifiers as the Markdown design and test register.
2. **Reformatted Main Flows.** Every use case now has numbered steps, with explicit preconditions, triggers, alternate/error flows, and postconditions. Updated descriptions to match overflow truncation and current console error behavior.
3. **Corrected WRITE formatting.** Output uses four magnitude digits instead of five positive digits: `1234` stays `1234`, `12` becomes `0012`, and `-5` becomes `-0005`.
4. **Changed arithmetic overflow to truncation.** Higher-order magnitude digits are discarded and the sign is preserved: `12345` becomes `2345`, `-12345` becomes `-2345`, and `10000` becomes `0`. Execution continues using the truncated accumulator value. Division still truncates fractional results toward zero; division by zero remains an error.
5. **Revised console usage documentation.** Explained that any accessible file path works, clarified that samples are included when cloning, and corrected output/overflow examples. The final root README.txt now documents GUI-first launch and all controls; legacy console mode requires --console.
6. **Updated tests and the spreadsheet.** Replaced overflow-error expectations with truncation checks, added three console regression methods, and aligned the PDF and test register to the existing separate Markdown use-case IDs. The original console suite contained 36 tests; see verification.md for the expanded final suite. The three console regression checks are retained in `tests/test_regression.py` (renamed from `test_feedback.py`) to catch future regressions in instructor-program output, WRITE formatting, and malformed-file rejection. The spreadsheet source-file references use the new name.
7. **Added instructor fixtures.** Test3, Test3b, Test4, and Test5 are included unchanged in `programs/`.
8. **Protected binary deliverables.** Git attributes prevent newline conversion for PDF/XLSX files.
9. **Completed GUI integration and recovery.** The main window, file picker, Run/Stop/status controls, and single scheduler connect to the real controller and READ/WRITE panel. Invalid READ input preserves memory and the pending instruction for correction; accepted input clears and resumes once. Failed file loading preserves the previous session and allows another selection. Deferred I/O events prevent terminal interaction, WRITE advances correctly, and Stop discards pending input. Permanent controller and real-widget tests verify the integrated behavior.
10. **Finalized Milestone 3 documentation.** Added the GUI README.txt and class contracts, refreshed the wireframe, reconciled the final SRS with implemented scope, and indexed the submission files. Original SRS drafts and revised Milestone 2 artifacts remain available.


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

## Historical console validation (September 25)

- `python -m unittest discover -s tests -q`: **36 tests passed**.
- Test1 and Test2 produced correct results, including reversed, equal, and negative Test2 inputs.
- Test3 produced `3333, 3, 3332, 1666, 666, -334`; Test3b produced `3333, 3, 1332, 666, -334, -1334`.
- Test4 produced `1111, 2222, 3333, 4444, 5555`; Test5 was rejected by the loader.
- The revised PDF and spreadsheet reflect the console implementation and were rendered for review.
## Final GUI validation

See [verification.md](verification.md) for October 2 results, instructor GUI checks,
input/file recovery, expanded test counts and environment limitations.
