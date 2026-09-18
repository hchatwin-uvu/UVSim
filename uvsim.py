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
        """TODO: fetch, decode, dispatch one instruction, and update the counter."""
        raise NotImplementedError("Instruction execution is not implemented yet.")

    def run(self) -> None:
        """TODO: execute until HALT; agree on runtime error handling first."""
        raise NotImplementedError("The execution loop is not implemented yet.")
