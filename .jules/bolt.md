## 2024-07-06 - Vue 3 List Rendering Bottleneck with Timers
**Learning:** In Vue 3, frequent global reactive state changes (like a ticking countdown timer updating every second) can cause expensive, unnecessary re-evaluations and re-renders of list items rendered with `v-for`, even if the underlying list data hasn't changed.
**Action:** Utilize the `v-memo` directive on `v-for` loops (e.g., `v-memo="[item, lang]"`) to explicitly tell Vue only to re-render the list items when specific dependencies change, effectively isolating the list from unrelated global state updates.

## 2024-07-16 - HTTP Connection Pooling for Concurrent API Requests
**Learning:** Using `requests.get` inside a `ThreadPoolExecutor` without a shared `requests.Session` creates a new TCP connection and performs a new TLS handshake for every single API request. For high-volume concurrent requests to the same host (like fetching hundreds of Hacker News items), this overhead is significant.
**Action:** When making concurrent requests to the same host using `requests` and a ThreadPool, always instantiate a `requests.Session()`, configure its connection pool size (`pool_connections`, `pool_maxsize`) to match the max workers using an `HTTPAdapter`, and pass the session to the worker threads to reuse connections.
