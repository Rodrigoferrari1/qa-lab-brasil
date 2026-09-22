# QA Lab Brasil 3.0 RC3 - Local Audit Report

Status: LOCAL / DO NOT DEPLOY YET

## Verified in this pass
- 186 content topics contain PT, EN and ES variants.
- 657 PDFs present; 99 are dedicated installation/configuration guides.
- Friendly routes remain supported, including /software, /functional-testing, /java, /glossary and /test-data-generator.
- No remaining occurrences of the previously identified generic filler patterns used in RC1/RC2.
- Search ranking now prioritizes exact topic title/key before partial content matches and clears the query after successful navigation.
- Search is cleared on language changes.
- Back-to-top resets the main document, sidebar scroll and expanded navigation while preserving the current route.
- Essential / Professional / Advanced controls are sticky in-page navigation and track the active reading level.
- Test Data Generator is localized for Brazil, United States and Spain, including country-specific identifiers, phones, addresses and postal codes; sandbox payment-card data was added.
- Glossary expanded and supports search/category filters.
- Contextual Learn more / Watch out / Good practices cards are retained when topic-specific content exists.
- Functional test-case example is structured for readability.
- Installation PDFs were regenerated with tool-specific prerequisites, official source, setup, validation and troubleshooting guidance; Java/Python include PATH recovery guidance.

## Release discipline
Production 2.6 remains unchanged. RC3 must be reviewed locally before the single final production deployment.
