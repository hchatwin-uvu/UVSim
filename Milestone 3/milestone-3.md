# Milestone 3 plan

Scrum leader: Hayden. Deadline: Friday night, October 2, 2026; confirm the exact time in Canvas. Non-GUI feedback corrections are complete. The toolkit and interfaces below are decisions for upcoming implementation; no GUI code is currently implemented.

## Rubric checklist

- [ ] Previous milestone modifications (10 points): complete the instructor feedback checklist below and resubmit the revised code/design documents and supporting documentation.
- [ ] GUI design document (10 points): create annotated wireframes for every window/screen; label each control and explain its use and workflow.
- [ ] Working GUI (35 points): allow users to select, open, and run a UVSim file with GUI input, output, and understandable errors. Preserve existing core functionality and all 12 opcodes; no new core features are required.
- [ ] Class definition document (10 points): document every class, including any interfaces, base classes, and abstract classes. Include each class's purpose and each function's purpose, parameters, return value, and pre-/post-conditions.
- [ ] Modular OO design: keep UI code out of machine state and business logic; divide responsibilities into manageable, loosely coupled classes.
- [ ] SRS documents (20 points): submit four individual drafts, two sub-team merged drafts, and one final official SRS for the current four-person team; label authors/groups and the final version clearly.
- [ ] Other documents (15 points): revised standalone README.txt (10 points) covering installation, launch, dependencies, and all GUI controls; real sprint meeting reports at least once per week (5 points).
- [ ] Verify all six instructor test files through the GUI, rerun existing unit tests, and check a fresh clone using README.txt alone.

## Milestone 2 feedback — required follow-up

Milestone 2 received 95/100: design 20/20, application 35/40, unit tests 30/30, and other documents 10/10. The instructor offered to regrade the application section after the display and error-handling fixes are included in Milestone 3; recovering points is subject to that review.

- [x] Split combined use cases: give ADD, SUBTRACT, and each branching operation its own separately tracked use case.
- [x] Reformat longer Main Flow sections into clear bulleted or numbered steps.
- [x] Update the unit-test spreadsheet's use-case references to match the revised use cases.
- [x] Correct WRITE formatting: show 1234 rather than 01234, with no extra fifth numeric digit; preserve the sign for negative values. Update the documented output format.
- [ ] Recover from invalid or out-of-range READ input inside the GUI: explain the error and allow re-entry while preserving the current execution and pending READ instruction. Continue after valid input without restarting the program.
- [ ] Recover from missing/unreadable files and malformed file contents inside the GUI: explain the problem and allow selection of another file without restarting the application. Malformed files do not need to execute.
- [x] Replace arithmetic overflow exceptions with truncation of higher-order digits, preserving the sign: 12345 becomes 2345 and -12345 becomes -2345. Store the truncated value in the accumulator and continue execution using it. READ must still reject values outside -9999 to 9999.
- [x] Revise README.txt to explain that files can be opened from any accessible path, not only the programs folder, and that the repository includes sample files users can run. Console explanations are complete; adapting them to the GUI remains part of WP-3/WP-4.
- [ ] Update affected design descriptions, tests, and documentation together; include verification of retry behavior, WRITE formatting, and positive/negative overflow truncation in the final review.

The checked corrections are implemented locally; GUI recovery remains deferred. Completed work is recorded in [feedback-changes.md](feedback-changes.md). Include them with the Milestone 3 submission for instructor review; no submission has been made.

## Toolkit and interface decision

Use **Python Tkinter with ttk widgets**, one main window, and the existing Python simulator. Verify Tkinter availability with `python -m tkinter`; document any platform-specific Tcl/Tk installation requirements in README.txt. Reference: [Python Tkinter documentation](https://docs.python.org/3/library/tkinter.html).

The window contains Open file, the selected filename, Run, Stop, a read-only scrollable output area, a READ input field with Submit, and a status/error area. All application interaction and messages belong in the GUI. READ controls are enabled only while waiting for input. Open file is disabled during execution/waiting; Stop lets the user abandon the run before selecting another file. Canceling file selection leaves the session unchanged.

A UI-independent `SimulatorController` sits between the GUI and the loader/UVSim. Tkinter imports and widget manipulation stay in GUI files. Use the existing loader and opcode implementations, preserving completed overflow and formatting fixes. These are implementation decisions for upcoming work, not code already implemented.

### Controller contract

| Method | Required behavior |
| --- | --- |
| `load_file(path: str) -> bool` | Validate the entire file before replacing machine state. On success reset the machine and outputs, enter `ready`, and return True. On failure preserve the prior program/state, set an explanatory message, and return False. Reject empty programs at the application boundary. |
| `start() -> None` | From `ready`, enter `running`. Other states are unchanged; load a file again for a new run. |
| `tick(max_steps: int = 100) -> None` | When running, execute at most max_steps instructions. Return early for READ, HALT, or runtime error; otherwise return control to the GUI. No blocking input or unbounded execution loop. |
| `submit_input(text: str) -> bool` | Accept input only in `waiting_input`. Validate a signed integer in -9999 through 9999 before changing memory. Invalid input returns False, updates the message, and preserves the pending READ and prior execution state. Valid input is consumed once by that READ, resumes execution, and returns True. |
| `stop() -> None` | From `running` or `waiting_input`, discard pending input and enter `stopped`. Keep output visible. Load a file again to begin a new session. Other states are unchanged. |

| Read-only property | Contract |
| --- | --- |
| `state` | One of `empty`, `ready`, `running`, `waiting_input`, `halted`, `stopped`, or `error`. Initial state is `empty`; HALT enters `halted`; runtime errors enter `error` without closing the application. |
| `message` | Current status or error explanation for the GUI to display. |
| `outputs` | Ordered collection of numeric WRITE values. The display uses the existing `format_word()`; clear only after a successful load. The GUI must not mutate this collection. |

The main window owns a single Tkinter `after()` scheduling loop that calls `tick()` and refreshes controls/output. Do not schedule a second loop on every Run click. Package 2 owns READ suspension/resumption and ensures that an input request does not skip an instruction or change memory before valid input arrives. Input validation must also occur at the controller boundary, even if the input widget validates it first.

### File ownership and component boundary

| Work package | Working files | Boundary |
| --- | --- | --- |
| WP-1: Window and file loading | `gui/app.py`, `gui/__init__.py`, `main.py` | Own the root window, file picker, Run/Stop/status controls, scheduling, and embedding the I/O panel. Call the controller; do not execute opcodes in widgets. |
| WP-2: Execution integration | `controller.py`, `uvsim.py`, execution-related changes in `operations/io_memory.py` | Own the controller, simulator state transitions, and removal of console coupling. Coordinate edits to the shared I/O module with WP-3. |
| WP-3: READ/WRITE controls | `gui/io_panel.py`, `input_validation.py`, formatting-related changes in `operations/io_memory.py` | Own input/output widgets, reusable validation, and display formatting. Supply validation to WP-2; do not maintain a second machine state. |
| WP-4: Automated tests and integration | `tests/test_controller.py`, `tests/test_input_validation.py`, `tests/test_gui_integration.py`, existing regression tests | Own new test code, integration verification, and recorded results. Coordinate fixes in another package's files with its owner. |

Package 3 exposes `IOPanel(parent, on_submit)`, where `on_submit(text) -> bool` passes raw text to the shared controller through the window and returns whether it was accepted. Its `refresh(state, outputs)` method enables/disables input and displays formatted output without duplicating prior lines. Package 1 refreshes the panel and status after controller actions. Package 3 supplies `parse_word(text: str) -> int`, raising ValueError with a user-readable explanation for invalid input; Package 2 calls it before accepting a READ value. This permits widget, controller, and validation work to proceed independently.

Scaffold files for all four packages now exist. They contain ownership notes, interface stubs that raise `NotImplementedError`, and test-case outlines only. No GUI or controller behavior is implemented; `main.py` and the existing simulator remain unchanged. The three new test files contain no executable tests yet and do not increase the existing test count.

## Task tracking — claim work here

Use this document as the task tracker. Claim a work package by replacing Unassigned with your name; record due dates, status, evidence, and blockers. Each teammate can own one package and contribute code. Package 4 includes writing automated tests, not only running existing ones. Documentation is part of each package's completion criteria.

Existing task rows have been consolidated into the four packages below; these replace the earlier meeting-based assignments. Historical Milestone 2 work remains recorded separately.

| ID | Task | Owner | Due | Status | Evidence / blocker |
| --- | --- | --- | --- | --- | --- |
| M3-01 | Completed non-GUI Milestone 2 corrections: overflow, WRITE formatting, separate use cases, spreadsheet references, and file-path/sample explanations. | Hayden | Completed September 25 | Done | [Change list](feedback-changes.md); 36 automated tests passed. |
| WP-1 | GUI layout, file loading, and annotated design document; checklist below. | Unassigned | TBD | Not started | — |
| WP-2 | Execution control, simulator integration, and class definition document; checklist below. | Unassigned | TBD | Not started | — |
| WP-3 | READ input, WRITE output, and related README instructions; checklist below. | Unassigned | TBD | Not started | — |
| WP-4 | New automated tests, integration verification, and final README/fresh-clone check; checklist below. | Unassigned | TBD | Not started | — |

### WP-1 — GUI layout and file loading

- [ ] Build the main window and controls described above; embed WP-3's panel.
- [ ] Connect file selection to `load_file()`. Display the selected path only after a successful load; handle cancellation and file failures without restarting.
- [ ] Connect Run/Stop and the single scheduled `tick()` loop; enable controls according to controller state.
- [ ] Show status, completion, and errors in the GUI; no required console interaction.
- [ ] Create annotated wireframes or screenshots covering every screen/dialog and each control's purpose. Match the final application; annotated screenshots after implementation are allowed.
- [ ] Supply README descriptions for file selection, Run, Stop, and status controls.

### WP-2 — Execution control and simulator integration

- [ ] Implement the controller contract and state transitions; keep GUI dependencies out of machine/business logic.
- [ ] Separate console READ/WRITE from simulator execution while preserving all 12 operations and the completed arithmetic/output policies.
- [ ] Pause at READ and resume the same instruction exactly once after valid input, retaining prior inputs and machine state on invalid attempts.
- [ ] Execute bounded batches so the window remains responsive, including programs with loops.
- [ ] Handle HALT, Stop, and runtime errors without closing the application; allow a subsequent load.
- [ ] Finalize the class definition document: each class's purpose, fields, relationships, and every method's purpose, parameters, return value, and pre/postconditions. Include any interfaces/base/abstract classes used. Everyone supplies details for their own classes.

### WP-3 — READ input and WRITE output

- [ ] Implement the I/O panel and refresh/submit boundary defined above.
- [ ] Implement reusable integer validation for READ, rejecting blank, invalid, and out-of-range values with clear explanations.
- [ ] Connect Submit and Enter to the controller, retain invalid text for correction, and clear accepted input. Keep controls disabled outside `waiting_input`.
- [ ] Display ordered WRITE output using `format_word()` in a read-only scrollable area; retain output after completion/errors and clear it after successful loading.
- [ ] Coordinate shared I/O-module edits with WP-2 so formatting/validation and execution changes do not conflict.
- [ ] Write README instructions for READ, Submit/Enter, WRITE formatting, invalid-input retry, and output behavior.

### WP-4 — Automated tests and integration

- [ ] Prepare tests against the controller contract while WP-1 through WP-3 are being implemented.
- [ ] Write automated tests for failed load preserving state, loading a valid file after failure, invalid READ retry preserving execution, and consuming valid input only once.
- [ ] Test state transitions, bounded execution, Stop, HALT, runtime errors, and GUI-to-controller integration. Keep core controller tests runnable without opening a window.
- [ ] Retain and rerun the 36 existing tests, adapting I/O setup to agreed interfaces where needed without weakening expected behavior.
- [ ] Run all six instructor files through the completed GUI using the verification table below; record actual results. Test5 is a rejection/recovery check.
- [ ] Review integrated changes and route defects to their code owners. Verify remaining feedback items before marking their checkboxes complete.
- [ ] Assemble README.txt from package contributions; include Python/Tkinter dependencies, installation, launch, all controls, any accessible file path, and included samples.
- [ ] Verify installation and use from a fresh clone using README.txt alone; record the result and remaining limitations.

## Dependencies and execution order

| Work package | Can begin immediately | Needed before final integration/completion |
| --- | --- | --- |
| WP-1 | Layout, file picker, wireframe, and calls against the agreed controller contract. | WP-2 controller implementation and WP-3 I/O panel. |
| WP-2 | Controller/state design and simulator refactoring using the agreed contract. | WP-3's reusable validator; coordinate READ/WRITE boundaries with WP-1/WP-3. |
| WP-3 | Validator, formatting, and isolated I/O widgets. | WP-1's embedding and WP-2's READ pause/resume implementation. |
| WP-4 | Test cases, fixtures, validator/controller tests against the contract, and documentation outline. | Integrated WP-1 through WP-3 for full GUI regression and fresh-clone verification. |

1. Claim packages, set dates, and review this contract together. Coordinate any interface changes in this document before dependent code changes.
2. Develop all four packages in parallel against the contract. Interface agreement is the initial prerequisite; completed execution code is not required to start widgets or tests.
3. Integrate file loading, execution, and READ/WRITE. WP-2 owns execution changes; WP-1 owns the window composition.
4. Run WP-4's verification and have each package owner resolve defects in their area.
5. Synchronize all documents with the finished application, then perform submission review.

## SRS and sprint deliverable tasks

SRS work remains required alongside the four code packages. Each teammate claims one independent draft; pair membership is assigned after drafts are collected.

| ID | Task and completion criteria | Owner | Due | Status |
| --- | --- | --- | --- | --- |
| M3-I1 | Independent SRS draft 1: at least 15 functional + 3 non-functional requirements, labeled with author. | Unassigned | TBD | Not started |
| M3-I2 | Independent SRS draft 2: same criteria, different teammate. | Unassigned | TBD | Not started |
| M3-I3 | Independent SRS draft 3: same criteria, different teammate. | Unassigned | TBD | Not started |
| M3-I4 | Independent SRS draft 4: same criteria, remaining teammate. | Unassigned | TBD | Not started |
| M3-S1 | First pair merges the other pair's drafts into one consistent document with at least 15 functional + 3 non-functional requirements. Depends on all individual drafts. | Unassigned pair | TBD | Not started |
| M3-S2 | Second pair merges the first pair's drafts with the same criteria. Depends on all individual drafts. | Unassigned pair | TBD | Not started |
| M3-S3 | Full team merges the two pair documents; preserve and label all seven documents. Depends on M3-S1/M3-S2. Owner coordinates full-team participation. | Unassigned | TBD | Not started |
| M3-LOG | Collect at least two real sprint meeting reports, one per week, recording attendance, decisions, tasks, and deadlines. | Unassigned | Before submission | Not started |
| M3-09 | Check all rubric items, final code, annotated GUI design, class document, README, seven SRS documents, tests/results, meeting reports, and corrected Milestone 2 deliverables. Include regrade fixes in the Milestone 3 Canvas submission only. | Unassigned | October 2; exact Canvas time TBD | Not started |

## SRS workflow — start early

1. Each teammate independently writes at least 15 functional and 3 non-functional requirements **without consulting other teammates**. Use “the system shall…” wording, one idea per requirement, and audit clarity and subjective wording.
2. Each teammate sends their labeled individual draft to Hayden. Preserve all four originals for submission.
3. After collecting drafts, Hayden divides the team into two groups and assigns half of the documents to each, the other group's drafts as required by the video.
4. Each group discusses, combines, and rewrites its assigned requirements into one consistent document with at least 15 functional and 3 non-functional requirements. Remove repetition, redundancy, and contradictions; do not simply concatenate drafts.
5. Both groups send their labeled merged documents to Hayden.
6. The full team meets to merge those two documents into one final official SRS with at least 15 functional and 3 non-functional requirements, again checking consistency.
7. Submit all seven documents: four individual, two group, and one final. If team size changes, confirm the assignment's alternate process/count before proceeding.

## Design and validation focus

- Use the selected Tkinter/ttk toolkit and document installation requirements.
- Agree on file selection → load → run → requested input → output/completion workflow, including cancellation, invalid input, and execution errors.
- Use the current loader, UVSim, and operation modules as a starting point. Refactor console-dependent execution and I/O behind agreed interfaces so the GUI stays separate from simulator logic and remains responsive.
- Design the class responsibilities as a team, then keep the class document and wireframes synchronized with the implemented GUI.
- Preserve the completed instructor-required overflow policy: truncate higher-order digits instead of raising an overflow error. Preserve the sign and continue with the truncated accumulator value; update existing overflow tests accordingly.
- Verify error recovery explicitly: invalid READ input retains execution state for retry, and file errors return the user to file selection without restarting the app. Show errors through the GUI.

| Instructor file | Planned verification |
| --- | --- |
| Test1.txt | Read two numbers through the GUI and display their sum; for example, 7 and 5 produce 12. |
| Test2.txt | Read two numbers and display the larger; also check equal and negative inputs. |
| Test3.txt | Verify required overflow truncation and continued execution produce 3333, 3, 3332, 1666, 666, -334. |
| Test3b.txt | Verify outputs 3333, 3, 1332, 666, -334, -1334 without overflow. |
| Test4.txt | Verify branching produces 1111, 2222, 3333, 4444, 5555 in order. |
| Test5.txt | Verify GUI reporting of malformed-file errors, including validation of malformed words and handling of blank lines under the documented policy. Then select and run a valid file without restarting the app. |

Use the supplied instructor files unchanged when assembling the regression set. Record actual results once implementation is ready; these checks are not completed test results.

## Coordination checklist

- [ ] Claim the four packages and supporting tasks; set due dates before October 2 with time for integration and fixes.
- [ ] Verify Tkinter on each development machine and review the controller/component contract together.
- [ ] Confirm exact Canvas submission time and document it here.
- [ ] Each teammate claims one independent SRS draft; schedule the pair and final merges early enough to finish.
- [ ] Record SRS pair membership and exchanged drafts in the SRS task rows.
- [ ] Keep task status, evidence, and weekly meeting reports current.
