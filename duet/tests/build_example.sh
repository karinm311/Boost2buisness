#!/usr/bin/env bash
# A full Duet journey for a FICTIONAL client (נתונים לדוגמה), from lead to accepted quote, then its client history.
# The texts in duet/example-input/ are what the skills draft (intake, discovery, proposal). Run from the repo root:
#   bash duet/tests/build_example.sh
set -euo pipefail
E=duet/example-clients
IN=duet/example-input
rm -rf "$E" && mkdir -p "$E"
CF="python3 duet/scripts/client_folder.py --root $E"
TMP=$(mktemp -d)

# b2b-intake: new lead + first reply
$CF new --name "נועה (דמות לדוגמה)" --phone "050-0000000" --email "noa@example.com" \
  --business "\"הדוגמה\" · משרד הנהלת חשבונות (עסק דמיוני)" --source "לינקדאין" --track "סוכן" \
  --message "ראיתי את העמוד של חני. אנחנו טובעים בחשבוניות ספקים" --consent-contact
$CF draft נועה --kind whatsapp --title "מענה ראשון (/שלום)" --body-file $IN/01-reply.txt
$CF approve נועה D001 && $CF sent נועה D001 --type reply_sent
$CF log נועה --type message_in --who client --channel whatsapp --summary "4 עובדים, החשבוניות מגיעות בוואטסאפ ובמייל, וחלק על נייר"

# b2b-followup: the call is booked
$CF log נועה --type call_booked --channel whatsapp --summary "שיחת אפיון נקבעה" --data call_date=$(date -I)

# b2b-discovery: transcript (consent given on the recording) + summary and task map
$CF log נועה --type call_transcript --summary "שיחת אפיון, 30 דקות: חשבוניות ספקים, שאלות לקוחות, למידה לצוות" \
  --file $IN/02-transcript.vtt --consent-given
$CF log נועה --type note --summary "סיכום שיחה + מפת משימות (b2b-discovery). נושאים: chani, learning" \
  --file templates/examples/call-summary.example.txt

# b2b-proposal: summary email with the value proposition, then the quote and its cover email
$CF draft נועה --kind email --title "סיכום שיחה + הצעת ערך" --to noa@example.com \
  --subject "סיכום השיחה שלנו + מה הכי שווה לעשות קודם · הדוגמה" --body-file $IN/03-call-summary-email.txt
$CF approve נועה D002 && $CF sent נועה D002 --type summary_sent
Q="$E/C-0001 נועה (דמות לדוגמה)/docs/Q-DEMO-001.pdf"
python3 tools/make_quote.py templates/examples/call-summary.example.txt -o "$Q" | head -1
$CF log נועה --type note --summary "הצעה Q-DEMO-001 הופקה (b2b-proposal). מחירים: [קארין ממלאת]" --file "$Q"
sed -e 's/{first_name}/נועה/; s/{quote_id}/Q-DEMO-001/g; s/{business}/הדוגמה/' \
    -e 's/{scope_one_line}/סוכן חשבוניות (חני) על ספק אחד, ואז הרחבה/; s/{hitl_one_line}/כל חשבונית לפני רישום/' \
    -e 's/{valid_until}/[קארין ממלאת]/' duet/shared/templates/email/quote-cover.md | grep -v '^<!--' > "$TMP/cover.txt"
$CF draft נועה --kind email --title "מייל מלווה להצעה Q-DEMO-001" --to noa@example.com \
  --subject "הצעה מס׳ Q-DEMO-001 · הדוגמה" --body-file "$TMP/cover.txt"
$CF approve נועה D003 && $CF sent נועה D003 --type quote_sent

# the client accepts → b2b-closing (payment waits for D5–D9)
$CF log נועה --type quote_accepted --who client --channel email --summary "\"מאשרת את הצעה מס׳ Q-DEMO-001\""

# b2b-client-file: the whole relationship in one file
$CF due --days 7
$CF board
$CF history נועה
rm -rf "$TMP"
