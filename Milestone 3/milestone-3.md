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

- [ ] Split combined use cases: give ADD, SUBTRACT, and each branching operation its own separately tracked use case.
- [ ] Reformat longer Main Flow sections into clear bulleted or numbered steps.
- [ ] Update the unit-test spreadsheet's use-case references to match the revised use cases.
- [ ] Correct WRITE formatting: show 1234 rather than 01234, with no extra fifth numeric digit; preserve the sign for negative values. Update the documented output format.
- [ ] Recover from invalid or out-of-range READ input inside the GUI: explain the error and allow re-entry while preserving the current execution and pending READ instruction. Continue after valid input without restarting the program.
- [ ] Recover from missing/unreadable files and malformed file contents inside the GUI: explain the problem and allow selection of another file without restarting the application. Malformed files do not need to execute.
- [ ] Replace arithmetic overflow exceptions with truncation of higher-order digits, preserving the sign: 12345 becomes 2345 and -12345 becomes -2345. Store the truncated value in the accumulator and continue execution using it. READ must still reject values outside -9999 to 9999.
- [ ] Revise README.txt to explain that files can be opened from any accessible path, not only the programs folder, and that the repository includes sample files users can run. Adapt these explanations to the GUI workflow.
- [ ] Update affected design descriptions, tests, and documentation together; include verification of retry behavior, WRITE formatting, and positive/negative overflow truncation in the final review.

These are planned corrections, not completed fixes. Track ownership and progress in the tasks below, and include the corrected application for the instructor's regrade review.

## Task tracking — claim work here

This document is the sprint task tracker. All tasks start unassigned. To claim a task, replace `Unassigned` with your name and enter an agreed due date. Use `Not started`, `In progress`, `Blocked`, or `Done`; add a file/PR link or blocker in the last column. Mark a task Done only when its completion criteria are met, and update the related rubric/feedback checkboxes above.

## Meeting 1 — first round of work

Each of the four teammates can pick up one main task (M3-01 through M3-04), plus their own independent SRS draft. Review the instructor feedback and agree on deadlines at the meeting. GUI-dependent feedback fixes continue in the second round.

| ID | Task and completion criteria | Owner |
| --- | --- | --- |
| M3-01 | **Milestone 2 fixes:** split combined use cases, reformat Main Flows, update spreadsheet references, fix WRITE formatting, implement sign-preserving overflow truncation with updated tests, and clarify README paths/sample files. Document required GUI retry behavior for M3-05/M3-06. | Unassigned |
| M3-02 | **GUI design:** propose a toolkit and create annotated wireframes for all screens, file selection, execution, READ/WRITE, completion, and error recovery. Ready for team review at Meeting 2. | Unassigned |
| M3-03 | **Class design:** propose class responsibilities and GUI/simulator I/O interfaces. Draft the class definition document with method purposes, parameters, returns, and pre-/post-conditions. Ready for team review at Meeting 2. | Unassigned |
| M3-04 | **Regression preparation:** assemble all six unchanged instructor files and document inputs, expected outputs, and checks for overflow, WRITE formatting, invalid READ retry, and file recovery. Identify affected existing tests; do not record unrun checks as passing. | Unassigned |
| M3-I1 | **Individual SRS draft 1:** independently write at least 15 functional + 3 non-functional requirements, label authorship, and submit to the scrum leader. | Unassigned |
| M3-I2 | **Individual SRS draft 2:** same criteria; a different teammate claims this draft. | Unassigned |
| M3-I3 | **Individual SRS draft 3:** same criteria; a different teammate claims this draft. | Unassigned |
| M3-I4 | **Individual SRS draft 4:** same criteria; the remaining teammate claims this draft. | Unassigned |

## Meeting 2 — review and second round of work

Review the first-round fixes, wireframes, class interfaces, and regression plan. Approve the GUI design and shared interfaces before implementation. The four main follow-up tasks are M3-05 through M3-08; claim them based on availability and the agreed design.

| ID | Task and completion criteria | Owner |
| --- | --- | --- |
| M3-05 | **GUI implementation:** build the approved screens and controls for file selection, running, input, output, and completion. Show file/READ errors in the GUI and support retry without restarting. Depends on M3-02 and agreed interfaces from M3-03; coordinate with M3-06. Update wireframes to match the result. | Unassigned |
| M3-06 | **Simulator refactoring and class documentation:** implement the approved separation of GUI and simulator logic, preserve execution state during READ retries, and keep execution responsive. Integrate M3-01 behavior and coordinate with M3-05. Finalize documentation for every implemented class and method. | Unassigned |
| M3-07 | **Integration and feedback verification:** coordinate reviewed changes from M3-01/M3-05/M3-06, resolve integration issues, and verify every instructor feedback item against the working app/documents. Link evidence and flag remaining blockers. | Unassigned |
| M3-08 | **Final regression and README:** use M3-04's plan to check the integrated GUI against all six files, retry behavior, and existing unit tests; record actual results. Finalize README.txt with dependencies, installation, launch, every GUI control, arbitrary file paths, and included samples. Verify a fresh clone using only the README. | Unassigned |
| M3-S1 | **Group SRS merge 1:** two teammates review the other pair's individual drafts and produce one labeled, consistent document with at least 15 functional + 3 non-functional requirements. | Unassigned pair |
| M3-S2 | **Group SRS merge 2:** the other pair reviews the first pair's drafts and produces a second labeled merged document with the same minimum counts. | Unassigned pair |
| M3-S3 | **Final SRS merge:** after M3-S1/M3-S2, reconvene as all four teammates to create the final official SRS. Preserve and label all seven documents. The owner coordinates; the full team participates. | Unassigned |
| M3-M2 | **Meeting 2 report:** record actual attendance, review decisions, SRS groups, second-round task claims, deadlines, and blockers. | Unassigned |
| M3-09 | **Submission review:** check all rubric items, seven SRS documents, revised design/use cases and spreadsheet, GUI wireframes, class document, source code, README, test results, and weekly meeting reports. Package the required deliverables and identify feedback fixes for regrade review. | Unassigned |

Reserve time at Meeting 2 for both group SRS merges and the full-team merge. If they cannot finish in that session, schedule a continuation before submission. Keep at least one documented meeting per week; add report tasks here if the sprint needs more meetings.

## SRS workflow — start early

1. Each teammate independently writes at least 15 functional and 3 non-functional requirements **without consulting other teammates**. Use “the system shall…” wording, one idea per requirement, and audit clarity and subjective wording.
2. Each teammate sends their labeled individual draft to Hayden. Preserve all four originals for submission.
3. After collecting drafts, Hayden divides the team into two groups and assigns half of the documents to each, ideally the other group's drafts.
4. Each group discusses, combines, and rewrites its assigned requirements into one consistent document with at least 15 functional and 3 non-functional requirements. Remove repetition, redundancy, and contradictions; do not simply concatenate drafts.
5. Both groups send their labeled merged documents to Hayden.
6. The full team meets to merge those two documents into one final official SRS with at least 15 functional and 3 non-functional requirements, again checking consistency.
7. Submit all seven documents: four individual, two group, and one final. If team size changes, confirm the assignment's alternate process/count before proceeding.

## Design and validation focus

- Choose the GUI toolkit and document installation requirements before implementation.
- Agree on file selection → load → run → requested input → output/completion workflow, including cancellation, invalid input, and execution errors.
- Use the current loader, UVSim, and operation modules as a starting point. Refactor console-dependent execution and I/O behind agreed interfaces so the GUI stays separate from simulator logic and remains responsive.
- Design the class responsibilities as a team, then keep the class document and wireframes synchronized with the implemented GUI.
- Implement the instructor-required overflow policy: truncate higher-order digits instead of raising an overflow error. Preserve the sign and continue with the truncated accumulator value; update existing overflow tests accordingly.
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

## Meeting decisions to record

- [ ] Confirm meeting dates and the course submission deadline in this document.
- [ ] Claim first-round tasks and set due dates; each teammate claims exactly one independent SRS draft.
- [ ] Review the instructor video for any additional requirements.
- [ ] At Meeting 2, approve the GUI toolkit, workflow, class responsibilities, and I/O interfaces.
- [ ] Form the two SRS review groups after all individual drafts are collected; record members and assigned source documents in M3-S1/M3-S2.
- [ ] Claim second-round tasks, including integration, documentation, meeting reports, and submission review.
- [ ] Record actual decisions and action items in the meeting reports and keep task status/evidence current here.
