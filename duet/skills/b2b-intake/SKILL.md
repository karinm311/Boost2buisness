---
name: b2b-intake
description: "Boost2Business new-lead intake. Use when a new person contacts Karin (WhatsApp, email, LinkedIn, site, referral) — opens a client folder, logs the first message and source, and drafts the first WhatsApp reply (/שלום) and the qualification questions."
---
# קליטת ליד חדש

## Steps
1. **Check it's new:** `client_folder.py find "<phone or name>"`. If a folder exists, log `message_in` there and stop.
2. **Open a folder:**
   `client_folder.py new --name "<name>" --phone "<phone>" --email "<email if given>" --business "<business if known>" --source "<מקור>" --track "<פתרון|סוכן|למידה|עוד לא ברור>" --channel <whatsapp|email|linkedin|site|phone> --message "<the first message, short>" [--consent-contact]`
   - Add `--consent-contact` only if the lead asked to be contacted, or agreed to it.
   - If the need is already clear, also add `--next "מענה ראשון + הזמנה לשיחה (/שיחה1)" --next-template whatsapp:/שיחה1`.
   - Source values: אתר/דף הבית, אתר/פתרונות, אתר/למידה, אתר/עמוד סוכן, לינקדאין, פייסבוק, וואטסאפ ישיר, המלצה מפה לאוזן, אחר, לא ידוע.
   - Keep only name, phone, email, business and need (privacy).
3. **Draft the first reply:**
   - Start from `/שלום` in `references/templates/whatsapp-replies.md`. Put their name in, and mirror one word from their message.
   - If the need is already clear, use `/שיחה1`: the first-contact invitation to the free 30-minute call.
   - Save it as a `whatsapp` draft.
4. **Clearly not a fit:** draft `/לאעכשיו` with a short, true reason. Note it so Karin can decide; don't close the folder yourself.
5. **Tell Karin:**
   - the draft;
   - that after she sends it she should log `reply_sent`, or say "שלחתי" and you log it. If the reply already invited them to the call, the next step is setting the call time;
   - the tracker row to add (`ops/lead-tracker.xlsx`): date, name, phone, source, track, first message, stage "0 ליד חדש".

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
