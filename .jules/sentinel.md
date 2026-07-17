## 2026-06-30 - Fix HTML Injection / XSS in Email Builder
**Vulnerability:** HTML Injection / Cross-Site Scripting (XSS) in HTML Email Generation. Unescaped single quotes (`'`) and unescaped URLs (`url`, `hn_url`, etc) could allow injection of arbitrary HTML/JS if user-provided content (like a GitHub repo description or link) was included in the email payload.
**Learning:** `_escape_html` function did not escape single quotes, which could lead to attribute injection. Several `url` parameters were not passed through `_escape_html` before being embedded in anchor tags (`<a>`).
**Prevention:** Always escape all user-controlled input, including attributes like URLs. `&apos;` or `&#x27;` should be included in basic HTML escaping. All dynamically provided fields (e.g., `url` variables) must be explicitly passed through `_escape_html` when generating raw HTML.

## 2026-07-17 - Prevent Log Injection Vulnerability
**Vulnerability:** User-controlled input such as `X-Forwarded-For` header, URL `path`, and `User-Agent` header were logged directly without sanitization. An attacker could inject newline characters `\n` or `\r` to forge log entries or cause log corruption.
**Learning:** Python's `logging` module does not automatically escape or remove newlines in interpolated strings. User input should always be sanitized before logging.
**Prevention:** Always strip `\n` and `\r` from user-provided inputs such as headers or URL paths before they are written to the application's logs, and handle `None` values gracefully.
