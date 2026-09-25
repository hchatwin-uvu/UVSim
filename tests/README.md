# UVSim tests

Run `python -m unittest discover -s tests -v` from the repository root.
36 tests cover loading, arithmetic, control flow, instructor programs, WRITE
formatting, and malformed-file rejection. Use-case IDs match `Milestone 2/design.md`
and the revised PDF. GUI and retry tests are deferred with GUI implementation.

`test_regression.py` retains the instructor-program, WRITE-formatting, and malformed-file checks for future changes.
