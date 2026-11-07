# Milestone 5 plan

Milestone 5 is the final development milestone. Work is divided into four tasks.
Each task owner implements and tests their own changes. The scrum master owns
documentation and all Milestone 4 feedback fixes, including the UI fixes. The
existing GUI owner retains all new Milestone 5 GUI implementation. Remaining
individual names and the submission deadline remain to be assigned.

## Agreed approach

- Expand the application to 250 memory registers and six-digit words.
- Use one-way conversion for legacy four-digit files, keeping the editor and
  execution engine centered on the new six-digit format.
- Use tabs to support multiple open files within one application instance.
- Use one execution engine. Prevent switching documents while execution is
  active, including waiting for input and stepping, until it finishes or stops.
- Each owner supplies test results and implementation details to the scrum
  master for the documentation and final submission.
- All new Milestone 5 GUI changes belong to Task 3. Tasks 1 and 2 provide backend
  interfaces for the GUI owner to integrate. Task 4 owns the Milestone 4 UI
  feedback fixes and coordinates shared GUI files with Task 3.

## Task 1 — Expand memory and word size

**Owner:** Team member to be assigned.

**Primary files:** `word.py`, `uvsim.py`, `input_validation.py`, `loader.py`,
`operations/`, and relevant files in `tests/`.

- [ ] Expand memory from 100 to 250 registers, addressed `000` through `249`.
- [ ] Support six-digit words with three-digit operation codes and addresses.
      Keep the existing operation codes, adding a leading zero: READ becomes
      `010`, so READ into address `007` is `010007`.
- [ ] Update instruction decoding, formatting, numeric input, and validation.
- [ ] Reject address-referencing instructions outside `000–249`.
- [ ] Provide backend validation enforcing a maximum of 250 lines; Task 3
      integrates that validation into loading and editing workflows.
- [ ] Support six-digit arithmetic and the existing overflow behavior at the
      new word limits. Calculations that only exceeded the old four-digit
      limits must now succeed when within the new limits.
- [ ] Test valid boundary addresses, invalid addresses, 250 versus 251 lines,
      six-digit numeric limits, arithmetic, overflow, and instruction execution.

## Task 2 — Support old-file conversion

**Owner:** Team member to be assigned.

**Primary files:** `loader.py`, a proposed `converter.py`,
and relevant files in `tests/`.

- [ ] Provide backend one-way conversion from four-digit programs to six-digit
      programs and file-writing support. Task 3 owns the user-facing controls
      and save dialog integration.
- [ ] Distinguish supported file formats and reject mixed four- and six-digit
      words within one file.
- [ ] Convert recognized instruction codes using `0XX0XX` formatting:
      `1007` becomes `010007`.
- [ ] Convert numeric data using `00XXXX` formatting while preserving its value
      and sign: `5555` becomes `005555`.
- [ ] Apply the assignment's simplifying rule: if the first two digits are a
      valid operation code, treat the word as an instruction; otherwise treat
      it as data. Instructor test data will avoid ambiguous numeric values.
- [ ] Preserve the source file, validate input, and expose save failures cleanly
      to the GUI. Task 3 owns cancellation and error presentation in the UI.
- [ ] Test instruction and data conversion, signs, invalid and mixed formats,
      file-size limits, and loading/executing saved converted programs.

## Task 3 — Milestone 5 GUI work and multiple open files

**Owner:** Existing GUI owner (you).

**Primary files:** `gui/` (including `app.py`, `file_actions.py`,
`editor_panel.py`, and `theme.py`), `program_store.py`, `controller.py`, and
relevant files in `tests/`.

- [ ] Add tabs for multiple open files in one application instance.
- [ ] Keep each document's program contents, filename, and unsaved-change state
      independent.
- [ ] Support switching, editing, saving, and executing documents in any order
      when execution is inactive.
- [ ] Run the selected document's current contents through the shared engine.
- [ ] Disable document switching while running, waiting for input, or stepping;
      restore switching when execution finishes or is manually stopped.
- [ ] Handle unsaved edits when closing a tab or the application, preserving
      data if saving fails or the user cancels.
- [ ] Update the editor for six-digit words, three-digit addresses, and the
      250-line limit in coordination with Task 1.
- [ ] Add conversion controls and save dialogs using Task 2's backend interface;
      handle cancellation and display validation/save errors clearly.
- [ ] Test document isolation, tab switching, save destinations, unsaved-change
      handling, execution restrictions, and running different tabs in sequence.
- [ ] Test conversion UI integration and six-digit editor validation.

## Task 4 — Documentation and Milestone 4 feedback fixes

**Owner:** Scrum master.

**Primary files:** `Milestone 5/`, root `README.md` and `README.txt`,
`gui/editor_panel.py`, `gui/app.py`, potentially `gui/theme.py`, and relevant
tests and test documentation.

### Milestone 4 feedback

- [ ] Fix the unreadable/distorted register value during editing; verify
      readability during editing and after committing the edit.
- [ ] Adjust the initial window size/layout so the status field is visible at
      launch without resizing.
- [ ] Test register-edit readability and initial status visibility, coordinating
      the fixes with Task 3's new GUI work.
- [ ] Split SRS requirement FR-31 into separate cut, copy, and paste requirements.
      Splitting the corresponding use case is optional, not a required TODO.
- [ ] Explain that theme colors use standard RGB hexadecimal color values.
- [ ] Remove "UVU" references from the README; describe the defaults as green
      (`#4C721D`) and white (`#FFFFFF`).
- [ ] Move edit-control documentation into the main UI-control sequence,
      between the existing controls 10 and 11, then renumber as needed.
- [ ] Keep both root README versions consistent and document the UI fixes.

### Milestone 5 documentation

- [ ] Use the latest Milestone 4 documents as the baseline and place updated
      milestone deliverables in `Milestone 5/`.
- [ ] Update the SRS/functional specifications for memory size, word format,
      conversion, multiple documents, validation, and execution restrictions.
- [ ] Update use cases for conversion and multiple-document workflows.
- [ ] Update class definitions and the class diagram to match the implementation.
- [ ] Update the GUI wireframe and its explanation for tabs and conversion.
- [ ] Update README instructions for the new format, limits, conversion, tabs,
      and execution behavior.
- [ ] Collect each owner's verification results and update test documentation
      as needed; each owner remains responsible for testing their own changes.
- [ ] Record actual sprint meetings, decisions, action items, and responsibilities.

## Coordination and implementation order

1. Agree on the six-digit word representation, loader/conversion interfaces,
   and per-document state before implementing shared integrations.
2. Establish the memory/format changes first. Conversion and tabs can proceed
   against the agreed interfaces; integrate them after the format is available.
3. Coordinate shared files explicitly:
   - Tasks 1 and 2 share `loader.py`.
   - Task 2 supplies the conversion API; Task 3 alone edits
     `gui/file_actions.py` to integrate it.
   - Task 3 owns new Milestone 5 GUI features; Task 4 owns Milestone 4 UI
     feedback fixes. Coordinate edits to `gui/app.py`, `gui/editor_panel.py`,
     and any shared theme code before changing them.
   - Task 3 supplies new GUI details to Task 4 for the wireframe and README.
4. Keep documentation current during development, then perform a final review
   against the integrated application.
5. Run a brief team integration check after individual testing. Each owner fixes
   defects in their own area; testing is not a separate fifth task.

## Final acceptance and submission checklist

- [ ] All four task owners have completed and reported their own verification.
- [ ] The full automated test suite passes.
- [ ] Supplied legacy programs convert, save, reload, and execute correctly.
- [ ] Six-digit programs exercise expanded memory and arithmetic successfully.
- [ ] Oversized files/edits and out-of-range addresses are rejected.
- [ ] Multiple documents retain independent contents and save correctly.
- [ ] Execution restrictions work while running, waiting for input, and stepping.
- [ ] Register editing is readable and status information is visible at launch.
- [ ] Documentation matches the final application and includes the feedback fixes.
- [ ] Submit code, updated documents, and actual meeting records together.

Rubric: previous-milestone TODOs **10 points**, functional changes **50 points**,
document updates **35 points**, and meeting reports **5 points**.
