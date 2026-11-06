#!/usr/bin/env python3
"""תיק לקוח · the client folder behind the Boost2Business Duet team.

One folder per client. Every input from the client or from Karin is one event
in timeline.jsonl. The event's rule (rules.json) moves the stage, sets the
next action and its due date, and names the Duet skill that handles it.
`history` returns the whole relationship in one file.

    <root>/C-0001 <name>/
        client.json      profile, stage, next action, consents, drafts waiting for Karin
        timeline.jsonl   one JSON line per event (append-only)
        inbox/           what the client sent (messages, files)
        calls/           recordings and transcripts
        outbox/          drafts (emails, messages) and what was sent
        docs/            summaries, quotes, specs, checklists
        HISTORY.md       generated: the full communication history

Root: --root, else $B2B_CLIENTS_DIR, else ./clients. Real client folders are
personal data: they never go to git (CLAUDE.md).

Standard library only, so it runs in Claude Code, in a claude.ai skill sandbox
and in Duet's virtual machine alike.

usage:
  client_folder.py new --name NAME [--phone P] [--email E] [--business B] [--source S] [--track T] [--message TEXT]
  client_folder.py log CLIENT --type TYPE --summary TEXT [--who client|karin|agent] [--channel C]
                       [--file PATH] [--date YYYY-MM-DD] [--data k=v ...] [--consent-given]
  client_folder.py draft CLIENT --kind email|whatsapp|doc --title T --body-file F [--to ADDR] [--subject S] [--gmail-id ID]
  client_folder.py approve CLIENT DRAFT_ID          (Karin approved; the draft can be sent)
  client_folder.py sent CLIENT DRAFT_ID --type EVENT   (Karin sent it; logs EVENT, e.g. summary_sent)
  client_folder.py cancel CLIENT DRAFT_ID --reason R   (a draft that is no longer relevant; never deletes Gmail drafts)
  client_folder.py set CLIENT key=value ...        (profile fields; consents.recording=yes etc.)
  client_folder.py show CLIENT | find TEXT | board | due [--days N] | history CLIENT [--out F] [--brief]
  client_folder.py events                          (the event types and what each triggers)
  client_folder.py lint CLIENT [DRAFT_ID ...]      (checks drafts: stamp, forbidden phrases, money/numbers, recipients)
CLIENT = id (C-0001), folder name, or any unique part of the name/phone/email.
"""
import argparse
import datetime as dt
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DRAFT = "טיוטה לאישור קארין"
WHO = {"client": "הלקוח", "karin": "קארין", "agent": "Duet"}
CHANNELS = {"whatsapp": "וואטסאפ", "email": "מייל", "call": "שיחה", "meeting": "פגישה", "note": "הערה",
            "file": "קובץ", "system": "מערכת", "phone": "טלפון", "linkedin": "לינקדאין", "site": "אתר"}
SUBDIR = {"call_recording": "calls", "call_transcript": "calls", "call_notes": "calls", "document_in": "inbox",
          "message_in": "inbox", "support_request": "inbox", "change_request": "inbox"}
TEXT_EXT = (".txt", ".md", ".vtt", ".srt", ".csv", ".json", ".eml", ".html")
CLOSED = ("X", "Z")


def find_rules():
    for p in (os.path.join(HERE, "rules.json"), os.path.join(HERE, "..", "rules.json"),
              os.path.join(HERE, "..", "references", "rules.json")):
        if os.path.exists(p):
            return json.load(open(p, encoding="utf-8"))
    raise SystemExit("rules.json not found next to the script, one level up, or in ../references/")


RULES = find_rules()


def root_dir(a):
    r = a.root or os.environ.get("B2B_CLIENTS_DIR") or os.path.join(os.getcwd(), "clients")
    os.makedirs(r, exist_ok=True)
    return r


def now():
    return dt.datetime.now().replace(microsecond=0)


def today():
    return dt.date.today()


def load(folder):
    return json.load(open(os.path.join(folder, "client.json"), encoding="utf-8"))


def save(folder, c):
    tmp = os.path.join(folder, "client.json.tmp")
    json.dump(c, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    os.replace(tmp, os.path.join(folder, "client.json"))


def timeline(folder):
    p = os.path.join(folder, "timeline.jsonl")
    if not os.path.exists(p):
        return []
    return [json.loads(line) for line in open(p, encoding="utf-8") if line.strip()]


def folders(root):
    out = []
    for n in sorted(os.listdir(root)):
        f = os.path.join(root, n)
        if os.path.isfile(os.path.join(f, "client.json")):
            out.append(f)
    return out


def resolve(root, key):
    fs = folders(root)
    exact = [f for f in fs if os.path.basename(f) == key or load(f)["id"] == key]
    if exact:
        return exact[0]
    k = key.lower()
    hits = []
    for f in fs:
        c = load(f)
        hay = " ".join(str(c.get(x) or "") for x in ("id", "name", "business", "phone", "email")).lower()
        if k in hay or k in os.path.basename(f).lower():
            hits.append(f)
    if len(hits) == 1:
        return hits[0]
    if not hits:
        raise SystemExit(f"no client matches '{key}'. Try: client_folder.py board")
    raise SystemExit(f"'{key}' matches {len(hits)} clients: " + ", ".join(os.path.basename(h) for h in hits))


def safe_name(s):
    s = re.sub(r'[\\/:*?"<>|\n\r\t]+', " ", s).strip()
    return re.sub(r"\s+", " ", s)[:40] or "לקוח"


def append_event(folder, ev):
    with open(os.path.join(folder, "timeline.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(ev, ensure_ascii=False) + "\n")


def apply_rule(c, etype, when, data):
    """Move the client per rules.json. Returns the rule (or {})."""
    rule = RULES["events"].get(etype, {})
    if rule.get("stage"):
        c["stage"] = rule["stage"]
    if rule.get("next_action") is not None:
        c["next_action"] = rule["next_action"]
        c["next_owner"] = rule.get("owner")
        c["next_template"] = rule.get("template")
        due = None
        if rule.get("due_days") is not None:
            due = when + dt.timedelta(days=rule["due_days"])
        if etype == "call_booked" and data.get("call_date"):
            cd = dt.date.fromisoformat(data["call_date"][:10])
            c["call_date"] = cd.isoformat()
            due = max(when, cd - dt.timedelta(days=1))
        c["next_action_date"] = due.isoformat() if due else ""
    if etype == "quote_declined" and data.get("reason"):
        c["lost_reason"] = data["reason"]
    return rule


def store_file(folder, src, etype, who):
    sub = SUBDIR.get(etype) or ("inbox" if who == "client" else "docs")
    os.makedirs(os.path.join(folder, sub), exist_ok=True)
    base = f"{today():%Y%m%d}-{os.path.basename(src)}"
    dst = os.path.join(folder, sub, base)
    i = 2
    while os.path.exists(dst):
        root_, ext = os.path.splitext(base)
        dst = os.path.join(folder, sub, f"{root_}-{i}{ext}")
        i += 1
    shutil.copy2(src, dst)
    return os.path.relpath(dst, folder)


def parse_data(pairs):
    d = {}
    for p in pairs or []:
        if "=" not in p:
            raise SystemExit(f"--data needs key=value, got '{p}'")
        k, v = p.split("=", 1)
        d[k.strip()] = v.strip()
    return d


def do_log(folder, etype, summary, who="karin", channel=None, file=None, date=None, data=None, consent_given=False,
           next_action=None, next_template=None):
    if etype not in RULES["events"]:
        raise SystemExit(f"unknown event type '{etype}'. See: client_folder.py events")
    c = load(folder)
    data = data or {}
    channel = channel or ("call" if etype.startswith("call_") and etype != "call_booked" else "note")
    when = dt.date.fromisoformat(date) if date else today()
    if etype in ("call_recording", "call_transcript"):
        if consent_given:
            c.setdefault("consents", {})["recording"] = "yes"
            c["consents"]["recording_at"] = now().isoformat()
        if c.get("consents", {}).get("recording") != "yes":
            raise SystemExit("אין הסכמה להקלטה בתיק. שואלים את הלקוח בתחילת השיחה, ואז מוסיפים --consent-given "
                             "(או: set CLIENT consents.recording=yes). בלי הסכמה מתעדים עם --type call_notes.")
    ev = {"ts": now().isoformat(), "date": when.isoformat(), "type": etype, "who": who, "channel": channel,
          "summary": summary.strip()}
    if file:
        if not os.path.isfile(file):
            raise SystemExit(f"file not found: {file}")
        ev["file"] = store_file(folder, file, etype, who)
        if etype == "call_recording" and not file.lower().endswith(TEXT_EXT):
            ev["note"] = "הקלטה בלי תמלול. Duet לא מתמלל אודיו: מעלים תמלול מהכלי שהקליט (--type call_transcript)."
    if data:
        ev["data"] = data
    rule = apply_rule(c, etype, when, data)
    if next_action is not None:  # the skill knows better than the generic rule (e.g. the call was already offered)
        c["next_action"] = next_action
    if next_template is not None:
        c["next_template"] = next_template
    if rule.get("next_action") is not None:
        ev["next"] = {"action": c.get("next_action"), "date": c.get("next_action_date"), "owner": c.get("next_owner")}
    c["updated"] = ev["ts"]
    c["last_contact"] = when.isoformat() if who == "client" else c.get("last_contact", "")
    append_event(folder, ev)
    save(folder, c)
    return ev, c


# ------------------------------------------------------------------ commands
def cmd_new(a):
    root = root_dir(a)
    nums = [int(m.group(1)) for f in folders(root) if (m := re.match(r"C-(\d+)", load(f)["id"]))]
    cid = f"C-{(max(nums) + 1) if nums else 1:04d}"
    folder = os.path.join(root, f"{cid} {safe_name(a.name)}")
    for sub in ("inbox", "calls", "outbox", "docs"):
        os.makedirs(os.path.join(folder, sub), exist_ok=True)
    c = {"id": cid, "name": a.name, "phone": a.phone or "", "email": a.email or "", "business": a.business or "",
         "source": a.source or "לא ידוע", "track": a.track or "עוד לא ברור", "created": today().isoformat(),
         "stage": "", "next_action": "", "next_action_date": "", "next_owner": None,
         "consents": {"contact": "yes" if a.consent_contact else "", "recording": ""},
         "pending_drafts": [], "lost_reason": "", "notes": ""}
    save(folder, c)
    ev, c = do_log(folder, "lead_in", a.message or "פנייה חדשה", who="client", channel=a.channel,
                   next_action=a.next, next_template=a.next_template)
    print(f"נפתח תיק: {os.path.basename(folder)}")
    print(f"הצעד הבא: {c['next_action']} · עד {c['next_action_date']} · מטפל: {c['next_owner']}")
    print(folder)


def cmd_log(a):
    folder = resolve(root_dir(a), a.client)
    ev, c = do_log(folder, a.type, a.summary, a.who, a.channel, a.file, a.date, parse_data(a.data), a.consent_given,
                   a.next, a.next_template)
    label = RULES["events"][a.type]["label"]
    print(f"נרשם ב-{c['id']}: {label}" + (f" · קובץ: {ev['file']}" if ev.get("file") else ""))
    if ev.get("note"):
        print(ev["note"])
    print(f"שלב: {c['stage']} · הצעד הבא: {c['next_action'] or '—'} · עד {c['next_action_date'] or '—'} · מטפל: {c['next_owner'] or '—'}")


def cmd_draft(a):
    folder = resolve(root_dir(a), a.client)
    c = load(folder)
    body = open(a.body_file, encoding="utf-8").read().strip()
    if DRAFT not in body and DRAFT not in (a.title or ""):
        body = f"[{DRAFT}]\n\n{body}"
    did = f"D{sum(1 for e in timeline(folder) if e['type'] == 'draft_created') + 1:03d}"
    stamp = f"{now():%Y%m%d-%H%M}"
    base = os.path.join(folder, "outbox", f"{stamp}-{did}-{a.kind}")
    md = [f"# {a.title}", f"- סטטוס: {DRAFT}", f"- סוג: {a.kind}"]
    if a.to:
        md.append(f"- אל: {a.to}")
    if a.subject:
        md.append(f"- נושא: {a.subject}")
    if a.gmail_id:
        md.append(f"- טיוטה ב-Gmail: {a.gmail_id}")
    open(base + ".md", "w", encoding="utf-8").write("\n".join(md) + "\n\n" + body + "\n")
    files = [os.path.relpath(base + ".md", folder)]
    if a.kind == "email":
        # an .eml Karin can open in any mail app (marked as a draft); she sends it herself
        eml = (f"X-Unsent: 1\nTo: {a.to or ''}\nSubject: {a.subject or a.title}\nMIME-Version: 1.0\n"
               f"Content-Type: text/plain; charset=utf-8\nContent-Transfer-Encoding: 8bit\n\n{body}\n")
        open(base + ".eml", "w", encoding="utf-8").write(eml)
        files.append(os.path.relpath(base + ".eml", folder))
    c.setdefault("pending_drafts", []).append({"id": did, "kind": a.kind, "title": a.title, "file": files[0],
                                               "created": now().isoformat(), "status": "draft",
                                               "gmail_id": a.gmail_id or ""})
    save(folder, c)
    do_log(folder, "draft_created", f"{a.title}" + (f" · אל {a.to}" if a.to else ""), who="agent",
           channel="email" if a.kind == "email" else a.kind, data={"draft_id": did, "file": files[0]})
    print(f"טיוטה {did} נשמרה ({DRAFT}): " + ", ".join(files))


def _draft(c, did):
    for d in c.get("pending_drafts", []):
        if d["id"] == did:
            return d
    raise SystemExit(f"no draft {did}. Pending: " + ", ".join(d["id"] for d in c.get("pending_drafts", [])) or "none")


def cmd_approve(a):
    folder = resolve(root_dir(a), a.client)
    c = load(folder)
    d = _draft(c, a.draft_id)
    d["status"] = "approved"
    save(folder, c)
    do_log(folder, "draft_approved", f"קארין אישרה: {d['title']}", who="karin", channel="note", data={"draft_id": d["id"]})
    print(f"{d['id']} אושרה. כשנשלחה: sent {c['id']} {d['id']} --type <event>")


def cmd_sent(a):
    folder = resolve(root_dir(a), a.client)
    c = load(folder)
    d = _draft(c, a.draft_id)
    c["pending_drafts"] = [x for x in c["pending_drafts"] if x["id"] != d["id"]]
    c.setdefault("sent", []).append({**d, "status": "sent", "sent": now().isoformat()})
    save(folder, c)
    ch = "email" if d["kind"] == "email" else ("whatsapp" if d["kind"] == "whatsapp" else "file")
    ev, c = do_log(folder, a.type, a.summary or f"נשלח: {d['title']}", who="karin", channel=ch,
                   data={"draft_id": d["id"], "file": d["file"]}, next_action=a.next, next_template=a.next_template)
    print(f"נרשם שנשלח ({RULES['events'][a.type]['label']}). הצעד הבא: {c['next_action'] or '—'} · עד {c['next_action_date'] or '—'}")


def cmd_cancel(a):
    folder = resolve(root_dir(a), a.client)
    c = load(folder)
    d = _draft(c, a.draft_id)
    c["pending_drafts"] = [x for x in c["pending_drafts"] if x["id"] != d["id"]]
    c.setdefault("cancelled", []).append({**d, "status": "cancelled", "reason": a.reason})
    save(folder, c)
    do_log(folder, "draft_cancelled", f"בוטלה: {d['title']} · {a.reason}", who="agent", channel="note",
           data={"draft_id": d["id"]})
    print(f"{d['id']} בוטלה ({a.reason}). אם יש טיוטה ב-Gmail, קארין מוחקת אותה בעצמה." if d.get("gmail_id") else f"{d['id']} בוטלה ({a.reason}).")


def cmd_set(a):
    folder = resolve(root_dir(a), a.client)
    c = load(folder)
    changed = []
    for p in a.pairs:
        k, _, v = p.partition("=")
        tgt = c
        parts = k.split(".")
        for part in parts[:-1]:
            tgt = tgt.setdefault(part, {})
        tgt[parts[-1]] = v
        changed.append(k)
    save(folder, c)
    do_log(folder, "profile_update", "עודכן: " + ", ".join(changed), who="karin", channel="note")
    print(f"{c['id']}: " + ", ".join(changed))


def cmd_show(a):
    folder = resolve(root_dir(a), a.client)
    c = load(folder)
    print(json.dumps(c, ensure_ascii=False, indent=2))
    print("\nאירועים אחרונים:")
    for e in timeline(folder)[-8:]:
        print(f"  {e['date']} · {WHO.get(e['who'], e['who'])} · {RULES['events'].get(e['type'], {}).get('label', e['type'])}: {e['summary'][:90]}")


def cmd_find(a):
    root = root_dir(a)
    k = a.text.lower()
    for f in folders(root):
        c = load(f)
        hay = json.dumps(c, ensure_ascii=False).lower()
        tl = [e for e in timeline(f) if k in json.dumps(e, ensure_ascii=False).lower()]
        if k in hay or tl:
            print(f"{os.path.basename(f)} · {c['stage']} · {len(tl)} אירועים תואמים")


def is_open(c):
    return bool(c.get("stage")) and not c["stage"].startswith(CLOSED)


def cmd_board(a):
    root = root_dir(a)
    rows = [load(f) for f in folders(root)]
    if not rows:
        print("אין עדיין תיקים.")
        return
    order = {s: i for i, s in enumerate(RULES["stages"])}
    for c in sorted(rows, key=lambda c: (order.get(c["stage"], 99), c.get("next_action_date") or "9")):
        pend = len(c.get("pending_drafts", []))
        flag = " ⏳" + str(pend) if pend else ""
        print(f"{c['id']} · {c['name'][:18]:<18} · {c['stage']:<16} · {c.get('next_action') or '—'} · {c.get('next_action_date') or '—'}{flag}")


def cmd_due(a):
    root = root_dir(a)
    limit = today() + dt.timedelta(days=a.days)
    hits = []
    for f in folders(root):
        c = load(f)
        if is_open(c) and c.get("next_action_date") and dt.date.fromisoformat(c["next_action_date"]) <= limit:
            hits.append(c)
    pending = [(load(f), d) for f in folders(root) for d in load(f).get("pending_drafts", [])]
    if not hits and not pending:
        print("אין משימות פתוחות לטווח הזה.")
    for c in sorted(hits, key=lambda c: c["next_action_date"]):
        late = (today() - dt.date.fromisoformat(c["next_action_date"])).days
        tag = f"באיחור {late} ימים" if late > 0 else ("היום" if late == 0 else f"בעוד {-late} ימים")
        print(f"{tag:<14} · {c['id']} {c['name']} · {c['next_action']} · מטפל: {c.get('next_owner') or '—'}")
    for c, d in pending:
        print(f"{'מחכה לאישור':<14} · {c['id']} {c['name']} · {d['id']} {d['title']} ({d['status']})")


def cmd_events(a):
    for k, r in RULES["events"].items():
        nxt = f" → {r['stage'] or 'אותו שלב'} · {r['next_action'] or '—'} · {r['owner'] or '—'}" if r["next_action"] is not None or r["stage"] else ""
        print(f"{k:<18} {r['label']}{nxt}")


def read_text(folder, rel, limit=None):
    p = os.path.join(folder, rel)
    if not rel.lower().endswith(TEXT_EXT) or not os.path.exists(p):
        return None
    t = open(p, encoding="utf-8", errors="replace").read().strip()
    if limit and len(t) > limit:
        t = t[:limit] + "\n…(קוצר. הקובץ המלא בתיק)"
    return t


def history_md(folder, brief=False):
    c = load(folder)
    tl = timeline(folder)
    L = [f"# תיק לקוח · {c['name']} ({c['id']})", ""]
    L += [f"- **עסק:** {c.get('business') or '—'} · **מסלול:** {c.get('track') or '—'} · **מקור:** {c.get('source') or '—'}",
          f"- **טלפון:** {c.get('phone') or '—'} · **מייל:** {c.get('email') or '—'}",
          f"- **נפתח:** {c.get('created')} · **קשר אחרון מהלקוח:** {c.get('last_contact') or '—'}",
          f"- **שלב:** {c.get('stage')} · **הצעד הבא:** {c.get('next_action') or '—'} · **עד:** {c.get('next_action_date') or '—'} · **מטפל:** {c.get('next_owner') or '—'}",
          f"- **הסכמות:** יצירת קשר: {c.get('consents', {}).get('contact') or '—'} · הקלטה: {c.get('consents', {}).get('recording') or '—'}"]
    if c.get("lost_reason"):
        L.append(f"- **למה לא המשיך:** {c['lost_reason']}")
    pend = c.get("pending_drafts", [])
    if pend:
        L += ["", "## מחכה לאישור קארין"] + [f"- {d['id']} · {d['title']} · `{d['file']}` ({d['status']})" for d in pend]
    counts = {}
    for e in tl:
        counts[e["channel"]] = counts.get(e["channel"], 0) + 1
    L += ["", f"## כל ההתקשרות ({len(tl)} אירועים)",
          " · ".join(f"{CHANNELS.get(k, k)}: {v}" for k, v in sorted(counts.items(), key=lambda x: -x[1])), ""]
    for e in tl:
        lab = RULES["events"].get(e["type"], {}).get("label", e["type"])
        L.append(f"### {e['date']} · {WHO.get(e['who'], e['who'])} · {CHANNELS.get(e['channel'], e['channel'])} · {lab}")
        L.append(e["summary"])
        if e.get("file"):
            L.append(f"\n📎 `{e['file']}`")
            if not brief:
                t = read_text(folder, e["file"], limit=6000)
                if t:
                    L += ["", "<details><summary>התוכן</summary>", "", "```", t, "```", "</details>"]
        if e.get("data", {}).get("file") and not brief and e["type"] in ("draft_created",):
            t = read_text(folder, e["data"]["file"], limit=4000)
            if t:
                L += ["", "<details><summary>הטיוטה</summary>", "", "```", t, "```", "</details>"]
        if e.get("note"):
            L.append(f"\n> {e['note']}")
        if e.get("next"):
            n = e["next"]
            L.append(f"\n→ הצעד הבא: {n['action'] or '—'} · עד {n['date'] or '—'} · {n['owner'] or ''}")
        L.append("")
    files = []
    for sub in ("inbox", "calls", "outbox", "docs"):
        p = os.path.join(folder, sub)
        if os.path.isdir(p):
            files += [f"{sub}/{n}" for n in sorted(os.listdir(p))]
    L += ["## כל הקבצים בתיק"] + ([f"- `{f}`" for f in files] or ["- אין"])
    L += ["", f"_נוצר ב-{now():%d/%m/%Y %H:%M} · מידע אישי של לקוח: לא משתפים ולא מעלים ל-GitHub._"]
    return "\n".join(L) + "\n"


def cmd_history(a):
    folder = resolve(root_dir(a), a.client)
    md = history_md(folder, a.brief)
    out = a.out or os.path.join(folder, "HISTORY.md")
    open(out, "w", encoding="utf-8").write(md)
    print(out)



FORBIDDEN = ["יד ימין", "קורא חוזים", "מחיר השקה"]
MONEY = re.compile(r"(₪\s*\d|\d[\d,.]*\s*(₪|ש\"ח|שקל|NIS|ils))", re.I)
PCT = re.compile(r"\d+(\.\d+)?\s*%")
HOURS = re.compile(r"\d+(\.\d+)?\s*(שעות|שעה|ימים|דקות)")


def lint_text(text, c):
    """Deterministic checks on one draft. Returns [(level, message)], level FAIL or WARN."""
    out = []
    if DRAFT not in text:
        out.append(("FAIL", f"חסרה החותמת \"{DRAFT}\""))
    for w in FORBIDDEN:
        if w in text:
            out.append(("FAIL", f"ביטוי אסור: {w}"))
    for line in text.splitlines():
        ok_src = any(k in line for k in ("לפי הלקוח", "נתונים לדוגמה", "קארין ממלאת"))
        if MONEY.search(line) and "קארין ממלאת" not in line:
            out.append(("FAIL", f"סכום כסף בלי החלטה של קארין: {line.strip()[:80]}"))
        if PCT.search(line) and not ok_src:
            out.append(("WARN", f"אחוז, לוודא שהלקוח אמר אותו: {line.strip()[:80]}"))
        if HOURS.search(line) and not ok_src and not re.search(r"30 דקות|שיחת אפיון|\d+ שבועות", line):
            out.append(("WARN", f"זמן או כמות, לוודא שמגיע מהלקוח: {line.strip()[:80]}"))
    for addr in set(re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", text)):
        if addr != c.get("email") and not addr.endswith("example.com"):
            out.append(("WARN", f"כתובת מייל שאינה של הלקוח: {addr}"))
    return out


def cmd_lint(a):
    folder = resolve(root_dir(a), a.client)
    c = load(folder)
    drafts = [d for d in c.get("pending_drafts", []) if not a.draft_ids or d["id"] in a.draft_ids]
    if not drafts:
        print("אין טיוטות פתוחות לבדיקה.")
        return
    fails = 0
    for d in drafts:
        text = open(os.path.join(folder, d["file"]), encoding="utf-8").read()
        res = lint_text(text, c)
        fails += sum(1 for lvl, _ in res if lvl == "FAIL")
        print(f"{d['id']} · {d['title']}: " + ("PASS" if not res else ""))
        for lvl, msg in res:
            print(f"  {lvl} · {msg}")
        todo = sorted(set(re.findall(r"\[[^\]]{2,40}\]", text)) - {f"[{DRAFT}]"})
        if todo:
            print("  למילוי לפני שליחה: " + " ".join(todo))
    if fails:
        raise SystemExit(f"{fails} FAIL")


def main(argv=None):
    ap = argparse.ArgumentParser(description="תיק לקוח · Boost2Business Duet")
    ap.add_argument("--root")
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("new")
    p.add_argument("--name", required=True)
    for k in ("phone", "email", "business", "source", "track", "message"):
        p.add_argument(f"--{k}")
    p.add_argument("--channel", default="whatsapp")
    p.add_argument("--consent-contact", action="store_true", help="the lead agreed to be contacted back")
    p.add_argument("--next", help="override the first next action, e.g. when the need is clear: מענה ראשון + הזמנה לשיחה (/שיחה1)")
    p.add_argument("--next-template")
    p.set_defaults(f=cmd_new)
    p = sp.add_parser("log")
    p.add_argument("client")
    p.add_argument("--type", required=True)
    p.add_argument("--summary", required=True)
    p.add_argument("--who", default="karin", choices=list(WHO))
    p.add_argument("--channel", help="whatsapp, email, call, meeting, note… (default: from the event type)")
    p.add_argument("--file")
    p.add_argument("--date")
    p.add_argument("--data", nargs="*")
    p.add_argument("--consent-given", action="store_true")
    p.add_argument("--next", help="override the rule's next action (text)")
    p.add_argument("--next-template", help="override the rule's template, e.g. whatsapp:/שיחה")
    p.set_defaults(f=cmd_log)
    p = sp.add_parser("draft")
    p.add_argument("client")
    p.add_argument("--kind", required=True, choices=["email", "whatsapp", "doc"])
    p.add_argument("--title", required=True)
    p.add_argument("--body-file", required=True)
    p.add_argument("--to")
    p.add_argument("--subject")
    p.add_argument("--gmail-id")
    p.set_defaults(f=cmd_draft)
    p = sp.add_parser("approve")
    p.add_argument("client")
    p.add_argument("draft_id")
    p.set_defaults(f=cmd_approve)
    p = sp.add_parser("sent")
    p.add_argument("client")
    p.add_argument("draft_id")
    p.add_argument("--type", required=True)
    p.add_argument("--summary")
    p.add_argument("--next", help="override the rule's next action (text)")
    p.add_argument("--next-template", help="override the rule's template")
    p.set_defaults(f=cmd_sent)
    p = sp.add_parser("cancel")
    p.add_argument("client")
    p.add_argument("draft_id")
    p.add_argument("--reason", required=True)
    p.set_defaults(f=cmd_cancel)
    p = sp.add_parser("set")
    p.add_argument("client")
    p.add_argument("pairs", nargs="+")
    p.set_defaults(f=cmd_set)
    for name, fn in (("show", cmd_show),):
        p = sp.add_parser(name)
        p.add_argument("client")
        p.set_defaults(f=fn)
    p = sp.add_parser("find")
    p.add_argument("text")
    p.set_defaults(f=cmd_find)
    sp.add_parser("board").set_defaults(f=cmd_board)
    p = sp.add_parser("due")
    p.add_argument("--days", type=int, default=0)
    p.set_defaults(f=cmd_due)
    sp.add_parser("events").set_defaults(f=cmd_events)
    p = sp.add_parser("lint")
    p.add_argument("client")
    p.add_argument("draft_ids", nargs="*")
    p.set_defaults(f=cmd_lint)
    p = sp.add_parser("history")
    p.add_argument("client")
    p.add_argument("--out")
    p.add_argument("--brief", action="store_true", help="summaries only, without file contents")
    p.set_defaults(f=cmd_history)
    a = ap.parse_args(argv)
    a.f(a)


if __name__ == "__main__":
    main()
