"""Shared machine state and execution contracts; coordinate changes as a group."""

from word import MAX_WORD, MIN_WORD, Word

MEMORY_SIZE = 250
MAX_ADDRESS = MEMORY_SIZE - 1


def check_address(address: int, purpose: str = "Memory address") -> None:
    """Raise ValueError if address is not a memory register 000–249."""
    if not 0 <= address < MEMORY_SIZE:
        raise ValueError(
            f"{purpose} {address:03d} is outside memory addresses "
            f"000–{MAX_ADDRESS:03d}"
        )


def check_program_length(word_length: int) -> None:
    """Raise ValueError if a program has more lines than memory registers.
        250-line limit;
    """
    if word_length > MEMORY_SIZE:
        raise ValueError(
            f"Program contains more than {MEMORY_SIZE} words "
            f"({word_length} given)."
        )


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

        check_program_length(len(words))

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

        # Load the program starting at memory location 000
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
        check_address(address, "Instruction counter")

        instruction = self.memory[address]
        self.instruction_register = instruction

        if instruction.value < 0:
            raise ValueError(
                f"Negative instruction at address {address:03d}."
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
                f"Invalid opcode {opcode:03d} at address {address:03d}."
            )

        # Reject 250–999 before any handler or deferred READ/WRITE can use it.
        if opcode != 43 and not 0 <= operand < MEMORY_SIZE:
            raise ValueError(
                f"Instruction {instruction.format()} at address {address:03d} "
                f"references address {operand:03d}, outside "
                f"000–{MAX_ADDRESS:03d}"
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
                print(f"Enter a word ({MIN_WORD} to {MAX_WORD}): ", end="", flush=True)
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
