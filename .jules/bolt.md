## 2024-07-06 - Vue 3 List Rendering Bottleneck with Timers
**Learning:** In Vue 3, frequent global reactive state changes (like a ticking countdown timer updating every second) can cause expensive, unnecessary re-evaluations and re-renders of list items rendered with `v-for`, even if the underlying list data hasn't changed.
**Action:** Utilize the `v-memo` directive on `v-for` loops (e.g., `v-memo="[item, lang]"`) to explicitly tell Vue only to re-render the list items when specific dependencies change, effectively isolating the list from unrelated global state updates.
## 2024-10-24 - JSON Parsing Overhead for Metadata
**Learning:** Fully parsing large JSON snapshot files (e.g., via `json.load()`) solely to extract a single top-level metadata field like `item_count` is a significant performance bottleneck on the backend.
**Action:** Extract specific top-level metadata fields from large JSON files using regex on a small initial chunk (e.g., the first 2KB with strict indentation rules) before falling back to `json.load()` if the fast path fails.
