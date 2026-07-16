## 2024-07-06 - Vue 3 List Rendering Bottleneck with Timers
**Learning:** In Vue 3, frequent global reactive state changes (like a ticking countdown timer updating every second) can cause expensive, unnecessary re-evaluations and re-renders of list items rendered with `v-for`, even if the underlying list data hasn't changed.
**Action:** Utilize the `v-memo` directive on `v-for` loops (e.g., `v-memo="[item, lang]"`) to explicitly tell Vue only to re-render the list items when specific dependencies change, effectively isolating the list from unrelated global state updates.

## 2024-07-26 - JSON parsing bottleneck on large snapshots
**Learning:** Calling `json.load()` on multi-megabyte JSON arrays just to extract a single top-level metadata key (e.g., `"item_count"`) creates a massive and unnecessary performance bottleneck. Standard JSON parsers must build the entire dictionary in memory before you can access that single key.
**Action:** Use a fast-path chunk reader with a precise regular expression (e.g., `re.MULTILINE` with `^` anchor to match indentation) on the first 2KB of the file to extract the key instantly. Always implement a full `json.load()` fallback in case the formatting changes or the regex fails.
