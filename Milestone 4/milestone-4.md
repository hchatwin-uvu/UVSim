# Milestone 4 plan
Scrum leader: Colton. Deadline: October 23, 2026

## Rubric checklist

- [ ] Revisions to previous milestone (10 points): complete every item in the TODO section below and resubmit the affected code and documents.
- [ ] New design modifications (50 points): implement the four client requests.
  - [ ] Color scheme: UVU default (primary `#4C721D`, off-color `#FFFFFF`), configurable by the user without recompiling or reinstalling. Text must be readable with the default scheme. Colors are loaded from a configuration file, and the user changes them by editing that file.
  - [ ] Program editing: load a file into the GUI, then view, add, modify, and delete function codes and data values before execution, including cut, copy, and paste. Handle edits that would exceed 100 entries (addresses 00–99).
  - [ ] Load from any folder: the user can open a file from any directory.
  - [ ] Save: the user can save the current program, optionally under a different name, to a directory they choose.
- [ ] Design document updates (35 points): audit and update unit tests, use cases, requirements, the GUI wireframe, class diagrams, and README so they match the finished application. No new design documents are required.
- [ ] Carried over from earlier milestones, not stated in the written Milestone 4 text: every teammate contributes code; real sprint meeting reports at least once per week. The three written sections total 95 points; confirm what the remaining 5 cover.
- [ ] Rerun the full test suite and all six instructor files through the GUI; check a fresh clone using README.txt alone.

## TODO — Milestone 3 feedback

Instructor feedback items, each mapped to the work package that owns it. Record completed work in `feedback-changes.md` in this folder as items are finished.

### UI

- [ ] **TODO-1 Run again without reloading.** The app currently makes the user select and reload the file for every run. Add the reset behavior (inside Run or as a separate Reset button) so the loaded program can be run repeatedly. — WP-4 (controller), WP-1 (button state)
- [ ] **TODO-2 Move input and status above the output.** The READ input field and the status message area sit below the large output box. Move both above the output so messages are noticeable and READ input sits in a natural workflow position. — WP-1
- [ ] **TODO-3 Selected File Name label.** The field the README calls "selected filename" has no label in the GUI. Add a visible label such as "Selected File Name" so users know what the field represents after loading. — WP-1

### Architecture

- [ ] **TODO-4 Separate file loading from `SimulatorController`.** Proper N-tier design: the controller and CPU code should not care whether a program came from a file, a database, or the editor, and should not need to change if the source changes. — WP-3 (data layer), WP-4 (controller side)
- [ ] **TODO-5 Memory register / word class.** Replace bare integers with a class that encapsulates the word format and exposes function code, address, and raw value, so a format change (for example, swapping which digits are the function code) stays inside one class. The team decided on October 10 to do this as described in the feedback: `Word` is adopted for memory cells and file parsing. — WP-4

## Current state

- GUI (`gui/app.py`, `gui/io_panel.py`) → `SimulatorController` → `UVSim`. The controller imports `loader` directly and its `load_file(path)` both reads the file and resets the machine (TODO-4).
- `UVSim.memory` is a list of plain ints; opcode and operand are split with `divmod(instruction, 100)` in `UVSim.step` (TODO-5).
- `start()` only acts from `ready`, so a halted, stopped, or errored program must be reloaded from disk (TODO-1).
- The file path field has no label, and the status message and READ input sit below the output box (TODO-2, TODO-3).
- Open file already uses the native file picker, which can browse any folder. That requirement is mostly met; it still needs a test, a README statement, and the same freedom for saving.
- There is no editor, no save, and no theming. Widgets use default ttk styling.
- Baseline: 50 automated tests pass (`py -3 -m unittest discover -s tests`, October 5).

## Proposed design

Three tiers, with Tkinter confined to `gui/`:

| Tier | Modules | Responsibility |
| --- | --- | --- |
| Presentation | `gui/app.py`, `gui/io_panel.py`, `gui/editor_panel.py` (new), `gui/file_actions.py` (new), `gui/theme.py` (new) | Window, layout, colors, editor, file dialogs. No opcode execution, no file parsing. |
| Business | `controller.py`, `uvsim.py`, `word.py` (new), `operations/`, `input_validation.py` | Session state, execution, word format. No file access, no Tkinter. |
| Data | `program_store.py` (new, replaces `loader.py`), `theme_config.py` (new) | Read and write program files and the color configuration file. No Tkinter. |

Workflow: Open reads a file through the program store and places the words in the editor. The editor is the single copy of the program the user sees. Run takes the editor's current words, hands them to the controller, and starts execution, so running again needs no reload. Save and Save As write the editor's words back through the program store.

Color configuration: the color scheme is loaded from a configuration file at startup. The user changes the colors by editing that file; no source change or reinstall is needed.

Proposed window order, top to bottom: toolbar (Open, Save, Save As, Run, Stop), Selected File Name, status message, READ input, then the program editor beside the program output.

### Interface contracts

| Owner | Interface | Required behavior |
| --- | --- | --- |
| WP-4 | `Word(value: int)` in `word.py` | Rejects values outside -9999..9999 with ValueError. Read-only `value`, `opcode`, `operand`. `Word.parse(text) -> Word` accepts the signed four-digit file format and raises ValueError with a readable explanation. `format() -> str` returns the file format, e.g. `+1007`. The digit layout is known only to this class. |
| WP-4 | `SimulatorController.load_program(words) -> bool` | Replaces `load_file(path)`. Validates before replacing machine state; rejects empty programs and more than 100 words; rejected while running or waiting for input. On success resets machine and outputs and enters `ready`. Callable from `empty`, `ready`, `halted`, `stopped`, and `error`. The controller no longer imports the loader. |
| WP-3 | `ProgramStore` in `program_store.py` | `load(path) -> list[Word]` with today's validation and line-numbered errors. `save(path, words) -> None` writes one formatted word per line. Both raise OSError or ValueError; a failed save must not leave a partly written file in place of the original. |
| WP-3 | `FileActions` in `gui/file_actions.py` | Owns the Open, Save, and Save As commands and their dialogs. Any directory can be chosen. Tracks the current path and reports it for the Selected File Name field. Save with no current path behaves as Save As. Warns before discarding unsaved edits. |
| WP-2 | `EditorPanel(parent, on_change)` in `gui/editor_panel.py` | `set_words(words)`, `get_words() -> list[Word]` (ValueError naming the offending line), `is_dirty`, `mark_saved()`, `set_enabled(bool)`. Shows the address 00–99 beside each entry. Supports add, modify, delete, cut, copy, paste. Read-only while a program is running or waiting for input. |
| WP-1 | `Theme(primary, off_color)` and `load_theme(path) -> Theme` in `theme_config.py` | Hex colors, loaded from the configuration file that the user edits to change the scheme. Missing file, missing key, or an invalid value falls back to the UVU defaults without crashing. `gui/theme.py` applies a Theme to the window and to the panels the other packages supply. |

## Task tracking

| ID | Task | Owner | Status |
| --- | --- | --- | --- |
| WP-1 | Color scheme, window layout, wireframe, README, and final verification; checklist below. | Hayden | Not started |
| WP-2 | Program editor and use cases; checklist below. | Josh | Not started |
| WP-3 | Open/save, data layer, requirements, and test spreadsheet; checklist below. | Hunter | Not started |
| WP-4 | Word class, controller re-run, and class diagrams; checklist below. | Colton | Not started |
| M4-LOG | Real sprint meeting reports, at least one per week. | Colton | Started |
| M4-SUB | Final rubric check and Canvas submission. | Colton | Not started |

### WP-1 — Color scheme, window layout, and verification

Files: `gui/app.py`, `gui/theme.py`, `theme_config.py`, the configuration file, layout of `gui/io_panel.py`, `tests/test_theme.py`, `tests/test_gui_integration.py`.

- [ ] Implement `Theme` and `load_theme` with UVU defaults and fallback on a missing or invalid file.
- [ ] Apply the primary and off-color across the window; confirm text is readable with the default scheme.
- [ ] Ship a default configuration file and make a user's change take effect on restart without touching source code.
- [ ] Rebuild the layout in the proposed order, adding the Selected File Name label (TODO-3) and moving status and READ input above the output (TODO-2).
- [ ] Embed WP-2's editor panel and WP-3's file actions in the window; enable and disable toolbar buttons by controller state, including Run after halt, stop, or error (TODO-1).
- [ ] Tests: default theme, valid custom theme, missing file, invalid color value; update the existing GUI integration tests for the new layout, label, and Run-again button states.
- [ ] Documents: update the annotated wireframe and GUI design description; keep the README.txt controls section in on-screen order as the layout changes, add color configuration instructions, and assemble the other packages' README contributions. Supply the color scheme use case to WP-2 and the color scheme requirements to WP-3.
- [ ] Verification: run all six instructor files through the finished GUI, plus an edit → save → reopen → run pass and a custom color scheme pass; record actual results in `verification.md` and completed feedback items in `feedback-changes.md`; check a fresh clone using README.txt alone.

### WP-2 — Program editor

Files: `gui/editor_panel.py`, `tests/test_editor.py`.

- [ ] Display the loaded program with one entry per address, 00–99.
- [ ] Add, modify, and delete entries; later entries shift so addresses stay consecutive.
- [ ] Cut, copy, and paste, single and multiple entries, through the keyboard shortcuts and visible controls or a menu.
- [ ] Enforce the 100-entry limit, including multi-line paste.
- [ ] Validate entries with `Word.parse`; mark or report the offending line instead of failing silently.
- [ ] Track unsaved changes and expose them to WP-3; become read-only during execution.
- [ ] Tests: set/get round trip, each edit operation, paste at and over the limit, invalid entry reporting, read-only state.
- [ ] Documents: add use cases for view, add, modify, delete, cut/copy/paste, and the over-limit case; revise existing use cases (UC-01, UC-02, UC-14) that the new load → edit → run flow changes. Supply README text for the editor.

### WP-3 — Open, save, and the data layer

Files: `program_store.py` (replaces `loader.py`), `gui/file_actions.py`, `main.py`, `tests/test_program_store.py` (replaces `tests/test_loader.py`), `tests/test_file_actions.py`.

- [ ] Move file reading out of the controller into `ProgramStore.load`, preserving current validation and error messages (TODO-4).
- [ ] Implement `ProgramStore.save` in the same format the loader accepts, so a saved file reloads identically.
- [ ] Implement Open, Save, and Save As with native dialogs that allow any directory; keep the Selected File Name current after Save As.
- [ ] Prompt before Open or window close discards unsaved edits; report unwritable locations in the status area without losing the editor contents.
- [ ] Update `main.py` so the optional command-line path and console mode use the store.
- [ ] Tests: load from a directory outside the repository, save then reload round trip, Save As to a new name and folder, unwritable path, cancelled dialogs, existing loader cases carried over.
- [ ] Documents: update the SRS requirements for theming, editing, any-folder loading, and saving, and remove the statement that editing is out of scope; add the open and save use cases to WP-2's set; maintain the unit-test spreadsheet, collecting rows from every package and keeping use-case references aligned. Supply README text for Open, Save, and Save As.

### WP-4 — Word class and controller

Files: `word.py`, `uvsim.py`, `controller.py`, `operations/`, `input_validation.py`, `tests/test_word.py`, `tests/test_controller.py`, existing core tests.

- [ ] Implement `Word` and deliver it first; WP-2 and WP-3 both depend on `Word.parse` and `format` (TODO-5).
- [ ] Convert `UVSim` memory and instruction decoding to use `Word`; adapt the operation handlers while preserving overflow truncation, WRITE formatting, and all 12 opcodes.
- [ ] Replace `load_file` with `load_program(words)` and remove the loader import from the controller (TODO-4).
- [ ] Allow a new run from `halted`, `stopped`, and `error` without rereading the file; each run starts from a reset machine and cleared output (TODO-1).
- [ ] Tests: word range, parse, format, opcode/operand; load from each inactive state; run twice with identical results; rejected load while running. Update the existing core, controller, and regression tests to the new interfaces without weakening what they assert; WP-1 and WP-3 update the GUI integration and loader tests.
- [ ] Documents: update the class definition document and class diagram for every new and changed class across all four packages (each owner supplies their own method details); remove the note about the legacy console path if it no longer applies. Supply the run-again changes to the execution use case (UC-14) to WP-2.

## Dependencies and execution order

| Work package | Can begin immediately | Needed before final integration |
| --- | --- | --- |
| WP-1 | Theme configuration, color application, layout reorder, label. | WP-2's editor panel, WP-3's file actions, WP-4's re-run behavior; all packages integrated for the GUI verification pass. |
| WP-2 | Editor widget and edit operations against the interface table, using existing loader validation as a stand-in. | WP-4's `Word`; WP-1's embedding and theme. |
| WP-3 | `ProgramStore` load and save, dialogs, tests with temporary directories. | WP-4's `Word` and `load_program`; WP-2's editor for dirty state and contents. |
| WP-4 | `Word`, controller changes, core test updates. | WP-1's toolbar wiring for re-run; WP-2 and WP-3 moved onto `Word` and `load_program`. |

1. WP-4 delivers `Word` early. All four packages then develop in parallel against the interface table above.
2. WP-1 integrates the editor and file actions into the window.
3. Each owner updates their documents against the integrated application, not the plan.
4. WP-1 runs verification; owners fix defects in their own areas; final submission review.

## Document audit

Every document from earlier milestones must match the finished application. One owner per document; everyone supplies the details for their own code.

| Document | Current location | Owner | What changes |
| --- | --- | --- | --- |
| Use cases / design document | `Milestone 2/design.md` and PDF | WP-2 | New editing, saving, and theming use cases; revised load and run flows. |
| Requirements (SRS) | `Milestone 3/srs/SRS_Final_Document.pdf` | WP-3 | New functional requirements for the four client requests; scope statement. |
| Unit-test spreadsheet | `Milestone 2/UVSim-Milestone-2-Unit-Tests.xlsx` | WP-3 | Rows for all new tests; use-case references; renamed test files. |
| GUI wireframe and description | `Milestone 3/gui-design/` | WP-1 | New layout, editor, Save buttons, label, colors; controls in on-screen order. |
| Class definitions and diagram | `Milestone 3/class-definitions.md` | WP-4 | `Word`, `ProgramStore`, `EditorPanel`, `FileActions`, `Theme`; changed controller and UVSim. |
| README.txt and README.md | Repository root | WP-1 | Controls in on-screen order, editing, saving, color configuration. |
| tests/README.md | `tests/` | WP-4 | New test counts and coverage summary. |
