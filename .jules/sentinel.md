## 2026-06-30 - Fix HTML Injection / XSS in Email Builder
**Vulnerability:** HTML Injection / Cross-Site Scripting (XSS) in HTML Email Generation. Unescaped single quotes (`'`) and unescaped URLs (`url`, `hn_url`, etc) could allow injection of arbitrary HTML/JS if user-provided content (like a GitHub repo description or link) was included in the email payload.
**Learning:** `_escape_html` function did not escape single quotes, which could lead to attribute injection. Several `url` parameters were not passed through `_escape_html` before being embedded in anchor tags (`<a>`).
**Prevention:** Always escape all user-controlled input, including attributes like URLs. `&apos;` or `&#x27;` should be included in basic HTML escaping. All dynamically provided fields (e.g., `url` variables) must be explicitly passed through `_escape_html` when generating raw HTML.

## 2026-07-09 - Fix Log Injection and Memory DoS in API Middleware
**Vulnerability:** CRLF Log Injection and Memory Exhaustion (DoS). The `access_log.py` middleware directly logged un-sanitized user inputs (IP, Path, User-Agent) allowing log forging via `\r` and `\n`. It also stored unbounded metrics keyed by `client_ip` and `path` in `_stats["IP计数"]` and `_stats["接口计数"]`, allowing attackers to cause an Out-Of-Memory (OOM) crash by sending high-cardinality requests.
**Learning:** Even simple telemetry features can become security liabilities if user input is trusted. In-memory aggregations without limits are highly susceptible to DoS attacks.
**Prevention:** Always strip `\r` and `\n` from untrusted strings before writing them to logs. Always enforce maximum size boundaries (e.g., `len(dict) < 10000`) on any in-memory data structure that keys off of user-supplied data (like IP or URL paths).
