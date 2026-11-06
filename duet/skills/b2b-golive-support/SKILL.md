---
name: b2b-golive-support
description: "Boost2Business go-live and support. Use when a build is ready for client testing, for the go-live checklist and message, and afterwards for support requests and the 2-week / 6-week check-ins (testimonial requests only from a genuinely happy real client, with permission)."
---
# עלייה לאוויר ותמיכה

## Steps
1. **Delivery to client testing:**
   - Draft `references/templates/email/delivery.md`. Take the acceptance checks from the signed spec.
   - After Karin sends it, log `delivered`.
2. **Go-live:**
   - Walk Karin through `references/templates/go-live-checklist.md` item by item. Save the filled checklist to `docs/`.
   - When the client confirms in writing, draft `/באוויר`, and log `golive` after it's sent. The 2-week check-in is set automatically.
3. **Support request:**
   - Log `support_request` with the client's words.
   - Draft a reply.
   - Classify it: a bug in what was built, or new scope. New scope goes to b2b-delivery.
   - Response times follow D13 once Karin decides; until then, "בהקדם".
   - When solved, log `support_resolved`.
4. **Check-ins** (2 weeks, 6 weeks, then per D13):
   - Draft `references/templates/email/support-checkin.md`, and log `checkin_done` after it's sent.
   - Add the testimonial ask only if the client said they're happy. A testimonial is used only with their explicit permission and exact words.
5. **Monthly maintenance price (D14):** Karin's decision only.

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
