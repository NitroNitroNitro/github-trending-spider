## 2024-07-06 - Vue 3 List Rendering Bottleneck with Timers
**Learning:** In Vue 3, frequent global reactive state changes (like a ticking countdown timer updating every second) can cause expensive, unnecessary re-evaluations and re-renders of list items rendered with `v-for`, even if the underlying list data hasn't changed.
**Action:** Utilize the `v-memo` directive on `v-for` loops (e.g., `v-memo="[item, lang]"`) to explicitly tell Vue only to re-render the list items when specific dependencies change, effectively isolating the list from unrelated global state updates.

## 2024-05-23 - JSON parsing bottleneck for historical dates
**Learning:** Fully parsing large JSON snapshot files with `json.load()` just to extract `item_count` in `list_recent_history_dates` causes unnecessary CPU usage and slows down the API response when iterating over 7 days of 9 sources (63 files).
**Action:** Extract top-level scalar fields (like `item_count`) from large JSON files by reading small chunks (e.g., first 2KB) and using a strict regex (accounting for `indent=2`) like `re.search(r'^  "item_count":\s*(\d+)', chunk, re.MULTILINE)`. Always include a fallback to full `json.load()` in case regex fails.
