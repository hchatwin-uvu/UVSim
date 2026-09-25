"""Console regression checks for the Milestone 2 feedback."""
import io
from contextlib import redirect_stdout
from pathlib import Path
import unittest
from unittest.mock import patch

from loader import load_program
from operations.io_memory import format_word
from uvsim import UVSim

ROOT = Path(__file__).resolve().parents[1]


class FeedbackTests(unittest.TestCase):
    def run_program(self, name, inputs=()):
        machine = UVSim()
        machine.load(load_program(ROOT / "programs" / name))
        output = io.StringIO()
        with patch("sys.stdin", io.StringIO("\n".join(map(str, inputs)) + "\n")), redirect_stdout(output):
            for _ in range(10000):
                machine.step()
                if machine.halted:
                    break
        self.assertTrue(machine.halted)
        text = output.getvalue().replace("Enter a word (-9999 to 9999): ", "")
        return text.splitlines()

    def test_instructor_programs(self):
        cases = [
            ("Test1.txt", [7, 5], [12]),
            ("Test2.txt", [7, 5], [7]),
            ("Test2.txt", [5, 7], [7]),
            ("Test2.txt", [-5, -7], [-5]),
            ("Test2.txt", [5, 5], [5]),
            ("Test3.txt", [], [3333, 3, 3332, 1666, 666, -334]),
            ("Test3b.txt", [], [3333, 3, 1332, 666, -334, -1334]),
            ("Test4.txt", [], [1111, 2222, 3333, 4444, 5555]),
        ]
        for name, inputs, expected in cases:
            with self.subTest(name=name, inputs=inputs):
                self.assertEqual([int(x) for x in self.run_program(name, inputs)], expected)

    def test_write_four_digits_and_negative_sign(self):
        for value, expected in [(1234, "1234"), (12, "0012"), (0, "0000"),
                                (-5, "-0005"), (-9999, "-9999")]:
            self.assertEqual(format_word(value), expected)

    def test_malformed_instructor_file_is_rejected(self):
        with self.assertRaises(ValueError):
            load_program(ROOT / "programs/Test5.txt")


if __name__ == "__main__":
    unittest.main()
