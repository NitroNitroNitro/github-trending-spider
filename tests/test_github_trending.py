# -*- coding: utf-8 -*-
import sys
import unittest

sys.path.insert(0, ".")

from github_trending import _parse_number

class TestGithubTrending(unittest.TestCase):
    def test_parse_number_happy_path(self):
        self.assertEqual(_parse_number("123"), 123)
        self.assertEqual(_parse_number("1,234"), 1234)
        self.assertEqual(_parse_number("1,234,567"), 1234567)
        self.assertEqual(_parse_number(" 1,234 "), 1234)
        self.assertEqual(_parse_number("0"), 0)

    def test_parse_number_edge_cases(self):
        self.assertEqual(_parse_number(""), 0)
        self.assertEqual(_parse_number(None), 0)

    def test_parse_number_error_cases(self):
        self.assertEqual(_parse_number("abc"), 0)
        self.assertEqual(_parse_number("12a"), 0)
        self.assertEqual(_parse_number("1,234.5"), 0)

if __name__ == "__main__":
    unittest.main()
