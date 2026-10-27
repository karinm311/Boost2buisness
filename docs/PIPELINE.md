# PIPELINE: from a WhatsApp lead to a supported client

Karin's request, verbatim (26 Oct 2026):
> "המטרה להמשיך מהלידים שפונים בווצאפ לניהול לידים אצלי, שיחת אפיון, הצעת מחיר, תשלום, אפיון מלא ואילוצי מערכת ועסק, יישום, תשתיות עסק, העלאה לאוויר ותמיכה"

## Design principles
- **One tracker row per lead,** from the first message to support. Every stage changes `stage`, `next_action` and `next_action_date`. Nothing lives only in her head or in WhatsApp history.
- **Templates over writing.** Every client-facing message or document starts from `templates/`. Karin edits and sends.
- **Human in the Loop.** Automations may draft, remind, file and count. Karin approves anything that goes to a client, commits money or commits time.
- **Free and simple first.** Her tools come first: Google Drive (connected to Claude), WhatsApp Business and n8n, which she knows. Add a paid tool only when it saves more than an hour a week.
- **Three tracks share one pipeline:**
  - `פתרון` (custom solution for an office or business);
  - `סוכן` (productized agent);
  - `למידה` (1:1 or group).
  
  The track decides which call questions, quote template and delivery steps apply.
- **Capacity:** about 6 hours a week. Track her hours per stage, so pricing and "limited slots" stay honest.

## Stage values (the `stage` column)
`0 ליד חדש` · `1 בסינון` · `2 שיחה נקבעה` · `2b שיחה התקיימה` · `3 הצעה נשלחה` · `4 ממתין לתשלום` · `5 באפיון מלא` · `6 ביישום` · `8 באוויר` · `9 בתמיכה` · `X לא רלוונטי` (with `lost_reason`) · `Z בהמתנה`

Stage 7, "business infrastructure", is Karin's own back office. It runs across the whole pipeline and is not a lead stage; see 7 below.

---

## 0. ליד חדש: lead capture
- **Trigger:** a WhatsApp message from the site, LinkedIn, Facebook or a referral.
- **Capture:** `created_at`, `name`, `phone`, `source`, `track_guess`, and `first_message` (short).
- **Source tracking:**
  - Today the link has no prefilled text, so the source is unknown. Decision **D2**: per-page prefilled text such as "היי קארין, הגעתי מעמוד חני" (`agents.json → wa_text`, `offer.json`).
  - UTM links per channel are in RESEARCH.md, Appendix C.
- **Tools:**
  - WhatsApp Business **labels** ("ליד חדש", "שיחה נקבעה", "הצעה נשלחה", "לקוח").
  - The tracker row is added by hand in phase 1, and by n8n in phase 3.
- **Done when:** every lead has a row within 24 h, or within the time decided in **D3**.

## 1. מענה ראשון וסינון: first reply and qualification
- **Goal:** answer fast and warmly, understand the need in 1–2 questions, and offer the free call.
- **Template:** `templates/whatsapp-replies.md`, sections 1–3.
- **Qualification:**
  - Is there a repeating task, systems that don't talk, or a wish to learn?
  - Is the person a decision maker?
  - Timeline?
  - Not a fit? Reply kindly and set `stage X` with a reason.
- **HITL:** Karin sends every reply. Quick replies make this a 10-second job.
- **Done when:** the call is booked or the lead is closed.

## 2. שיחת אפיון: discovery call (30 min, free)
- **Booking (D4):** a booking link (calendar appointment page) or manual scheduling. Remind the day before, using template 4.
- **Script:** `templates/discovery-call.md`. Agenda: 5′ rapport → 15′ questions → 7′ map and recommendation → 3′ next step.
- **Output, the same day:**
  - The **call summary** (form at the end of the script).
  - The "**מפת המשימות**": tasks → which agent, solution or learning (the /solutions demo, made real).
  - `stage 2b` and `next_action` = quote.
- **Ethics:** the call is free and without commitment, and the client leaves with a clear picture even if they don't buy.

## 3. הצעת מחיר: quote
- **Template:** `templates/quote.md`. Its sections:
  - what we understood;
  - scope;
  - out of scope;
  - phases and timeline;
  - what we need from you;
  - price;
  - payment terms;
  - validity;
  - support;
  - approval.
- **Pricing (D5, D6):** Karin's numbers only. RESEARCH.md §ו has market ranges to show her; they are proposals, not prices.
- **Delivery:** a PDF in WhatsApp plus a short message (template 6). Follow up after 3 days (template 7).
- **HITL:** Karin approves scope and price, and sends it herself.
- **Done when:** accepted (→ 4), declined (→ X, with the reason), or expired.

## 4. תשלום: agreement and payment
- **Prerequisites (Karin's open steps):**
  - business registration (עוסק פטור/מורשה, D7);
  - invoicing/receipt tool (D8);
  - clearing provider or payment link (D9; research: Grow supports card, Bit, PayBox and Apple Pay; verify fees);
  - terms/contract checked by a lawyer (D10).
- **Flow:** acceptance → payment request with a link (template 8) → receipt/invoice → `paid_status` → kickoff message (template 9).
- **Structure (D6):** for example, an advance payment plus milestones, or packages. Her decision.
- **Done when:** the payment is received and the document is issued.

## 5. אפיון מלא ואילוצי מערכת ועסק: full specification
- **Template:** `templates/spec.md`. Its sections:
  - processes as-is and to-be;
  - systems inventory;
  - data and privacy;
  - access (granted by the client in their own accounts; never shared passwords in chat);
  - business constraints (budget, people, hours, regulation);
  - HITL points;
  - acceptance criteria;
  - risks;
  - timeline.
- **Sign-off:** the client approves the spec in writing (WhatsApp or e-mail is OK) before any build.
- **Done when:** the spec is signed and the access list is ready.

## 6. יישום: implementation
- **Playbook:**
  - build in a test environment with sample data;
  - keep a weekly 3-line update to the client (template 10);
  - keep a change log;
  - raise change requests as new scope with a price.
- **Tools by need:**
  - n8n or Power Automate (automation);
  - the client's CRM/ERP (Salesforce, Oracle, ServiceNow or others);
  - Claude or Azure AI (agents);
  - Google Sheets or Excel (data).
- **HITL in the product itself:** every sensitive step waits for the client's approval. This is the brand promise.
- **Done when:** all acceptance criteria from the spec pass on sample data.

## 7. תשתיות עסק: Karin's business infrastructure (runs across all stages)
A checklist to set up once, in order of need:
1. WhatsApp Business: profile, labels, quick replies, away message.
2. Lead tracker (D1).
3. Booking calendar (D4).
4. Business registration (D7).
5. Invoicing (D8).
6. Payment link (D9).
7. Terms and contract (D10).
8. Templates folder in Drive.
9. Password manager.
10. Backups.
11. Analytics on the site (D11).
12. A business e-mail/domain (optional, D12).

For each item: Karin signs up herself, and Claude prepares the setup guide and the content.

## 8. העלאה לאוויר: go-live
- **Checklist:** `templates/go-live-checklist.md`. It covers:
  - user acceptance by the client;
  - real data;
  - permissions;
  - monitoring and alerts;
  - rollback plan;
  - client training (links to the learning track);
  - handover documents;
  - the go-live message (template 11).
- **Done when:** the client confirms it runs in production and `stage 8` is set.

## 9. תמיכה: support
- **Draft:** `templates/support.md`. It covers:
  - the support channel;
  - response times (D13);
  - what is included;
  - monthly maintenance (D14, priced by Karin);
  - change requests;
  - a check-in after 2 and 6 weeks;
  - asking for a testimonial **only from a real client, with permission**, which becomes the site's first real social proof.
- **Done when:** the support terms are agreed and the next check-in is in the tracker.

---

## Roadmap for this repo
| Phase | Deliverables | Depends on |
|---|---|---|
| **1. Lead → call → quote** (docs/TASK.md) | Tracker (sheet + dashboard tab), WhatsApp kit, call kit, quote generator (Doc/PDF) | D1–D4 |
| **2. Payment and onboarding** | Payment flow, kickoff pack, spec template in use, terms draft for the lawyer | D5–D10 |
| **3. Automation** | n8n: new WhatsApp/site lead → tracker row; reminders; weekly funnel summary to Karin (HITL) | Phase 1, and WhatsApp Business API cost check |
| **4. Delivery and support** | Delivery playbook, go-live and support packs, first case study (real, with permission) | First client |
| **5. Site feedback loop** | Analytics, per-page source tags, the first real testimonial on the site, prices when decided | D2, D11 |

## Funnel metrics (dashboard tab)
Count the leads that reach each stage, per week and per source:
- leads → calls booked → calls held → quotes sent → won → paid → live.

Also show:
- average days per stage;
- Karin's hours per client.

The baseline forecast is in RESEARCH.md, Appendix A. Compare actuals to it monthly.
