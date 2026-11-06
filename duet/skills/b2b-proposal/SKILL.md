---
name: b2b-proposal
description: "Boost2Business proposal writer. Use to draft the same-day call-summary email with a value proposition matched to the topics discussed, and then the quote (scope, out of scope, timeline, what we need, price left for Karin) with its cover email, from the call summary in the client folder."
---
# הצעת ערך והצעת מחיר

## A. Summary email + value proposition (same day as the call)
1. **Inputs:** the call summary (client folder, `note` with the summary file) and the 1–3 topic ids.
2. **Fill `references/templates/email/call-summary.md`:**
   - `{pain_in_their_words}` and `{success}`: from the summary, in their words.
   - `{task_map}`: one line per task.
   - `{value_blocks}`: for each topic from `references/value-props.json`, the name, `value`, `hitl` ("איפה אתם מאשרים"), `proof` and the `page` link. Adapt one clause to their business. Don't add claims.
   - `{first_step}`: the recommendation from the summary.
   - `{quote_date}`: ask Karin, or default to two working days.
3. **Draft it:** Gmail draft to the client's email (or `client_folder.py draft --kind email --to <email> --subject "<subject>" --body-file mail.txt`).
4. **After Karin sends:** `client_folder.py sent <client> <D###> --type summary_sent`.

## B. The quote
1. **Build it from the same summary file:**
   - In Claude Code inside the Boost2Business repo: `python3 tools/make_quote.py <summary.txt> -o <client>/docs/<quote_id>.pdf`. This makes a branded PDF with prices left `[קארין ממלאת]`.
   - Elsewhere: write the quote following `references/templates/quote.md` as a Google Doc or .docx, with the same sections and the same placeholders.
2. **Draft the cover email** from `references/templates/email/quote-cover.md`.
3. **Tell Karin exactly what she must fill:** setup price, monthly price, payment terms, validity and weeks. Never fill or suggest a number as if decided. Market ranges are in docs/RESEARCH.md, for her eyes only.
4. **After she sends it:** `sent … --type quote_sent`. The follow-up is then set automatically for 3 days later.

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
