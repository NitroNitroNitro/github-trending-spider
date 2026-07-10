## 2024-07-06 - Vue 3 List Rendering Bottleneck with Timers
**Learning:** In Vue 3, frequent global reactive state changes (like a ticking countdown timer updating every second) can cause expensive, unnecessary re-evaluations and re-renders of list items rendered with `v-for`, even if the underlying list data hasn't changed.
**Action:** Utilize the `v-memo` directive on `v-for` loops (e.g., `v-memo="[item, lang]"`) to explicitly tell Vue only to re-render the list items when specific dependencies change, effectively isolating the list from unrelated global state updates.

## 2024-07-07 - Python JSON Parsing Optimization
**Learning:** Using `json.load()` to extract a single top-level field (like `item_count`) from large snapshot files causes significant CPU and memory overhead.
**Action:** Instead, read a small chunk (e.g., first 2KB) and use regex to quickly extract the value. Ensure the regex strictly accounts for `indent=2` formatting (e.g., matching exactly two spaces like `\n  "item_count":`) to avoid erroneously matching identically named keys nested within inner objects.
