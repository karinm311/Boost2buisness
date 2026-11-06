---
name: b2b-followup
description: "Boost2Business follow-up and reminders. Use for scheduling the discovery call, the day-before reminder, no-shows, the 3-day quote follow-up, closing a lead kindly, on-hold leads, and for the daily list of overdue next actions across all clients."
---
# מעקב ותזכורות

## Steps
1. **Today's list:** `client_folder.py due --days 1`. Work late items first.
2. **Pick the template by the client's `next_template`:**
   - `/שיחה`: offer two concrete times (from Karin's calendar if the Calendar connector is connected; otherwise ask her) or her booking link if D4 is decided.
   - `/תזכורת`: the day before the call.
   - `/פספסנו`: after a no-show. Log `call_no_show` first.
   - `email:follow-up` or `/מעקב`: 3 days after the quote, on the channel the client used.
   - `/לאעכשיו`: when they declined. Log `quote_declined --data reason=<סיבה>` with a true reason.
3. **Booked a call?** Log `call_booked --data call_date=YYYY-MM-DD`. The reminder date is set automatically to the day before.
   - With Calendar connected, offer Karin a draft event, titled `שיחת אפיון · <name>`, 30 minutes. She approves before anything is created.
4. **No answer after 2 follow-ups:** suggest `on_hold` (30 days) rather than chasing. Karin decides.
5. **Draft every message** (`client_folder.py draft`). Never send.

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
