import time
import json
import logging
from unittest.mock import patch
import os

# mock LOG_DIR so setup_logging doesn't fail
os.environ["LOG_DIR"] = "/tmp/logs"

from content_store import load_latest_snapshot, _redis_key, load_latest_archive_snapshot, OUTPUT_ARCHIVE_DIR
from source_registry import SOURCE_DEFINITIONS
from redis_client import get_redis_client

def get_rss_feed_sequential():
    snapshots = []
    for source in SOURCE_DEFINITIONS:
        source_id = source["id"]
        try:
            snapshot, served_from = load_latest_snapshot(source_id)
            if snapshot:
                snapshots.append(snapshot)
        except Exception as e:
            pass
    return snapshots

def get_rss_feed_mget():
    # New MGET implementation
    source_ids = [s["id"] for s in SOURCE_DEFINITIONS]
    results = {}
    redis_client = get_redis_client()

    if redis_client:
        keys = [_redis_key(sid) for sid in source_ids]
        try:
            raw_values = redis_client.mget(keys)
            for i, raw_value in enumerate(raw_values):
                if raw_value:
                    if isinstance(raw_value, bytes):
                        raw_value = raw_value.decode("utf-8")
                    results[source_ids[i]] = (json.loads(raw_value), "redis")
        except Exception:
            pass

    snapshots = []
    for source in SOURCE_DEFINITIONS:
        source_id = source["id"]
        snapshot, served_from = results.get(source_id, (None, "empty"))
        if not snapshot:
            snapshot = load_latest_archive_snapshot(source_id, OUTPUT_ARCHIVE_DIR)
            if snapshot:
                served_from = "archive"
            else:
                served_from = "empty"
        if snapshot:
            snapshots.append(snapshot)

    return snapshots


def setup_mock_data():
    client = get_redis_client()
    if not client:
        print("No Redis client available.")
        return False

    for source in SOURCE_DEFINITIONS:
        sid = source["id"]
        snapshot = {
            "generated_at": "2023-10-10T10:00:00",
            "source": source,
            "item_count": 10,
            "items": [{"title": f"Test {i}", "link": f"http://example.com/{i}"} for i in range(10)]
        }
        client.setex(f"github-trending:source:{sid}:latest", 3600, json.dumps(snapshot))
    return True

if __name__ == "__main__":
    if setup_mock_data():
        iterations = 100

        start = time.time()
        for _ in range(iterations):
            get_rss_feed_sequential()
        seq_time = time.time() - start

        start = time.time()
        for _ in range(iterations):
            get_rss_feed_mget()
        mget_time = time.time() - start

        print(f"Sequential Time (100 iters): {seq_time:.4f}s")
        print(f"MGET Time (100 iters): {mget_time:.4f}s")
        if mget_time > 0:
            print(f"Speedup: {seq_time / mget_time:.2f}x")
