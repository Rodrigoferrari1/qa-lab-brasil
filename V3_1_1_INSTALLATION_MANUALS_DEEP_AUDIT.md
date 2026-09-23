# QA Lab Brasil 3.1.1 - Deep Audit of Installation Manuals

Date: 2026-09-23
Scope: 40 installation/configuration manuals x PT/EN/ES = 120 PDFs.

## Verdict
NOT YET CERTIFIED FOR PRODUCTION.

The visual structure and novice-oriented organization are approved, but the deep audit found three blocking content classes.

## Blocking findings

### 1. Residual language leakage
Narrative English remains inside PT/ES manuals in first-use instructions. Confirmed examples include SonarQube, WireMock, Grafana, Jenkins and GUI-oriented tools that retain actions such as Open/Launch in English.

### 2. PT/ES OS steps are generated too generically
The current generator preserves tool-specific Windows/macOS/Linux instructions only for English. For Portuguese and Spanish, `os_text()` replaces those instructions with a generic paragraph telling the reader to access the official source, choose the OS package and complete installation/configuration. This loses important beginner detail and creates semantic asymmetry between EN and PT/ES.

### 3. Generic command explanations can be semantically wrong
`command_explain()` classifies commands using broad string rules. Example: `appium driver list --installed` contains the token `install`, so it is incorrectly described as installing a component even though it lists installed drivers.

## Generic-fallback manuals
Nine manuals currently rely on fallback metadata rather than explicit tool-specific workflows:
- Charles Proxy
- DBeaver
- Fiddler
- MongoDB Compass
- MySQL Workbench
- Oracle SQL Developer
- Pact
- pgAdmin
- Proxyman

These must receive explicit installation, validation, first-use and troubleshooting procedures instead of generic vendor guidance.

## Approved aspects
- 120/120 PDFs exist and are readable.
- Consistent QA Lab Brasil visual identity.
- Beginner-oriented section structure is present.
- Windows/macOS/Linux sections exist.
- Validation, PATH/environment, first use, expected result, troubleshooting and final checklist are present.
- Strong samples include Python, Robot Framework, Appium EN, Maven and ADB EN.

## Required exit criteria
1. 0 narrative language leaks in PT/EN/ES.
2. Tool-specific OS instructions in all three languages.
3. Tool-specific explanation for every command/action.
4. 0 manuals using generic fallback workflow where a concrete documented workflow exists.
5. PT/EN/ES semantic parity for each tool.
6. Beginner can follow download -> install -> configure -> validate -> first use without needing undocumented assumptions.
7. Re-render and visually inspect representative CLI, GUI, Java, Node, Python, mobile, proxy, database, DevOps and observability manuals.
