# QA Lab Brasil 3.3.0 — IA & Quality Engineering Expansion

## Base
Built exclusively on the production package supplied on 2026-09-28.

## Preservation rule
No existing topic was removed or semantically rewritten. The previous `ai` topic content remains intact and receives additive sections only. Existing HTML, forms, simulators, Logic Lab, chatbot, header, footer and mobile assessment behavior were not edited.

## Added
- IA & Quality Engineering landing under the existing **IA & Futuro** navigation.
- QA + AI learning roadmap.
- AI FAQ covering where to start, career concerns, trust and technical knowledge.
- AI tools guide by use case, without absolute rankings.
- New official-tool topics: Sabiá/Maritaca, Microsoft Copilot, Gemini Notebook, Midjourney, Runway and ElevenLabs.
- Prompt Engineering for QA.
- QA Prompt Library with copy actions.
- Interactive Prompt Builder.
- AI Testing Lab.
- AI agents, tools and MCP.
- AI evaluation, regression, observability, tokens, latency and cost.
- AI security, privacy, prompt injection, jailbreak and safe red teaming.
- “My first day using AI as QA” guided journey.
- AI Radar for QA.
- Expanded existing AI fundamentals with technical-knowledge, context-engineering, privacy and roadmap sections.
- Sitemap entries for all new routes.

## Editorial principle
**AI accelerates. Technical knowledge evaluates. Critical thinking challenges. Evidence confirms.**

Content is original QA Lab educational writing informed by official vendor documentation; it does not reproduce vendor pages.

## Validation performed
- JavaScript syntax check (`node --check`).
- JSON validation for topics and UI.
- XML sitemap parse.
- PT/EN/ES completeness check for all new topics.
- Semantic comparison against production: all pre-existing topics unchanged, except additive sections appended to the existing `ai` topic.
- File comparison against production: only `assets/js/app.js`, `assets/css/site.css`, `content/topics.json`, `sitemap.xml` plus this release note changed.
