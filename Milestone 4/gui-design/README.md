# Milestone 4 GUI — WP-1

Updated October 16, 2026. This describes the implemented branch, not the final
editor/save integration. Earlier milestone designs remain historical.

![Annotated current layout](wireframe.svg)

1. The header and enabled buttons use primary green; header/button text and
   content surfaces use the off-color. Dark body text is readable on default white.
2. Toolbar: Open file, Run, Stop. Open browses any accessible folder. Run starts
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
Open and Close call a temporary discard confirmation defaulting to No. This
protects edited source while saving is unavailable; tests bypass it only during
cleanup. Failed reads and canceled file pickers preserve the editor.

Pending WP-3: replace the loader boundary with FileActions/ProgramStore, add Save
and Save As, route close confirmation through save-aware FileActions, and support
malformed source loading in coordination with WP-2. Reapply the theme after any
new widgets are constructed. Do not instantiate unfinished placeholder classes.

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
