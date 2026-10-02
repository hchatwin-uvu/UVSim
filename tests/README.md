# UVSim tests

Run `python -m unittest discover -s tests -v` from the repository root.
The final suite contains 50 tests: 36 original console/core regressions, five
input-validation tests, five isolated GUI tests, and four controller regressions.

GUI tests create hidden Tk windows and skip only when Tk cannot initialize.
Windows does not require a DISPLAY environment variable. A successful run with
skips does not establish GUI behavior on that machine. Core/controller tests
need no display. GUI test doubles isolate window behavior; real-widget instructor
checks and the clean-checkout result are recorded in ../Milestone 3/verification.md.

The controller regressions target READ pause/retry and one-time consumption,
WRITE progression, output retention after failed loading, successful reload,
Stop while waiting, and bounded execution. Existing test_regression.py checks
all instructor programs, output formatting and malformed-file rejection.
