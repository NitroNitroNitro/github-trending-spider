## 2026-06-30 - Fix HTML Injection / XSS in Email Builder
**Vulnerability:** HTML Injection / Cross-Site Scripting (XSS) in HTML Email Generation. Unescaped single quotes (`'`) and unescaped URLs (`url`, `hn_url`, etc) could allow injection of arbitrary HTML/JS if user-provided content (like a GitHub repo description or link) was included in the email payload.
**Learning:** `_escape_html` function did not escape single quotes, which could lead to attribute injection. Several `url` parameters were not passed through `_escape_html` before being embedded in anchor tags (`<a>`).
**Prevention:** Always escape all user-controlled input, including attributes like URLs. `&apos;` or `&#x27;` should be included in basic HTML escaping. All dynamically provided fields (e.g., `url` variables) must be explicitly passed through `_escape_html` when generating raw HTML.

## 2024-07-15 - Prevent Log Injection and DoS in Access Logs
**Vulnerability:** User-controlled inputs like `User-Agent`, `X-Forwarded-For`, and request paths were logged directly in `access_log.py`, allowing log injection attacks via `\r\n`. In addition, dynamically tracking every unique IP and path in the in-memory `_stats` dictionary without a size limit created a severe Denial of Service (DoS) risk through unbounded memory growth (e.g. from an attacker hitting random paths).
**Learning:** Even simple logging and memory-based stats collection can be targeted by malicious inputs. In-memory aggregations must always have boundaries.
**Prevention:** Sanitize all user inputs by stripping newline characters before logging, and explicitly bound the size of dynamic memory aggregations (like dictionaries) to a safe limit, aggregating overflow into an "OTHER" bucket to prevent data loss.
