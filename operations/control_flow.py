"""
@author Colton Bettinson
"""
from uvsim import UVSim, check_address

"""
On Handler 040: Jumps to instruction address given by operand
"""
def branch(machine: UVSim, operand: int) -> None:
    check_address(operand, "Instruction address")
    machine.instruction_counter = operand

"""
On 041: If accumulator is less than 0, jump to instruction address given by operand
"""
def branch_neg(machine: UVSim, operand: int) -> None:
    check_address(operand, "Instruction address")
    if machine.accumulator < 0:
        machine.instruction_counter = operand

"""
On 042: If accumulator is equal to 0, jump to instruction address given by operand
"""
def branch_zero(machine: UVSim, operand: int)  -> None:
    check_address(operand, "Instruction address")
    if machine.accumulator == 0:
        machine.instruction_counter = operand

"""
On 043: Set machine state to halted.
"""
def halt(machine: UVSim, operand: int) -> None:
    machine.halted = True


# Keys are the three-digit operation codes 040-043
CONTROL_FLOW_HANDLERS = {
    40: branch,
    41: branch_neg,
    42: branch_zero,
    43: halt
}