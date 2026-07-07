## 2024-05-24 - [Keyboard Accessibility: Focus States]
**Learning:** Found a recurring pattern in the app's components where `:focus-visible` had `outline: none;` set, which severely hinders keyboard accessibility for users relying on tab navigation.
**Action:** When updating styles for buttons and interactive elements, ensure `:focus-visible` provides a clear visual indicator (e.g., `outline: 2px solid var(--primary); outline-offset: 2px;`) instead of removing it.
