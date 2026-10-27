# ops · כלי העבודה של שלב 1 (מהליד ועד הצעת מחיר) · טיוטה לאישור קארין

| קובץ | מה זה | איך משתמשים |
|---|---|---|
| `lead-tracker.xlsx` | טבלת הלידים: לידים, משפך, הסבר, רשימות | מעלים ל-Google Drive (חדש ← העלאת קובץ ← פתיחה ב-Google Sheets). הקובץ ריק; לידים אמיתיים רק ב-Drive, אף פעם לא כאן |
| `whatsapp-setup.pdf` | הגדרת WhatsApp Business + כל 12 התשובות המהירות | פעם אחת, כ-20 דקות בטלפון |
| `discovery-call-kit.pdf` | תסריט שיחת אפיון + טופס סיכום להדפסה | בכל שיחה |
| `pipeline-onepager.pdf` | 10 השלבים בעמוד אחד: מי עושה מה ואיפה את מאשרת | מפה לתלות ליד המחשב |
| `examples/quote-sample.pdf` | הצעת מחיר לדוגמה לעסק דמיוני | ככה נראית הצעה מהמחולל |

**לבנות מחדש:** `python3 tools/build_ops_docs.py` (ה-PDF-ים) · `python3 tools/make_tracker.py` (הטבלה) · `python3 tools/make_quote.py summary.txt` (הצעה אמיתית, נשמרת ב-`out/quotes/` שלא נכנס ל-git).
