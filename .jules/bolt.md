## 2024-07-06 - Vue 3 List Rendering Bottleneck with Timers
**Learning:** In Vue 3, frequent global reactive state changes (like a ticking countdown timer updating every second) can cause expensive, unnecessary re-evaluations and re-renders of list items rendered with `v-for`, even if the underlying list data hasn't changed.
**Action:** Utilize the `v-memo` directive on `v-for` loops (e.g., `v-memo="[item, lang]"`) to explicitly tell Vue only to re-render the list items when specific dependencies change, effectively isolating the list from unrelated global state updates.
## 2024-07-14 - Fast Extraction of JSON Metadata via Regex Chunking
**Learning:** In the Python backend, loading full snapshot JSON files (which can be very large) solely to extract a single top-level field like `item_count` creates a significant I/O and memory bottleneck.
**Action:** Use a regex match on a small read chunk (e.g., first 2KB) to quickly extract the required metadata, accounting for the `indent=2` JSON formatting (`\n  "key"`). Always include a fallback to `json.load()` since chunk-based regex can be brittle and miss the key.
