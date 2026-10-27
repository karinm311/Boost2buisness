# TASK — the "סלקו אותי" site (v6: the agents team)

Status: **ready to build**. Research is done (docs/RESEARCH.md). This file is the plan Karin asked for with `/plan`. Start by sending her a one-screen Hebrew summary of it plus the open questions (§8). Then build right away using the defaults; don't wait for answers. She wants results, and her bar is explicit (§1).

---

## 1. Karin's brief, verbatim (Oct 2026)

> /plan נחמד אבל ציפיתי למשהו יותר מעניין. הקהל יעד הוא עסקים חלשים או אנשים שלא בקיאים בai ואולי רק מדברים איתו עדיין שיחות ושורפית עלויות אבל לא באמת מנצלים את הערך לעסק להכשיר עובד שיעבוד בשבילם שהם יהפכו לנהל את העסק ולא לעבוד בו. במקום הלוגן אתם תעשו מקצוע את תנהלו והסוכנים שלכם יעבדו בשבילכם. זה נשמע רחוק אבל זה אפשרי יד ביד. הלי קורסים וסרטונים אתם צריכים מישהו שיבין מה קורה אצלכם מה העסק שלכם צריך ולא סיסמאות. תכניס קישור לכל אחד מהפתרונות שלי עם הסבר ואילוסטרציה אינפוגרפיקה ותרשימים כולל הדגמה חיה לכל סוכן תייצר סוכנים עם שמות וציור 👩‍💻🕵️‍♀️. אנחנו רוצים לסלוק תשתמש בעיצוב מיוחד הדגשה פס מתחת למילה גופן צעיר מקפיץ טרנדי. תעדה מחקר. אל תסיים עד שיש לי דף ששצועק סלוקקקק אותיייי
>
> תעביר לסשיין בclaude code
>
> יופי תמשיך לססשין לclaude code. Compact all neede and my history process here and resarch

### What each part means
- **"נחמד אבל ציפיתי למשהו יותר מעניין"**: v5 (live now) is clean and fast but too plain. The new one must have personality.
- **Audience:**
  - Small and "weak" businesses that aren't AI-savvy.
  - At most they *chat* with ChatGPT and burn money and time on it.
  - They have never "trained an employee" (an agent) that works for them.
  - The outcome to sell: they **manage the business instead of working in it**.
- **New headline**, replacing "אתם עושים את המקצוע. ה-AI עושה את השאר.": **"אתם תנהלו. הסוכנים שלכם יעבדו בשבילכם."**
- **Supporting lines (her words):**
  - "זה נשמע רחוק, אבל זה אפשרי. יד ביד."
  - "בלי קורסים ובלי סרטונים. אתם צריכים מישהו שיבין מה קורה אצלכם, מה העסק שלכם צריך, ולא סיסמאות."
- **"קישור לכל אחד מהפתרונות שלי":** each solution gets its own page. Each page has an explanation, an illustration, an infographic and diagrams, and a **live demo for every agent**.
- **"סוכנים עם שמות וציור 👩‍💻🕵️‍♀️":** named agents with original illustrations.
- **"אנחנו רוצים לסלוק":** she wants to *sell and get paid*. The page must "scream *take my money*": an irresistible, clear offer and obvious next steps.
- **Design:**
  - Special and young.
  - **Highlighter marks** and an **underline bar** under key words.
  - A punchy, trendy font.
  - Her colours stay purple/blue (CLAUDE.md → Brand).
- **"אל תסיים עד ש…":** you're done only when the page truly screams "סלקו אותי" *and* passes the doctor loop (CLAUDE.md → Definition of done).

## 2. The core idea: sell a team, not "AI"
**The visitor's business gets a team of digital employees.**
- Each agent has a face, a name, a job and a live demo.
- The business owner is the **manager**: agents do the work, report, and wait for the owner's approval at sensitive points (Human in the Loop).
- **Karin** is the human who understands the business, recruits and trains the right agents, connects them to the existing systems, and stays *יד ביד*.

Her own words for the manager role, from her LinkedIn draft, are copy gold:
> "אתה רק מנהל — העובדים שלך מדווחים ומחכים לאישור שלך. אז מה תעשה עם כל הזמן הפנוי שיתפנה לך?!"

⚠️ **Correction to the research:**
- RESEARCH §ב/§ד shows *Karin* as "מנהלת הצוות" holding the approvals board. That clashes with her slogan "**אתם** תנהלו".
- **The owner** approves. Karin builds, trains and supports.
- The founder section should be titled something like **"מי בונה לכם את הצוות?"**, not "מי מנהלת את הצוות?".

**Why this works** (RESEARCH §1–§3):
- Lack of know-how is the fastest-growing barrier among Israeli businesses (8% → 16%).
- Most people only *ask* ChatGPT things; 49% of messages are "Asking".
- Named, illustrated helpers (Sintra, Marblism) raise trust.
- Cartoon style beats hyper-real avatars, which trigger the uncanny valley.

## 3. The team (names are proposals, Karin may rename)

| Agent | Emoji | Job, built on Karin's real builds | Accent | Prop | Live demo (scripted, client-side) |
|---|---|---|---|---|---|
| **חני חשבונית** | 🕵️‍♀️ | Reads invoices and receipts (PDF or photo from WhatsApp or email). Extracts supplier, amount, VAT and date, files them, flags duplicates. *(Karin built an invoice reader.)* | teal | detective hat + magnifier | Pick 1 of 3 sample invoices → fields fill a table one by one → "נמצאה כפילות — לאשר?" → owner taps ✅ |
| **דנה דאטה** | 📊 | Financial dashboard plus anomaly detection. Sends a weekly plain-Hebrew summary. *(Karin built financial dashboards with anomaly detection.)* | electric blue | glasses + radar/graph screen | Fake dashboard → "הריצי בדיקה" → "⚠️ הוצאות הדלק גבוהות מהממוצע" + one-line insight (labelled sample data) |
| **שירה שירות** | 💬 | Customer-service chatbot. Answers FAQs 24/7, collects lead details, hands over to a human when needed. *(Karin built a chatbot.)* | lilac | headset + chat bubble | WhatsApp-style chat: visitor picks a ready question → Shira answers → a sensitive question → "מעבירה לבעל העסק לאישור" |
| **נגה נכסים** | 🔧 | Property management and service calls. Opens a ticket from a message, assigns it to property and supplier, tracks it, updates the tenant. *(Karin built a property-management and service-calls system.)* | amber | wrench + key ring | Visitor types or picks "נזילה בדירה 4" → a kanban card moves חדש → שובץ ספק → נסגר, with tenant update messages |
| **גל גשר** | 🔗 | Automation and system integration. Connects CRM ↔ accounting ↔ forms ↔ WhatsApp, so an order becomes an invoice and then a payment reminder with no copy-paste. *(Karin's core: ERP/CRM, order-to-cash, integrations, n8n/Power Automate.)* | indigo | cables/plugs building a bridge | Animated flow "טופס → CRM → חשבונית → תזכורת תשלום" lights up step by step. Counter "0 הקלדות ידניות" |

Plus one **non-agent solution page**, **הדרכות AI**: practical training for individuals and groups, in Hebrew or English.

Plus **Karin herself**, drawn in the same style 👩‍💻 as the team builder. Use her real studio photo in the founder section; the photo is the trust anchor.

### Character style sheet (one style for all six)
- Flat 2D, thick rounded outlines, sticker/emoji-like, friendly. **Not** realistic, and no 3D.
- **Original drawings only.** Never draw or imitate a known character, mascot or brand figure.
- Build them as inline **SVG**, ≤ 8 KB each after minify, sharing one `<symbol>` sprite or one file.
- Each agent has:
  - **one accent colour** within the palette;
  - **one identifying prop**;
  - **one idle micro-animation**: blink, wave or bob, transform-only, off under `prefers-reduced-motion`.
- Mixed, natural skin tones and hairstyles across the team.
- Karin's cartoon should loosely match `photos/karin-avatar-192.jpg` (long, light blond hair, warm smile). Look at the photo first and keep it a cartoon.

**Demo scenarios.** Her prospect lists are law offices, CPA offices, property-management companies and insurance agencies, so set demos there with **fictional** businesses. Never name a real firm.

## 4. Information architecture
```
/                        home (short, ~600–800 words; depth lives on the agent pages)
/team/chani.html         חני חשבונית
/team/dana.html          דנה דאטה
/team/shira.html         שירה שירות
/team/noga.html          נגה נכסים
/team/gal.html           גל גשר
/training.html           הדרכות AI
```
- On Netlify, add `_redirects` so that `/team/chani` serves `/team/chani.html` with status 200.
- In the claude.ai artifact, publish the extra pages through `files`. Each one is a full HTML document.
- **After publishing, test every cross-page link** in the artifact viewer. If multi-page links misbehave there, keep real pages for Netlify. For the artifact preview only, fall back to `#team-<slug>` sections.
- **One source of truth.** Keep agent data in `site/src/data/agents.json`: names, jobs, demo scripts, prices (off by default) and WhatsApp text (off by default). A small build script renders all pages for both flavours: artifact = Google Fonts; Netlify = self-hosted subset fonts.

### Home: section by section
Based on RESEARCH §ב, adjusted.

0. **Sticky top bar:** logo · "הכירו את הצוות" · CTA "שיחת אפיון חינם".
1. **Hero:**
   - H1 "אתם <u>תנהלו</u>. הסוכנים שלכם <mark>יעבדו בשבילכם</mark>."
   - Subline about the team doing the grunt work while you approve only what matters. No courses, no slogans.
   - The illustrated team around the owner's chair.
   - CTA "אני רוצה שיחת אפיון חינם" with micro-copy "30 דקות · קובעים בוואטסאפ".
   - Secondary link "הכירו את הצוות ←".
2. **"נשמע מוכר?"**: 3 pain bubbles, for example "ChatGPT כותב לי יפה, אבל העבודה עדיין עליי". Then the punch line **"שיחה עם AI ≠ עובד"**.
3. **"הכירו את הצוות שלכם"**: a bento grid of 5 agent cards. Each card has the drawing, name, one-line job, "מה היא לוקחת מכם" (qualitative, **no invented hours**) and "לעמוד של חני ←".
4. **"תראו אותם עובדים"**: tabbed live demos, the same components as the agent pages.
5. **"היום שלכם — בלי ועם"**: a two-lane 07:00–23:00 timeline infographic. On mobile it stacks vertically.
6. **"איך זה עובד"**: 3 steps.
   - ① שיחת אפיון (חינם)
   - ② קארין בונה ומחברת
   - ③ הסוכנים עובדים — אתם מאשרים
   
   Add a Human-in-the-Loop diagram: owner 👑 decides, agents execute, Karin 👩‍💻 builds and supports.
7. **Calculator:**
   - "כמה שעות בשבוע הולכות לכם על…"
   - 3 RTL sliders and an hourly value, giving hours and ₪ per month.
   - Then "בואו נחזיר לכם אותן" with the CTA.
   - Label it as the visitor's own estimate.
8. **"מי בונה לכם את הצוות?"**: Karin's story, from CLAUDE.md's whitelist only.
   - Real photo.
   - "מ-2011"
   - "הפכתי את התחביב למוצר"
   - "בונה לכם. מלמדת אתכם."
9. **The offer, the "סלקו אותי" block:**
   - The free call is the hero of the offer.
   - **Founders pilot** card.
   - Package cards ("סוכן ראשון", "צוות קטן", "מערכת מחוברת", "הדרכה").
   - Guarantee box.
   - **Prices, pilot numbers and the guarantee are OFF until Karin approves them** (see §7).
10. **FAQ.** Keep her v5 answers and add:
    - "יקר?"
    - "מסובך?"
    - "מה אם הוא טועה?" (HITL)
    - "מה עם הנתונים שלי?"
    - "זה בשבילי?"
11. **Final CTA:** repeat the H1 idea and the double button: WhatsApp plus phone.

Keep from v5: the mobile sticky CTA bar, reveal failsafe, canvas discipline, a11y, OG tags and the analytics hook (`data-cta`).

### Agent page template (Marblism-style)
1. Big drawing and a first-person H1, for example "אני חני. החשבוניות שלכם — עליי."
2. "התפקיד שלי": one line.
3. "מה אני עושה ביום־יום": 3–5 tasks with icons.
4. **Live demo**, inline, playable with a thumb, 60–90 s max, 3–5 steps, no sound. Badge **"הדגמה · נתונים לדוגמה"**.
5. **Diagram:** where the agent sits in the flow, plus **"איפה אתם מאשרים"** (the HITL points).
6. **Before → after:** qualitative unless Karin gives real measured numbers.
7. "עובדת טוב עם…": links to 2 other agents.
8. CTA "אני רוצה את חני בצוות שלי" → WhatsApp.
9. Its own `<title>`, meta description, OG tags, and ideally its own OG image (1200×627) for LinkedIn posts per agent.

## 5. Design direction ("יותר מעניין", young and punchy)
- **Fonts** (max 3 families, self-hosted subsets on Netlify):
  - **Secular One** for headlines; Rubik 800–900 is the fallback.
  - **Rubik** 400/700 for body.
  - **Playpen Sans Hebrew** for handwritten notes such as "← זאת אני!".
  - Retire Amatic SC.
  - npm sources: `@expo-google-fonts/secular-one`, `@expo-google-fonts/playpen-sans-hebrew` and `@expo-google-fonts/rubik`. All verified on npm.
- **Highlights:**
  - `mark` as a highlighter: `background: linear-gradient(transparent 55%, var(--lav) 55%)`, tuned for the dark background.
  - **Underline bar** under key words: a thick SVG or `text-decoration-thickness:.18em; text-underline-offset:.28em`. The offset clears descenders ק ן ך ף ץ.
  - The bar draws in from right to left when it enters view (transform-only).
- **Layout:**
  - Bento grid for the team.
  - Big type.
  - Stickers and handwritten arrows.
  - A little playful tilt (±2°) on cards.
  - Generous whitespace. "Simple, consistent, uncrowded" still applies: one idea per section.
- **Colour:**
  - Keep the night/indigo base and the cyan CTA, because the CTA must be the most contrasting thing on screen.
  - Agent accents live inside the palette: teal, electric blue, lilac, amber, indigo.
  - The research suggested a warm CTA. **Karin's palette wins**, so keep cyan.
- **Motion:**
  - Character idle animations, button "pop" on hover or tap, line draw-ins, demo animations.
  - Transform/opacity only, `prefers-reduced-motion` respected, nothing that hurts LCP.
- **Reference feel:**
  - `references/` holds ad-style pages with a big face and a bold headline.
  - She liked davidamagid.com (motion, personal brand) and oronai.co.il (#process; calm, connected).

## 6. Copy rules
- Plain Hebrew at a grade 5–7 reading level, because simple copy converts about 2× (RESEARCH §4).
- **No jargon** in headings: no LLM, RAG, agentic or API.
- Address the reader in plural "אתם".
- CTAs are first-person and positive: "אני רוצה…".
- The **facts whitelist** in CLAUDE.md is law:
  - No invented clients, testimonials, logos or savings numbers.
  - Demo data is always labelled.
- Never "Stop hiring humans" framing. The framing is "your people (and you) stop doing grunt work".
- Never "יד ימין".
- Never name her employer.
- Never mention the contract reader.
- More of her own lines are in docs/COPY.md.

## 7. Selling, prices and payment ("לסלוק")
- **The primary conversion stays: WhatsApp → free 30-minute discovery call.** A custom service worth thousands of ₪ closes in a conversation, not with a Buy button (RESEARCH §ו).
- Put prices, the pilot and the guarantee in config (`agents.json` / `offer.json`), **all off by default**. When off, cards say "הצעה מותאמת אחרי שיחת האפיון".
  - Turn them on only with numbers Karin typed herself.
  - RESEARCH §ו has market ranges and suggestions to show her: "סוכן ראשון" from ~4,900 ₪ setup + ~450 ₪/month; "צוות קטן" from ~12,000 ₪ + ~1,200 ₪/month.
- **Founders pilot:** a discounted first agent in exchange for a testimonial and a case study.
  - Show a slot count **only if Karin confirms a real number**. She has about 6 hours a week for the business, so capacity really is limited.
  - No fake countdowns.
- **Guarantee:**
  - Default is her own non-monetary promise: "אני איתכם עד שזה עובד".
  - A money-back or "keep working free" guarantee needs her explicit OK, and RESEARCH suggests a lawyer check.
- **Payment link:**
  - Grow (ex-Meshulam) supports card, Bit, PayBox and Apple Pay. It is recommended **after** the call, sent in WhatsApp.
  - Karin hasn't opened an *עוסק פטור* or a clearing account yet; it's an open step in her plan.
  - Support an optional `PAYMENT_URL` (for example, a pilot reservation). The block stays hidden while it's empty.
  - **Never sign her up to anything or invent credentials.** She signs up herself.

## 8. Open questions for Karin
Ask once at the start, in Hebrew, with the defaults. Don't block on them.

1. Are the agent names OK: חני חשבונית / דנה דאטה / שירה שירות / נגה נכסים / גל גשר? **Default: yes.**
2. Prices "החל מ-" for each package? **Default: hidden** ("הצעה מותאמת אחרי שיחת האפיון").
3. Founders pilot: how many slots, what discount, what she asks in return? **Default: shown without numbers.**
4. Guarantee wording? **Default: "אני איתכם עד שזה עובד"** (her own promise), no money-back.
5. Prefilled WhatsApp text per agent ("היי קארין, ראיתי את חני…")? It helps her know which agent sold. **Default: plain link** (her v5 decision).
6. Payment link? **Default: none until she has a clearing account.**
7. A durable home: a GitHub repo, so Netlify auto-deploys on every change? **Default: zip upload in Netlify Deploys.**
8. A sixth agent for **law offices**? In her own planning she has talked about a contracts product for law firms ("ברור לחוזים"), and most of her lead lists are law and CPA offices. But she removed the contract reader from her public materials. **Default: no contracts agent.** Ask once; build it only if she says yes, using her wording.

## 9. Execution plan
1. Read CLAUDE.md and the docs. Look at `site/src/index.html` (v5) and the screenshots in `references/`.
2. Run `tools/` on v5 (`serve.py` + `qa.py`) to confirm the environment works.
3. Send Karin the plan summary and §8 questions, one screen in Hebrew.
4. **Design system first:**
   - tokens, fonts, `mark` / underline components, buttons;
   - the 6-character SVG style sheet.
   
   Render one test page with all six characters, check it at 390 and 1280, and screenshot it.
5. Build the home page sections 0–11 and the shared components: demo engine, timeline, HITL diagram, calculator.
6. Build the 5 agent pages and the training page from `agents.json`.
7. Wire the offer from config, with defaults off.
8. Build both flavours: the artifact (Google Fonts) and Netlify `site/dist` (subset fonts incl. new families, WebP images, favicon, `_headers`, `_redirects`, per-page OG).
9. Run the **doctor loop** on home + every page (CLAUDE.md → Definition of done). Fix and repeat until clean. Get the independent review from a fresh subagent.
10. **Ship:**
    - Publish v6 as a **new** artifact, for example "Boost2Business · הצוות".
    - Leave the v5 artifact (https://claude.ai/artifact/DiQv7YTSa47nMYtnz8tmNR, shared publicly) untouched until Karin approves v6. Then offer to move v6 onto that URL; read it first.
    - Zip `site/dist` and send it with SendUserFile.
    - Send Karin a short Hebrew summary covering:
      - the numbers, translated into what a visitor experiences;
      - the open decisions;
      - how to deploy: Netlify → project boost2business → Deploys → drag the zip.
    - The live site changes only when **she** uploads.

## 10. Acceptance checklist (all ✅ before "done")
- [ ] The hero says **"אתם תנהלו. הסוכנים שלכם יעבדו בשבילכם."** with a marker and an underline bar.
- [ ] Problem and value are clear in 3 seconds. The CTA is in the first screen on all 10 viewports (`tools/firstscreen.py`).
- [ ] 5 original illustrated agents plus Karin's cartoon, one consistent style, no known characters.
- [ ] 5 agent pages and the training page, each with explanation, illustration, diagram/infographic and CTA.
- [ ] 5 live demos that work by tap at 360 px and by keyboard, labelled "הדגמה · נתונים לדוגמה", finishing in ≤ 90 s.
- [ ] Infographics: the day with/without timeline and the HITL "who does what" diagram. Optional: an order-to-cash map on Gal's page.
- [ ] The calculator works in RTL, labels its output as an estimate, and leads to the CTA.
- [ ] Offer block: free call, pilot and packages. **No price, pilot number or guarantee without Karin's approval.**
- [ ] Copy: whitelist facts only, no jargon, no "יד ימין", no employer name, no contract reader, demo data labelled.
- [ ] `tools/qa.py` reports 0 issues on every page at 360/390/768/1024/1280/1440.
- [ ] Lighthouse mobile median of 5 runs on home and one agent page: all four scores ≥ 95, LCP ≤ 2.0 s.
- [ ] The independent review passed and its findings are fixed.
- [ ] Shipped: artifact published, Netlify zip sent, Hebrew summary plus decision list sent.
