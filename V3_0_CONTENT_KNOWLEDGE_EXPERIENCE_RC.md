# QA Lab Brasil 3.0 — Content & Knowledge Experience (Local RC)

Local release candidate. Do not deploy before final review.

## Consolidated changes
- Contextual editorial audit: generic/repeated insight cards removed globally.
- Software Engineering promoted to a top-level knowledge domain and expanded as the conceptual hub.
- Scrum rewritten around the current official Scrum Guide concepts and event purposes.
- DevOps, Waterfall, Kanban, Lean and TestRail expanded with topic-specific content.
- API and Jira contextual cautions corrected.
- Learning guidance moved to the end and renamed “Continue sua jornada / Continue your journey / Continúe su camino”.
- Glossary expanded with practical QA/Quality Engineering definitions.
- Installation sections improved for Java, Python, Playwright, Appium and Robot Framework; global installation PDF pattern added for installable tools.
- Two PDFs for installable tools: educational guide + installation/configuration guide.
- New global QA Test Data Generator at `/test-data-generator`, with desktop header shortcut, mobile compact button, synthetic data, valid/invalid/boundary modes, copy and JSON/CSV export.
- Existing SEO-friendly URLs remain stable; sitemap includes the generator URL.
- PT / EN / ES preserved.

## Local run
Use `python serve_local.py` from this folder. This local server includes SPA fallback so direct routes and refresh work locally.
