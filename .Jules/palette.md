## 2026-06-30 - Modal/Drawer Accessibility & Icon Buttons
**Learning:** Drawers and modals often implement custom mask/overlay logic for clicking outside to close, but frequently miss 'Escape' key support. Additionally, icon-only buttons like '×' for closing drawers need `aria-label` attributes to be comprehensible to screen reader users since they lack visual text content.
**Action:** When implementing custom modal or drawer components (like history drawers), always ensure keyboard accessibility by binding 'Escape' to the close action and verify that all icon-only interactive elements possess descriptive `aria-label` attributes.

## 2024-10-24 - Accessibility improvements for language switch
**Learning:** Custom toggle controls like language switches require `aria-pressed` to explicitly communicate their active semantic state to screen readers. Additionally, purely decorative elements like text separators should have `aria-hidden="true"` to reduce screen reader noise.
**Action:** Always add `aria-pressed` to custom toggle buttons and `aria-hidden="true"` to decorative separators to improve accessibility.
