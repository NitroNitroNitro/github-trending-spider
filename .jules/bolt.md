## 2024-07-06 - Vue 3 List Rendering Bottleneck with Timers
**Learning:** In Vue 3, frequent global reactive state changes (like a ticking countdown timer updating every second) can cause expensive, unnecessary re-evaluations and re-renders of list items rendered with `v-for`, even if the underlying list data hasn't changed.
**Action:** Utilize the `v-memo` directive on `v-for` loops (e.g., `v-memo="[item, lang]"`) to explicitly tell Vue only to re-render the list items when specific dependencies change, effectively isolating the list from unrelated global state updates.

## 2024-05-24 - Strict Regex Formatting for Chunked JSON Parsing
**Learning:** When using regex on file chunks to avoid full `json.load()` parsing (e.g. finding top-level keys like `item_count` in large snapshot arrays), the regex must be tightly bound to the expected indentation format to prevent false positives. If the JSON is serialized with `indent=2`, nested properties (e.g., `"item_count"` inside an item object) will have more indentation.
**Action:** When applying such regex chunking optimizations, strictly enforce the formatting constraint in the regex (e.g., `\n  "item_count"` instead of `\n\s*"item_count"`) and add tests ensuring nested occurrences are correctly bypassed.
