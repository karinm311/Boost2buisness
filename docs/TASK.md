# TASK: phase 1, from WhatsApp lead to call to quote

Status: **ready to start**. Read CLAUDE.md, docs/HANDOVER.md, docs/PIPELINE.md and docs/DECISIONS.md first.

## 0. Session start (the first session in the new GitHub repo)
1. If the repo is empty, bring the kit in, following the first prompt in README.md: Artifact read → copy → commit "Boost2Business handover kit (v6.1 site + ops)" → push.
2. Send Karin a one-screen Hebrew message:
   - what phase 1 delivers;
   - the 4 blocking decisions D1–D4 with their defaults;
   - a request to confirm that https://boost2business.netlify.app shows v6.
   
   Then build with the defaults; don't wait.

## 1. Deliverables
1. **Lead tracker** (D1; default: a Google Sheet "Boost2Business · לידים").
   - **Tab "לידים":** the columns of `data/leads.example.csv`, with dropdowns for `stage`, `source`, `track` and `lost_reason`, plus conditional formatting on overdue `next_action_date`.
   - **Tab "משפך":** a funnel built with formulas, per week and per source (PIPELINE.md → Funnel metrics).
   - **Tab "הסבר":** how to use it, in 5 lines of Hebrew.
   - **How to build it:**
     - If the Google Drive connector is available, create it in her Drive and give her the link.
     - Otherwise build an .xlsx with the same structure, which she can upload to Drive.
     - Never put real lead data in git.
2. **WhatsApp kit** (`templates/whatsapp-replies.md` → final):
   - quick replies with shortcuts (for example `/שלום`, `/שיחה`, `/תזכורת`);
   - greeting and away messages;
   - the label list;
   - a 1-page Hebrew PDF setup guide for WhatsApp Business. She configures it herself. Verify the current WhatsApp Business app features before you write the steps.
3. **Discovery-call kit** (`templates/discovery-call.md` → final):
   - the script;
   - questions per track;
   - a summary form;
   - a 1-page printable PDF;
   - the "מפת המשימות" summary, which feeds the quote.
4. **Quote generator:**
   - `templates/quote.md` as a branded Hebrew PDF/Doc template (same palette and fonts as the site), with a small script or Doc that fills it from the call summary;
   - price fields stay `[קארין ממלאת]` until D5 is decided;
   - one sample quote for a **fictional** business, clearly labelled "דוגמה".
5. **The pipeline one-pager:** a Hebrew infographic PDF of the 10 stages, with who does what (Karin / the client / automation) and where Karin approves.

## 2. Acceptance
- Karin can take a new WhatsApp lead through to a sent quote using only these assets, in under 15 minutes of her time, excluding the call itself.
- Every client-facing text is a draft marked "טיוטה לאישור קארין" until she approves it. It has no invented numbers, no "יד ימין", no employer name and no contract reader.
- No credentials or real personal data are in the repo. `data/` holds only `*.example.*` files.
- PDFs:
  - are Hebrew and RTL;
  - render correctly (check the screenshots);
  - use the brand (night/indigo, cyan CTA, Secular One / Rubik).
- DECISIONS.md, HANDOVER.md and HISTORY.md are updated at the end of the session.
- **Ship:**
  - commit and push;
  - send the files to Karin;
  - send a short Hebrew summary with what she must decide next.

## 3. Next phases
See PIPELINE.md → Roadmap. In short:
- payment and onboarding, after D5–D10;
- n8n automations: lead → row, reminders, a weekly funnel summary to Karin;
- delivery and support packs;
- the site feedback loop: analytics, source tags, the first real testimonial and prices.
