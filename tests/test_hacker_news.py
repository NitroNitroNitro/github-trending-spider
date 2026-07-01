# -*- coding: utf-8 -*-
"""
Hacker News 模块测试用例
"""

import sys
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, ".")

from hacker_news import _apply_hn_summaries

class TestApplyHNSummaries(unittest.TestCase):
    def setUp(self):
        self.stories = [
            {"id": 1, "title": "Story 1"},
            {"id": 2, "title": "Story 2"},
            {"id": 3, "title": "Story 3"},
        ]

    def test_apply_hn_summaries_success(self):
        """测试正常情况：所有故事都成功分配了摘要"""
        summaries = [
            {"index": 1, "summary": "Summary 1"},
            {"index": 2, "summary": "Summary 2"},
            {"index": 3, "summary": "Summary 3"},
        ]
        missing_indices = _apply_hn_summaries(self.stories, summaries)

        self.assertEqual(missing_indices, [])
        self.assertEqual(self.stories[0]["ai_summary"], "Summary 1")
        self.assertEqual(self.stories[1]["ai_summary"], "Summary 2")
        self.assertEqual(self.stories[2]["ai_summary"], "Summary 3")

    def test_apply_hn_summaries_empty_summaries(self):
        """测试摘要为空列表的情况"""
        missing_indices = _apply_hn_summaries(self.stories, [])
        self.assertEqual(missing_indices, [0, 1, 2])
        for story in self.stories:
            self.assertNotIn("ai_summary", story)

    def test_apply_hn_summaries_none_summaries(self):
        """测试摘要为 None 的情况"""
        missing_indices = _apply_hn_summaries(self.stories, None)
        self.assertEqual(missing_indices, [0, 1, 2])
        for story in self.stories:
            self.assertNotIn("ai_summary", story)

    def test_apply_hn_summaries_partial(self):
        """测试部分摘要缺失的情况"""
        summaries = [
            {"index": 1, "summary": "Summary 1"},
            {"index": 3, "summary": "Summary 3"},
        ]
        missing_indices = _apply_hn_summaries(self.stories, summaries)

        self.assertEqual(missing_indices, [1])
        self.assertEqual(self.stories[0]["ai_summary"], "Summary 1")
        self.assertNotIn("ai_summary", self.stories[1])
        self.assertEqual(self.stories[2]["ai_summary"], "Summary 3")

    def test_apply_hn_summaries_invalid_index_out_of_bounds(self):
        """测试摘要 index 超出范围的情况"""
        summaries = [
            {"index": 0, "summary": "Invalid (0 mapped to -1)"},
            {"index": 4, "summary": "Out of bounds (index 4)"},
            {"index": 1, "summary": "Summary 1"},
        ]
        missing_indices = _apply_hn_summaries(self.stories, summaries)

        self.assertEqual(missing_indices, [1, 2])
        self.assertEqual(self.stories[0]["ai_summary"], "Summary 1")

    def test_apply_hn_summaries_missing_index_key(self):
        """测试摘要缺少 index 键的情况"""
        # get("index", 0) defaults to 0, maps to -1
        summaries = [
            {"summary": "Missing index key"},
            {"index": 2, "summary": "Summary 2"},
        ]
        missing_indices = _apply_hn_summaries(self.stories, summaries)

        self.assertEqual(missing_indices, [0, 2])
        self.assertNotIn("ai_summary", self.stories[0])
        self.assertEqual(self.stories[1]["ai_summary"], "Summary 2")

    def test_apply_hn_summaries_empty_summary_string(self):
        """测试摘要字符串为空或只包含空白字符的情况"""
        summaries = [
            {"index": 1, "summary": ""},
            {"index": 2, "summary": "   "},
            {"index": 3, "summary": "Summary 3"},
        ]
        missing_indices = _apply_hn_summaries(self.stories, summaries)

        self.assertEqual(missing_indices, [0, 1])
        self.assertNotIn("ai_summary", self.stories[0])
        self.assertNotIn("ai_summary", self.stories[1])
        self.assertEqual(self.stories[2]["ai_summary"], "Summary 3")

if __name__ == "__main__":
    unittest.main()
