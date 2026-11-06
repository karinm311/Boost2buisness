---
name: b2b-spec
description: "Boost2Business full specification. Use after payment: drafts the kickoff email with what to prepare, prepares the full spec document (processes as-is/to-be, systems, data and privacy, access, business and system constraints, HITL points, acceptance criteria, risks, timeline) from the call summary and kickoff meeting, and tracks written sign-off."
---
# אפיון מלא ואילוצי מערכת ועסק

## Steps
1. **Kickoff:** draft `references/templates/email/kickoff.md` (`{spec_meeting}` = the date Karin sets). After she sends it, log `message_out`.
2. **Spec meeting input:** take the transcript or notes and log them (`call_transcript` with consent, or `call_notes`).
3. **Draft the spec:** fill `references/templates/spec.md` from the call summary, the kickoff meeting and documents the client sent (`inbox/`).
   - Mark every HITL point 👑.
   - Write acceptance criteria as testable sentences.
   - Mark open questions `[לברר עם הלקוח]`.
   - Mark anything legal or privacy-related `[לבדיקת עו״ד]`.
4. **Save it:** `docs/spec-v1.md` (or a Google Doc); log `note` with the file.
5. **Draft the cover email** asking for written approval (a reply is enough). After Karin sends it, log `spec_sent`.
6. **Client approves in writing:** log `spec_signed` with their message. Building starts only after this.
7. **Access:** list what access is needed and who grants it. Never accept passwords in chat or email.

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
