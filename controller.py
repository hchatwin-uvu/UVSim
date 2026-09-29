"""
@author Colton Bettinson
"""

"""WP-2: UI-independent controller scaffold; no Tkinter imports.

Implement the state machine and simulator integration defined in
Milestone 3/milestone-3.md. Coordinate READ/WRITE changes in
operations/io_memory.py with WP-3. No execution behavior is implemented here.
"""
from uvsim import UVSim, MIN_WORD, MAX_WORD
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
        self._state = ControllerState.READY
        self._message = "Ready"
        self._outputs = []

    def load_file(self, path: str) -> bool:
        """Validate before replacing state; report failure without a partial load."""
        try:
            #load from loader.py
            words = loader.load_program(path)

            #load words from file into uvsim if validated
            self.machine.load(words)

            self._outputs = []
            self._state = ControllerState.READY
            self._message = "Program loaded successfully."

            return True

        except(OSError, ValueError) as error:
            self._state = ControllerState.ERROR
            self._message = str(error)
            return False

    def start(self) -> None:
        """Enter running only from ready; leave other states unchanged."""
        if self._state == ControllerState.READY:
                self._state = ControllerState.RUNNING
                self._message = "Program running."


    def tick(self, max_steps: int = 100) -> None:
        """Run a bounded batch; return early for READ, HALT, or an error."""
        #TODO: uvsim step() currently void. May want to return a value
        if self._state != ControllerState.RUNNING:
            return

        try:
            for _ in range(max_steps):
                #check halted
                if self.machine.halted:
                    self._state = ControllerState.HALTED
                    self._message = "Program halted."
                    return

                result = self.machine.step() #return?

                if result == "READ": #10?
                    self._state = ControllerState.WAITING_INPUT
                    self._message = "Input required."
                    return

                if result == "WRITE":   #11?
                    self._outputs.append(self.machine.output)
                    continue

                if result == "HALT":    #43?
                    self._state = ControllerState.HALTED
                    self._message = "Program halted."
                    return

        except Exception as error:
            self._state = ControllerState.ERROR
            self._message = str(error)

    def submit_input(self, text: str) -> bool:
        """Validate through WP-3's parse_word; preserve state on invalid input."""
        #check if correct state
        if self._state != ControllerState.WAITING_INPUT:
            return False

        try:
            #validation using input_validation.py
            user_input = input_validation.parse_word(text)

            self._state = ControllerState.RUNNING
            self._message = "Input accepted."
            
            return True

        except ValueError as error:
            #preserve state
            self._message =  str(error)
            return False

    def stop(self) -> None:
        """Stop running/waiting execution, discard pending input, retain output."""
        if self._state in (ControllerState.RUNNING, ControllerState.WAITING_INPUT):
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
