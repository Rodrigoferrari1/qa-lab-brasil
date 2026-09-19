# QA Lab Brasil 2.5.1 - Final Mobile Section Offset Hotfix

Local validation package only.

## Fix
- Corrects the mobile navigation offset for Home anchors such as **Sobre o Autor / About the Author / Sobre el Autor** and **Contato / Contact / Contacto**.
- The mobile navigation tree is collapsed **before** the target position is measured, preventing the layout reflow from moving the selected section underneath the sticky header.
- Uses the real sticky header bottom plus a 20 px safety gap.
- Performs a final post-reflow correction on mobile browsers so the section icon and title remain fully visible.
- Desktop behavior is preserved.

No other QA Lab 2.5 functionality is changed.
