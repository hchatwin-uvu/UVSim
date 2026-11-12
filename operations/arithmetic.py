"""BasicML arithmetic handlers; results stay in the accumulator."""

from uvsim import UVSim, check_address
from word import MAX_WORD

# Results keep only the low six digits
_WORD_MODULUS = MAX_WORD + 1


def _operand_value(machine: UVSim, operand: int) -> int:
    check_address(operand, "Arithmetic operand address")
    return machine.memory[operand].value


def _store_result(machine: UVSim, result: int) -> None:
    magnitude = abs(result) % _WORD_MODULUS
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


# Keys are the three-digit operation codes 030-033
ARITHMETIC_HANDLERS = {
    30: add,
    31: subtract,
    32: divide,
    33: multiply,
}
