## 2026-07-04 - [Vue 3 v-memo for v-for]
**Learning:** In Vue 3, a global reactive state change (like a countdown timer) in a parent component causes the VDOM to diff and re-render expensive `v-for` list items unnecessarily.
**Action:** Utilize the `v-memo` directive on `v-for` loops (e.g., `v-memo="[item, lang]"`) to prevent expensive, unnecessary re-evaluations and re-renders of list items caused by frequent global reactive state changes, such as a ticking countdown timer. Ensure localization state (like `lang`) is included in dependencies if used.
