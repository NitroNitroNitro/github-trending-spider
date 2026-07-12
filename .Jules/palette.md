## 2026-06-30 - Modal/Drawer Accessibility & Icon Buttons
**Learning:** Drawers and modals often implement custom mask/overlay logic for clicking outside to close, but frequently miss 'Escape' key support. Additionally, icon-only buttons like '×' for closing drawers need `aria-label` attributes to be comprehensible to screen reader users since they lack visual text content.
**Action:** When implementing custom modal or drawer components (like history drawers), always ensure keyboard accessibility by binding 'Escape' to the close action and verify that all icon-only interactive elements possess descriptive `aria-label` attributes.
## 2026-07-12 - Adding aria-pressed to toggle controls
**Learning:** When using custom toggle controls (like language switches or custom tabs) in Vue that rely on class bindings for visual active states, screen readers miss the semantic state.
**Action:** Always use `aria-pressed="true/false"` alongside visual active classes to explicitly communicate the state to assistive technologies.
