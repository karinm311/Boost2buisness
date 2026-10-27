# DECISIONS: Karin decides, Claude prepares the options

How to use this file:
- Ask her about open items in Hebrew, a few at a time, each with its default.
- When she answers, move the item to "Decided", with her words and the date.
- Never fill a money, legal or identity item yourself.

## Open: blocks phase 1 (lead → call → quote)
| # | Decision | Options | Default until she answers |
|---|---|---|---|
| D1 | Lead tracker tool | Google Sheet in her Drive · Notion · a CRM (HubSpot free, etc.) | **Google Sheet** (free; Claude can read and write it through the Drive connector) |
| D2 | Prefilled WhatsApp text per page, to know where each lead came from | Plain link (her v5 choice) · per-page text, e.g. "היי קארין, הגעתי מעמוד חני" | **Plain link.** Recommend turning it on: without it the funnel can't be measured by source |
| D3 | Response-time promise to new leads | Same day · within 24 h · other | Not shown on the site; internal goal of 24 h |
| D4 | Booking the discovery call | Booking link (calendar appointment page) · manual in WhatsApp | **Manual**, until she opens a booking page herself |

Phase 1 was built on 27 Oct 2026 with these defaults: `ops/lead-tracker.xlsx` (D1, upload to Drive → Google Sheet), plain link (D2; the funnel's "by source" table will show mostly "לא ידוע" until D2 changes), 24 h internal goal shown only as a placeholder in the greeting message (D3), manual booking with `/שיחה` and `/תזכורת` (D4).

## Open: money, legal, identity (Karin only)
| # | Decision | Notes |
|---|---|---|
| D5 | Prices per track and package (סוכן ראשון, צוות קטן, פתרון למשרד, למידה 1:1, למידה בקבוצה) | RESEARCH §ו has market ranges, which are proposals only. Shown on the site only when `offer.json → show_prices` is true |
| D6 | Payment structure: advance, milestones, monthly fee | — |
| D7 | Business registration: עוסק פטור or מורשה | Her open step. A tax advisor or accountant decides |
| D8 | Invoicing/receipts tool | Depends on D7. Verify options at the time |
| D9 | Clearing provider or payment link | Research: Grow (card, Bit, PayBox, Apple Pay). Fee tracks conflict between sources, so verify. The site's `payment_url` stays empty until then |
| D10 | Terms, contract and privacy notice | Needs a lawyer. Claude drafts the questions for the lawyer, not the contract |
| D13 | Support response times | — |
| D14 | Monthly maintenance price | — |
| P1 | Founders pilot: slots, discount, what she asks in return | Site shows the pilot without numbers |
| P2 | Guarantee wording | The site's guarantee box is OFF. Her FAQ promise "אני פה בשבילכם וזה תמיד עובד" stays as is |

## Open: site and brand
| # | Decision | Default |
|---|---|---|
| S1 | Agent names חני / דנה / שירה / נגה / גל | Keep |
| S2 | The law-office chip and demo option on /solutions (no mention of contracts) | Keep, unless she says no |
| S3 | A contracts agent for law offices | **No.** Build only on her explicit yes |
| D11 | Analytics (GA4 / Clarity / GTM) | None yet. The `data-cta` hooks are ready |
| D12 | Own domain and business e-mail | Optional; stays on netlify.app |
| S4 | A GitHub-linked Netlify auto-deploy | Default: zip upload. Linking Netlify to the new repo makes every push go live; she connects it herself |

## Decided (keep unless she changes them)
| Date | Decision | Her words |
|---|---|---|
| Oct 2026 | Brand colours purple/blue; cyan CTA | "הצבעים שלי" |
| Oct 2026 | Offer: free 30-minute discovery call, "הטבת השקה ללקוחות חדשים" | — |
| Oct 2026 | Remove the contract reader from everything public | "תוריד את הקורא חוזים" |
| Oct 2026 | Netlify hosting, uploaded by her through Deploys | — |
| 26 Oct 2026 | v6 design approved and locked | "יפה סופסוף, תשמר את העיצוב" |
| 26 Oct 2026 | All three offerings stay visible: solutions for offices and businesses, the agents team, learning 1:1 and 1:n | "אני עדיין מוכרת גם פתרונות ai למשרדים ובעלי עסקים ולמידה 1:1, 1:n" |
| 26 Oct 2026 | A new GitHub project continues the business build: lead to support | "/Handover … פרויקט חדש בgithub" |
