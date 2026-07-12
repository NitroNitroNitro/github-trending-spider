## 2026-06-30 - Fix HTML Injection / XSS in Email Builder
**Vulnerability:** HTML Injection / Cross-Site Scripting (XSS) in HTML Email Generation. Unescaped single quotes (`'`) and unescaped URLs (`url`, `hn_url`, etc) could allow injection of arbitrary HTML/JS if user-provided content (like a GitHub repo description or link) was included in the email payload.
**Learning:** `_escape_html` function did not escape single quotes, which could lead to attribute injection. Several `url` parameters were not passed through `_escape_html` before being embedded in anchor tags (`<a>`).
**Prevention:** Always escape all user-controlled input, including attributes like URLs. `&apos;` or `&#x27;` should be included in basic HTML escaping. All dynamically provided fields (e.g., `url` variables) must be explicitly passed through `_escape_html` when generating raw HTML.

## 2025-02-12 - Fix Log Injection and Memory Exhaustion DoS in Access Log Middleware
**Vulnerability:** Log Injection (CRLF) and Memory Exhaustion Denial of Service (DoS) in API access logging.
**Learning:** User-controlled headers (`User-Agent`, `X-Forwarded-For`) and request paths were logged and added to unbounded memory dictionaries (`_stats["IP计数"]`, `_stats["接口计数"]`) without sanitization or size limits. This allowed attackers to inject newlines to forge logs and spam unique paths/IPs to exhaust server memory.
**Prevention:** Always sanitize strings derived from external requests (e.g., by stripping `\r` and `\n`) before logging them. Enforce an upper bound on the size of any in-memory tracking structure (e.g., dictionaries, lists) that stores data derived from user input.
