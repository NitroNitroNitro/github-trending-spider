# -*- coding: utf-8 -*-
"""
Tests for source registry utilities.
"""

import sys
import unittest

sys.path.insert(0, ".")

from source_registry import (
    get_source_by_id,
    get_source_by_content_source,
    SOURCE_GITHUB_DAILY_ID,
)


class TestSourceRegistryUtilities(unittest.TestCase):
    def test_get_source_by_id_valid(self):
        """Test getting a valid source by ID."""
        source = get_source_by_id(SOURCE_GITHUB_DAILY_ID)
        self.assertIsNotNone(source)
        self.assertEqual(source["id"], SOURCE_GITHUB_DAILY_ID)
        self.assertEqual(source["name"], "GitHub Daily")

    def test_get_source_by_id_invalid(self):
        """Test getting an invalid source by ID returns None."""
        source = get_source_by_id("invalid-source-id")
        self.assertIsNone(source)

    def test_get_source_by_content_source_valid(self):
        """Test getting a valid source by content source."""
        source = get_source_by_content_source("GitHub Trending Daily")
        self.assertIsNotNone(source)
        self.assertEqual(source["content_source"], "GitHub Trending Daily")
        self.assertEqual(source["id"], SOURCE_GITHUB_DAILY_ID)

    def test_get_source_by_content_source_invalid(self):
        """Test getting an invalid source by content source returns None."""
        source = get_source_by_content_source("Invalid Content Source")
        self.assertIsNone(source)


if __name__ == "__main__":
    unittest.main()
