## 2026-06-30 - Fix HTML Injection / XSS in Email Builder
**Vulnerability:** HTML Injection / Cross-Site Scripting (XSS) in HTML Email Generation. Unescaped single quotes (`'`) and unescaped URLs (`url`, `hn_url`, etc) could allow injection of arbitrary HTML/JS if user-provided content (like a GitHub repo description or link) was included in the email payload.
**Learning:** `_escape_html` function did not escape single quotes, which could lead to attribute injection. Several `url` parameters were not passed through `_escape_html` before being embedded in anchor tags (`<a>`).
**Prevention:** Always escape all user-controlled input, including attributes like URLs. `&apos;` or `&#x27;` should be included in basic HTML escaping. All dynamically provided fields (e.g., `url` variables) must be explicitly passed through `_escape_html` when generating raw HTML.

## 2024-07-08 - [Log Injection and Memory Exhaustion DoS in Access Logging]
**Vulnerability:** Unsanitized HTTP headers (IP, user agent) and request path were logged directly, leading to potential log injection. Additionally, unbounded tracking of distinct IPs and paths in memory could lead to a memory exhaustion DoS attack by a malicious actor providing randomized headers.
**Learning:** Even internal logging middleware must treat all HTTP request data as untrusted input. It is crucial to enforce size limits on structures storing unbounded unique string values derived from network input.
**Prevention:** Always strip line breaks (`\r`, `\n`) from logged values. Implement hard limits on the size of dictionaries used for tracking unique inputs (e.g., using a fixed size limit or an LRU cache) and log the issue if bounds are exceeded, rather than allowing unbounded growth.
