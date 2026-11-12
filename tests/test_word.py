"""WP-4: tests for word.Word.

Covers range limits; parse valid and malformed text; format; opcode and operand
in the Milestone 5 six-digit layout (three-digit opcode, three-digit address).
"""
import unittest

from word import MAX_WORD, MIN_WORD, Word


class TestWord(unittest.TestCase):

    def test_limits_and_zero_are_accepted(self):
        for value in (MIN_WORD, -1, 0, 1, 9999, 10000, MAX_WORD):
            with self.subTest(value=value):
                self.assertEqual(Word(value).value, value)

    def test_out_of_range_is_rejected(self):
        for value in (MIN_WORD - 1, MAX_WORD + 1, 1234567, -1234567):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    Word(value)

    def test_fields_are_read_only(self):
        word = Word(10007)
        for name in ("value", "opcode", "operand"):
            with self.subTest(name=name):
                with self.assertRaises(AttributeError):
                    setattr(word, name, 0)

    def test_parse_accepts_valid_text(self):
        cases = {
            "+010007": 10007,
            "-000005": -5,
            "+000000": 0,
            "-000000": 0,
            "+999999": 999999,
            "-999999": -999999,
            "+043000": 43000,
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(Word.parse(text).value, expected)

    def test_parse_ignores_surrounding_whitespace(self):
        self.assertEqual(Word.parse("  +010007\n").value, 10007)

    def test_parse_rejects_malformed_text(self):
        cases = (
            "", "   ", "010007", "+1007", "-0005", "+01007", "+0100070",
            "+010a07", "abcdefg", "++01000", "+ 01000", "+010.07",
            "+-01000", "²" * 7, "+00000²",  # superscript digit
            "+０１０００７",  # full-width digits
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
        self.assertIn("six digits", message)
        self.assertIn("+010007", message)

    def test_format_is_sign_plus_six_digits(self):
        cases = {
            10007: "+010007",
            -5: "-000005",
            0: "+000000",
            7: "+000007",
            43000: "+043000",
            MAX_WORD: "+999999",
            MIN_WORD: "-999999",
        }
        for value, expected in cases.items():
            with self.subTest(value=value):
                self.assertEqual(Word(value).format(), expected)

    def test_format_then_parse_round_trips(self):
        for value in (MIN_WORD, -123456, -1, 0, 1, 43000, MAX_WORD):
            with self.subTest(value=value):
                word = Word(value)
                self.assertEqual(Word.parse(word.format()), word)

    def test_opcode_and_operand(self):
        cases = {
            10007: (10, 7),     # READ 007  -> +010007
            11249: (11, 249),   # WRITE 249 -> +011249
            43000: (43, 0),     # HALT      -> +043000
            21099: (21, 99),
            20150: (20, 150),
            5: (0, 5),
            0: (0, 0),
            MAX_WORD: (999, 999),
        }
        for value, (opcode, operand) in cases.items():
            with self.subTest(value=value):
                word = Word(value)
                self.assertEqual((word.opcode, word.operand), (opcode, operand))

    def test_negative_word_decodes_from_magnitude(self):
        word = Word(-10007)
        self.assertEqual((word.value, word.opcode, word.operand), (-10007, 10, 7))

    def test_equal_values_are_equal(self):
        self.assertEqual(Word(10007), Word(10007))
        self.assertNotEqual(Word(10007), Word(10008))
        self.assertNotEqual(Word(10007), Word(-10007))

    def test_word_is_not_equal_to_a_plain_int(self):
        self.assertNotEqual(Word(10007), 10007)


if __name__ == "__main__":
    unittest.main()
