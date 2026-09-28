# QA Lab Brasil 3.2.5.4-M5.3 - Multilingual Offensive Filter

Baseline: approved 3.2.5.4-M5.2.

Scope: offensive-language validation only. No HTML, CSS, layout, navigation, assessment, footer, or responsive structure changes.

Updated the existing normalized validation detector in `assets/js/app.js` with whole-word / phrase patterns for PT-BR, ES, and EN, including the newly approved terms and common variants. Existing normalization for case, accents, spacing, punctuation, and simple leetspeak remains unchanged.
