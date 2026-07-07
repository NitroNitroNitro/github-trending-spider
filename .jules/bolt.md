## 2024-07-06 - Vue 3 List Rendering Bottleneck with Timers
**Learning:** In Vue 3, frequent global reactive state changes (like a ticking countdown timer updating every second) can cause expensive, unnecessary re-evaluations and re-renders of list items rendered with `v-for`, even if the underlying list data hasn't changed.
**Action:** Utilize the `v-memo` directive on `v-for` loops (e.g., `v-memo="[item, lang]"`) to explicitly tell Vue only to re-render the list items when specific dependencies change, effectively isolating the list from unrelated global state updates.

## 2024-07-08 - Lazy JSON Parsing for Single Keys
**Learning:** Using full JSON parsing (`json.load`) to extract a single top-level field (`item_count`) from large snapshot arrays is a major bottleneck and wastes CPU/Memory, slowing down the `/api/history/dates` endpoint.
**Action:** Use partial file reading (first few KB) and regex to quickly extract single fields from large JSON blobs instead of parsing the entire document into memory.
