## 2026-06-30 - Fix HTML Injection / XSS in Email Builder
**Vulnerability:** HTML Injection / Cross-Site Scripting (XSS) in HTML Email Generation. Unescaped single quotes (`'`) and unescaped URLs (`url`, `hn_url`, etc) could allow injection of arbitrary HTML/JS if user-provided content (like a GitHub repo description or link) was included in the email payload.
**Learning:** `_escape_html` function did not escape single quotes, which could lead to attribute injection. Several `url` parameters were not passed through `_escape_html` before being embedded in anchor tags (`<a>`).
**Prevention:** Always escape all user-controlled input, including attributes like URLs. `&apos;` or `&#x27;` should be included in basic HTML escaping. All dynamically provided fields (e.g., `url` variables) must be explicitly passed through `_escape_html` when generating raw HTML.

## 2026-07-19 - Fix Log Injection and Memory Exhaustion DoS in Access Logging
**Vulnerability:** Log Injection vulnerabilities via unsanitized inputs (headers, paths) and a Memory Exhaustion Denial of Service (DoS) due to unbounded `defaultdict` growth for tracking IP addresses and endpoints.
**Learning:** Python's standard `logging` module does not automatically escape newlines (`\r` and `\n`), which allows malicious actors to forge log entries. Unbounded `defaultdict` sizes can crash the application when tracking millions of spoofed unique IPs or request paths.
**Prevention:** Always sanitize user-supplied data (such as HTTP headers and paths) by stripping out `\r` and `\n` characters prior to logging. To prevent memory leaks, limit the maximum number of items in tracking caches or dicts; gracefully handle overflows by grouping subsequent unknown keys into a generic "<其他>" key.
