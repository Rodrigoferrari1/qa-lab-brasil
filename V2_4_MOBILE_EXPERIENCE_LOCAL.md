# QA Lab Brasil 2.4 - Mobile Experience (Local Test)

Scope: mobile-only visual refinements. Desktop/web styling is intentionally unchanged.

Implemented:
- Mobile card spacing between level badges and headings.
- Responsive search field/button sizing to prevent clipping/overflow.
- Compact, explicit mobile language selector showing flag + PT/EN/ES + arrow.
- Reduced excessive card padding/min-height on mobile.
- More compact Learning Guidance section and controls.
- Safer top offset for topic headings under the sticky header.
- Mobile positioning refinements for Back to Top and QA Assistant controls.
- Existing mobile topic navigation behavior is preserved.

Suggested responsive checks: 360px, 390px, 412px and 430px widths.


Hotfix final: offset mobile dinâmico considera a altura real do header + 20px de margem, mantendo o título do conteúdo totalmente visível. Google Analytics 4 instalado com Measurement ID G-F1SV6ME5JX e page_view explícito para navegação SPA/hash em produção.
