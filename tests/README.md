# UVSim tests

Run `python -m unittest discover -s tests -v` from the repository root.
The current suite contains 112 test methods; subcases are included within those methods. All 112 passed on October 23, 2026 with Python 3.13, Windows, and real Tk widgets, with zero skips.

Coverage includes core arithmetic/control flow, instructor programs, Word formatting/decoding, controller READ retry/Stop/reset behavior, editor operations and capacity limits, themes and fallback configuration, source loading, atomic saving, file-action cancellation/failure handling, and integrated edit/save/reopen/run workflows. GUI tests also check that reruns use current source without reloading, and that source/dirty state survive execution.

Strict legacy loader and ProgramStore.load tests reject malformed words. GUI ProgramStore.load_source tests instead permit malformed words for editing; Run and Save validate the corrected editor contents. Files above 100 nonblank entries are rejected without truncation.

GUI tests require working Tk and may skip when it cannot initialize. A run with skips does not establish GUI behavior. Core/controller tests need no display. File tests require writable temporary directories.

See the [current test register](../Milestone%204/UVSim-Milestone-4-Unit-Tests.xlsx) for each method's use-case references, expected results, pass criterion, and source location. [Verification](../Milestone%204/verification.md) records executed checks and outstanding manual acceptance work.
