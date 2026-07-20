## 2026-06-30 - Fix HTML Injection / XSS in Email Builder
**Vulnerability:** HTML Injection / Cross-Site Scripting (XSS) in HTML Email Generation. Unescaped single quotes (`'`) and unescaped URLs (`url`, `hn_url`, etc) could allow injection of arbitrary HTML/JS if user-provided content (like a GitHub repo description or link) was included in the email payload.
**Learning:** `_escape_html` function did not escape single quotes, which could lead to attribute injection. Several `url` parameters were not passed through `_escape_html` before being embedded in anchor tags (`<a>`).
**Prevention:** Always escape all user-controlled input, including attributes like URLs. `&apos;` or `&#x27;` should be included in basic HTML escaping. All dynamically provided fields (e.g., `url` variables) must be explicitly passed through `_escape_html` when generating raw HTML.

## 2026-06-30 - Fix Log Injection and Memory Exhaustion DoS in Access Logs
**Vulnerability:** Log Injection via `\r\n` characters in headers/paths, and Memory Exhaustion DoS by unbounded state dictionaries logging IP counts and Paths.
**Learning:** Python's standard `logging` does not escape newlines automatically. Also, unbounded dictionaries in `access_log.py` can be exhausted by malicious actors, leading to OOM. We must avoid naive limits that silently drop data.
**Prevention:** Explicitly strip `\r` and `\n` using `_sanitize` before passing any external input to `logger.info`. Flush dictionaries safely with `_dump_stats_unlocked` under the existing lock when a threshold is met (e.g. 10,000 items) rather than dropping entries entirely.
