# -*- coding: utf-8 -*-
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, ".")

import access_log
from access_log import _reset_stats, _dump_stats


class TestAccessLog(unittest.TestCase):
    def setUp(self):
        _reset_stats()

    def test_reset_stats(self):
        access_log._stats["总请求数"] = 100
        access_log._stats["错误请求数"] = 5
        access_log._stats["累计耗时ms"] = 5000
        access_log._stats["IP计数"]["127.0.0.1"] = 10
        access_log._stats["接口计数"]["/api/v1/test"] = 20

        _reset_stats()

        self.assertEqual(access_log._stats["总请求数"], 0)
        self.assertEqual(access_log._stats["错误请求数"], 0)
        self.assertEqual(access_log._stats["累计耗时ms"], 0)
        self.assertEqual(len(access_log._stats["IP计数"]), 0)
        self.assertEqual(len(access_log._stats["接口计数"]), 0)

    @patch("access_log.logger.info")
    def test_dump_stats_zero_total(self, mock_logger_info):
        access_log._stats["总请求数"] = 0
        # Modify some other stat to ensure _reset_stats is called
        access_log._stats["错误请求数"] = 1

        _dump_stats()

        # Logger should not be called if total is 0
        mock_logger_info.assert_not_called()
        # _reset_stats should be called, so this should be reset to 0
        self.assertEqual(access_log._stats["错误请求数"], 0)

    @patch("access_log.logger.info")
    def test_dump_stats_with_data(self, mock_logger_info):
        access_log._stats["总请求数"] = 100
        access_log._stats["错误请求数"] = 5
        access_log._stats["累计耗时ms"] = 5000
        access_log._stats["IP计数"]["127.0.0.1"] = 60
        access_log._stats["IP计数"]["192.168.1.1"] = 40
        access_log._stats["接口计数"]["/api/v1/test"] = 80
        access_log._stats["接口计数"]["/api/v1/other"] = 20

        _dump_stats()

        self.assertTrue(mock_logger_info.called)

        # _reset_stats should be called after logging
        self.assertEqual(access_log._stats["总请求数"], 0)
        self.assertEqual(access_log._stats["错误请求数"], 0)
        self.assertEqual(access_log._stats["累计耗时ms"], 0)
        self.assertEqual(len(access_log._stats["IP计数"]), 0)
        self.assertEqual(len(access_log._stats["接口计数"]), 0)

if __name__ == "__main__":
    unittest.main()
