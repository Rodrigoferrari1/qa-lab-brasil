# QA Lab Brasil 3.2.5.4-M5.1

Baseline: approved 3.2.5.4-M5.

Scope: mobile-only typography refinement for the required-answer notice in CTFL/Simulators and Logic Lab.

Change:
- Increased `.qa-answer-notice` from 12px to 13.5px on mobile widths up to 820px.
- Kept a 12px fallback for very narrow widths up to 360px.
- Preserved `white-space: nowrap`, notice geometry, margins, navigation, viewport behavior, and all desktop/web rules.

No JavaScript or HTML changes.
