
from uvsim import UVSim, MEMORY_SIZE

"""
On Handler 40: Jumps to instruction address given by operand
"""
def branch(machine: UVSim, operand: int) -> None:
    if not 0 <= operand < MEMORY_SIZE:
        raise ValueError("Instruction address must be between 00 and 99.")
    machine.instruction_counter = operand

"""
On 41: If accumulator is less than 0, jump to instruction address given by operan
"""
def branch_neg(machine: UVSim, operand: int) -> None:
    if not 0 <= operand < MEMORY_SIZE:
        raise ValueError("Instruction address must be between 00 and 99.")
    if machine.accumulator < 0:
        machine.instruction_counter = operand

"""
On 42: If accumulator is equal to 0, jump to instruction address given by operand
"""
def branch_zero(machine: UVSim, operand: int)  -> None:
    if not 0 <= operand < MEMORY_SIZE:
        raise ValueError("Instruction address must be between 00 and 99.")
    if machine.accumulator == 0:
        machine.instruction_counter = operand

"""
On 43: Set machine state to halted.
"""
def halt(machine: UVSim, operand: int) -> None:
    machine.halted = True


CONTROL_FLOW_HANDLERS = {
    40: branch,
    41: branch_neg,
    42: branch_zero,
    43: halt
}