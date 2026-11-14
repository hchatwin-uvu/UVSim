# UVSim tests

Run `python -m unittest discover -s tests -v` from the repository root.
The current suite contains 155 test methods; subcases are included within those methods. All 155 passed on November 13, 2026 with Python 3.13, Windows, and real Tk widgets, with zero skips.

Coverage includes six-digit arithmetic and 250-register boundaries, independent tabs, conversion dialogs and file protection, legacy convert/save/reload/run, core arithmetic/control flow, instructor programs, Word formatting/decoding, controller READ retry/Stop/reset behavior, editor operations and capacity limits, themes and fallback configuration, source loading, atomic saving, file-action cancellation/failure handling, and integrated edit/save/reopen/run workflows. GUI tests also check that reruns use current source without reloading, and that source/dirty state survive execution.

Native six-digit loader and ProgramStore.load tests reject malformed words. GUI ProgramStore.load_source tests instead permit malformed words for editing; Run and Save validate the corrected editor contents. Files above 250 nonblank entries are rejected without truncation.

GUI tests require working Tk and may skip when it cannot initialize. A run with skips does not establish GUI behavior. Core/controller tests need no display. File tests require writable temporary directories.

See [Milestone 5 verification](../Milestone%205/verification-task4.md) for executed checks and outstanding manual acceptance work. `test_tabs.py` and `test_conversion_ui.py` cover the new GUI workflows.
