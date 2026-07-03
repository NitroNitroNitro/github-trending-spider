## 2024-05-24 - Vue 3 Global State Ticking Performance Bottleneck
**Learning:** The root-level interval timer (`countdownTimer`) causes expensive full-list re-renders in Vue 3 because the global reactive state changes every second. Without explicit memoization, all feed list items are re-evaluated and re-rendered.
**Action:** Utilize the `v-memo` directive on `v-for` loops (e.g., `v-memo="[item, lang]"`) in Vue 3 frontends to prevent unnecessary re-evaluations and re-renders of list items caused by frequent global reactive state changes.
