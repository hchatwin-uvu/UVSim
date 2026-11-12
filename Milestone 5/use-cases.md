# Milestone 5 use cases
Team A | Draft for integration review

These extend the existing Milestone 4 use cases.

## UC-24 — Convert a legacy program
**Actor:** Student. **Precondition:** A supported four-digit BasicML file exists.
1. User selects the legacy file or conversion action.
2. Application identifies the format and validates the input.
3. Backend converts recognized opcodes to three-digit opcodes and three-digit operands, and converts data without changing its value or sign.
4. User chooses a destination for the converted file.
5. Application writes the converted six-digit program and reports success.
**Alternatives:** Mixed/invalid format is rejected; canceled destination selection makes no changes; write failure preserves the original and reports an error.
**Postcondition:** Source file remains unchanged; saved output is available for loading and execution.

## UC-25 — Open and switch among multiple programs
**Actor:** Student.
1. User opens a program in a new tab.
2. Application maintains that tab's source, path, and dirty state independently.
3. User switches tabs, edits, saves, or runs the selected document.
**Alternative:** While execution is running, awaiting READ, or stepping, switching is disabled.
**Postcondition:** Each tab retains its own source and save destination.

## UC-26 — Close a modified tab
**Actor:** Student. **Precondition:** Tab contains unsaved edits.
1. User closes the tab or application.
2. Application prompts to save, discard, or cancel.
3. On successful save or explicit discard, closure continues.
**Alternatives:** Cancel or failed save leaves the tab and its contents intact.

## UC-27 — Execute selected tab
**Actor:** Student. **Precondition:** Execution is inactive and selected source is valid.
1. User selects a tab and chooses Run.
2. Shared engine loads that tab's current source, including unsaved edits.
3. Tab switching remains disabled during running, READ wait, and stepping.
4. Completion or Stop restores tab switching.
**Postcondition:** Other tabs' contents and paths remain unchanged.

## UC-28 — Edit expanded program
**Actor:** Student.
1. User adds, modifies, cuts, copies, or pastes six-digit words at three-digit addresses.
2. Editor validates words and checks the 250-entry capacity.
3. Invalid entries are indicated for correction where supported.
**Alternatives:** A 251st entry or invalid clipboard data is rejected without partial changes.

## Clipboard use cases
The existing UC-19 may remain combined per instructor feedback. For clarity: Cut removes selected rows after copying them; Copy preserves rows; Paste validates clipboard words and capacity before insertion.
