# Boost2Business — Karin's business (רמה 0: שורש)

> **קובץ דק בכוונה.** נטען בכל סשן, גם כשעובדים רק ברמה נמוכה. פרטים נמצאים ברמות שמתחת, ונטענים רק כשפותחים סשן בתיקייה שלהן.

## מפת הרמות (פותחים את הסשן בתיקייה הרלוונטית)
| רמה | תיקייה | מה בה | קובץ הנחיות |
|---|---|---|---|
| 0 | שורש | כללי יסוד, כסף, נתוני לקוחות | הקובץ הזה |
| 1 | `site/` | האתר, העיצוב המאושר, בדיקות איכות, Netlify | `site/CLAUDE.md` |
| 1 | `duet/` + `ops/` | צנרת מליד עד תמיכה, צוות Duet, תיקי לקוחות | `duet/CLAUDE.md` |
| 1 | `Aggi - new customer agent/` | סוכן א': שירות לקוחות ללקוחות חדשים מוואטסאפ | `Aggi - new customer agent/CLAUDE.md` |
| לפי דרישה | `docs/` | `FACTS.md` (עובדות והצעה), `HANDOVER`, `DECISIONS`, `HISTORY`, `RESEARCH`, `COPY` | לא נטען אוטומטית |

טקסט על קארין או על ההצעה (לאתר, ללקוח, לסוכן): קודם `docs/FACTS.md`.
תיקיות נוספות: `brand/` לוגו, `photos/`, `templates/` טיוטות מסמכים, `tools/` סקריפטים, `data/` נתוני אמת (חסום ל-git).

## Business-operations rules (on top of the rules below)
- **Human in the Loop everywhere.** Automations draft; Karin approves anything that is sent to a client, costs money or commits her time.
- **Money, legal and identity are Karin's.** That covers:
  - prices, discounts and payment terms;
  - the guarantee;
  - contracts and terms;
  - the business registration type (עוסק פטור/מורשה) and the clearing provider.
  
  Prepare options and drafts. She decides and types the numbers. Mark every draft "טיוטה לאישור קארין".
- **Never create accounts, sign her up, or type, store or ask for passwords or API keys in chat or in the repo.** Use placeholders (`<WA_TOKEN>`) and `.env.example`. Secrets live only in the tool that needs them, entered by her.
- **Client data is personal data.**
  - Keep only what the stage needs.
  - Never commit real lead or client data to git: `data/` is gitignored, and only `*.example.*` files are committed.
  - Israel's Privacy Protection Law applies (Amendment 13 took effect in Aug 2025). Verify obligations before collecting more than name, phone and need, and flag anything legal for a lawyer.
- **Capacity is real:** about 6 hours a week next to a full-time job. Every process must save her time. Prefer free or cheap tools she already has, such as Google (Drive is connected), WhatsApp Business and n8n.
- **Never message leads or clients yourself.** Draft the messages; Karin sends them.


## Working with Karin
- **Plans:** show every plan to her briefly, as short numbered steps she can approve (her request, Nov 2026).
- Reply in Hebrew when she writes Hebrew. Be warm, direct and human ("תכלס"), with no corporate polish. She addresses Claude as "אתה", so use masculine or neutral forms for yourself.
- She types fast. Known shorthand and typos:
  - "דולות" = dashboards
  - "לסלוק" = to charge or get paid ("דף שצועק סלקו אותי" means a page that screams "take my money")
  - "סקלסילים" = scalable
  - "בולק" = בודק
  
  Interpret sensibly, and confirm only when the answer changes the outcome.
- She wants finished, working results. Run the full check loop (below) before saying "done". She often says "/loop: don't stop until…".
- **"מסמך" means a downloadable PDF** with full detail and appendices, not a web page.
- **Never use the phrase "יד ימין"**, which she finds insulting. "יד ביד" is her own phrase and is fine.
- **Taste:**
  - She wants vibrant, eye-catching pages with motion and a "wow" factor. Pale or "anemic" is "not me".
  - She also wants pages simple, consistent and uncrowded (v4/v5 feedback).
  - On v5 she said: "nice, but I expected something more interesting". v5 felt too plain and corporate.
- **"Don't make up":** never invent facts, clients, testimonials, logos or result numbers. Mark any demo data "נתונים לדוגמה".
- **Her approval rule:** act on your own. Ask her only for money or credit (this includes publishing prices, guarantees or pilot terms), signatures, identifying details and deletions. Never create accounts or type passwords for her. She signs up herself.
- **Capacity:** she runs this next to a full-time job, with about 6 hours a week. Offers must be productized, and "limited slots" are literally true.
- She often uses slash-style words such as `/loop`, `/plan`, `/doctor`, `/pro`, `/design`, `/markting`. Treat them as intent:
  - `/loop`: iterate until done.
  - `/plan`: show the plan first.
  - `/doctor`: run the full check loop.

