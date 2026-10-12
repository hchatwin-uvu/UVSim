"""WP-4: tests for word.Word.

Covers range limits; parse valid and malformed text; format; opcode and operand.
"""
import unittest

from word import MAX_WORD, MIN_WORD, Word


class TestWord(unittest.TestCase):

    def test_limits_and_zero_are_accepted(self):
        for value in (MIN_WORD, -1, 0, 1, MAX_WORD):
            with self.subTest(value=value):
                self.assertEqual(Word(value).value, value)

    def test_out_of_range_is_rejected(self):
        for value in (MIN_WORD - 1, MAX_WORD + 1, 12345, -12345):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    Word(value)

    def test_fields_are_read_only(self):
        word = Word(1007)
        for name in ("value", "opcode", "operand"):
            with self.subTest(name=name):
                with self.assertRaises(AttributeError):
                    setattr(word, name, 0)

    def test_parse_accepts_valid_text(self):
        cases = {
            "+1007": 1007,
            "-0005": -5,
            "+0000": 0,
            "-0000": 0,
            "+9999": 9999,
            "-9999": -9999,
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(Word.parse(text).value, expected)

    def test_parse_ignores_surrounding_whitespace(self):
        self.assertEqual(Word.parse("  +1007\n").value, 1007)

    def test_parse_rejects_malformed_text(self):
        cases = (
            "", "   ", "1007", "+107", "+10070", "+10a7", "abcde",
            "++100", "+ 100", "+10.7", "+-100", "\u00b2" * 5,
        )
        for text in cases:
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    Word.parse(text)

    def test_parse_error_names_the_text_and_the_format(self):
        with self.assertRaises(ValueError) as caught:
            Word.parse("10x7")
        message = str(caught.exception)
        self.assertIn("10x7", message)
        self.assertIn("four digits", message)

    def test_format_is_sign_plus_four_digits(self):
        cases = {
            1007: "+1007",
            -5: "-0005",
            0: "+0000",
            7: "+0007",
            MAX_WORD: "+9999",
            MIN_WORD: "-9999",
        }
        for value, expected in cases.items():
            with self.subTest(value=value):
                self.assertEqual(Word(value).format(), expected)

    def test_format_then_parse_round_trips(self):
        for value in (MIN_WORD, -1234, -1, 0, 1, 4300, MAX_WORD):
            with self.subTest(value=value):
                word = Word(value)
                self.assertEqual(Word.parse(word.format()), word)

    def test_opcode_and_operand(self):
        cases = {
            1007: (10, 7),
            4300: (43, 0),
            2199: (21, 99),
            5: (0, 5),
            0: (0, 0),
            MAX_WORD: (99, 99),
        }
        for value, (opcode, operand) in cases.items():
            with self.subTest(value=value):
                word = Word(value)
                self.assertEqual((word.opcode, word.operand), (opcode, operand))

    def test_negative_word_decodes_from_magnitude(self):
        word = Word(-1007)
        self.assertEqual((word.value, word.opcode, word.operand), (-1007, 10, 7))

    def test_equal_values_are_equal(self):
        self.assertEqual(Word(1007), Word(1007))
        self.assertNotEqual(Word(1007), Word(1008))
        self.assertNotEqual(Word(1007), Word(-1007))

    def test_word_is_not_equal_to_a_plain_int(self):
        self.assertNotEqual(Word(1007), 1007)


if __name__ == "__main__":
    unittest.main()
