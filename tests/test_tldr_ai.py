# -*- coding: utf-8 -*-
import sys
import unittest

sys.path.insert(0, ".")

from tldr_ai import _clean_text, _is_noise_title, _limit_text


class TestTldrAi(unittest.TestCase):
    def test_clean_text(self):
        # Normal text with extra spaces
        self.assertEqual(_clean_text("  hello   world  "), "hello world")
        self.assertEqual(_clean_text("newline \n and \t tab"), "newline and tab")
        # None and empty
        self.assertEqual(_clean_text(None), "")
        self.assertEqual(_clean_text(""), "")
        # No extra spaces
        self.assertEqual(_clean_text("hello world"), "hello world")

    def test_limit_text(self):
        # Shorter than max_len
        self.assertEqual(_limit_text("hello", 10), "hello")
        # Equal to max_len
        self.assertEqual(_limit_text("hello", 5), "hello")
        # Longer than max_len
        self.assertEqual(_limit_text("hello world", 5), "hello...")
        # Empty text
        self.assertEqual(_limit_text("", 5), "")
        # Max len 0
        self.assertEqual(_limit_text("hello", 0), "...")

    def test_is_noise_title(self):
        # Text in SKIP_LINK_TEXTS
        self.assertTrue(_is_noise_title("Subscribe"))
        self.assertTrue(_is_noise_title("read more"))
        self.assertTrue(_is_noise_title("Free Trial"))
        # Specific prefixes
        self.assertTrue(_is_noise_title("TLDR AI Daily Update"))
        self.assertTrue(_is_noise_title("keep up with ai news"))
        self.assertTrue(_is_noise_title("tldr ai stuff"))
        self.assertTrue(_is_noise_title("Keep up with AI today"))
        # Valid titles
        self.assertFalse(_is_noise_title("TLDR AI: Daily Update")) # Note: doesn't match 'tldr ai '
        self.assertFalse(_is_noise_title("Google launches new AI model"))
        self.assertFalse(_is_noise_title("OpenAI update"))
        self.assertFalse(_is_noise_title("Subscribe to my newsletter")) # Not exact match to SKIP_LINK_TEXTS

if __name__ == "__main__":
    unittest.main()
