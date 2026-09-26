"""WP-4: Add controller tests when WP-2 implements the agreed contract.

Planned cases:
- Failed loads preserve the prior machine; a subsequent valid load succeeds.
- Invalid READ retains prior inputs, memory, and the pending instruction.
- Valid input is consumed once, and execution resumes at the correct point.
- Bounded execution yields; Stop, HALT, and runtime errors set correct states.
- Output is retained until a successful new load.

Scaffold only: no placeholder passing or skipped tests. Core tests should run
without a Tkinter window. Existing regression tests remain in test_regression.py.
"""
