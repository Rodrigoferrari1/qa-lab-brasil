# QA Lab Brasil 3.1.1 - PDF + Mobile Hotfix Audit

Baseline: production package supplied by the user on 23/09/2026.

## Scope implemented

1. Installation manuals rebuilt for novice users in PT/EN/ES.
   - 40 tools x 3 languages = 120 installation/configuration PDFs.
   - Official download/documentation reference included from the topic metadata.
   - Windows, macOS and Linux sections.
   - Terminal guidance (CMD / PowerShell / Terminal).
   - Tool-specific validation/setup/first-use commands or vendor-specific first-use action.
   - Expected-result guidance, PATH/environment-variable recovery, troubleshooting and final checklist.
   - Commands remain technical where appropriate; surrounding narrative is localized.
2. Mobile: Test Data and Practice Exams navigation now moves the viewport to the opened destination.
3. Mobile: utility row rebalanced for PT/EN/ES; long labels can wrap inside their own buttons instead of overflowing.
4. Mobile: global search result navigation now moves the viewport to the opened topic.

## Automated checks

- JavaScript syntax: PASS (`node --check assets/js/app.js`).
- Python scripts compile: PASS.
- Installation PDFs found: 120/120.
- PDF readability: PASS for all 120.
- Minimum extracted text per installation manual: > 3,400 characters.
- Minimum pages: 2; maximum pages: 3 (dense A4 beginner manuals).
- Known generator-language contamination phrases in PT/ES: 0.
- Visual render samples: Python PT and Appium EN rendered successfully with no clipping observed.

## Preserved

The existing production site structure, topic content, simulator logic/layout, PDF Center, Forms, Analytics, SEO, desktop header and previously approved components were not removed.
