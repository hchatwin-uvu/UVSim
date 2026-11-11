"""Console regression checks for the Milestone 2 feedback, in six-digit format.

The instructor programs in programs/ are still in the legacy four-digit format.
Converting them is Task 2's job and is tested there. These tests run hand-written
six-digit equivalents of the same programs (same logic, same data values)."""
import io
import os
import tempfile
from contextlib import redirect_stdout
from pathlib import Path
import unittest
from unittest.mock import patch

from loader import load_program
from operations.io_memory import format_word
from uvsim import UVSim
from word import MAX_WORD, MIN_WORD, Word

ROOT = Path(__file__).resolve().parents[1]

# Six-digit equivalents of programs/Test*.txt; data values are unchanged.
PROGRAMS = {
    "Test1": """
        +010007 +010008 +020007 +030008 +021009 +011009 +043000
        +000000 +000000 +000000
    """,
    "Test2": """
        +010009 +010010 +020009 +031010 +041007 +011009 +043000
        +011010 +043000 +000000 +000000
    """,
    "Test3": """
        +020020 +030021 +021027 +011027 +032022 +021027 +011027
        +033023 +021027 +011027 +032024 +021027 +011027 +030025
        +021027 +011027 +031026 +021027 +011027 +043000
        +001111 +002222 +001111 +004444 +000002 -001000 +001000
    """,
    "Test3b": """
        +020020 +030021 +021027 +011027 +032022 +021027 +011027
        +033023 +021027 +011027 +032024 +021027 +011027 +030025
        +021027 +011027 +031026 +021027 +011027 +043000
        +001111 +002222 +001111 +000444 +000002 -001000 +001000
    """,
    "Test4": """
        +011015 +040003 +043000 +011016 +042006 +043000 +011017
        +020015 +042005 +011018 +020019 +041013 +043000 +011020
        +043000
        +001111 +002222 +003333 +004444 -004444 +005555
    """,
}


class FeedbackTests(unittest.TestCase):
    def load_text(self, text):
        """Write one word per line to a temporary file and load it."""
        with tempfile.NamedTemporaryFile(
                "w", suffix=".txt", delete=False) as temp:
            temp.write("\n".join(text.split()) + "\n")
        self.addCleanup(os.remove, temp.name)
        return load_program(temp.name)

    def run_program(self, name, inputs=()):
        machine = UVSim()
        machine.load([Word(value) for value in self.load_text(PROGRAMS[name])])
        output = io.StringIO()
        with patch("sys.stdin", io.StringIO("\n".join(map(str, inputs)) + "\n")), redirect_stdout(output):
            for _ in range(10000):
                machine.step()
                if machine.halted:
                    break
        self.assertTrue(machine.halted)
        prompt = f"Enter a word ({MIN_WORD} to {MAX_WORD}): "
        text = output.getvalue().replace(prompt, "")
        return text.splitlines()

    def test_instructor_programs(self):
        cases = [
            ("Test1", [7, 5], [12]),
            ("Test2", [7, 5], [7]),
            ("Test2", [5, 7], [7]),
            ("Test2", [-5, -7], [-5]),
            ("Test2", [5, 5], [5]),
            # Test3 multiplies 3 * 4444; the old machine truncated 13332 to
            # 3332. Six-digit words hold it, so later results change too.
            ("Test3", [], [3333, 3, 13332, 6666, 5666, 4666]),
            ("Test3b", [], [3333, 3, 1332, 666, -334, -1334]),
            ("Test4", [], [1111, 2222, 3333, 4444, 5555]),
        ]
        for name, inputs, expected in cases:
            with self.subTest(name=name, inputs=inputs):
                self.assertEqual([int(x) for x in self.run_program(name, inputs)], expected)

    def test_values_beyond_four_digits_round_trip_through_read_and_write(self):
        # Test1 adds two inputs; this sum would have overflowed the old format
        self.assertEqual(self.run_program("Test1", [9999, 1]), ["010000"])
        self.assertEqual(self.run_program("Test1", [500000, 499999]), ["999999"])

    def test_write_six_digits_and_negative_sign(self):
        for value, expected in [(1234, "001234"), (12, "000012"), (0, "000000"),
                                (-5, "-000005"), (-999999, "-999999"),
                                (123456, "123456")]:
            self.assertEqual(format_word(value), expected)

    def test_malformed_instructor_file_is_rejected(self):
        with self.assertRaises(ValueError):
            load_program(ROOT / "programs/Test5.txt")


if __name__ == "__main__":
    unittest.main()
