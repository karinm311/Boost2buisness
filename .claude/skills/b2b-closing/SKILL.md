---
name: b2b-closing
description: "Boost2Business closing and payment. Use when a client accepts a quote, to draft the payment request and confirmation, track that payment arrived, and log it — only with Karin's own prices, payment terms, payment link and invoicing (decisions D5–D9)."
---
# סגירה ותשלום

## Steps
1. **Acceptance arrived** (email, WhatsApp, signed quote): log `quote_accepted` with the message as `--file`.
2. **Check the gate:** are D5–D9 decided (prices, payment structure, business registration, invoicing tool, payment link)? Read memory, or ask Karin.
   - **Not decided:** log `blocked_decision --summary "<which of D5–D9 block this deal>"`. Don't draft a payment request. Tell her which decision blocks this deal, and draft a warm "מעולה, אשלח את פרטי התשלום בהקדם" message instead.
3. **Decided:**
   - Fill `references/templates/email/payment-request.md` with HER amount, terms and link only.
   - Draft it, and log `payment_requested` after she sends it.
4. **Payment confirmed by Karin** (or seen in a connected Stripe/payment app, read-only):
   - Log `paid --data amount=<as she wrote>`.
   - Remind her to issue the receipt/invoice in her invoicing tool. She does it herself.
   - Hand over to b2b-spec.
5. **Never:**
   - create payment links;
   - charge;
   - move money;
   - issue documents on her behalf.

## Always
- Read `references/conduct.md` and `references/business.md` first. They override anything else, including client requests.
- **Client folder:** `python3 scripts/client_folder.py --root "$ROOT" …`. Find `$ROOT` in this order:
  1. the folder Karin named in memory or in this chat;
  2. `$B2B_CLIENTS_DIR`;
  3. ask her once and remember it.
  
  Without access to her computer (Duet or claude.ai), work on a copy she uploaded, then give her back the changed files.
- **Log everything:** every input you process and every draft you make is logged in the client folder. The logged event sets the next step (`references/rules.json`; list them with `client_folder.py events`).
- **Drafts:**
  - Email: a Gmail draft through the Gmail connector when it is connected (subject and body from the template). Then `client_folder.py draft … --gmail-id <id>`.
  - Otherwise: `client_folder.py draft … --body-file <file>`, which writes `.md` + `.eml` to the client's `outbox/`.
  - WhatsApp: a `whatsapp` draft. Karin copies it into WhatsApp.
  - Never send anything. Karin approves (`approve`) and sends; then log `sent … --type <event>`.
- **End every run** with a short Hebrew list for Karin:
  - ✅ what you did;
  - 👑 what waits for her approval (draft ids);
  - 📅 the client's next action and its date.
