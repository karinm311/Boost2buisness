"""Tests for duet/scripts/client_folder.py: run with  python3 -m unittest discover duet/tests"""
import contextlib
import datetime as dt
import io
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import client_folder as cf  # noqa: E402


def run(root, *argv):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        cf.main(["--root", root, *argv])
    return out.getvalue()


class ClientFolderTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name
        run(self.root, "new", "--name", "בדיקה לדוגמה", "--phone", "050-0000000", "--source", "לינקדאין",
            "--message", "רוצה לחבר אקסל להנהלת חשבונות")
        self.folder = cf.resolve(self.root, "C-0001")

    def tearDown(self):
        self.tmp.cleanup()

    def client(self):
        return cf.load(self.folder)

    def file(self, text, name="x.txt"):
        p = os.path.join(self.root, name)
        open(p, "w", encoding="utf-8").write(text)
        return p

    def test_new_lead_sets_first_step(self):
        c = self.client()
        self.assertEqual(c["stage"], "0 ליד חדש")
        self.assertEqual(c["next_owner"], "b2b-intake")
        self.assertEqual(c["next_action_date"], dt.date.today().isoformat())
        self.assertEqual(len(cf.timeline(self.folder)), 1)

    def test_every_rule_owner_is_a_skill(self):
        skills = set(os.listdir(os.path.join(os.path.dirname(__file__), "..", "skills")))
        for k, r in cf.RULES["events"].items():
            if r["owner"]:
                self.assertIn(r["owner"], skills, k)
            if r["stage"]:
                self.assertIn(r["stage"], cf.RULES["stages"], k)

    def test_call_booked_reminder_is_day_before(self):
        d = (dt.date.today() + dt.timedelta(days=5)).isoformat()
        run(self.root, "log", "C-0001", "--type", "call_booked", "--summary", "נקבע", "--data", f"call_date={d}")
        c = self.client()
        self.assertEqual(c["stage"], "2 שיחה נקבעה")
        self.assertEqual(c["next_action_date"], (dt.date.today() + dt.timedelta(days=4)).isoformat())

    def test_transcript_requires_consent(self):
        t = self.file("תמלול")
        with self.assertRaises(SystemExit):
            run(self.root, "log", "C-0001", "--type", "call_transcript", "--summary", "s", "--file", t)
        self.assertEqual(len(cf.timeline(self.folder)), 1)  # nothing logged, nothing stored
        self.assertEqual(os.listdir(os.path.join(self.folder, "calls")), [])
        run(self.root, "log", "C-0001", "--type", "call_transcript", "--summary", "s", "--file", t, "--consent-given")
        c = self.client()
        self.assertEqual(c["consents"]["recording"], "yes")
        self.assertEqual(c["stage"], "2b שיחה התקיימה")
        self.assertEqual(c["next_owner"], "b2b-discovery")
        ev = cf.timeline(self.folder)[-1]
        self.assertTrue(ev["file"].startswith("calls/"))
        self.assertEqual(ev["channel"], "call")

    def test_call_notes_without_consent(self):
        run(self.root, "log", "C-0001", "--type", "call_notes", "--summary", "סיכום ידני")
        self.assertEqual(self.client()["stage"], "2b שיחה התקיימה")

    def test_draft_approve_sent_moves_pipeline(self):
        b = self.file("גוף המייל", "b.txt")
        out = run(self.root, "draft", "C-0001", "--kind", "email", "--title", "סיכום שיחה", "--to", "a@example.com",
                  "--subject", "סיכום", "--body-file", b)
        self.assertIn("D001", out)
        c = self.client()
        self.assertEqual(c["pending_drafts"][0]["status"], "draft")
        md = open(os.path.join(self.folder, c["pending_drafts"][0]["file"]), encoding="utf-8").read()
        self.assertIn(cf.DRAFT, md)
        self.assertTrue(any(n.endswith(".eml") for n in os.listdir(os.path.join(self.folder, "outbox"))))
        run(self.root, "approve", "C-0001", "D001")
        self.assertEqual(self.client()["pending_drafts"][0]["status"], "approved")
        run(self.root, "sent", "C-0001", "D001", "--type", "summary_sent")
        c = self.client()
        self.assertEqual(c["pending_drafts"], [])
        self.assertEqual(c["next_owner"], "b2b-proposal")
        self.assertEqual(c["sent"][0]["id"], "D001")

    def test_quote_declined_closes_with_reason(self):
        run(self.root, "log", "C-0001", "--type", "quote_declined", "--who", "client", "--summary", "לא עכשיו",
            "--data", "reason=תקציב")
        c = self.client()
        self.assertTrue(c["stage"].startswith("X"))
        self.assertEqual(c["lost_reason"], "תקציב")
        self.assertNotIn("C-0001", run(self.root, "due", "--days", "30"))

    def test_due_lists_late_items(self):
        run(self.root, "log", "C-0001", "--type", "reply_sent", "--summary", "נשלח",
            "--date", (dt.date.today() - dt.timedelta(days=10)).isoformat())
        self.assertIn("באיחור", run(self.root, "due"))

    def test_history_returns_everything(self):
        t = self.file("שורה ייחודית מהתמלול")
        run(self.root, "log", "C-0001", "--type", "call_transcript", "--summary", "שיחה", "--file", t, "--consent-given")
        run(self.root, "log", "C-0001", "--type", "message_in", "--who", "client", "--channel", "email",
            "--summary", "שאלה על לוח זמנים")
        path = run(self.root, "history", "C-0001").strip()
        h = open(path, encoding="utf-8").read()
        for s in ("רוצה לחבר אקסל", "שורה ייחודית מהתמלול", "שאלה על לוח זמנים", "כל הקבצים בתיק"):
            self.assertIn(s, h)
        brief = open(run(self.root, "history", "C-0001", "--brief", "--out",
                         os.path.join(self.root, "b.md")).strip(), encoding="utf-8").read()
        self.assertNotIn("שורה ייחודית מהתמלול", brief)

    def test_resolve_by_partial_name_and_phone(self):
        self.assertEqual(cf.resolve(self.root, "בדיקה"), self.folder)
        self.assertEqual(cf.resolve(self.root, "050-0000000"), self.folder)

    def test_set_nested_consent(self):
        run(self.root, "set", "C-0001", "consents.recording=yes", "email=a@example.com")
        c = self.client()
        self.assertEqual(c["consents"]["recording"], "yes")
        self.assertEqual(c["email"], "a@example.com")

    def test_lint_catches_money_and_forbidden(self):
        b = self.file("זה יעלה 500 ₪\nיד ימין", "bad.txt")
        run(self.root, "draft", "C-0001", "--kind", "email", "--title", "t", "--body-file", b)
        with self.assertRaises(SystemExit):
            run(self.root, "lint", "C-0001")

    def test_lint_passes_clean_draft_with_placeholders(self):
        b = self.file("היי, המחיר: [קארין ממלאת]. שיחת אפיון של 30 דקות.", "ok.txt")
        run(self.root, "draft", "C-0001", "--kind", "email", "--title", "t", "--body-file", b)
        out = run(self.root, "lint", "C-0001")
        self.assertIn("PASS", out)
        self.assertIn("[קארין ממלאת]", out)

    def test_unknown_event_rejected(self):
        with self.assertRaises(SystemExit):
            run(self.root, "log", "C-0001", "--type", "nope", "--summary", "x")

    def test_timeline_is_valid_jsonl(self):
        run(self.root, "log", "C-0001", "--type", "note", "--summary", 'עם "מרכאות" ו\nשורה חדשה')
        for line in open(os.path.join(self.folder, "timeline.jsonl"), encoding="utf-8"):
            json.loads(line)


if __name__ == "__main__":
    unittest.main()
