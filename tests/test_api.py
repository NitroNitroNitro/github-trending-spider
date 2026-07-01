# -*- coding: utf-8 -*-
"""
API endpoints tests.
"""

import sys
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

sys.path.insert(0, ".")

from api import app  # noqa: E402
from source_registry import SOURCE_DEFINITIONS  # noqa: E402


class TestApi(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health_check(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_list_sources(self):
        response = self.client.get("/api/sources")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("sources", data)
        self.assertIn("count", data)
        self.assertEqual(data["count"], len(SOURCE_DEFINITIONS))
        self.assertEqual(data["sources"], SOURCE_DEFINITIONS)

    @patch("api.load_latest_snapshot")
    def test_get_rss_feed(self, mock_load_latest):
        # Mock load_latest_snapshot to return a simple snapshot
        mock_snapshot = {
            "source": {"id": "test", "name": "Test Source"},
            "items": [{"title": "Test Item", "link": "http://test.com"}]
        }
        mock_load_latest.return_value = (mock_snapshot, "redis")

        response = self.client.get("/api/rss.xml")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.headers["content-type"].startswith("application/rss+xml"))
        self.assertIn("每日AI前沿信息".encode("utf-8"), response.content)
        self.assertIn(b"<title>Test Item</title>", response.content)

    @patch("api.list_recent_history_dates")
    def test_list_history_dates(self, mock_list_dates):
        mock_list_dates.return_value = ["2023-10-25", "2023-10-24"]
        response = self.client.get("/api/history/dates")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["count"], 2)
        self.assertEqual(data["dates"], ["2023-10-25", "2023-10-24"])

    @patch("api.load_latest_snapshot")
    def test_get_latest_source_success(self, mock_load_latest):
        mock_snapshot = {
            "source": {"id": "github-daily", "name": "GitHub Daily"},
            "items": [{"title": "Item 1", "link": "http://github.com"}],
            "generated_at": "2023-10-26T12:00:00"
        }
        mock_load_latest.return_value = (mock_snapshot, "redis")

        response = self.client.get("/api/sources/github-daily/latest")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["served_from"], "redis")
        self.assertEqual(data["generated_at"], "2023-10-26T12:00:00")
        self.assertEqual(data["item_count"], 1)
        self.assertEqual(data["items"][0]["title"], "Item 1")

    def test_get_latest_source_unknown(self):
        response = self.client.get("/api/sources/unknown-source/latest")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Unknown source"})

    @patch("api.load_latest_snapshot")
    def test_get_latest_source_empty(self, mock_load_latest):
        mock_load_latest.return_value = (None, "redis")

        response = self.client.get("/api/sources/github-daily/latest")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["served_from"], "redis")
        self.assertEqual(data["generated_at"], "")
        self.assertEqual(data["item_count"], 0)
        self.assertEqual(data["items"], [])

if __name__ == "__main__":
    unittest.main()
