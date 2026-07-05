## 2024-07-06 - Prevent Unnecessary Re-renders from Ticking Timer
**Learning:** The global ticking countdown timer in the Vue 3 frontend triggers frequent reactive updates every second. Because list items are large and complex, this causes expensive, unnecessary re-evaluations and re-renders of the entire feed item list.
**Action:** Use the `v-memo` directive (e.g., `v-memo="[item, lang]"`) on `v-for` loops rendering large lists to memoize the items and isolate them from global reactive state changes that don't affect them.
