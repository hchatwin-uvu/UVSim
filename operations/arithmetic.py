"""BasicML arithmetic handlers; results stay in the accumulator."""

from uvsim import MAX_WORD, MEMORY_SIZE, MIN_WORD, UVSim


def _operand_value(machine: UVSim, operand: int) -> int:
    if not 0 <= operand < MEMORY_SIZE:
        raise ValueError("Arithmetic operand address must be between 00 and 99.")
    return machine.memory[operand]


def _store_result(machine: UVSim, result: int) -> None:
    if not MIN_WORD <= result <= MAX_WORD:
        raise ValueError("Arithmetic result must be between -9999 and 9999.")
    machine.accumulator = result


def add(machine: UVSim, operand: int) -> None:
    _store_result(machine, machine.accumulator + _operand_value(machine, operand))


def subtract(machine: UVSim, operand: int) -> None:
    _store_result(machine, machine.accumulator - _operand_value(machine, operand))


def divide(machine: UVSim, operand: int) -> None:
    divisor = _operand_value(machine, operand)
    if divisor == 0:
        raise ValueError("Cannot divide by zero.")
    # Use integer arithmetic to truncate toward zero, including negative results.
    result = abs(machine.accumulator) // abs(divisor)
    if (machine.accumulator < 0) != (divisor < 0):
        result = -result
    _store_result(machine, result)


def multiply(machine: UVSim, operand: int) -> None:
    _store_result(machine, machine.accumulator * _operand_value(machine, operand))


ARITHMETIC_HANDLERS = {
    30: add,
    31: subtract,
    32: divide,
    33: multiply,
}
