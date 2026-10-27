# HISTORY: how we got here (Oct 2026)

This is a compact log of the previous working session with Karin, in the claude.ai app. Read it to understand her taste and to avoid repeating mistakes. Her words are quoted as she typed them, because her shorthand matters.

## 1. Timeline of requests and deliverables

| # | What she asked | What was delivered | Her reaction / decision |
|---|---|---|---|
| 1 | A reply to a Facebook post (themes: dashboards, anomalies, Human in the Loop; phone 054-7501261) | Edited reply | — |
| 2 | A reply to a prospect, Oren, an accounting office: "ראיתי שרשמת שיש לך פתרון ai למשרד רואי חשבון". She wanted questions, the process and costs, leading to a no-commitment call. | Reply plus discovery questions | — |
| 3 | "/goal /pro /sell … תשלח לו pdf כמו דף נחיתה קצר. פגישת אפיון ראשוני בעלות סמלית של 150 שח ואם ממשיכים יחד ללא עלות. חשוב לי משהו מגניב צעיר בועט… /gril-me dont make up" | PDF one-pager | "ההיסטוריה לא מעניינת… משהו קצר עדין פשוט כדף נחיתה מעוצב מושך". She added her builds: invoice reader, chatbot, property-management + service-calls system. |
| 4 | "מה הקטע של המילה השחור לא מובן" | Removed unclear wording (avoid jargon / odd words) | — |
| 5 | A brand: "Boost ro buianeses B2b… לוגו שמשדר ai אלגנט" | Logo options | She picked **"הראשון"**: the B-circuit monogram, later recoloured purple/blue |
| 6 | WhatsApp link 0547501261 | `https://wa.me/972547501261` | Kept **plain, with no prefilled text** |
| 7 | /code-review "output הכותרת לא בטובב" | Fixed the headline. Its gradient text rendered as a box. | Lesson: no `background-clip:text` |
| 8 | "תהפוך לדף נחיתה… קצת עלי וכל מה שיש בדף נחיתה ממיר… סקילס של שיווק" | Landing page v1 as an artifact | — |
| 9 | "שים תמונה שלי… פונטים הדגשות ואלמנטי עיצוב שגורמים לוואו. שאלות כואבות של עסקים… מה אם זה לא יעבוד - אין כזה דבר אני פה בשבילכם וזה תמיד עובד :) … הפתרונות שלי הם סקלסילים" | v2 with photo, wow elements and pain FAQ in her words | — |
| 10 | Photo: "התמונה מזעזעת תעצב אותה כתמונת סטודיו… שתיהיה באמצע ולא על הצד", then "שברת את זה תבחר תמונה אחרת", "תבחר ייצוגיתתתת" | Several studio retouch rounds, finally the balcony selfie: refined matting, indigo backdrop, relit, upper body | Approved: `photos/karin-studio-1040x1300.jpg` |
| 11 | "איך הופכים לדף נחיתה שעובד ובאוויר… lovable…?" | Compared free hosting; chose **Netlify** | She signed up herself. Live at **https://boost2business.netlify.app** |
| 12 | LinkedIn: an experience entry ("שורת ניסיון חדשה כעסק פעיל ביעוץ ויישום תהליכי אוטמציה וai… מגשרת איתך על הפערים ונותנת לעסק שלך הרבה חמצן…"), "תוסיף שורה הפכתי את ההובי למוצר **תוריד את הקורא חוזים מהנסיון**", a company page, logo, cover, tagline | Texts, company-page guide, logo and cover files | Link preview failed ("הוא לא מקבל את הלינק") and was fixed with a real `og.jpg` and absolute OG URLs |
| 13 | "תערוך שוב את האתר… מדריכת ai ליחיד וקבוצות בעברית או אנגלית… עיצוב מרהיב ומתקדם… רפרנס davidamagid.com /loop אל תסיים עד שהדף עבר code review qa tests ומוכן לשיתוף", plus 2 reference screenshots ("להבין רעיון… עיצובים שעובדים ותומכים בתוכן") | v3 | "יותר טוב". Pull the photo back to show the upper body. Replace the Sisyphean wording with "(את השאר)". Stress **process automation and systems**. "לא ראיתי שעשית אפקטים של תזוזה". Use **purple/blue**. |
| 14 | "תהפוך את ההצעה מ-149 שח לשיחת אפיון ל30 דקות חינם מחיר השקה ללקוחות חדשים… תשמור על הצבעים שלי… פשוט עיקבי ולא עמוס!!… חלוקה… אנושית ופשוטה… 'אין לך מושג למה כולם מדברים ai ואתה מאחור' משהו מחבר אבל מרגיע", ref oronai.co.il#process | v4 | — |
| 15 | "/markting… אל תסיים עד שהעברת doctor… דוח מפורט… כולל תחזיות המרה /loop", plus her CRO checklist and B2B framework | v5: CRO pass, doctor loop, a 13-page PDF pre-launch report with forecasts (`reports/pre-launch-report-v5.pdf`) | **"נחמד אבל ציפיתי למשהו יותר מעניין"**, leading to the new brief (docs/TASK.md) |
| 16 | "תעדה מחקר" | Research report (docs/RESEARCH.md) | — |
| 17 | "תעביר לסשיין בclaude code… Compact all neede and my history process here and resarch" | This kit | — |
| 18 | Cloud Claude Code session (26 Oct): build v6 "סלקו אותי" per docs/TASK.md | v6. The H1 "אתם תנהלו. הסוכנים שלכם יעבדו בשבילכם." 5 illustrated agents + Karin. 5 agent pages + training, each with a live demo. Day timeline, HITL diagram, calculator, offer from config (money items OFF). Doctor loop: Lighthouse 100×4, QA 0 issues, independent review (21 findings fixed) | **"יפה סופסוף, תשמר את העיצוב"**: v6 design approved and locked. She added: "לפני שנהפוך לסקייל… אני עדיין מוכרת גם פתרונות ai למשרדים ובעלי עסקים ולמידה 1:1, 1:n", and asked for a clear, aesthetic layout with infographics |
| 19 | Same session | v6.1. Home `#paths` ("שלוש דרכים לעבוד איתי") infographic after the hero. New `solutions.html` (sectors, 3 pillars, "מפת המשרד" demo, 4-step process). The training page got a 1:1 vs 1:n comparison. Offer wording now covers all three. Second independent review fixed | — |
| 20 | "מעולה איך הופכים ללינק שיעבוד לכולם ללא התחברות" | Explained that the public link is boost2business.netlify.app (the project is Public), with step-by-step links. Her first upload went through Netlify Drop and created a stray site that requires login (wonderful-hotteok-98f4c2); she was guided to Deploys of the existing project | In progress, she was uploading |
| 21 | "/Handover … פקטה להעברה להמשך פרויקט בניית עסק בקלוד קוד… פרויקט חדש בgithub… מהלידים שפונים בווצאפ… ועד תמיכה" | This repo kit: v6.1 site, tools, CLAUDE.md for the new mission, HANDOVER, PIPELINE, DECISIONS, TASK (phase 1), Hebrew templates, and a Hebrew handover PDF | — |
| 22 | New GitHub repo karinm311/Boost2buisness (27 Oct): "/github init /git init" with the kit zip | Kit committed and pushed to `main`. Phase 1 built with the D1–D4 defaults: lead tracker (`ops/lead-tracker.xlsx`, Sheet-ready), WhatsApp kit (`ops/whatsapp-setup.pdf`), discovery-call kit (`ops/discovery-call-kit.pdf`), quote generator (`tools/make_quote.py`, sample `ops/examples/quote-sample.pdf`), pipeline one-pager (`ops/pipeline-onepager.pdf`). All drafts, no prices | Waiting for her D1–D4 answers |

## 2. What v5 is (the live baseline)
Source: `site/src/index.html`. Build: `site/dist/`.

**Sections:**
- Nav with logo and a small CTA.
- Hero: kicker "כולם מדברים על AI ואתם מרגישים מאחור?", H1 "אתם עושים את המקצוע. / ה-AI עושה את השאר.", lead, cyan CTA "אני רוצה שיחת אפיון חינם / 30 דקות · קובעים בוואטסאפ", trust row, handwritten note "בונה לכם. מלמדת אתכם.", portrait and a drifting connection-network canvas.
- "נשמע מוכר?": a 5-pain checklist.
- 4 services.
- A 4-step process.
- About, with credentials and "כבר בניתי" chips.
- FAQ (6).
- Final CTA box with phone and copy button.
- Mobile sticky CTA bar.

**Numbers:**
- Lighthouse mobile median 100/100/100/100; desktop 100 ×4.
- LCP 1.66 s; TBT 0; CLS 0.
- 133 KB over 9 requests.
- CTA in the first screen on all 10 tested viewports (93% visible at 360×640).
- Contrast 7.9–13.4:1.

**Independent review:** 16 findings. 14 were fixed, 1 partly; 1 was left to Karin (the plain WhatsApp link, which she kept).

**Forecast model** (from the report, mid case):
- Visitors needed per client: warm traffic ≈ 23, Facebook ≈ 143, LinkedIn ≈ 163, cold ≈ 190.
- Of 200 visitors a month: about 0.4 / 1.7 / 4.3 clients (low / mid / high).
- The full model with benchmarks is in RESEARCH.md, Appendix A.

## 3. Decisions Karin made (keep unless she changes them)
- Brand colours are **purple/blue** ("הצבעים שלי"). The earlier pink/orange palette is retired.
- Offer: a **free 30-minute discovery call**, "הטבת השקה ללקוחות חדשים". It replaced a 149/150 ₪ meeting.
- The WhatsApp CTA is a **plain link without prefilled text**.
- FAQ answers stay in her voice: "אין כזה דבר… וזה תמיד עובד 🙂"; solutions are scalable and change with you.
- Remove the **contract reader** from anything public.
- AI **training** for individuals and groups, in Hebrew or English, is part of the offer.
- Netlify is the host (free tier). She uploads the zip herself, in Deploys.
- Superseded headline: "אתם עושים את המקצוע / ה-AI עושה את השאר". The new one is "אתם תנהלו. הסוכנים שלכם יעבדו בשבילכם."

## 4. Lessons learned (don't repeat)
**Photos**
- Never place the portrait so that a z-index layer covers it. Crop the upper body, not the face only.
- The `birefnet` matting model gets OOM-killed. `rembg u2net_human_seg` + `pymatting` works.

**Rendering**
- Gradient-clipped text renders as a box in some viewers and prints a frame in PDFs. Use solid colours.
- Bidi: arrows between Latin words reorder. Wrap each Latin token in `.ltr`.
- Selector collisions: `.facts span` styled nested spans. Use `>` child combinators.
- Flex containers split inline text into gapped items. Wrap the text in one span.

**Link previews**
- LinkedIn can't preview a single-file base64 page. Use a real `og.jpg` (1200×627) and absolute URLs.

**Lighthouse**
- Scores are noisy, and the first cold run scored 88. Use the median of 5.
- The hero canvas cost about 680 ms of TBT until it was batched, throttled and deferred.
- An `aria-label` that doesn't match the visible text fails a11y. Use a `title` instead.

**Shell and network**
- `pkill -f` can kill your own shell. Kill by PID.
- GitHub raw downloads are blocked (403). Fonts come from npm `@expo-google-fonts/*`.
- Replacements: a counted replace failed because `imagesizes` also matched `sizes`. Prefer exact unique anchors.

**Copy**
- "מחיר השקה" next to "חינם" contradicts itself. Use "הטבת השקה".
- "NLP" is ambiguous. Always add "(תכנות נוירו־לשוני)".
- Write Hebrew self-references in masculine or neutral forms. She addresses Claude as "אתה".

**Facts**
- Monthly forecast arithmetic was wrong once ("כל 2 חודשים" vs 2.5). Compute in code; never in prose.

**Accounts**
- She once asked Claude to register her on a site with an invented password. Claude declined and never creates accounts or enters passwords. She signs up herself, for example with Google sign-in.

## 5. Where the deliverables are
| Thing | In this kit | Elsewhere |
|---|---|---|
| v5 site source | `site/src/` | Artifact https://claude.ai/artifact/DiQv7YTSa47nMYtnz8tmNR (public link) |
| v5 Netlify build | `site/dist/` | Live at https://boost2business.netlify.app |
| Logos | `brand/logo-icon.png`, `logo-dark.png`, `logo-light.png`, SVG source `brand/logo-source.html` | — |
| LinkedIn cover (old pink/orange palette; redo in purple/blue if she asks) | `brand/linkedin-cover_OLD-PALETTE.png` | — |
| Portrait + avatar | `photos/` | — |
| Pre-launch report v5 | `reports/pre-launch-report-v5.pdf` | — |
| Research | `docs/RESEARCH.md` | claude.ai research report |
| Phase 1 ops kit (tracker, WhatsApp, call, quote, pipeline) | `ops/` (built by `tools/build_ops_docs.py`, `tools/make_tracker.py`, `tools/make_quote.py`) | — |
