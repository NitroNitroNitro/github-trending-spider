## 2026-06-30 - Modal/Drawer Accessibility & Icon Buttons
**Learning:** Drawers and modals often implement custom mask/overlay logic for clicking outside to close, but frequently miss 'Escape' key support. Additionally, icon-only buttons like '×' for closing drawers need `aria-label` attributes to be comprehensible to screen reader users since they lack visual text content.
**Action:** When implementing custom modal or drawer components (like history drawers), always ensure keyboard accessibility by binding 'Escape' to the close action and verify that all icon-only interactive elements possess descriptive `aria-label` attributes.

## 2024-05-18 - Language Toggle & Separator Accessibility
**Learning:** Custom toggle controls like language switches often rely solely on visual cues to indicate state, leaving screen reader users without context. Additionally, purely decorative elements like text separators create unnecessary noise.
**Action:** Always use `aria-pressed` to explicitly communicate the active semantic state of toggle buttons to screen readers, and add `aria-hidden="true"` to decorative text separators.
