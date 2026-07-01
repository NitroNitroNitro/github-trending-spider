# -*- coding: utf-8 -*-
"""
Main utility function tests.
"""

import sys
import unittest
from datetime import datetime

sys.path.insert(0, ".")

from main import (  # noqa: E402
    _parse_email_send_times,
    _normalize_scheduled_time,
    _parse_recipient_list,
    _parse_mail_to_by_time,
)


class TestMainUtils(unittest.TestCase):
    def test_parse_email_send_times(self):
        # Valid cases
        self.assertEqual(_parse_email_send_times("08:30, 14:00"), {"08:30", "14:00"})
        self.assertEqual(_parse_email_send_times("08:30,14:00"), {"08:30", "14:00"})
        self.assertEqual(_parse_email_send_times(" 08:30 , 14:00 "), {"08:30", "14:00"})
        self.assertEqual(_parse_email_send_times("08:30"), {"08:30"})
        self.assertEqual(_parse_email_send_times(""), set())
        self.assertEqual(_parse_email_send_times(None), set())

        # Invalid cases
        with self.assertRaises(ValueError):
            _parse_email_send_times("24:00")
        with self.assertRaises(ValueError):
            _parse_email_send_times("-1:00")
        with self.assertRaises(ValueError):
            _parse_email_send_times("08:60")
        with self.assertRaises(ValueError):
            _parse_email_send_times("08:-1")
        with self.assertRaises(ValueError):
            _parse_email_send_times("0830")
        with self.assertRaises(ValueError):
            _parse_email_send_times("abc")
        with self.assertRaises(ValueError):
            _parse_email_send_times("08:30,24:00")

    def test_normalize_scheduled_time(self):
        self.assertEqual(_normalize_scheduled_time(None), "")

        # Test datetime object
        dt = datetime(2023, 1, 1, 8, 30)
        self.assertEqual(_normalize_scheduled_time(dt), "08:30")

        # Test strings
        self.assertEqual(_normalize_scheduled_time("08:30"), "08:30")
        self.assertEqual(_normalize_scheduled_time("08:30:00"), "08:30")
        self.assertEqual(_normalize_scheduled_time(" 08:30 "), "08:30")

    def test_parse_recipient_list(self):
        # Valid strings
        self.assertEqual(_parse_recipient_list("a@test.com, b@test.com"), ["a@test.com", "b@test.com"])
        self.assertEqual(_parse_recipient_list("a@test.com,b@test.com"), ["a@test.com", "b@test.com"])
        self.assertEqual(_parse_recipient_list(" a@test.com , b@test.com "), ["a@test.com", "b@test.com"])
        self.assertEqual(_parse_recipient_list("a@test.com"), ["a@test.com"])
        self.assertEqual(_parse_recipient_list(""), [])
        self.assertEqual(_parse_recipient_list("   "), [])
        self.assertEqual(_parse_recipient_list(" , "), [])

        # Valid lists
        self.assertEqual(_parse_recipient_list(["a@test.com", "b@test.com"]), ["a@test.com", "b@test.com"])
        self.assertEqual(_parse_recipient_list([" a@test.com ", " b@test.com "]), ["a@test.com", "b@test.com"])
        self.assertEqual(_parse_recipient_list(["a@test.com", ""]), ["a@test.com"])
        self.assertEqual(_parse_recipient_list([]), [])

        # Invalid or other types
        self.assertEqual(_parse_recipient_list(None), [])
        self.assertEqual(_parse_recipient_list(123), [])

    def test_parse_mail_to_by_time(self):
        # Valid cases
        valid_json = '{"08:30": "a@test.com, b@test.com", "14:00": ["c@test.com", "d@test.com"]}'
        expected = {
            "08:30": ["a@test.com", "b@test.com"],
            "14:00": ["c@test.com", "d@test.com"]
        }
        self.assertEqual(_parse_mail_to_by_time(valid_json), expected)

        self.assertEqual(_parse_mail_to_by_time(""), {})
        self.assertEqual(_parse_mail_to_by_time(None), {})

        # Invalid time formats inside valid JSON
        invalid_time_json = '{"08:30,14:00": "a@test.com"}'
        with self.assertRaises(ValueError):
            _parse_mail_to_by_time(invalid_time_json)

        invalid_time_format_json = '{"24:00": "a@test.com"}'
        with self.assertRaises(ValueError):
            _parse_mail_to_by_time(invalid_time_format_json)

        # Invalid JSON
        with self.assertRaises(ValueError): # Should raise ValueError according to implementation "MAIL_TO_BY_TIME 必须是 JSON 对象"
            _parse_mail_to_by_time("[]")

        import json
        with self.assertRaises(json.JSONDecodeError):
            _parse_mail_to_by_time("invalid json")


if __name__ == "__main__":
    unittest.main()
