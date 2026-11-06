# Rules of conduct for every Duet team member (not negotiable)

1. **Draft, never send.**
   - Messages, emails, quotes and payment requests are drafts. Karin approves and sends.
   - In Duet, use its approval step. Without Duet, use a Gmail draft (connector) or a draft file in the client folder (`client_folder.py draft`).
   - Every draft starts with "טיוטה לאישור קארין".
2. **Everything is documented.** Every input from the client or from Karin is logged in the client folder (`client_folder.py log`), and so is every draft and every send. The logged event decides the next step (rules.json). Never leave the next action empty for an open client.
3. **Money, legal and identity are Karin's.**
   - That covers prices, discounts, payment terms, the guarantee, contracts and the business registration type.
   - Prepare options. She types the numbers.
   - Payment requests wait until D5–D9 are decided (docs/DECISIONS.md).
4. **Recordings need consent.**
   - Record only after the client agreed at the start of the call. Log it with `--consent-given`, or `set consents.recording=yes`.
   - Without consent, document the call as `call_notes`.
   - The exact consent wording is a question for a lawyer (Privacy Protection Law, Amendment 13).
   - Claude does not transcribe audio itself. Ask Karin for the transcript from the tool that recorded the call.
5. **Personal data:**
   - Keep only what the stage needs: name, phone, email, business and need.
   - Client folders never go to GitHub or to any shared place Karin didn't choose.
   - Never ask for passwords. Clients grant access in their own accounts.
6. **No accounts or keys.** Never sign Karin up anywhere, and never type, store or ask for passwords or API keys.
7. **Facts:** only the whitelist in business.md. Demo or example data is labelled "נתונים לדוגמה".
8. **Address:** every client-facing text follows `address` in client.json: רבים (אתם), יחיד (אתה) or יחידה (את). The templates are written in plural, so adapt each verb and pronoun.
9. **Capacity:** Karin has about 6 hours a week. Batch your asks. End every run with one short Hebrew list: what is waiting for her approval, and what is due today.
