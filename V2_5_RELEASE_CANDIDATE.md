# QA Lab Brasil 2.5 — Experience & Analytics — Release Candidate

Consolidated local release candidate. No production deploy performed.

Included:
- final mobile topic scroll offset correction so headings remain fully visible below the sticky header;
- GA4 G-F1SV6ME5JX with SPA/hash page views and interaction events, excluding localhost from production analytics;
- Mission, Vision and Values in PT/EN/ES;
- compact contact form with expanded categories;
- final Home layout: Mission/Vision/Values in three cards, then About the Author + Contact QA Lab side by side on desktop and stacked on mobile;
- desktop search aligned to the main content grid;
- interactive PT · EN · ES quick language selector preserving the current topic;
- About the Author side-menu shortcuts for author section, LinkedIn, GitHub and contact;
- global desktop spacing between level badges and their headings while preserving the already-correct mobile spacing.

Validation required before production:
1. Desktop/Web smoke.
2. Mobile smoke, especially Waterfall/Cascata and Engenharia de Software heading visibility.
3. Language switching PT/EN/ES.
4. About/Contact navigation shortcuts.
5. Contact form layout.
6. After production only: GA4 Realtime / typeof gtag === 'function'.
