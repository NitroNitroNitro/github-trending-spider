## 2026-06-30 - Fix HTML Injection / XSS in Email Builder
**Vulnerability:** HTML Injection / Cross-Site Scripting (XSS) in HTML Email Generation. Unescaped single quotes (`'`) and unescaped URLs (`url`, `hn_url`, etc) could allow injection of arbitrary HTML/JS if user-provided content (like a GitHub repo description or link) was included in the email payload.
**Learning:** `_escape_html` function did not escape single quotes, which could lead to attribute injection. Several `url` parameters were not passed through `_escape_html` before being embedded in anchor tags (`<a>`).
**Prevention:** Always escape all user-controlled input, including attributes like URLs. `&apos;` or `&#x27;` should be included in basic HTML escaping. All dynamically provided fields (e.g., `url` variables) must be explicitly passed through `_escape_html` when generating raw HTML.

## 2026-06-30 - Fix Log Injection and Memory Exhaustion in Access Logs
**Vulnerability:** Unsanitized user inputs (`User-Agent`, `X-Forwarded-For`, URL paths) logged via `logger.info` in `access_log.py` allowed log injection (CRLF injection) attacks. Further, unbounded tracking of unique IPs and paths in the memory structure `_stats` created a Denial of Service (DoS) risk via memory exhaustion (e.g. by spoofing many IPs).
**Learning:** Log injection can obscure malicious activity. Unbounded memory growth in middleware is an easy DoS vector.
**Prevention:** Always strip `\r` and `\n` characters from variables derived from untrusted client input before writing to logs. Always enforce strict upper bounds (e.g., `10000` items) on memory dictionaries tracking dynamic HTTP requests data (like unique IPs or requested paths).
