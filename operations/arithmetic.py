"""BasicML arithmetic handlers; results stay in the accumulator."""

from uvsim import MEMORY_SIZE, UVSim


def _operand_value(machine: UVSim, operand: int) -> int:
    if not 0 <= operand < MEMORY_SIZE:
        raise ValueError("Arithmetic operand address must be between 00 and 99.")
    return machine.memory[operand]


def _store_result(machine: UVSim, result: int) -> None:
    magnitude = abs(result) % 10000
    machine.accumulator = -magnitude if result < 0 else magnitude


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
