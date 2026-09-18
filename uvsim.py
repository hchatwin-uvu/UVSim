"""Shared machine state and execution contracts; coordinate changes as a group."""

MEMORY_SIZE = 100
MIN_WORD = -9999
MAX_WORD = 9999


class UVSim:
    def __init__(self) -> None:
        self.memory = [0] * MEMORY_SIZE
        self.accumulator = 0
        self.instruction_counter = 0
        self.instruction_register = 0
        self.halted = False

    def load(self, words: list[int]) -> None:
        """Load a BasicML program into memory and reset the machine."""

        if len(words) > MEMORY_SIZE:
            raise ValueError("Program contains more than 100 words.")
    
        for word in words:
            if word < MIN_WORD or word > MAX_WORD:
                raise ValueError(f"Word out of range: {word}")

        # Reset the machine
        self.memory = [0] * MEMORY_SIZE
        self.accumulator = 0
        self.instruction_counter = 0
        self.instruction_register = 0
        self.halted = False

        # Load the program starting at memory location 00
        for address, word in enumerate(words):
            self.memory[address] = word

    def step(self) -> None:
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

        if instruction < 0:
            raise ValueError(
                f"Negative instruction at address {address:02d}."
            )

        opcode, operand = divmod(instruction, 100)
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
