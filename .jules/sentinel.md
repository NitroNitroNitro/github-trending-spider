## 2026-06-30 - Fix HTML Injection / XSS in Email Builder
**Vulnerability:** HTML Injection / Cross-Site Scripting (XSS) in HTML Email Generation. Unescaped single quotes (`'`) and unescaped URLs (`url`, `hn_url`, etc) could allow injection of arbitrary HTML/JS if user-provided content (like a GitHub repo description or link) was included in the email payload.
**Learning:** `_escape_html` function did not escape single quotes, which could lead to attribute injection. Several `url` parameters were not passed through `_escape_html` before being embedded in anchor tags (`<a>`).
**Prevention:** Always escape all user-controlled input, including attributes like URLs. `&apos;` or `&#x27;` should be included in basic HTML escaping. All dynamically provided fields (e.g., `url` variables) must be explicitly passed through `_escape_html` when generating raw HTML.

## 2024-07-11 - Fix Log Injection and DoS in Access Log Middleware
**Vulnerability:** Unsanitized user inputs (IP, path, User-Agent) logged could lead to Log Injection. Unbounded dictionary keys in `_stats["IP计数"]` and `_stats["接口计数"]` could lead to memory exhaustion DoS attacks by malicious actors providing arbitrary IP addresses or paths.
**Learning:** Even internal logging mechanisms require input sanitization. Memory-bound operations based on user input must have upper bounds to prevent abuse.
**Prevention:** Always sanitize input by removing newline characters before logging. Limit the maximum size of data structures driven by user inputs.
