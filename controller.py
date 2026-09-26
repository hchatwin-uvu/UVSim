"""WP-2: UI-independent controller scaffold; no Tkinter imports.

Implement the state machine and simulator integration defined in
Milestone 3/milestone-3.md. Coordinate READ/WRITE changes in
operations/io_memory.py with WP-3. No execution behavior is implemented here.
"""


class SimulatorController:
    """Coordinate loading, bounded execution, input requests, and output."""

    def __init__(self) -> None:
        """Initialize the simulator and empty session once implemented."""
        raise NotImplementedError("WP-2: initialize the controller.")

    def load_file(self, path: str) -> bool:
        """Validate before replacing state; report failure without a partial load."""
        raise NotImplementedError("WP-2: implement file loading and recovery.")

    def start(self) -> None:
        """Enter running only from ready; leave other states unchanged."""
        raise NotImplementedError("WP-2: implement start.")

    def tick(self, max_steps: int = 100) -> None:
        """Run a bounded batch; return early for READ, HALT, or an error."""
        raise NotImplementedError("WP-2: implement bounded execution.")

    def submit_input(self, text: str) -> bool:
        """Validate through WP-3's parse_word; preserve state on invalid input."""
        raise NotImplementedError("WP-2: implement pending READ recovery.")

    def stop(self) -> None:
        """Stop running/waiting execution, discard pending input, retain output."""
        raise NotImplementedError("WP-2: implement stop.")

    @property
    def state(self) -> str:
        """empty, ready, running, waiting_input, halted, stopped, or error."""
        raise NotImplementedError("WP-2: expose the session state.")

    @property
    def message(self) -> str:
        """Current status or user-readable error explanation."""
        raise NotImplementedError("WP-2: expose the status message.")

    @property
    def outputs(self) -> list[int]:
        """Ordered numeric WRITE results; callers must not mutate session data."""
        raise NotImplementedError("WP-2: expose output values safely.")
