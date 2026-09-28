# QA Lab Brasil 3.2.5.4 - Final Scoped Hotfix

Baseline: approved 3.2.5.3-G.

Changes only:
1. Mobile CTFL/simulators reserve dynamic space for the fixed assessment nav so long answers/review/notice cannot sit behind it.
2. Mobile assessment nav is visible only while the question card is in the viewport; it hides outside the assessment area and reappears on return.
3. Mobile Test Data Generator navigation focuses the useful section, matching the approved Logic Lab/Simulator navigation behavior.
4. Mobile Back-to-top arrow dynamically clears the institutional footer instead of covering copyright/CNPJ/links.
5. Contact submission normalizes all categories to stable Netlify values (Dúvida, Sugestão, Feedback, Reportar problema, Parceria) while preserving displayed labels.
6. Offensive-language validation expanded with normalized matching and common phrase/word variants, including arrombado and vai se fuder/foder.

Frozen/preserved: approved WEB assessment layout/spacing, mobile down arrow, chatbot, sidebar, question banks, multilingual header, and all unrelated content.
