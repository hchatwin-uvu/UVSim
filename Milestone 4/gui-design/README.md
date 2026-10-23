# Milestone 4 GUI — WP-1

Updated October 23, 2026. The editor and file actions are integrated.
Earlier milestone designs remain historical.

![GUI-matched initial state and separate design notes](wireframe.svg)

The wireframe follows the supplied Windows GUI screenshot: green rectangular
buttons, actual toolbar spacing, empty initial filename/editor/output, disabled
Stop and READ controls, separate table headings, and the editor scrollbar.
Annotations sit below the application frame rather than appearing as invented
GUI footer text. It is a design illustration, not a screenshot; font metrics,
scrollbar rendering, and available space vary with display scaling and resizing.

1. The header and enabled buttons use primary green; header/button text and
   content surfaces use the off-color. Dark body text is readable on default white.
2. Toolbar: Open file, Save, Save As, Run, Stop. Open browses any accessible folder. Run starts
   a fresh execution from the loaded source, including after HALT, Stop, or error.
   Active execution disables Open/Run and enables Stop.
3. Selected File Name explicitly labels the last successfully loaded path.
4. Status/error messages precede READ input and remain visible above output.
5. READ and Submit/Enter are enabled only while waiting. Invalid input can be
   corrected; accepted input clears. Moving these controls does not change their
   controller contract.
6. Output is scrollable, read-only, and cleared before every fresh run. Closing
   cancels the one scheduled execution timer. Native file dialogs retain OS styling.

## Configuration and component handoff

`theme_config.Theme` is an immutable pair of colors. `load_theme(path)` reads
UTF-8 INI with `[theme]`, `primary`, and `off_color`. Both must be six-digit hex;
any missing/invalid setting or unreadable file returns the whole UVU palette.
The default file path is absolute and relative to the module, independent of cwd.
`gui.theme.apply_theme(root, theme)` configures ttk styles and existing Tk Text
widgets. Call it after embedding new panels; new ttk widgets inherit styles.
`UVSimApp(..., theme=None)` loads configuration unless a Theme is supplied.

## Editor integration — October 20, 2026

The window is 1100x720 by default with a 1000x620 minimum. Status and shared READ
controls appear above a two-column workspace: editor on the left, output on the
right. Both columns expand together. The theme is applied after both panels exist.
`IOPanel(parent, on_submit, output_parent=None)` optionally places output under a
separate parent while retaining the original combined layout for other callers.

`UVSimApp.editor` owns the displayed source. Open fills it with validated words;
Run commits an in-progress edit via get_words(), validates, calls load_program(),
clears visible output, and starts execution. No cached source copy remains in the
window. Invalid/empty source never starts a previous program. New programs can
be created with Add without first opening a file. Execution preserves dirty state.

During running/waiting_input, editor mutations and Open/Run are disabled; Copy
and Stop remain available. Editing returns after HALT, Stop, or runtime error.
Open and Close use FileActions.confirm_discard with Save/Discard/Cancel.
Canceled or failed saves prevent replacement/closing. Save As updates the path
only after a successful atomic write; Save without a path opens Save As.

ProgramStore.load_source reads editable strings, ignoring blank lines and
rejecting more than 100 entries without truncation. EditorPanel.set_entries
accepts malformed words, highlights them, and records a clean loaded baseline.
Run and Save validate with get_words(); displayed line numbers refer to editor
rows after blank lines are removed. ProgramStore.load remains the strict API
for console execution. FileActions loads source before asking to discard, then
reads again after confirmation in case Save changed the selected file.

## Contributions for other document owners

- Use case: user edits both colors in theme.ini, saves, and restarts; the new
  scheme appears. Invalid/missing configuration results in the UVU palette.
- Functional requirement: the system shall load configurable primary/off-colors
  at startup without recompilation or reinstallation.
- Functional requirement: the system shall use #4C721D and #FFFFFF by default
  and when configuration cannot be loaded or validated.
- Nonfunctional requirement: default branding shall keep text readable.
- Test references: tests/test_theme.py and TestRealWindow in
  tests/test_gui_integration.py; supply these cases to the test spreadsheet owner.
