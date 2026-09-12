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
        """TODO: validate, reset machine state, and copy words starting at 00."""
        raise NotImplementedError("Program loading into memory is not implemented yet.")

    def step(self) -> None:
        """TODO: fetch, decode, dispatch one instruction, and update the counter."""
        raise NotImplementedError("Instruction execution is not implemented yet.")

    def run(self) -> None:
        """TODO: execute until HALT; agree on runtime error handling first."""
        raise NotImplementedError("The execution loop is not implemented yet.")
