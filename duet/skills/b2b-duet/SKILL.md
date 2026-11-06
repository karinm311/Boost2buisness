---
name: b2b-duet
description: "Boost2Business Duet team lead. Use for ANY new input about a Boost2Business lead or client — a WhatsApp/email message, a call recording or transcript, a note from Karin, a quote reply, a payment, a change request, a support issue — and for 'what's waiting for me today'. Logs the input in the client folder, decides the next step and routes to the right team member (intake, followup, discovery, proposal, closing, spec, delivery, golive-support, client-file)."
---
# מנהל הצוות · Duet של Boost2Business

The entry point. Every input passes through here, so nothing gets lost and every input drives the next step.

## The team (one skill per touch point)
| Touch point | Skill | Main events |
|---|---|---|
| New lead, first reply | b2b-intake | lead_in, reply_sent |
| Follow-up and reminders | b2b-followup | call_booked, call_no_show, quote_sent, followup_sent, quote_declined, on_hold |
| Discovery call: transcript → summary + value proposition | b2b-discovery | call_recording, call_transcript, call_notes |
| Summary email, quote | b2b-proposal | summary_sent, quote_sent |
| Closing and payment | b2b-closing | quote_accepted, payment_requested, paid |
| Full spec | b2b-spec | paid, spec_sent, spec_signed |
| Build and weekly updates | b2b-delivery | spec_signed, build_update, change_request |
| Go-live and support | b2b-golive-support | delivered, golive, support_request, checkin_done |
| Client folder / full history | b2b-client-file | any "what happened with X" |

## Steps
1. **Identify the client:** `client_folder.py find "<name / phone / email>"`. If there is no folder and this is a new lead, hand over to b2b-intake.
2. **Classify the input:**
   - it is one event type from `references/rules.json`;
   - who sent it: client / karin;
   - the channel;
   - a one-line Hebrew summary in the client's own words.
3. **Save the raw input:** put the message or file text in a temp file, then log it:
   `client_folder.py log <client> --type <event> --who <client|karin> --channel <ch> --summary "<summary>" --file <tmp>`
4. **Route:** read `next_owner` from the output and run that team member's steps now (its skill), unless Karin only asked to log.
5. **"What's waiting for me?":** run `client_folder.py due --days 1` and `client_folder.py board`. Group the result by client.
6. **Morning brief / periodic checks (Duet):** run `due --days 1`. Also look in connected Gmail for replies from clients who have a folder (match by email). Log each reply as `message_in`. Then report: due today, late, waiting for approval, and new client replies. Only message Karin when something needs her.

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
