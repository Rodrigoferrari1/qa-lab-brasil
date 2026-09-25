# QA Lab Brasil 3.1.6.1 - Newsletter Submit Hotfix

Baseline: production 3.1.6 package supplied by the user.

Change only:
- Keep the visitor on QA Lab when submitting the embedded Brevo newsletter form.
- Preserve the existing Brevo POST endpoint, consent fields, locale, Double Opt-in and email templates.
- Submit into a hidden iframe instead of navigating the browser to the raw Brevo JSON response.
- Show an inline localized PT/EN/ES confirmation message after Brevo completes the POST.
- Disable the submit button while the request is being processed to reduce duplicate submissions.

No Brevo configuration, newsletter visual fields, PDFs, footer, chatbot, simulator, search, content, Analytics or SEO were changed.
