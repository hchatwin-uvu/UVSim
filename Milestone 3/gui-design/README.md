# GUI design and WP-1 handoff

Owner: Hayden. Updated September 27, 2026.

![Annotated main window and dialogs](wp1-wireframe.svg)

The main window is implemented in `gui/app.py`. The shaded I/O panel is the planned WP-3 component; its controls are illustrated to define placement, not to claim they are implemented. The native file picker varies by operating system. The integration-pending screen is temporary and should be removed from final submission screenshots after WP-2/WP-3 are ready.

## Controls and workflow

1. **Open file:** Browse to any accessible file. Text files and all files are available as filters. Cancel changes nothing. Successful loading updates the filename and clears outputs through the controller; failed loading preserves the filename/session and shows the controller's explanation. Select another file to retry.
2. **Run:** Enabled only in `ready`. Starts execution through the controller. One 20 ms timer calls bounded `tick()` batches; Run never creates another timer.
3. **Stop:** Enabled while running or waiting for READ input. Delegates to the controller and leaves output visible. Open a file again to begin a new run.
4. **Selected filename:** Displays only the last successfully loaded path, wrapping with window width.
5. **Input/output panel:** WP-3 owns its widgets and validation. The window passes `submit_input(text)` and returns the controller's acceptance boolean. Invalid input does not cause the window to reload or restart the program. The panel must retain rejected text, clear accepted text, and avoid duplicate output on refresh.
6. **Status/error area:** Displays the controller message, including READ errors, file errors, HALT, and runtime errors. Errors are persistent text in the main window, not separate pop-up dialogs. Unexpected boundary errors are shown here and suspend timer execution until a user action.
7. **Close window:** Cancels the scheduled callback and destroys the window. No execution thread remains.

## Package boundaries

- `UVSimApp(root, controller, panel_factory=IOPanel)` composes the window with one shared controller.
- `load_file(path)` returns the controller's success value and updates the filename only on success.
- `submit_input(text)` returns False unless the controller is waiting for input; it returns the controller result otherwise.
- `refresh()` projects controller state/message/outputs into the controls and panel without modifying machine state.
- WP-3 builds its widgets within the supplied panel parent. The window owns the parent layout, so the panel does not need to expose pack/grid methods.
- WP-2 must preserve memory and pending READ on validation failure; the GUI cannot guarantee that on its own.

## Current launch and integration status

`python main.py` still runs the console application. `python main.py --gui` invokes the GUI path; an optional file argument is supported. Until WP-2's controller and WP-3's panel are implemented, this shows a clear integration-pending notice instead of claiming a working simulator. Verify Tkinter availability with `python -m tkinter`.

Once the dependencies are implemented, the same launch function composes them automatically. Full GUI file/READ recovery must then be tested with Test1 through Test5 (including Test3b), and the final application launch/documentation can switch to GUI by default during integration.

## Testing handoff to WP-4

WP-4 owns the permanent GUI/controller tests. The temporary WP-1 test file was removed at Hayden's request; do not run `python -m unittest tests.test_gui_app`. No replacement tests have been added by WP-1. Add the agreed coverage in `tests/test_gui_integration.py`, `tests/test_controller.py`, and `tests/test_input_validation.py` as appropriate.

The existing console suite remains runnable with `python -m unittest discover -s tests -q` and currently contains 36 tests. Passing that suite does not verify the GUI.

### Scenarios to implement

- Cancel file selection: filename, status, output, and machine state remain unchanged.
- Load a valid file, then a missing/unreadable/malformed file: preserve the previous successful filename and machine state, display the error, and allow a subsequent valid selection. Include Test5 followed by Test4.
- Reject invalid READ input: retain prior inputs, memory, accumulator, and pending instruction. Correct the value, accept it exactly once, and continue without restarting.
- Check Open/Run/Stop and READ controls in every controller state, including HALT, errors, and Stop while awaiting input.
- Repeat Run clicks: retain exactly one scheduled execution loop. Closing cancels its callback; no callback accesses a destroyed window.
- Exercise a looping program: tick batches return control so Stop and window interaction remain responsive.
- Trigger a boundary exception: show a status message instead of repeatedly executing the failing callback. Verify subsequent recovery.
- Refresh output repeatedly: no duplicate lines; four-digit formatting is retained; only a successful new load clears output.
- Verify all six instructor files through the integrated GUI, including overflow and branch outputs.

### Test setup and remaining integration

For isolated window tests, inject a controller double and `panel_factory` into `UVSimApp`. For real-widget tests, create a Tk root and a panel double that builds within the supplied parent; close the app in cleanup. Mock native file-picker results when appropriate. Test the real WP-2/WP-3 implementations separately and together before marking recovery complete.

Earlier development-only checks used doubles and a hidden Tk window. Those checks are historical, not a retained test suite or proof of integrated simulator behavior. Full GUI testing and final manual usability review remain pending with WP-4.
