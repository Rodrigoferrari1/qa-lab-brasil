# QA Lab Brasil 3.1 - Review Fixes Local

Applied over the approved 3.1 local candidate.

- Simulator navigation repositions each new question into a usable viewport.
- Mobile simulator navigation stays accessible with responsive sticky controls.
- Question selection deduplicates by conceptual ID (variant suffix), so one concept is not repeated inside the same attempt.
- Concept variants are spaced and never silently duplicated within an attempt.
- Desktop/notebook search width restored and header uses uniform gaps across Search / Test Data / Simulators / Language.
- Existing 3.1 mobile fixes preserved: search first, utilities second row, language dropdown viewport-safe, level controls one row.
- No production deploy performed.
