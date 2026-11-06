---
name: b2b-client-file
description: "Boost2Business client folder / full communication history. Use when Karin asks 'what's going on with <client>', 'show me everything with <client>', before a call with a client, or to export a client's history — returns all communication (messages, calls, emails, drafts, documents) in order, with the current stage and next action."
---
# תיק לקוח: כל ההתקשרות

## Steps
1. **Find the client:** `client_folder.py find "<name / phone / email / business>"`.
2. **Full history:** `client_folder.py history <client>`. This writes `HISTORY.md` in the client's folder:
   - the profile;
   - the stage and next action;
   - drafts waiting for approval;
   - every event in order (who, channel, summary, files with their text content);
   - the list of all files.
   
   For a short version, use `--brief`.
3. **Answer Karin in Hebrew, briefly:**
   - where things stand;
   - the last 3 interactions;
   - what's open;
   - what she should do next.
   
   Offer the full HISTORY.md.
4. **Before a call with the client:** a 5-line brief: who they are, the pain in their words, what was promised, what's open, and one question to ask.
5. **Keep it complete:** if Karin mentions something that isn't in the folder (a call, a message), log it now with the right event type, so the folder stays the single source of truth.
6. **Privacy:** share the history only with Karin. Never put it anywhere public or in GitHub.

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
