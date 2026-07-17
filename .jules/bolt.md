## 2024-07-06 - Vue 3 List Rendering Bottleneck with Timers
**Learning:** In Vue 3, frequent global reactive state changes (like a ticking countdown timer updating every second) can cause expensive, unnecessary re-evaluations and re-renders of list items rendered with `v-for`, even if the underlying list data hasn't changed.
**Action:** Utilize the `v-memo` directive on `v-for` loops (e.g., `v-memo="[item, lang]"`) to explicitly tell Vue only to re-render the list items when specific dependencies change, effectively isolating the list from unrelated global state updates.
## 2024-05-18 - Optimize JSON Extraction
**Learning:** In the Python backend, using full `json.load()` to extract a single field from large snapshot files is a major performance bottleneck for history date listing operations.
**Action:** Implemented chunk-based regex extraction (first 2KB) with strict format matching (e.g. `indent=2`) and a full `json.load()` fallback to vastly improve extraction speed while maintaining robustness.
