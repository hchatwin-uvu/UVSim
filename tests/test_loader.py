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
        path = self.make_temp_file("+010007\n+020007\n+043000\n")

        words = load_program(path)

        self.assertEqual(words, [10007, 20007, 43000])

    def test_invalid_word_missing_sign(self):
        path = self.make_temp_file("010007\n+043000\n")

        with self.assertRaises(ValueError):
            load_program(path)

    def test_invalid_word_contains_letters(self):
        path = self.make_temp_file("+0100AB\n")

        with self.assertRaises(ValueError):
            load_program(path)


    def test_program_over_250_words(self):
        path = self.make_temp_file("+000000\n" * 251)

        with self.assertRaisesRegex(ValueError, "more than 250"):
            load_program(path)

    def test_file_not_found(self):
        with self.assertRaises(OSError):
            load_program("file_that_does_not_exist.txt")

    def test_uvsim_loads_program_at_zero(self):
        machine = UVSim()

        machine.load([Word(10007), Word(20007), Word(43000)])

        self.assertEqual(machine.memory[0], Word(10007))
        self.assertEqual(machine.memory[1], Word(20007))
        self.assertEqual(machine.memory[2], Word(43000))

    def test_uvsim_unused_memory_is_zero(self):
        machine = UVSim()

        machine.load([Word(10007), Word(43000)])

        self.assertEqual(len(machine.memory), 250)
        self.assertEqual(machine.memory[2:], [Word(0)] * 248)

    def test_reload_resets_machine_state(self):
        machine = UVSim()

        # Simulate a machine that has already been running
        machine.accumulator = 50
        machine.instruction_counter = 12
        machine.instruction_register = Word(30005)
        machine.halted = True
        machine.memory[249] = Word(999999)

        machine.load([Word(10007), Word(43000)])

        self.assertEqual(machine.accumulator, 0)
        self.assertEqual(machine.instruction_counter, 0)
        self.assertEqual(machine.instruction_register, Word(0))
        self.assertFalse(machine.halted)
        self.assertEqual(machine.memory[0], Word(10007))
        self.assertEqual(machine.memory[1], Word(43000))
        self.assertEqual(machine.memory[249], Word(0))

    def test_uvsim_accepts_exactly_250_words(self):
        machine = UVSim()

        machine.load([Word(1)] * 250)

        self.assertEqual(machine.memory[249], Word(1))

    def test_uvsim_rejects_too_many_words(self):
        machine = UVSim()

        with self.assertRaisesRegex(ValueError, "more than 250"):
            machine.load([Word(0)] * 251)

    def test_uvsim_rejects_out_of_range_word(self):
        machine = UVSim()

        # Word enforces the range before the machine ever sees the value
        with self.assertRaises(ValueError):
            machine.load([Word(1000000)])

    def test_uvsim_rejects_plain_integers(self):
        machine = UVSim()

        with self.assertRaises(TypeError):
            machine.load([10007, 43000])


if __name__ == "__main__":
    unittest.main()
