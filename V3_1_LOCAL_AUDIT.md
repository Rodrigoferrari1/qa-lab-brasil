# QA Lab Brasil 3.1 — Local Audit

## Added
- Header utility: 🎓 Simulados / Practice Exams / Simuladores.
- `/simulators` route and sitemap entry.
- CTFL v4.0.1-aligned authored question bank: 300 unique IDs, PT/EN/ES equivalents.
- Modes: quick (10), exam (40/60 min), study, by topic, mistakes, unseen, random.
- Exam mode chapter distribution follows the current CTFL v4.0 exam structure: 8 / 6 / 4 / 11 / 9 / 2 across chapters 1–6.
- Progress, mistakes, best score and repetition avoidance stored locally with localStorage; no login required.
- GA4 events prepared for simulator start/finish in production.

## Mobile-only fixes
- Global search moved before navigation.
- Second utility row: Massa / Simulados / Idioma.
- Language dropdown constrained to viewport with full language labels.
- Essencial / Profissional / Avançado stays on one line.

## Preservation checks
- Existing `qa-lab-contact` Netlify form preserved.
- Existing content, PDFs, test-data generator, URLs and GA4 bootstrap preserved.
- No production deploy performed.
