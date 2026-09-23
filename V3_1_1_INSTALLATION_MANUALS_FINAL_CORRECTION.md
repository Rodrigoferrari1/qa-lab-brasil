# QA Lab Brasil 3.1.1 - Installation Manuals Final Correction

Date: 2026-09-23
Scope: 40 tools x PT/EN/ES = 120 installation/configuration PDFs.

## Corrections applied
- Preserved the approved 3.1.1 site and mobile hotfix baseline.
- Rebuilt all 120 installation/configuration PDFs.
- PT/ES now retain tool-specific Windows/macOS/Linux guidance instead of generic OS paragraphs.
- Removed residual narrative English from PT/ES first-use instructions.
- Corrected command explanation classification (for example, `appium driver list --installed` is treated as listing/verification, not installation).
- Replaced the generic workflow for DBeaver, MongoDB Compass, MySQL Workbench, Oracle SQL Developer, pgAdmin, Charles Proxy, Fiddler and Proxyman with explicit beginner workflows.
- Pact keeps an explicit Node.js/Pact JS installation path.
- Commands remain untranslated where they are literal CLI syntax.

## Automated checks
- PT installation PDFs: 40
- EN installation PDFs: 40
- ES installation PDFs: 40
- Total: 120
- PT residual narrative-English pattern hits: 0
- ES residual narrative-English pattern hits: 0
- Python syntax check: PASS
- Main JavaScript syntax check: PASS

## Visual checks
Representative manuals rendered after regeneration: Python, Appium, SonarQube, Terraform and DBeaver. Layout remained readable with no observed clipping in the inspected samples.

## Validation focus for final user smoke
Python, Appium, Robot Framework, Java, DBeaver, Terraform, SonarQube and one proxy/database tool in PT/EN/ES.
