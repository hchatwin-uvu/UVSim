"""WP-4: Add GUI/controller integration tests after the components exist.

Planned cases:
- File selection/cancellation and recovery from missing or malformed files.
- Run/Stop/input control states agree with the controller state.
- Submit/Enter forwards input once; rejected text can be corrected.
- Output refresh does not duplicate lines and uses the agreed formatting.
- GUI actions show errors and completion without requiring console interaction.
- Repeated Run clicks do not create duplicate scheduled execution loops.

Scaffold only: no placeholder passing or skipped tests. Keep tests requiring
Tk/display access distinct from the controller's headless tests.
"""
