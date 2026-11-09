# Test Data Generation & Obfuscation Method

- **Tool Used:** AI Chat (EPAM DIAL / CodeMie) with structured JSON prompting.
- **Obfuscated Fields:** Customer names, real email addresses, phone numbers, and physical addresses were replaced with fictional, plausible equivalents ending in `@meridian-sandbox.com` to guarantee full GDPR/PII safety.
- **Variety Dimensions Exercised:** 
  - **Country/Region:** Italy (IT), Germany (DE), Japan (JP), UK, and US.
  - **Language & Character Sets:** Latin characters with diacritics (Italian, German) and multi-byte scripts (Japanese Kanji/Kana).
  - **Payment Methods:** SCA credit cards, PayPal, Apple Pay, Klarna split-pay, expired cards, and failed PSD2 challenges.
  - **Edge Cases:** Cross-region purchases (Italian customer picking up in Berlin), account merge conflicts, malformed inputs (SQLi/XSS test strings), boundary values (0 items, 999 items, max-length strings), and null/missing fields.
- **Intentionally Omitted:** Underlying raw SAP ECC database state values and raw financial transaction tokens, adhering strictly to out-of-scope boundaries defined in `00-test-plan.md`.