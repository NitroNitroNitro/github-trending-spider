## 2024-05-24 - Initial File
**Learning:** Initializing bolt journal.
**Action:** Use this file to record critical performance learnings for this codebase.
## 2024-05-24 - Fast JSON regex extraction
**Learning:** The Python backend's history date listing loaded entire JSON archive files just to fetch `item_count`, leading to unnecessary memory overhead.
**Action:** Used regex on the first 2KB of the file chunk to quickly extract `item_count` by matching exactly two spaces `\n  "item_count"` to respect the JSON indentation, drastically reducing load time.
