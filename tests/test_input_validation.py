import unittest

from input_validation import parse_word


class TestParseWord(unittest.TestCase):
    def test_accepts_valid_integers(self):
        self.assertEqual(parse_word("42"), 42)
        self.assertEqual(parse_word("+42"), 42)
        self.assertEqual(parse_word("-42"), -42)
        self.assertEqual(parse_word("  -42  "), -42)

    def test_accepts_zero_and_boundary_values(self):
        self.assertEqual(parse_word("0"), 0)
        self.assertEqual(parse_word("-9999"), -9999)
        self.assertEqual(parse_word("9999"), 9999)

    def test_rejects_blank_input(self):
        with self.assertRaisesRegex(ValueError, "Input cannot be blank."):
            parse_word("   ")

    def test_rejects_nonnumeric_input(self):
        for value in ["abc", "12.5", "1,000", "3e2", "--5", "+"]:
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "Input must be a whole number."):
                    parse_word(value)

    def test_rejects_out_of_range_values(self):
        for value in ["-10000", "10000", "+10000"]:
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "Input must be between -9999 and 9999."):
                    parse_word(value)


if __name__ == "__main__":
    unittest.main()
