## 2026-06-30 - Fix HTML Injection / XSS in Email Builder
**Vulnerability:** HTML Injection / Cross-Site Scripting (XSS) in HTML Email Generation. Unescaped single quotes (`'`) and unescaped URLs (`url`, `hn_url`, etc) could allow injection of arbitrary HTML/JS if user-provided content (like a GitHub repo description or link) was included in the email payload.
**Learning:** `_escape_html` function did not escape single quotes, which could lead to attribute injection. Several `url` parameters were not passed through `_escape_html` before being embedded in anchor tags (`<a>`).
**Prevention:** Always escape all user-controlled input, including attributes like URLs. `&apos;` or `&#x27;` should be included in basic HTML escaping. All dynamically provided fields (e.g., `url` variables) must be explicitly passed through `_escape_html` when generating raw HTML.
## 2025-02-28 - Sanitize Log Inputs
**Vulnerability:** Access logs were susceptible to log injection due to missing newline sanitization on headers and path.
**Learning:** Using `replace('\n', '')` on external inputs limits arbitrary line forgery, but requires careful cast to `str` and handling `None` to prevent `AttributeError`. A naive memory exhaustion fix limits new valid IPs, and should be carefully approached.
**Prevention:** Always cast HTTP headers and path to strings and sanitize control characters before logging to prevent CRLF injection.
