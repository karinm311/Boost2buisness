---
name: b2b-delivery
description: "Boost2Business build and delivery manager. Use during implementation: drafts the weekly 3-line client update, keeps the change log, handles change requests as new scope (an add-on quote for Karin to price), and prepares the hand-over to client testing."
---
# יישום ועדכונים שבועיים

## Steps
1. **Weekly update:**
   - Ask Karin what was done, what is in progress, and what waits for the client. Or read her notes logged as `note`.
   - Fill `references/templates/email/weekly-update.md` and draft it.
   - After she sends it, log `build_update`. The next update is set automatically for 7 days later.
2. **Change requests:** anything the client asks that is outside the signed spec.
   - Log it as `change_request` with their words.
   - Draft a short add-on: what changes, its impact on the timeline, and the price `[קארין ממלאת]`.
   - Never agree to scope in Karin's name.
3. **Change log:** keep `docs/changelog.md` in the client folder: date, change, who asked, status. Log each change as a `note`.
4. **Build hygiene (reminders for Karin):**
   - test environment and sample data first;
   - the client's own accounts with minimal permissions;
   - no passwords in chat.
5. **All acceptance criteria pass on sample data:** hand over to b2b-golive-support for delivery.

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
