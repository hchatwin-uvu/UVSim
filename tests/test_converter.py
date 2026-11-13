import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from converter import (
    ProgramFormat,
    convert_file,
    convert_program,
    detect_program_format,
)
from loader import load_program
from uvsim import UVSim
from word import Word


class ConverterTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.directory = Path(self.temp_dir.name)

    def test_detects_uniform_supported_formats(self):
        self.assertEqual(
            detect_program_format(["+1007", "-5555"]),
            ProgramFormat.FOUR_DIGIT,
        )
        self.assertEqual(
            detect_program_format(["+010007", "-005555"]),
            ProgramFormat.SIX_DIGIT,
        )

    def test_converts_instructions_and_data_with_signs(self):
        converted = convert_program(["+1007", "-4300", "+5555", "-5555"])
        self.assertEqual(
            [word.format() for word in converted],
            ["+010007", "-043000", "+005555", "-005555"],
        )

    def test_unknown_legacy_opcode_is_preserved_as_numeric_data(self):
        self.assertEqual(
            convert_program(["+9907"])[0].format(),
            "+009907",
        )

    def test_rejects_mixed_formats(self):
        with self.assertRaisesRegex(ValueError, "Mixed four- and six-digit"):
            detect_program_format(["+1007", "+010007"])
        with self.assertRaisesRegex(ValueError, "Mixed four- and six-digit"):
            convert_program(["+010007", "+1007"])

    def test_rejects_malformed_and_empty_programs(self):
        for entries in (["1007"], ["+10A7"], ["+10000"], ["  ", "\n"]):
            with self.subTest(entries=entries):
                with self.assertRaises(ValueError):
                    convert_program(entries)

    def test_rejects_six_digit_program_for_one_way_conversion(self):
        with self.assertRaisesRegex(ValueError, "Only four-digit"):
            convert_program(["+010007"])

    def test_accepts_250_words_and_rejects_251(self):
        converted = convert_program(["+0000"] * 250)
        self.assertEqual(len(converted), 250)
        with self.assertRaisesRegex(ValueError, "more than 250"):
            convert_program(["+0000"] * 251)

    def test_convert_file_writes_loadable_executable_program_and_keeps_source(self):
        source = self.directory / "legacy.txt"
        destination = self.directory / "converted.txt"
        source_text = "+2002\n+4300\n+0055\n"
        source.write_text(source_text, encoding="utf-8")

        converted = convert_file(source, destination)

        self.assertEqual(source.read_text(encoding="utf-8"), source_text)
        self.assertEqual(
            [word.format() for word in converted],
            ["+020002", "+043000", "+000055"],
        )
        loaded = load_program(str(destination))
        machine = UVSim()
        machine.load([Word(value) for value in loaded])
        machine.run()
        self.assertEqual(machine.accumulator, 55)

    def test_convert_file_rejects_same_source_and_destination(self):
        source = self.directory / "legacy.txt"
        source.write_text("+4300\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "must not overwrite"):
            convert_file(source, source)
        self.assertEqual(source.read_text(encoding="utf-8"), "+4300\n")

    def test_save_failure_is_propagated_without_changing_source_or_destination(self):
        source = self.directory / "legacy.txt"
        destination = self.directory / "converted.txt"
        source.write_text("+4300\n", encoding="utf-8")
        destination.write_text("existing output\n", encoding="utf-8")

        with patch("program_store.os.replace", side_effect=OSError("disk full")):
            with self.assertRaisesRegex(OSError, "disk full"):
                convert_file(source, destination)

        self.assertEqual(source.read_text(encoding="utf-8"), "+4300\n")
        self.assertEqual(
            destination.read_text(encoding="utf-8"),
            "existing output\n",
        )


if __name__ == "__main__":
    unittest.main()
