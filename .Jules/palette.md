## 2026-06-30 - Modal/Drawer Accessibility & Icon Buttons
**Learning:** Drawers and modals often implement custom mask/overlay logic for clicking outside to close, but frequently miss 'Escape' key support. Additionally, icon-only buttons like '×' for closing drawers need `aria-label` attributes to be comprehensible to screen reader users since they lack visual text content.
**Action:** When implementing custom modal or drawer components (like history drawers), always ensure keyboard accessibility by binding 'Escape' to the close action and verify that all icon-only interactive elements possess descriptive `aria-label` attributes.

## 2024-07-11 - Dynamic ARIA labels for i18n
**Learning:** ARIA labels on icon-only buttons (like a GitHub link) must be internationalized just like visible text to prevent jarring experiences for screen reader users who switch languages.
**Action:** Always use translation functions (e.g., `t('key')`) for `aria-label` and `title` attributes in multilingual applications.
