"""Arithmetic use cases UC-07 through UC-10."""

import unittest

from operations.arithmetic import ARITHMETIC_HANDLERS, add, divide, multiply, subtract
from uvsim import MAX_WORD, MIN_WORD, UVSim


class ArithmeticTests(unittest.TestCase):
    def setUp(self) -> None:
        self.machine = UVSim()
        self.operand = 42

    def test_add_positive(self) -> None:
        self.machine.accumulator = 7
        self.machine.memory[self.operand] = 5
        add(self.machine, self.operand)
        self.assertEqual(self.machine.accumulator, 12)

    def test_add_negative(self) -> None:
        self.machine.accumulator = 7
        self.machine.memory[self.operand] = -10
        add(self.machine, self.operand)
        self.assertEqual(self.machine.accumulator, -3)

    def test_subtract_positive(self) -> None:
        self.machine.accumulator = 12
        self.machine.memory[self.operand] = 5
        subtract(self.machine, self.operand)
        self.assertEqual(self.machine.accumulator, 7)

    def test_subtract_negative_result(self) -> None:
        self.machine.accumulator = 5
        self.machine.memory[self.operand] = 12
        subtract(self.machine, self.operand)
        self.assertEqual(self.machine.accumulator, -7)

    def test_subtract_negative_value(self) -> None:
        self.machine.accumulator = 5
        self.machine.memory[self.operand] = -12
        subtract(self.machine, self.operand)
        self.assertEqual(self.machine.accumulator, 17)

    def test_divide_exact(self) -> None:
        self.machine.accumulator = 12
        self.machine.memory[self.operand] = 3
        divide(self.machine, self.operand)
        self.assertEqual(self.machine.accumulator, 4)

    def test_divide_truncates_toward_zero(self) -> None:
        for dividend, divisor, expected in (
            (7, 3, 2), (-7, 3, -2), (7, -3, -2), (-7, -3, 2),
            (1, -3, 0), (0, 3, 0),
        ):
            with self.subTest(dividend=dividend, divisor=divisor):
                self.machine.accumulator = dividend
                self.machine.memory[self.operand] = divisor
                divide(self.machine, self.operand)
                self.assertEqual(self.machine.accumulator, expected)
                self.assertIsInstance(self.machine.accumulator, int)

    def test_divide_by_zero_preserves_accumulator(self) -> None:
        self.machine.accumulator = 12
        self.machine.memory[self.operand] = 0
        with self.assertRaisesRegex(ValueError, "divide by zero"):
            divide(self.machine, self.operand)
        self.assertEqual(self.machine.accumulator, 12)

    def test_multiply_positive(self) -> None:
        self.machine.accumulator = 7
        self.machine.memory[self.operand] = 5
        multiply(self.machine, self.operand)
        self.assertEqual(self.machine.accumulator, 35)

    def test_multiply_zero(self) -> None:
        self.machine.accumulator = 7
        self.machine.memory[self.operand] = 0
        multiply(self.machine, self.operand)
        self.assertEqual(self.machine.accumulator, 0)

    def test_multiply_negative(self) -> None:
        self.machine.accumulator = 7
        self.machine.memory[self.operand] = -5
        multiply(self.machine, self.operand)
        self.assertEqual(self.machine.accumulator, -35)

    def test_overflow_truncates_and_preserves_sign(self) -> None:
        for handler, accumulator, value, expected in (
            (add, MAX_WORD, 1, 0), (add, MIN_WORD, -1, 0),
            (subtract, MIN_WORD, 1, 0), (subtract, MAX_WORD, -1, 0),
            (multiply, MAX_WORD, 2, 9998), (multiply, MIN_WORD, 2, -9998),
            (multiply, 2469, 5, 2345), (multiply, -2469, 5, -2345),
            (multiply, MAX_WORD, MAX_WORD, 1),
        ):
            with self.subTest(handler=handler.__name__, accumulator=accumulator):
                self.machine.accumulator = accumulator
                self.machine.memory[self.operand] = value
                handler(self.machine, self.operand)
                self.assertEqual(self.machine.accumulator, expected)

    def test_word_limits_are_allowed(self) -> None:
        for handler, value in ((add, 0), (subtract, 0), (divide, 1), (multiply, 1)):
            for limit in (MIN_WORD, MAX_WORD):
                with self.subTest(handler=handler.__name__, limit=limit):
                    self.machine.accumulator = limit
                    self.machine.memory[self.operand] = value
                    handler(self.machine, self.operand)
                    self.assertEqual(self.machine.accumulator, limit)

    def test_invalid_addresses_preserve_accumulator(self) -> None:
        for handler in (add, subtract, divide, multiply):
            for address in (-1, 100):
                with self.subTest(handler=handler.__name__, address=address):
                    self.machine.accumulator = 12
                    with self.assertRaisesRegex(ValueError, "address"):
                        handler(self.machine, address)
                    self.assertEqual(self.machine.accumulator, 12)

    def test_opcode_mapping_and_boundary_addresses(self) -> None:
        for opcode, expected in ((30, 15), (31, 9), (32, 4), (33, 36)):
            for address in (0, 99):
                with self.subTest(opcode=opcode, address=address):
                    self.machine.accumulator = 12
                    self.machine.memory[address] = 3
                    memory_before = self.machine.memory.copy()
                    self.machine.instruction_counter = 8
                    self.machine.instruction_register = opcode * 100 + address
                    instruction = self.machine.instruction_register
                    ARITHMETIC_HANDLERS[instruction // 100](self.machine, instruction % 100)
                    self.assertEqual(self.machine.accumulator, expected)
                    self.assertEqual(self.machine.memory, memory_before)
                    self.assertEqual(self.machine.instruction_counter, 8)
                    self.assertEqual(self.machine.instruction_register, instruction)
                    self.assertFalse(self.machine.halted)


if __name__ == "__main__":
    unittest.main()
