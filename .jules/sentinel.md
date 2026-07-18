## 2026-06-30 - Fix HTML Injection / XSS in Email Builder
**Vulnerability:** HTML Injection / Cross-Site Scripting (XSS) in HTML Email Generation. Unescaped single quotes (`'`) and unescaped URLs (`url`, `hn_url`, etc) could allow injection of arbitrary HTML/JS if user-provided content (like a GitHub repo description or link) was included in the email payload.
**Learning:** `_escape_html` function did not escape single quotes, which could lead to attribute injection. Several `url` parameters were not passed through `_escape_html` before being embedded in anchor tags (`<a>`).
**Prevention:** Always escape all user-controlled input, including attributes like URLs. `&apos;` or `&#x27;` should be included in basic HTML escaping. All dynamically provided fields (e.g., `url` variables) must be explicitly passed through `_escape_html` when generating raw HTML.

## 2025-02-23 - Log Injection and Memory DoS in AccessLogMiddleware
**Vulnerability:** User-controlled input (headers, path) was directly passed to `logger.info`, allowing log injection via `\r` and `\n`. Furthermore, the `_stats` dictionary grew indefinitely with unique client IPs or paths, opening up a memory exhaustion DoS vulnerability.
**Learning:** Python's standard `logging` module does not automatically escape newlines. Always sanitize user input before logging. Also, unbounded dictionaries in middleware are a vector for memory exhaustion.
**Prevention:** Sanitize inputs by stripping `\n` and `\r`. Implement upper bounds for dictionary sizes, aggregating excess entries into generic buckets (like `"OTHER_IPS"`) to prevent unconstrained memory growth without losing data points.
