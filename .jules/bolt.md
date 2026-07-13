## 2024-07-06 - Vue 3 List Rendering Bottleneck with Timers
**Learning:** In Vue 3, frequent global reactive state changes (like a ticking countdown timer updating every second) can cause expensive, unnecessary re-evaluations and re-renders of list items rendered with `v-for`, even if the underlying list data hasn't changed.
**Action:** Utilize the `v-memo` directive on `v-for` loops (e.g., `v-memo="[item, lang]"`) to explicitly tell Vue only to re-render the list items when specific dependencies change, effectively isolating the list from unrelated global state updates.
## 2024-07-13 - Optimize JSON Parsing with Chunking
**Learning:** Full `json.load()` on large archive snapshots to extract just the `item_count` causes significant I/O and parsing overhead. Using regex on a small chunk (e.g., first 2KB) provides a 14x speedup, but requires an exact structural fallback as chunk regex is brittle.
**Action:** Prioritize regex extraction on chunks for metadata in large uniform files, but ALWAYS implement a robust `json.load()` fallback.
