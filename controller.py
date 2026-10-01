"""
@author Colton Bettinson
"""

"""WP-2: UI-independent controller scaffold; no Tkinter imports.

Implement the state machine and simulator integration defined in
Milestone 3/milestone-3.md. Coordinate READ/WRITE changes in
operations/io_memory.py with WP-3. No execution behavior is implemented here.
"""
from uvsim import UVSim
from enum import Enum, auto
import input_validation
import loader


class ControllerState(Enum):
    EMPTY = auto()
    READY = auto()
    RUNNING = auto()
    WAITING_INPUT = auto()
    HALTED = auto()
    STOPPED = auto()
    ERROR = auto()


class SimulatorController:
    """Coordinate loading, bounded execution, input requests, and output."""

    def __init__(self) -> None:
        """Initialize the simulator and empty session"""
        self.machine = UVSim()
        self._state = ControllerState.EMPTY
        self._message = "Open a BasicML file to begin"
        self._outputs = []
        self._pending_read: int | None = None

    def load_file(self, path: str) -> bool:
        """Validate before replacing state; report failure without a partial load."""
        if self._state in (
                ControllerState.RUNNING,
                ControllerState.WAITING_INPUT
        ):
            self._message = "Stop the current program before loading another."
            return False

        try:
            #load from loader.py
            words = loader.load_program(path)
            if not words:
                    raise ValueError("Program file is empty.")
            replacement = UVSim()
            replacement.load(words)

        except (OSError, ValueError) as error:
            self._message = str(error)
            return False

        #load words from file into uvsim if validated
        self.machine = replacement
        self._outputs = []
        self._pending_read = None
        self._state = ControllerState.READY
        self._message = "Program loaded successfully."

        return True

    def start(self) -> None:
        """Enter running only from ready; leave other states unchanged."""
        if self._state == ControllerState.READY:
                self._state = ControllerState.RUNNING
                self._message = "Program running."


    def tick(self, max_steps: int = 100) -> None:
        """Run a bounded batch; return early for READ, HALT, or an error."""

        if self._state != ControllerState.RUNNING:
            return

        try:
            for _ in range(max_steps):
                #check halted
                if self.machine.halted:
                    self._state = ControllerState.HALTED
                    self._message = "Program halted."
                    return

                event = self.machine.step(defer_io=True)

                if event is not None:
                    kind, value = event
                    if kind == "READ":
                        self._pending_read = value
                        self._state = ControllerState.WAITING_INPUT
                        self._message = "Input a word(-9999 to 9999)"
                        return

                    if kind == "WRITE":
                        self._outputs.append(value)
                        continue

                if self.machine.halted:
                    self._state = ControllerState.HALTED
                    self._message = "Program halted."
                    return

        except (ValueError, EOFError, ArithmeticError) as error:
            self._pending_read = None
            self._state = ControllerState.ERROR
            self._message = str(error)

    def submit_input(self, text: str) -> bool:
        """Validate through WP-3's parse_word; preserve state on invalid input."""
        if (
            self._state != ControllerState.WAITING_INPUT\
            or self._pending_read is None
        ):
            return False

        try:
            value = input_validation.parse_word(text)

        except ValueError as error:
            self._message = str(error)
            return False

        self.machine.memory[self._pending_read] = value
        self.machine.instruction_counter += 1
        self._pending_read = None
        self._state = ControllerState.RUNNING
        self._message = "Input accepted."
        return True



    def stop(self) -> None:
        """Stop running/waiting execution, discard pending input, retain output."""
        if self._state in (ControllerState.RUNNING, ControllerState.WAITING_INPUT):
            self._pending_read = None
            self._state = ControllerState.STOPPED
            self._message = "Program stopped."

    @property
    def state(self) -> str:
        """empty, ready, running, waiting_input, halted, stopped, or error."""
        return self._state.name.lower()

    @property
    def message(self) -> str:
        """Current status or user-readable error explanation."""
        return self._message

    @property
    def outputs(self) -> list[int]:
        """Ordered numeric WRITE results; callers must not mutate session data."""
        return self._outputs.copy()
