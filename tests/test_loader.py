import os
import tempfile
import unittest

from loader import load_program
from uvsim import UVSim
from word import Word


class TestLoader(unittest.TestCase):

    def make_temp_file(self, contents):
        temp = tempfile.NamedTemporaryFile(
            mode="w",
            delete=False,
            suffix=".txt"
        )
        temp.write(contents)
        temp.close()
        self.addCleanup(os.remove, temp.name)
        return temp.name

    def test_load_valid_program(self):
        path = self.make_temp_file("+1007\n+2007\n+4300\n")

        words = load_program(path)

        self.assertEqual(words, [1007, 2007, 4300])

    def test_invalid_word_missing_sign(self):
        path = self.make_temp_file("1007\n+4300\n")

        with self.assertRaises(ValueError):
            load_program(path)

    def test_invalid_word_contains_letters(self):
        path = self.make_temp_file("+10AB\n")

        with self.assertRaises(ValueError):
            load_program(path)

    def test_program_over_100_words(self):
        path = self.make_temp_file("+0000\n" * 101)

        with self.assertRaises(ValueError):
            load_program(path)

    def test_file_not_found(self):
        with self.assertRaises(OSError):
            load_program("file_that_does_not_exist.txt")

    def test_uvsim_loads_program_at_zero(self):
        machine = UVSim()

        machine.load([Word(1007), Word(2007), Word(4300)])

        self.assertEqual(machine.memory[0], Word(1007))
        self.assertEqual(machine.memory[1], Word(2007))
        self.assertEqual(machine.memory[2], Word(4300))

    def test_uvsim_unused_memory_is_zero(self):
        machine = UVSim()

        machine.load([Word(1007), Word(4300)])

        self.assertEqual(machine.memory[2:], [Word(0)] * 98)

    def test_reload_resets_machine_state(self):
        machine = UVSim()

        # Simulate a machine that has already been running
        machine.accumulator = 50
        machine.instruction_counter = 12
        machine.instruction_register = Word(3005)
        machine.halted = True
        machine.memory[50] = Word(9999)

        machine.load([Word(1007), Word(4300)])

        self.assertEqual(machine.accumulator, 0)
        self.assertEqual(machine.instruction_counter, 0)
        self.assertEqual(machine.instruction_register, Word(0))
        self.assertFalse(machine.halted)
        self.assertEqual(machine.memory[0], Word(1007))
        self.assertEqual(machine.memory[1], Word(4300))
        self.assertEqual(machine.memory[50], Word(0))

    def test_uvsim_rejects_too_many_words(self):
        machine = UVSim()

        with self.assertRaises(ValueError):
            machine.load([Word(0)] * 101)

    def test_uvsim_rejects_out_of_range_word(self):
        machine = UVSim()

        # Word enforces the range before the machine ever sees the value
        with self.assertRaises(ValueError):
            machine.load([Word(10000)])

    def test_uvsim_rejects_plain_integers(self):
        machine = UVSim()

        with self.assertRaises(TypeError):
            machine.load([1007, 4300])


if __name__ == "__main__":
    unittest.main()