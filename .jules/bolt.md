## 2024-07-06 - Vue 3 List Rendering Bottleneck with Timers
**Learning:** In Vue 3, frequent global reactive state changes (like a ticking countdown timer updating every second) can cause expensive, unnecessary re-evaluations and re-renders of list items rendered with `v-for`, even if the underlying list data hasn't changed.
**Action:** Utilize the `v-memo` directive on `v-for` loops (e.g., `v-memo="[item, lang]"`) to explicitly tell Vue only to re-render the list items when specific dependencies change, effectively isolating the list from unrelated global state updates.

## 2024-07-06 - Optimized JSON Parsing for Large Snapshot Files
**Learning:** Using `json.load()` to extract a single top-level field from large snapshot files creates significant CPU and memory overhead.
**Action:** Read a small chunk (e.g., first 2KB) and use regex to quickly extract the value. Ensure the regex strictly accounts for the `indent=2` formatting of snapshot files (e.g., matching exactly two spaces like `\n  "key"`) to avoid erroneously matching identically named keys nested within inner objects.
