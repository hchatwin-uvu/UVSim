"""Milestone 5 Task 1: 250 registers, six-digit words, three-digit opcodes.

Executes whole programs through UVSim.step so decoding, address checks, and
handlers are exercised together.
"""
import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from uvsim import MEMORY_SIZE, UVSim, check_program_length
from word import Word


def program(*lines: str) -> list[Word]:
    return [Word.parse(line) for line in lines]


class MemoryExpansionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.machine = UVSim()

    def run_machine(self, inputs=(), max_steps=1000) -> list[str]:
        output = io.StringIO()
        stdin = io.StringIO("".join(f"{value}\n" for value in inputs))
        with patch("sys.stdin", stdin), redirect_stdout(output):
            for _ in range(max_steps):
                self.machine.step()
                if self.machine.halted:
                    break
        self.assertTrue(self.machine.halted)
        return [line.split(": ")[-1] for line in output.getvalue().splitlines()]

    def test_read_into_007_uses_opcode_010(self):
        self.machine.load(program("+010007", "+043000"))
        self.run_machine(inputs=[123456])
        self.assertEqual(self.machine.memory[7], Word(123456))

    def test_every_opcode_with_leading_zero(self):
        self.machine.load(program(
            "+010200",  # 000 READ 200
            "+010201",  # 001 READ 201
            "+020200",  # 002 LOAD 200
            "+030201",  # 003 ADD 201
            "+021249",  # 004 STORE 249
            "+011249",  # 005 WRITE 249
            "+031201",  # 006 SUBTRACT 201
            "+033201",  # 007 MULTIPLY 201
            "+042010",  # 008 BRANCHZERO 010
            "+043000",  # 009 HALT (skipped)
            "+020200",  # 010 LOAD 200
            "+032201",  # 011 DIVIDE 201
            "+041015",  # 012 BRANCHNEG 015 (not taken)
            "+040016",  # 013 BRANCH 016
            "+043000",  # 014 HALT (skipped)
            "+043000",  # 015 HALT (skipped)
            "+043000",  # 016 HALT
        ))
        output = self.run_machine(inputs=[100000, 50000])
        self.assertEqual(output, ["150000"])
        self.assertEqual(self.machine.memory[249], Word(150000))
        self.assertEqual(self.machine.accumulator, 2)
        self.assertEqual(self.machine.instruction_counter, 17)

    def test_instruction_at_last_address_executes(self):
        self.machine.load(program("+040249"))
        self.machine.memory[249] = Word.parse("+043000")
        self.run_machine()
        self.assertEqual(self.machine.instruction_register, Word(43000))

    def test_data_and_branch_targets_at_boundary_addresses(self):
        for address in (0, 99, 100, 249):
            with self.subTest(address=address):
                self.machine.load(program(f"+020{address:03d}", "+043000"))
                self.machine.memory[address] = Word(777777) if address else Word(20000)
                self.run_machine()
                expected = 777777 if address else 20000
                self.assertEqual(self.machine.accumulator, expected)

    def test_address_referencing_instructions_reject_250_to_999(self):
        for opcode in (10, 11, 20, 21, 30, 31, 32, 33, 40, 41, 42):
            for address in (250, 500, 999):
                with self.subTest(opcode=opcode, address=address):
                    self.machine.load([Word(opcode * 1000 + address)])
                    with self.assertRaisesRegex(ValueError, f"{address:03d}.*000–249"):
                        self.machine.step(defer_io=opcode in (10, 11))
                    # The failed instruction does not advance or change state
                    self.assertEqual(self.machine.instruction_counter, 0)
                    self.assertEqual(self.machine.accumulator, 0)
                    self.assertFalse(self.machine.halted)

    def test_halt_ignores_its_address_field(self):
        self.machine.load(program("+043999"))
        self.machine.step()
        self.assertTrue(self.machine.halted)

    def test_unknown_three_digit_opcodes_are_rejected(self):
        for text in ("+100007", "+001007", "+099000", "+999249"):
            with self.subTest(text=text):
                self.machine.load(program(text))
                with self.assertRaisesRegex(ValueError, "Invalid opcode"):
                    self.machine.step()

    def test_running_off_the_end_of_memory_is_an_error(self):
        self.machine.load(program("+040249"))
        self.machine.memory[249] = Word.parse("+020000")  # LOAD, then counter = 250
        self.machine.step()
        self.machine.step()
        with self.assertRaisesRegex(ValueError, "Instruction counter 250"):
            self.machine.step()

    def test_deferred_read_and_write_return_three_digit_addresses(self):
        self.machine.load(program("+010249", "+011248", "+043000"))
        self.assertEqual(self.machine.step(defer_io=True), ("READ", 249))
        self.machine.instruction_counter = 1
        self.machine.memory[248] = Word(-999999)
        self.assertEqual(self.machine.step(defer_io=True), ("WRITE", -999999))

    def test_read_rejects_values_outside_six_digits(self):
        self.machine.load(program("+010007", "+043000"))
        with self.assertRaises(ValueError):
            self.run_machine(inputs=[1000000])
        self.assertEqual(self.machine.instruction_counter, 0)

    def test_program_length_validation_250_versus_251(self):
        check_program_length(250)
        with self.assertRaisesRegex(ValueError, "more than 250"):
            check_program_length(251)


if __name__ == "__main__":
    unittest.main()
