"""Shared machine state and execution contracts; coordinate changes as a group."""

from word import MAX_WORD, MIN_WORD, Word

MEMORY_SIZE = 100


class UVSim:
    def __init__(self) -> None:
        # Word is immutable, so every cell can safely share one Word(0)
        self.memory = [Word(0)] * MEMORY_SIZE
        self.accumulator = 0
        self.instruction_counter = 0
        self.instruction_register = Word(0)
        self.halted = False

    def load(self, words: list[Word]) -> None:
        """Load a BasicML program into memory and reset the machine."""

        if len(words) > MEMORY_SIZE:
            raise ValueError("Program contains more than 100 words.")

        # Word already enforces the range; only the type needs checking here
        for word in words:
            if not isinstance(word, Word):
                raise TypeError(
                    f"UVSim.load expects Word objects, not {type(word).__name__}."
                )

        # Reset the machine
        self.memory = [Word(0)] * MEMORY_SIZE
        self.accumulator = 0
        self.instruction_counter = 0
        self.instruction_register = Word(0)
        self.halted = False

        # Load the program starting at memory location 00
        for address, word in enumerate(words):
            self.memory[address] = word

    def step(self, *, defer_io: bool = False) -> tuple[str, int] | None:
        """Fetch, decode, and execute one instruction."""
        import sys

        # Local imports avoid cycles because handler modules import UVSim.
        from operations.arithmetic import ARITHMETIC_HANDLERS
        from operations.control_flow import CONTROL_FLOW_HANDLERS
        from operations.io_memory import (
            handle_read,
            handle_write,
            handle_load,
            handle_store,
        )

        if self.halted:
            return

        address = self.instruction_counter
        if not 0 <= address < MEMORY_SIZE:
            raise ValueError(
                "Instruction counter is outside memory addresses 00–99."
            )

        instruction = self.memory[address]
        self.instruction_register = instruction

        if instruction.value < 0:
            raise ValueError(
                f"Negative instruction at address {address:02d}."
            )

        # Word owns the digit layout; never split the raw value here
        opcode, operand = instruction.opcode, instruction.operand
        handlers = {
            10: handle_read,
            11: handle_write,
            20: handle_load,
            21: handle_store,
            **ARITHMETIC_HANDLERS,
            **CONTROL_FLOW_HANDLERS,
        }

        handler = handlers.get(opcode)
        if handler is None:
            raise ValueError(
                f"Invalid opcode {opcode:02d} at address {address:02d}."
            )

        if defer_io and opcode == 10:
                return ("READ", operand)

        if defer_io and opcode == 11:
                value = self.memory[operand].value
                self.instruction_counter = address + 1
                return ("WRITE", value)
        # Continue forward unless a branch handler changes the destination.
        self.instruction_counter = address + 1

        try:
            if opcode == 10:
                print("Enter a word (-9999 to 9999): ", end="", flush=True)
                handler(self, operand, sys.stdin)
            else:
                handler(self, operand)
        except (ValueError, EOFError):
            self.instruction_counter = address
            raise

    def run(self) -> None:
        """Execute instructions until HALT or an error."""
        while not self.halted:
            self.step()
