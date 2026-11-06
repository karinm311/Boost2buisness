---
name: b2b-discovery
description: "Boost2Business discovery-call processing. Use after a discovery call: takes the transcript (or Karin's notes; checks recording consent), stores it in the client folder, writes the call summary and 'מפת המשימות' (task map), detects the topics for the value proposition, and hands over to the proposal skill for the summary email and quote."
---
# שיחת אפיון: מתמלול לסיכום

## Before the call (if asked)
- Give Karin the script: `references/templates/discovery-call.md`.
- Remind her of the consent line at the start of the call:
  > "אני מקליטה כדי לסכם בשבילכם מדויק, ההקלטה נשארת אצלי. זה בסדר מבחינתכם?"
  
  The wording is a draft for her lawyer.

## Steps
1. **Consent:**
   - With a recording or transcript: log it with `--consent-given` only if Karin confirms the client agreed.
   - Without consent, use `call_notes` with her notes.
   - An audio file only: log `call_recording --file <audio>` and ask her for the transcript from the tool that recorded it (Meet, Zoom, a phone recorder app). Claude does not transcribe audio.
2. **Log the transcript:** `client_folder.py log <client> --type call_transcript --who karin --summary "<one line>" --file <transcript>`
3. **Write the call summary.** Use the exact fields of `references/templates/call-summary.example.txt`, filled from the transcript in the client's own words:
   - לקוח, עסק, מסלול;
   - הכאב, הצלחה;
   - one `משימה:` line per task (task | time today, as the client said it | who takes it | approval point);
   - מערכות, אילוצים, מחליט, צעד ראשון.
   
   Leave price, payment terms, weeks and validity empty. Those are Karin's.
   
   Save it in the folder: `client_folder.py log <client> --type note --summary "סיכום שיחה + מפת משימות" --file summary.txt`
4. **Detect topics:**
   - Match the transcript against `keywords` in `references/value-props.json`.
   - Keep the 1–3 strongest topics the client really talked about.
   - Note any topic Karin should confirm.
5. **Hand over to b2b-proposal** with the summary file and topic ids, so it drafts the summary email the same day.
6. **Never invent:** if something wasn't said, write `[לא עלה בשיחה]`. Hours and quantities appear only in the client's words, as "לפי הלקוח".

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
