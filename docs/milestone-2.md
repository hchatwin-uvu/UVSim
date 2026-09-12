# Milestone 2 plan
Based on the written assignment shared in the milestone conversation.
Instructor video clarifications have not been transcribed or incorporated.

## Rubric checklist
- [ ] Design document (20 points): at least 2 user stories and 10–15 use cases.
- [ ] Working CLI prototype (40 points): ask for a file, load at 00, execute all 12 listed opcodes, and use console I/O.
- [ ] Every teammate contributes code; include repository link or contribution screenshot.
- [ ] Unit tests (30 points): two per use case, about 20–30 total or more; success and failure coverage; test code in source control.
- [ ] Spreadsheet: test name, description, use-case reference, inputs, expected outputs, and pass/fail criterion.
- [ ] Other documents (10 points): standalone README.txt with launch instructions and prerequisites; sprint meeting reports.
- [ ] Test1 and Test2 pass, plus additional programs for remaining opcodes and errors.
- [ ] Fresh-clone check using README.txt alone.

## Proposed ownership — confirm at the meeting
| Member | Code area | Related work |
| --- | --- | --- |
| Joshua | main.py, loader.py, UVSim.load | Loader tests; Scrum coordination and meeting report |
| Hayden | operations/arithmetic.py | Arithmetic tests and related use cases |
| Hunter | operations/io_memory.py | I/O and memory tests and related use cases |
| Colton | operations/control_flow.py | Branch/HALT tests and related use cases |
| Group | UVSim.step/run integration | Review all tests, examples, and documentation |

Assign one integration owner for step/run before coding. Also assign design,
test spreadsheet, and README owners; everyone supplies their own test/use-case details.
Assignments and deadlines here are proposals, not recorded team commitments.

## Suggested week
- Wednesday: individual code and tests ready.
- Thursday: reviewed PRs integrated.
- Friday: integration tests and documentation complete.
- Saturday: final review and submission.
Confirm actual calendar dates and course deadline in Jira.

## Immediate meeting decisions
- [ ] Confirm ownership and collaborator access for all four members.
- [ ] Approve shared interfaces and policies in design.md.
- [ ] Assign documentation owners and create Jira tasks.
- [ ] Record agreed dates and decisions in a real meeting report.
