import unittest

from uvsim import UVSim
from operations import control_flow


class FlowControlTests(unittest.TestCase):
    def setUp(self) -> None:
        self.machine = UVSim()
        self.machine.instruction_counter = 10

    def test_branch(self) -> None:
        self.machine.accumulator = 8
        control_flow.branch(self.machine, 20)
        self.assertEqual(self.machine.instruction_counter, 20)

    def test_branch_neg_when_accumulator_is_negative(self) -> None:
        self.machine.accumulator = -1
        control_flow.branch_neg(self.machine, 20)
        self.assertEqual(self.machine.instruction_counter, 20)

    def test_branch_neg_when_accumulator_is_zero(self) -> None:
        self.machine.accumulator = 0
        control_flow.branch_neg(self.machine, 20)
        self.assertEqual(self.machine.instruction_counter, 10)

    def test_branch_neg_when_accumulator_is_positive(self) -> None:
        self.machine.accumulator = 8
        control_flow.branch_neg(self.machine, 20)
        self.assertEqual(self.machine.instruction_counter, 10)

    def test_branch_zero_when_accumulator_is_zero(self) -> None:
        self.machine.accumulator = 0
        control_flow.branch_zero(self.machine, 20)
        self.assertEqual(self.machine.instruction_counter, 20)

    def test_branch_zero_when_accumulator_is_negative(self) -> None:
        self.machine.accumulator = -6
        control_flow.branch_zero(self.machine, 20)
        self.assertEqual(self.machine.instruction_counter, 10)

    def test_branch_zero_when_accumulator_is_positive(self) -> None:
        self.machine.accumulator = 9
        control_flow.branch_zero(self.machine, 20)
        self.assertEqual(self.machine.instruction_counter, 10)

    def test_halt(self) -> None:
        control_flow.halt(self.machine, 00)
        self.assertTrue(self.machine.halted)

if __name__ == '__main__':
    unittest.main()
