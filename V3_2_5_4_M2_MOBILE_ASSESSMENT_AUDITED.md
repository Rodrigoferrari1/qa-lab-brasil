# QA Lab Brasil 3.2.5.4-M2 - Mobile Assessment Audited

Base: production ZIP supplied on 2026-09-28 (qa-lab-brasil(20260928-094839).zip).

Scope: mobile Logic Lab + Simulators/CTFL only. Web/desktop is reference-only and was not edited.

Changes:
- Mobile assessment navigation is in normal question-card flow (not fixed over content).
- Balanced vertical rhythm: content/review -> optional answer notice -> nav -> white bottom breathing room.
- Required-answer notice keeps balanced top/bottom spacing.
- Removed fixed-nav padding reserve and contextual hide/show behavior on mobile.
- Start/Next/Previous focus the beginning of the current assessment.
- When the required-answer notice appears, mobile scroll adjusts only as needed so the notice/navigation tail is reachable and the nav is not clipped below the viewport.
- CTFL review checkbox remains in normal flow before the notice/navigation.

Preserved:
- Web/desktop assessment styling and behavior.
- Contact/e-mail fixes, header, arrows, chatbot, sidebar, question banks and all other approved behavior.

Validation performed before packaging:
- JavaScript syntax check with node --check.
- Audited all mobile assessment CSS overrides and JS wrappers from the production baseline.
- Verified final mobile rules occur after legacy fixed-navigation CSS and override it only under max-width: 820px.
- Verified desktop rules were not changed by this patch.
