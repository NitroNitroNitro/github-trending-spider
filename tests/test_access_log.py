# -*- coding: utf-8 -*-
"""
Tests for access_log.py module.
"""

import sys
import unittest
from unittest.mock import patch, call
from collections import defaultdict

sys.path.insert(0, ".")

from access_log import _reset_stats, _dump_stats, _stats


class TestAccessLog(unittest.TestCase):
    def setUp(self):
        # Reset stats before each test to ensure a clean state
        _reset_stats()

    def test_reset_stats(self):
        # Setup: populate stats with dummy data
        _stats["总请求数"] = 10
        _stats["错误请求数"] = 2
        _stats["累计耗时ms"] = 500
        _stats["IP计数"]["127.0.0.1"] = 5
        _stats["接口计数"]["/api/test"] = 10
        _stats["统计起始时间"] = "00:00"

        # Execute
        _reset_stats()

        # Assert: verify stats are reset
        self.assertEqual(_stats["总请求数"], 0)
        self.assertEqual(_stats["错误请求数"], 0)
        self.assertEqual(_stats["累计耗时ms"], 0)
        self.assertEqual(len(_stats["IP计数"]), 0)
        self.assertEqual(len(_stats["接口计数"]), 0)
        # 统计起始时间 should be updated to current time, but let's just check it's not "00:00" or check type
        self.assertNotEqual(_stats["统计起始时间"], "00:00")
        self.assertIsInstance(_stats["统计起始时间"], str)
        self.assertEqual(len(_stats["统计起始时间"]), 5)  # "HH:MM"

    @patch("access_log.logger.info")
    @patch("access_log.datetime")
    def test_dump_stats_with_data(self, mock_datetime, mock_logger_info):
        # Setup mocked time
        mock_datetime.now.return_value.strftime.return_value = "12:00"

        # Setup: populate stats
        _stats["总请求数"] = 100
        _stats["错误请求数"] = 5
        _stats["累计耗时ms"] = 1000  # avg = 10ms
        _stats["IP计数"]["192.168.1.1"] = 60
        _stats["IP计数"]["192.168.1.2"] = 40
        _stats["接口计数"]["/api/1"] = 80
        _stats["接口计数"]["/api/2"] = 20
        _stats["统计起始时间"] = "11:00"

        # Execute
        _dump_stats()

        # Assert: log called with correct values
        self.assertEqual(mock_logger_info.call_count, 3)
        mock_logger_info.assert_any_call(
            "[统计] 时段=%s~%s | 总请求=%d | 独立IP数=%d | 平均耗时=%dms | 错误数=%d",
            "11:00", "12:00", 100, 2, 10, 5
        )
        mock_logger_info.assert_any_call("[统计] 热门接口: %s", "/api/1=80次, /api/2=20次")
        mock_logger_info.assert_any_call("[统计] 活跃IP: %s", "192.168.1.1=60次, 192.168.1.2=40次")

        # Assert: stats are reset
        self.assertEqual(_stats["总请求数"], 0)
        self.assertEqual(len(_stats["IP计数"]), 0)

    @patch("access_log.logger.info")
    def test_dump_stats_empty(self, mock_logger_info):
        # Setup
        _stats["总请求数"] = 0
        _stats["统计起始时间"] = "10:00"

        # Execute
        _dump_stats()

        # Assert
        mock_logger_info.assert_not_called()
        self.assertEqual(_stats["总请求数"], 0)
        self.assertNotEqual(_stats["统计起始时间"], "10:00")  # Resets to current time

if __name__ == "__main__":
    unittest.main()
