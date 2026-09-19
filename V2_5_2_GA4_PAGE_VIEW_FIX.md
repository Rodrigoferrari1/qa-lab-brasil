# QA Lab Brasil 2.5.2 - GA4 Page View Fix

Base: production 2.5.1 supplied by the project owner.

Scope:
- Analytics-only hotfix.
- Preserves all approved Web/Desktop and Mobile UI/UX from 2.5.1.
- Changes the route page-view dispatch to an explicit GA4 config update with `send_page_view: true`, `page_title`, and `page_location`.
- Keeps localhost excluded from GA4 production measurement.

Production validation:
1. DevTools > Network > filter `collect`.
2. Navigate between QA Lab topics.
3. Open Payload and confirm `en = page_view`.
4. GA4 > Realtime pages should show Views > 0 and page titles.
