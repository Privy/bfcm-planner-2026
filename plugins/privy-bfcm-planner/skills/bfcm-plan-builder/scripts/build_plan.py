#!/usr/bin/env python3
"""Validate a Privy BFCM plan-data.json (v4: starting point, tasks by week or area) and build the plan HTML.

Usage:
  python3 build_plan.py plan-data.json OUTPUT.html                  # validate, then build
  python3 build_plan.py plan-data.json OUTPUT.html --pdf PLAN.pdf   # also render a PDF (needs Playwright)
  python3 build_plan.py plan-data.json --check                      # validate only
  python3 build_plan.py plan-data.json --check --previous OLD.json  # revising: flag removed or repurposed task IDs

Exit code 1 on errors (nothing is built). Warnings print but don't block.
Standard library only; no network access.
"""
from zoneinfo import ZoneInfo
import json, re, sys, datetime as dt
from pathlib import Path

HERE = Path(__file__).resolve().parent
RENDERER = HERE.parent / "assets" / "plan-renderer.html"
if not RENDERER.exists():
    RENDERER = HERE / "plan-renderer.html"   # flat layout (e.g., Claude Project knowledge files)

STATUSES = {"ready", "update", "missing", "unknown", "at_risk"}
PROFILES = {"returning", "switched", "new_store"}
ANCHORS = {"review", "plan", "sends"}
CATEGORIES = {"offer", "flows", "displays", "campaigns", "segments", "site", "compliance", "reporting"}
TASK_STATUS = {"update", "missing", "unknown", "question"}
EVIDENCE = {"privy", "shopify", "merchant", "recommended"}
BLOCKS = {"prose", "table", "callout", "stats", "list"}
ID_RANGES = {"F": 15, "S": 20, "R": 48}
# Attribution: Shopify counts revenue on the order date; Privy credits it to the send date. Never mix them.
SOURCE_BASIS = {  # allowed bases per source; each stat carries exactly one
    "Shopify": {"order_date", "count", "rate"},
    "Privy": {"send_date", "attribution_date", "event_date", "order_date", "count", "rate"},
    "Merchant": {"as_reported"},
}
PLATFORMS = {"shopify", "bigcommerce", "wix", "weebly", "other"}

COMPETITORS = ["klaviyo", "omnisend", "postscript", "mailchimp", "justuno", "optimonk", "sendlane", "drip.com", "yotpo sms", "smsbump", "sms bump", "recart"]
HYPE = ["unlock", "supercharge", "skyrocket", "game-changing", "game changer", "seamless", "effortless", "revolutionary"]
FORECAST_KEYS = {"target", "targets", "forecast", "forecasts", "projection", "projections", "projected"}
FORECAST_TEXT = re.compile(r"\b(forecast(ed|s)?|projected (revenue|sales)|revenue target|target revenue|sales target|we (predict|expect) you|you(?:'ll| will) (make|earn|generate|hit) \$)", re.I)
DEADLINE = re.compile(r"\b(last chance|final hours?|final call|ends? (tonight|today|at midnight|soon)|ending (soon|tonight)|last day|hours? left|now or never|don'?t miss out|countdown)\b", re.I)
SCARCITY = re.compile(r"\b(almost gone|selling (out )?fast|only \d+ left|low stock|limited quantit(y|ies)|while supplies last|going fast)\b", re.I)
MIXED_SHARE = re.compile(r"\b(share|percent|%)\b.*\b(of|from)\b.*\b(email|text|sms|privy)\b|\b(email|text|sms|privy)\b.*\b(share|%)\b", re.I)
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?<!\d)(\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}(?!\d)")
GENRE = {"offer", "flows", "segments", "timeline", "sends", "displays", "deliverability", "review", "plan", "overview", "summary", "grow the list", "sell", "prep", "build"}

errors, warnings = [], []
# Errors block the build; these style and wording rules only warn, so they never trap a build in a fix loop.
STYLE_RULES = (
    "em dashes", "never text or texts", "never coach", "headings name what", "name the dates",
    "unsubscribes as a rat", "per popup view", "hype word", "but the calendar has",
    "3 or 4 plan-specific ideas", "insight tool", "90 characters at most", "shows current numbers only",
)
def err(p, m):
    if any(s in m for s in STYLE_RULES): return warn(p, m)
    errors.append(f"ERROR  {p}: {m}")
def warn(p, m): warnings.append(f"WARN   {p}: {m}")
def tp(t):
    """Name a task by its ID and a text preview, so errors point at the right task even after sorting."""
    return f"tasks.{t.get('id', '?')} (\"{str(t.get('text', ''))[:45]}\")"
def d(v, p):
    try: return dt.date.fromisoformat(str(v)[:10])
    except Exception: err(p, f"not a YYYY-MM-DD date: {v!r}"); return None
def dtm(v, p):
    try: return dt.datetime.fromisoformat(str(v))
    except Exception: err(p, f"not a YYYY-MM-DDTHH:MM datetime: {v!r}"); return None
def need(o, keys, p):
    if not isinstance(o, dict): err(p, "missing or not an object"); return False
    ok = True
    for k in keys:
        if o.get(k) in (None, "", []): err(f"{p}.{k}", "required"); ok = False
    return ok
def cid(v, p, allow=("F", "S", "R")):
    m = re.fullmatch(r"([FSR])(\d\d)", str(v or ""))
    if not m or m.group(1) not in allow or not 1 <= int(m.group(2)) <= ID_RANGES[m.group(1)]:
        err(p, f"invalid checklist ID {v!r} (F01-F15, S01-S20, R01-R48)"); return None
    return v
def claim(t, p):
    if t and (t.strip().lower() in GENRE or len(t.split()) < 4): warn(p, f"\"{t}\" reads like a label; state the claim for this store")
    if t and "\u2014" in t: warn(p, "avoid em dashes in headings")
def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if k.lower() in FORECAST_KEYS: err(f"{path}.{k}" if path else k, "forecast/target fields aren't allowed")
            yield from walk(v, f"{path}.{k}" if path else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            # name items with IDs (tasks, findings) by ID, so paths survive the build re-sorting tasks
            key = f".{v['id']}" if isinstance(v, dict) and v.get("id") else f"[{i}]"
            yield from walk(v, f"{path}{key}")
    elif isinstance(o, str):
        yield path, o

PLATFORM_NAME = {"shopify": "Shopify", "bigcommerce": "BigCommerce", "wix": "Wix", "weebly": "Weebly", "squarespace": "Squarespace", "woocommerce": "WooCommerce"}

def add_standard_tasks(data):
    """Add the tasks the rules always require, unless the plan already has one that meets the rule.
    Generated tasks use fixed IDs (t-std-*) so progress stays attached across rebuilds.
    Skip any by listing its ID in meta.skip_standard_tasks. Returns the IDs added."""
    M, W = data.get("meta") or {}, data.get("window") or {}
    TK = data.setdefault("tasks", [])
    try:
        prep = dt.date.fromisoformat(str(M["prepared_date"]))
        bf = dt.date.fromisoformat(str(W["black_friday"]))
        start = dt.datetime.fromisoformat(str(W["offer_start"])).date()
        end = dt.datetime.fromisoformat(str(W["offer_end"])).date()
    except Exception:
        return []
    cm = bf + dt.timedelta(days=3)
    exposure = min(start, dt.date.fromisoformat(str(W["early_access_start"])[:10])) if W.get("early_access_start") else start
    rows = (data.get("sends") or {}).get("rows") or []
    has_sms = any(r.get("channel") == "sms" for r in rows)
    displays_only = M.get("privy_scope") == "displays"
    skip = set(M.get("skip_standard_tasks") or [])
    owners = M.get("area_owners") or {}
    plat = PLATFORM_NAME.get(str(M.get("platform", "")).lower(), "your store's admin")
    def ds(x): return f"{x.strftime('%b')} {x.day}"
    def iso(x): return max(x, prep + dt.timedelta(days=1)).isoformat()
    def txt(t): return str(t.get("text", "")) + " " + str(t.get("detail", ""))
    def has(pred): return any(pred(t) for t in TK)
    ready = data.get("already_set") or []
    def is_ready(ref=None, name=None):
        return any((ref and str(a.get("ref", "")) == ref) or (name and re.search(name, str(a.get("name", "")), re.I)) for a in ready)
    added = []
    def add(tid, date, cat, pri, text, detail=None, ref=None):
        if tid in skip or any(t.get("id") == tid for t in TK): return
        t = {"id": tid, "date": iso(date), "category": cat, "owner": owners.get(cat, "You"), "status": "missing", "priority": pri, "evidence": "recommended", "text": text}
        if detail: t["detail"] = detail
        if ref: t["ref"] = ref
        TK.append(t); added.append(tid)
    check = lambda t: re.search(r"\b(check|confirm|verify)\b", str(t.get("text", "")), re.I)
    if not has(lambda t: t.get("category") == "offer" and re.search(r"\b(set up|build|create)\b", str(t.get("text", "")), re.I) and re.search(r"\b(discounts?|gifts?|offers?|codes?)\b", str(t.get("text", "")), re.I)):
        add("t-std-discount", start - dt.timedelta(days=21), "offer", "P1", f"Set up the sale discount in {plat}, scheduled with the sale",
            f"Schedule it to start {ds(exposure)} and end {ds(end)}, with the exclusions in your offer terms. Then check it once it's scheduled.")
    if not has(lambda t: re.search(r"\bstack", txt(t), re.I)):
        add("t-std-stacking", start - dt.timedelta(days=18), "offer", "P1", "Check that welcome and popup codes can't stack on the sale discount",
            f"Test a welcome code on a sale-priced order in {plat}, and pause or adjust any code that combines with the sale.")
    pre = exposure - dt.timedelta(days=1)
    if not has(lambda t: t.get("date") == pre.isoformat() and t.get("category") in ("site", "offer") and check(t)):
        add("t-std-precheck", pre, "site", "P1", "Check the sale is set up correctly the day before launch",
            "Confirm the discount is scheduled with the right dates and exclusions, and popups and flows are set to switch on. Test with a hidden code that has the same settings.")
    if not has(lambda t: t.get("date") == exposure.isoformat() and t.get("category") in ("site", "offer") and check(t)):
        add("t-std-golive", exposure, "site", "P1", "Confirm sale prices are showing before the first send", "A quick look: sale prices on a few products and the exclusions holding. The full check happened yesterday.")
    if not has(lambda t: t.get("category") == "displays" and t.get("date") and start - dt.timedelta(days=10) <= dt.date.fromisoformat(t["date"]) <= start):
        add("t-std-display-sale", start - dt.timedelta(days=7), "displays", "P1", "Schedule a sale popup and announcement bar for the whole sale",
            f"Show the offer and the end date. Set it to go live {ds(exposure)} and switch back {ds(end + dt.timedelta(days=1))}.")
    if end < bf and not has(lambda t: t.get("category") in ("campaigns", "displays") and re.search(r"black friday", str(t.get("text", "")), re.I)):
        add("t-std-bfweekend", bf - dt.timedelta(days=11), "campaigns", "P1", "Decide what shoppers see over Black Friday weekend, after your sale ends",
            "A gift-guide or restock email with no discount keeps you in front of shoppers. Switch your popups back to your usual signup offer.")
    if not displays_only and M.get("timezone_sending") and not has(lambda t: re.search(r"time ?zone", str(t.get("text", "")), re.I)):
        add("t-std-tzsend", prep + dt.timedelta(days=11), "campaigns", "P2", "Turn on timezone-based sending for pre-sale emails",
            "Teasers and regular emails then go out at each subscriber's local time. Sale-day sends go out on your store's clock, so shoppers everywhere hear the sale is live at the same moment.")
    if rows and not has(lambda t: t.get("category") == "campaigns" and re.search(r"\bschedule\b", str(t.get("text", "")), re.I)):
        add("t-std-schedule", start - dt.timedelta(days=13), "campaigns", "P1", "Schedule every sale send and preview each one",
            "Check links, the offer wording, and each send's audience before scheduling. Pick exact times a few minutes off the hour, like 9:07, to avoid the queue at the top of the hour.")
    if any(re.search(r"\bS19\b", str(r.get("suppress", ""))) for r in rows) and not is_ready("S19", r"recent.buyers") and not has(lambda t: "S19" in str(t.get("ref", "")) or re.search(r"recent.buyers", txt(t), re.I)):
        add("t-std-recentbuyers", start - dt.timedelta(days=20), "segments", "P2", "Build a recent-buyers segment for the launch email", "People who ordered in the last 7 days. They skip only the launch email.", "S19")
    if any("bought today" in str(r.get("suppress", "")).lower() for r in rows) and not is_ready(None, r"bought today") and not has(lambda t: re.search(r"bought today", txt(t), re.I)):
        add("t-std-boughttoday", bf - dt.timedelta(days=5), "segments", "P2", "Build a \"Bought today\" segment for the evening emails on Black Friday and Cyber Monday",
            "People who ordered in the last 24 hours. They skip the evening email on those days, after buying from the morning one.")
    days = [("launch day", start)]
    if start < bf <= end: days.append(("Black Friday", bf))
    if start < cm <= end: days.append(("Cyber Monday", cm))
    if (end - start).days >= 3 and end not in [x[1] for x in days]: days.append(("the final day", end))
    for label, day in days:
        if has(lambda t, day=day: t.get("date") == day.isoformat() and t.get("category") in ("compliance", "displays") and check(t)): continue
        slug = {"launch day": "launch", "Black Friday": "bf", "Cyber Monday": "cm", "the final day": "final"}[label]
        if displays_only:
            add(f"t-std-watch-{slug}", day, "displays", "P1", f"Check popup signup rates on {label}", "If a sale popup drops well below its usual rate, check it on a phone first.")
        else:
            what = "complaints, bounces, unsubscribes, and SMS opt-outs" if has_sms else "spam complaints, bounces, and unsubscribes"
            add(f"t-std-watch-{slug}", day, "compliance", "P1", f"Check {what} after {label}'s sends", "If spam complaints pass 0.1% on a send, send the rest only to your most engaged contacts.")
    after = end + dt.timedelta(days=1)
    if not has(lambda t: t.get("category") == "reporting" and re.search(r"switch|back|restart|undo|return|turn off|remove", str(t.get("text", "")), re.I)):
        add("t-std-undo", end, "reporting", "P1", "Switch flows and popups back as soon as the sale ends tonight", f"Set it for {W['offer_end'][11:16] or 'the end time'} so flow emails sent overnight stop mentioning the sale. Restart anything you paused, and switch your popups back to your usual signup offer.")
    if not has(lambda t: t.get("category") == "reporting" and re.search(r"\brecap\b|results|mid-december", str(t.get("text", "")), re.I)):
        add("t-std-recap", after, "reporting", "P3", "Book a recap for mid-December")
    TK.sort(key=lambda t: str(t.get("date", "")))
    P = data.get("plan") or {}
    if P.get("title"): P["title"] = re.sub(r"^\d+ tasks\b", f"{len(TK)} tasks", str(P["title"]))
    return added

def main():
    if len(sys.argv) < 3: print(__doc__); sys.exit(2)
    data = json.loads(Path(sys.argv[1]).read_text())
    _added = add_standard_tasks(data)
    if _added: print(f"Added {len(_added)} standard task(s): {', '.join(_added)}")
    M, W = data.get("meta", {}), data.get("window", {})
    need(M, ["store_name", "prepared_date", "timezone", "tz_label", "profile"], "meta")
    if M.get("profile") not in PROFILES: err("meta.profile", f"one of {sorted(PROFILES)}")
    need(W, ["black_friday", "offer_start", "offer_end"], "window")
    if not isinstance(W.get("extension"), bool): err("window.extension", "must be true or false (decide before launch)")
    prep, bf = d(M.get("prepared_date"), "meta.prepared_date"), d(W.get("black_friday"), "window.black_friday")
    start, end = dtm(W.get("offer_start"), "window.offer_start"), dtm(W.get("offer_end"), "window.offer_end")
    cm = bf + dt.timedelta(days=3) if bf else None
    fri = bf + dt.timedelta(days=7) if bf else None
    sat = bf + dt.timedelta(days=8) if bf else None
    if end and fri and end.date() > fri: err("window.offer_end", f"plan window ends {fri} (Friday after Cyber Monday)")
    if end and cm and W.get("extension") is True and end.date() <= cm: err("window.offer_end", "extension is true, so the offer should end after Cyber Monday")
    if start and end and start >= end: err("window", "offer_start must be before offer_end")

    def inwin(v, p):
        x = d(v, p)
        if x and prep and x < prep: err(p, f"{x} is before the plan date {prep}")
        if x and sat and x > sat: err(p, f"{x} is after the plan window (ends {sat} with wrap-up)")
        return x

    need(data.get("sale", {}), ["headline", "terms"], "sale")
    if len(data.get("sale", {}).get("headline", "")) > 110: warn("sale.headline", "over 110 characters; the offer should read in one breath")

    # ---- tasks (one list, shown by week and by area); owners must come from the team the merchant named
    need(data.get("plan", {}), ["title"], "plan"); claim(data.get("plan", {}).get("title"), "plan.title")
    if not re.fullmatch(r"[A-Z]{3}", str(M.get("currency", ""))): err("meta.currency", "ISO 4217 code, e.g. USD or CAD")
    if M.get("platform") not in PLATFORMS: err("meta.platform", f"one of {sorted(PLATFORMS)}")
    PROPER = sorted({str(n) for n in (M.get("proper_names") or [])}
                    | {str(x.get("name")) for sec in ("segments", "flows") for grp in ("included", "skipped") for x in ((data.get("scope") or {}).get(sec, {}).get(grp) or []) if x.get("name")}
                    | {str(a.get("name")) for a in (data.get("already_set") or []) if a.get("name")}, key=len, reverse=True)
    def own_words(s):
        """The text with the merchant's own names removed, so wording rules apply only to our words."""
        s = str(s)
        for n in PROPER: s = s.replace(n, " ")
        return s
    DISPLAYS_ONLY = M.get("privy_scope") == "displays"
    if M.get("privy_scope") not in (None, "full", "displays"): err("meta.privy_scope", "full (default) or displays")
    team = {str(n).strip().lower() for n in (M.get("team") or [])} | {"you"}
    HAS_CSM = bool(M.get("has_csm") or M.get("has_coach"))
    if HAS_CSM: team.add("your privy csm")
    if not M.get("team"): warn("meta.team", "no team names from the interview; every owner will be \"You\"")
    TK = data.get("tasks") or []
    if len(TK) < 8: warn("tasks", "fewer than 8 tasks; is anything missing?")
    if len(TK) > 35: warn("tasks", f"{len(TK)} tasks; keep the plan to what the team can do (about 20-30)")
    step_ids, refs = {}, set()
    _bad_owner, _you_owner = [], []
    for i, t in enumerate(TK):
        p = tp(t); need(t, ["id", "date", "text", "owner", "category", "status", "priority", "evidence"], p)
        if t.get("id") in step_ids: err(p, f"duplicate task id {t.get('id')}")
        step_ids[t.get("id")] = inwin(t.get("date"), f"{p}.date")
        if t.get("category") not in CATEGORIES: err(f"{p}.category", f"one of {sorted(CATEGORIES)}")
        if t.get("status") not in TASK_STATUS: err(f"{p}.status", f"one of {sorted(TASK_STATUS)} (items already Ready go in already_set, not tasks)")
        if t.get("priority") not in ("P1", "P2", "P3"): err(f"{p}.priority", "P1, P2, or P3")
        if t.get("evidence") not in EVIDENCE: err(f"{p}.evidence", f"one of {sorted(EVIDENCE)}")
        if t.get("owner") and str(t["owner"]).strip().lower() not in team: _bad_owner.append(f"{t.get('id')} ({t['owner']})")
        for rf in ([t["ref"]] if isinstance(t.get("ref"), str) else (t.get("ref") or [])):
            if cid(rf, f"{p}.ref"): refs.add(rf)
        if len(t.get("text", "")) > 110: warn(f"{p}.text", "over 110 characters; move the how into detail")
        if re.search(r"\b[FSR]\d\d\b", str(t.get("text", "")) + " " + str(t.get("detail", ""))): warn(p, "internal checklist codes show on the page; use names (keep codes in ref)")
    if start:
        srows = (data.get("sends") or {}).get("rows") or []
        exposure = start.date()
        if W.get("early_access_start"):
            exposure = min(exposure, dt.date.fromisoformat(str(W["early_access_start"])[:10]))
        checks = [t for t in TK if t.get("date") == exposure.isoformat() and t.get("category") in ("site", "offer") and re.search(r"\b(check|confirm|verify)\b", str(t.get("text", "")), re.I)]
        if not checks: err("tasks", f"add a go-live check on {exposure} (the first day anyone sees sale pricing, early access included): pricing live, exclusions holding, one test order, before that day's first send")
        pub = sorted(dtm(f"{r['date']}T{r['time']}", "_") for r in srows if r.get("channel") == "email" and r.get("date") and r.get("time") and dtm(f"{r['date']}T{r['time']}", "_") >= start)
        if pub and (pub[0] - start) < dt.timedelta(minutes=30):
            err("sends", f"the first sale email goes out {int((pub[0] - start).total_seconds() // 60)} minutes after the sale starts; leave at least 30 minutes for the launch-morning confirmation")
        if pub and (pub[0] - start) > dt.timedelta(hours=3):
            warn("sends", f"the sale is live {round((pub[0] - start).total_seconds() / 3600, 1)} hours before the first sale email; start it closer to the send, since the full check happens the day before")
        pre = (exposure - dt.timedelta(days=1)).isoformat()
        if not any(t.get("date") == pre and t.get("category") in ("site", "offer") and re.search(r"\b(check|confirm|verify)\b", str(t.get("text", "")), re.I) for t in TK):
            err("tasks", f"add the day-before check on {pre}: discount scheduled with the right dates and exclusions, popups and flows set to switch on, and a test with a hidden code that has the same settings")
    for i, t in enumerate(TK):
        mm = re.search(r"\b(\d{1,3})\s+(?:sale\s+)?(?:emails|sends|texts)\b", str(t.get("text", "")))
        if mm and int(mm.group(1)) >= 8: warn(tp(t), "a task covering 8+ sends is too big for one date; split writing from scheduling and QA")
        if re.search(r"after every", str(t.get("text", "")), re.I): warn(tp(t), "'after every send' isn't one task; add a monitoring task on each peak day")
    rows_by_date = {}
    for r in (data.get("sends") or {}).get("rows") or []: rows_by_date.setdefault(r.get("date"), []).append(r)
    def as12(hhmm):
        h, m = map(int, hhmm.split(":")); return f"{h % 12 or 12}{'' if m == 0 else f':{m:02d}'}{'am' if h < 12 else 'pm'}"
    for i, t in enumerate(TK):
        for tm in re.findall(r"\b(\d{1,2}(?::\d{2})?\s?(?:am|pm))\b", str(t.get("text", "")) + " " + str(t.get("detail", "")), re.I):
            said = tm.replace(" ", "").lower()
            have = [as12(r["time"]) for r in rows_by_date.get(t.get("date"), []) if r.get("time")]
            if have and said not in have:
                err(tp(t), f"says {tm}, but the calendar's sends that day are at {', '.join(have)}; keep times in the calendar only")
    for k, w in enumerate((data.get("warmup") or {}).get("steps") or []):
        if not any(t.get("date") == w.get("from") and t.get("category") == "campaigns" for t in TK):
            err(f"warmup.steps[{k}]", f"add a campaigns task dated {w.get('from')} for this warm-up send")
    sale_rows = [r for r in (data.get("sends") or {}).get("rows") or [] if r.get("date")]
    if start and sale_rows:
        _sale_start = dt.date.fromisoformat(str(W["early_access_start"])[:10]) if W.get("early_access_start") else start.date()
        _sale_dates = [dt.date.fromisoformat(r["date"]) for r in sale_rows if dt.date.fromisoformat(r["date"]) >= _sale_start]
        first = min(_sale_dates) if _sale_dates else min(dt.date.fromisoformat(r["date"]) for r in sale_rows)
        ramp = [dt.date.fromisoformat(t["date"]) for t in TK if t.get("category") == "campaigns" and t.get("date") and first - dt.timedelta(days=35) <= dt.date.fromisoformat(t["date"]) <= first - dt.timedelta(days=3)]
        ramp += [dt.date.fromisoformat(r["date"]) for r in sale_rows if first - dt.timedelta(days=35) <= dt.date.fromisoformat(r["date"]) <= first - dt.timedelta(days=3)]
        if len(ramp) < 2 or min(ramp) > first - dt.timedelta(days=14):
            warn("tasks", "add at least two regular sends to engaged contacts in the 5 weeks before the first sale send, one of them 2+ weeks out, so volume ramps up instead of starting cold")
    if start and not any(t.get("category") == "displays" and t.get("date") and start.date() - dt.timedelta(days=10) <= dt.date.fromisoformat(t["date"]) <= start.date() for t in TK):
        err("tasks", "add a displays task in the 10 days before the sale: a sale-period popup or bar live for the whole sale, reverted after")
    has_sms = any(r.get("channel") == "sms" for r in sale_rows)
    for i, t in enumerate(TK):
        if t.get("category") == "compliance" and re.match(r"check", str(t.get("text", "")), re.I) and has_sms and "opt-out" not in str(t.get("text", "")).lower():
            warn(tp(t), "monitoring should include SMS opt-outs, since this plan sends SMS")
    if has_sms and not any(t.get("category") == "displays" and re.search(r"\bsms\b", str(t.get("text", "")), re.I) for t in TK):
        warn("tasks", "the plan sends SMS but has no task to grow the SMS list (an SMS step on the popup)")
    send_txt = " ".join(str(r.get("audience", "")) + " " + str(r.get("suppress", "")) for r in (data.get("sends") or {}).get("rows") or [])
    for t in TK:
        for rf in ([t["ref"]] if isinstance(t.get("ref"), str) else (t.get("ref") or [])):
            if re.fullmatch(r"S\d\d", str(rf)) and rf not in ("S19", "S20", "S02") and t.get("category") == "segments" and not re.search(r"\b" + rf + r"\b", send_txt):
                warn(f"tasks.{t.get('id')}", f"{rf} gets built but no send uses it; add a send or drop the build")
    if M.get("team"):
        for t in TK:
            if str(t.get("owner", "")).strip().lower() == "you": _you_owner.append(str(t.get("id")))
    srows_all = (data.get("sends") or {}).get("rows") or []
    if any(r.get("channel") == "sms" for r in srows_all) and start:
        bfd = W.get("black_friday")
        if not any(r.get("channel") == "sms" and r.get("date") == bfd for r in srows_all): warn("sends", "the plan sends SMS but none on Black Friday")
        if end and not any(r.get("channel") == "sms" and r.get("date") and dtm(f"{r['date']}T{r['time']}", "_") and end - dtm(f"{r['date']}T{r['time']}", "_") <= dt.timedelta(hours=24) for r in srows_all):
            warn("sends", "the plan sends SMS but none in the sale's final 24 hours")
    for t in TK:
        if re.search(r"\b(check|confirm|find out) whether\b.*\b(works?|supported|available)\b", str(t.get("text", "")), re.I):
            warn(f"tasks.{t.get('id')}", "look Privy capabilities up in Privy's help center (search_help_docs) instead of asking the merchant")
    if start and end:
        bfd = dt.date.fromisoformat(W["black_friday"]); cmd = bfd + dt.timedelta(days=3)
        offer_txt = " ".join(str((data.get("sale") or {}).get(k, "")) for k in ("headline", "terms"))
        for phrase, day in (("through cyber monday", cmd), ("through black friday", bfd)):
            if phrase in offer_txt.lower() and end.date() != day:
                err("sale", f"says '{phrase}', but the offer ends {end.date()}; make the words and the dates match")
        if end.date() < bfd and not any(t.get("date") and re.search(r"black friday", str(t.get("text", "")), re.I) and t.get("category") in ("campaigns", "displays") for t in TK):
            err("tasks", "the sale ends before Black Friday; add a task deciding what shoppers see over Black Friday weekend (a restock or gift-guide email, or a site message)")
        if (end.date() - start.date()).days >= 3 and not any(t.get("date") == end.date().isoformat() and re.match(r"check", str(t.get("text", "")), re.I) and t.get("category") in ("compliance", "displays") for t in TK):
            warn("tasks", f"add a monitoring check on the sale's final day, {end.date()}")
    for i, t in enumerate(TK):
        if start and t.get("date") and t.get("category") in ("flows", "displays") and dt.date.fromisoformat(t["date"]) < start.date() \
           and re.search(r"\b(sale|event|black friday week)\b", str(t.get("text", "")), re.I) and not re.search(r"go(es)? live", str(t.get("detail", "")), re.I):
            warn(f"tasks.{t.get('id')}", "prepared early: say when it goes live and when it switches back, so the build date isn't read as the start date")
    if start and not any(t.get("category") == "offer" and re.search(r"\b(set up|build|create)\b", str(t.get("text", "")), re.I) and re.search(r"\b(discounts?|gifts?|offers?|codes?)\b", str(t.get("text", "")), re.I) for t in TK):
        warn("tasks", "add a task to set up the sale discount (or gift) itself, scheduled to start and end with the sale")
    RX = data.get("remix")
    if RX is None: warn("remix", "add 3 or 4 plan-specific ideas for 'Make it yours' (things to ask the agent)")
    else:
        if not isinstance(RX, list) or not 3 <= len(RX) <= 4: err("remix", "3 or 4 plan-specific ideas")
        for k, q in enumerate(RX if isinstance(RX, list) else []):
            if len(str(q)) > 90: err(f"remix[{k}]", "90 characters at most")
            if re.match(r"\s*(write|draft|compose)\b", str(q), re.I):
                err(f"remix[{k}]", "the planner is an insight tool and doesn't write campaigns; phrase it as a question (\"What should the Black Friday email lead with?\")")
            if re.search(r"\b(set up|create|turn (on|off)|switch (on|off)|enable|disable|publish|delete)\b", str(q), re.I):
                err(f"remix[{k}]", "ideas can't suggest the agent changes the store or Privy; it only reads them. Phrase it as planning or writing help")
    SLOGAN = re.compile(r",\s*not\s|\bnot an?\b.*\b(promise|guarantee)\b|\b(is|are) (key|everything)\b|\bgame.?changer\b", re.I)
    for path_, val in (("plan.title", (data.get("plan") or {}).get("title")), ("sends.title", (data.get("sends") or {}).get("title")), ("closing.title", (data.get("closing") or {}).get("title"))):
        if val and SLOGAN.search(str(val)): err(path_, "headings name what's there; no slogans or \"X, not Y\" lines")
    if str(M.get("platform", "")).lower() != "shopify":
        _plat = str(M.get("platform") or "their platform")
        for path_, val in ([(f"tasks.{t.get('id')}", str(t.get("text", "")) + " " + str(t.get("detail", ""))) for t in TK]
                           + [(f"review.findings[{k}]", str(f.get("change", "")) + " " + str(f.get("observation", ""))) for k, f in enumerate(((data.get("review") or {}).get("findings")) or [])]
                           + [(f"sends.rows[{k}]", str(r.get("subject", "")) + " " + str(r.get("message", ""))) for k, r in enumerate(((data.get("sends") or {}).get("rows")) or [])]):
            if re.search(r"\bshopify\b|buy x get y", own_words(val), re.I) and not re.search(r"\bneeds? shopify\b|only (on|for) shopify|shopify only|isn.t available", val, re.I):
                err(path_, f"this store runs on {_plat}; use its wording, not Shopify's (platform wording)")
    for t_ in TK:
        if re.search(r"\b(stale|out of date|outdated|last (updated|refreshed)|hasn.t refreshed)\b", str(t_.get("detail", "")) + " " + str(t_.get("text", "")), re.I):
            warn(f"tasks.{t_.get('id')}", "Privy-side data issues (stale counts, sync delays) aren't merchant tasks; if one affects a number the merchant relies on, tell them in chat and note it in basis")
    _lim = M.get("email_limit") or {}
    _em = sorted({r.get("date") for r in ((data.get("sends") or {}).get("rows") or []) if r.get("channel") == "email" and r.get("date")})
    if _lim.get("per_day"):
        from collections import Counter as _C
        _cnt = _C(r.get("date") for r in ((data.get("sends") or {}).get("rows") or []) if r.get("channel") == "email")
        for _d, _n in sorted(_cnt.items()):
            if _n > int(_lim["per_day"]): err("sends", f"{_d} has {_n} emails, but the merchant asked for at most {_lim['per_day']} a day")
    if _lim.get("every_days"):
        for _a, _b in zip(_em, _em[1:]):
            if (dt.date.fromisoformat(_b) - dt.date.fromisoformat(_a)).days < int(_lim["every_days"]):
                err("sends", f"emails on {_a} and {_b} are closer than the merchant's pace of one email every {_lim['every_days']} days")
    _MON = {m: i for i, m in enumerate(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"], 1)}
    for t_ in TK:
        try: _td = dt.date.fromisoformat(str(t_.get("date")))
        except Exception: continue
        _later = [dt.date(_td.year, _MON[mm], int(dd)) for mm, dd in re.findall(r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2})\b", str(t_.get("text", "")) + " " + str(t_.get("detail", "")))]
        _later = [x for x in _later if (x - _td).days > 7]
        _txt = str(t_.get("text", "")) + " " + str(t_.get("detail", ""))
        if _later and t_.get("category") == "flows" and not re.search(r"go(es)? live|switch(es)? back|set (it )?to", _txt, re.I) and not re.match(r"\s*pause\b", str(t_.get("text", "")), re.I):
            warn(tp(t_), f"its details reach {max(_later).strftime('%b')} {max(_later).day}, well after its own date; split it into one task per date (set up now, add sale wording when the public sale starts, remove it when the sale ends)")
    WHOLE = re.compile(r"\b(everyone|whole list|full list|full-list|entire list|all contacts|all subscribers)\b", re.I)
    _bf = dt.date.fromisoformat(W["black_friday"]) if W.get("black_friday") else None
    _peak = {(_bf).isoformat(), (_bf + dt.timedelta(days=3)).isoformat()} if _bf else set()
    _risk = bool(M.get("deliverability_risk")) or bool(data.get("warmup"))
    _rows = (data.get("sends") or {}).get("rows") or []
    for k, r in enumerate(_rows):
        aud = str(r.get("audience", "")); peak = r.get("date") in _peak and r.get("channel") == "email" and not r.get("post_sale")
        if WHOLE.search(aud): err(f"sends.rows[{k}].audience", "never 'everyone' or 'all contacts'; the broadest email audience is 'All engaged contacts', or 'All email subscribers' on Black Friday and Cyber Monday")
        if re.fullmatch(r"\s*all email subscribers\s*", aud, re.I) and not peak: err(f"sends.rows[{k}].audience", "'All email subscribers' is only for Black Friday and Cyber Monday emails; use 'All engaged contacts' with the unengaged exclusion")
        if r.get("channel") == "email" and not re.search(r"\bS20\b", str(r.get("suppress", ""))) and not (peak and not _risk):
            err(f"sends.rows[{k}].suppress", "this email excludes unengaged contacts (S20). Only Black Friday and Cyber Monday emails skip it, and not when the plan has a warm-up or meta.deliverability_risk")
        if peak and any(o.get("channel") == "email" and o.get("date") == r.get("date") and str(o.get("time", "")) < str(r.get("time", "")) and not o.get("post_sale") for o in _rows) and "bought today" not in str(r.get("suppress", "")).lower():
            err(f"sends.rows[{k}].suppress", "a later email on Black Friday or Cyber Monday leaves out people who bought earlier that day (\"Bought today\")")
    for key in ("title", "lede"):
        if WHOLE.search(str((data.get("sends") or {}).get(key, ""))): err(f"sends.{key}", "don't recommend the whole list; say 'all engaged contacts'")
    for i, t in enumerate(TK):
        if WHOLE.search(own_words(str(t.get("text", "")) + " " + str(t.get("detail", "")))): err(tp(t), "don't recommend the whole list; say 'all engaged contacts' (or 'broad sends' for past ones)")
    for k, f in enumerate(((data.get("review") or {}).get("findings")) or []):
        if WHOLE.search(str(f.get("change", "")) + " " + str(f.get("observation", ""))): err(f"review.findings[{k}]", "don't recommend the whole list; say 'all engaged contacts' (or 'broad sends' for past ones)")
    BROWSE_SMS = re.compile(r"\b(add|adding|build|create|set up|start)\w*\s+(an?\s+)?sms\b[^.]*\bbrowse|\bbrowse\b[^.]*\b(add|adding|build|create|set up|start)\w*\s+(an?\s+)?sms\b", re.I)
    for i, t in enumerate(TK):
        if BROWSE_SMS.search(str(t.get("text", "")) + ". " + str(t.get("detail", ""))): err(tp(t), "never recommend adding SMS to browse abandonment; SMS is for higher-intent flows")
    for k, f in enumerate(((data.get("review") or {}).get("findings")) or []):
        if BROWSE_SMS.search(str(f.get("change", "")) + ". " + str(f.get("observation", ""))): err(f"review.findings[{k}]", "never recommend adding SMS to browse abandonment; SMS is for higher-intent flows")
    for i, a_ in enumerate(data.get("already_set") or []):
        need(a_, ["category", "name"], f"already_set[{i}]")
        if a_.get("category") not in CATEGORIES: err(f"already_set[{i}].category", f"one of {sorted(CATEGORIES)}")
        for rf in ([a_["ref"]] if isinstance(a_.get("ref"), str) else (a_.get("ref") or [])):
            if cid(rf, f"already_set[{i}].ref"): refs.add(rf)
    G = data.get("goals") or {}
    for i, g in enumerate(G.get("items") or []):
        need(g, ["goal", "by", "check"], f"goals.items[{i}]"); inwin(g.get("by"), f"goals.items[{i}].by")
    if not G.get("items"): warn("goals", "no goals the merchant controls (signups, flows live, complaint rate)")
    WU = data.get("warmup")
    if WU:
        need(WU, ["intro", "steps"], "warmup")
        for k, w in enumerate(WU.get("steps") or []):
            need(w, ["audience", "from"], f"warmup.steps[{k}]")
            if w.get("from") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(w["from"])):
                err(f"warmup.steps[{k}].from", f"a date like \"2026-11-06\" (when this audience starts getting sends), not \"{w['from']}\"")
            else: inwin(w.get("from"), f"warmup.steps[{k}].from")
            if re.search(r"\d[\d,]*\s*(emails|sends|messages|contacts)?\s*(/|per)\s*(day|hour)", str(w.get("audience")), re.I):
                err(f"warmup.steps[{k}]", "no volume numbers or daily caps; give the audience order only")
    # warm-up depends on recent Privy sending, not on the profile
    fs = d(M.get("privy_first_send"), "meta.privy_first_send") if M.get("privy_first_send") else None
    ls = d(M.get("privy_last_send"), "meta.privy_last_send") if M.get("privy_last_send") else None
    if "privy_first_send" not in M or "privy_last_send" not in M:
        err("meta", "privy_first_send and privy_last_send are required (dates, or null when there are no Privy sends)")
    elif prep and DISPLAYS_ONLY:
        pass
    elif prep:
        why = None
        if not fs or not ls: why = "no Privy sending history"
        elif (prep - fs).days < 90: why = f"first Privy send was {(prep - fs).days} days ago"
        elif (prep - ls).days > 30: why = f"no Privy sends for {(prep - ls).days} days"
        if why and not WU: err("warmup", f"a warm-up is required ({why}); give the audience order, no volume numbers")
        if not why and WU: warn("warmup", "recent, established Privy sending; a warm-up usually isn't needed")
    # today: the store snapshot from stage 3
    TD = data.get("today")
    if TD:
        need(TD, ["as_of", "stats"], "today"); ao = d(TD.get("as_of"), "today.as_of")
        if ao and prep and (ao > prep or (prep - ao).days > 14): warn("today.as_of", "snapshot should be from the last two weeks")
        if len(TD.get("stats") or []) > 4: err("today.stats", "4 stats at most")
        for k, s_ in enumerate(TD.get("stats") or []):
            p = f"today.stats[{k}]"; need(s_, ["label", "value", "source", "basis"], p)
            if s_.get("source") not in ("Privy", "Shopify"): err(f"{p}.source", "Privy or Shopify (today's numbers come from the connected data)")
            if s_.get("basis") not in ("count", "rate", "order_date", "send_date"): err(f"{p}.basis", "count, rate, order_date, or send_date")
    else:
        warn("today", "no store snapshot; show today's list, displays, flows, and deliverability from stage 3")
    _st = (TD or {}).get("stats") or []
    _first = [str(x.get("text", "")).strip().lower() for x in _st[:2]]
    if _first != ["total mailable contacts", "total textable contacts"]:
        _msg = "the first two today.stats must be {\"text\": \"Total mailable contacts\", ...} then {\"text\": \"Total textable contacts\", ...}, with any others after. Today at Privy starts with \"Total mailable contacts\" and \"Total textable contacts\" (contacts with email and SMS consent subscribed, PV2)"
        if str(M.get("prepared_date", "")) >= "2026-10-01": err("today.stats", _msg)
        else: warn("today.stats", _msg + "; this plan predates the rule")
    for k, s_ in enumerate((TD or {}).get("stats") or []):
        if re.search(r"\blast (30|60|90|365) days\b", str(s_.get("text", "")), re.I):
            (err if str(M.get("prepared_date", "")) >= "2026-10-01" else warn)(f"today.stats[{k}].text", "name the dates (\"Jul 3 to Sep 30\"), not \"last 90 days\"; the dashboard's window moves")
        if str(s_.get("source", "Privy")).lower() not in ("privy", ""):
            err(f"today.stats[{k}].source", "the Today at Privy card shows Privy figures only; put store figures in the snapshot or a recommendation")
        if s_.get("text") and len(s_["text"]) > 70: warn(f"today.stats[{k}].text", "keep it under 70 characters")
        if re.search(r"\b(up|down)\s+(\d|a\b|an\b|from\b|by\b)", str(s_.get("text", "")), re.I):
            err(f"today.stats[{k}].text", "Today at Privy shows current numbers only; put a comparison in a recommendation and name both periods")

    # ---- review: observations only, never mix Shopify order-date and Privy send-date revenue
    R = data.get("review")
    if R:
        if M.get("profile") == "new_store": err("review", "new_store has no BFCM history; omit the review")
        if not (R.get("daily") or R.get("channels") or R.get("findings")): err("review", "needs daily store revenue, Privy channels, or findings")
        if (R.get("daily") or {}).get("peak_label") and len(R["daily"]["peak_label"]) > 20: err("review.daily.peak_label", "20 characters at most")
        co = R.get("callout")
        if co is not None:
            need(co, ["figure", "text"], "review.callout")
            if len(str(co.get("figure", ""))) > 16: err("review.callout.figure", "16 characters at most")
            if len(str(co.get("text", ""))) > 90: err("review.callout.text", "90 characters at most")
            if not R.get("channels"): err("review.callout", "the callout sits in the Privy card, so it needs review.channels")
        py = (bf.year - 1) if bf else None
        def in_last_year(v, p):
            x = d(v, p)
            if x and py and not (dt.date(py, 11, 1) <= x <= dt.date(py, 12, 31)): err(p, f"{x} isn't in last year's Nov-Dec")
            return x
        dl = R.get("daily")
        if dl:
            if dl.get("source") not in ("Shopify", "Privy") or dl.get("basis") != "order_date":
                err("review.daily", "daily revenue is store orders by order date: source Shopify (preferred) or Privy (store totals), basis order_date")
            if dl.get("source") == "Privy" and M.get("platform") == "shopify":
                warn("review.daily", "Shopify store: pull daily revenue from Shopify when the connector is available")
            hl = dl.get("highlight")
            if hl:
                need(hl, ["start", "end"], "review.daily.highlight")
                hs, he = in_last_year(hl.get("start"), "review.daily.highlight.start"), in_last_year(hl.get("end"), "review.daily.highlight.end")
                if hs and he and hs > he: err("review.daily.highlight", "start is after end")
            for k, day in enumerate(dl.get("days") or []):
                in_last_year(day.get("date"), f"review.daily.days[{k}].date")
                if not isinstance(day.get("revenue"), (int, float)): err(f"review.daily.days[{k}].revenue", "must be a number")
                if "orders" in day and not isinstance(day.get("orders"), int): err(f"review.daily.days[{k}].orders", "must be a whole number")
        ch = R.get("channels")
        if ch:
            src = ch.get("source"); need(ch, ["source", "basis", "total"], "review.channels")
            ok = {"Privy": ("send_date", "attribution_date"), "Merchant": ("as_reported",)}
            if src not in ok: err("review.channels.source", "Privy or Merchant")
            elif ch.get("basis") not in ok[src]: err("review.channels.basis", f"{src} uses {' or '.join(ok[src])}")
            if src == "Privy" and M.get("profile") != "returning": err("review.channels", "merchant wasn't on Privy last BFCM; use source Merchant with their reported numbers, or omit")
            if ch.get("basis") == "attribution_date" and (ch.get("by_channel") or ch.get("by_type")):
                err("review.channels", "before Privy's reporting boundary the splits are unavailable; show the total only")
            for key, legs in (("by_channel", ("email", "sms")), ("by_type", ("campaign", "flow"))):
                if ch.get(key) is not None:
                    for leg in legs:
                        if not isinstance((ch.get(key) or {}).get(leg), (int, float)): err(f"review.channels.{key}.{leg}", "must be a number")
        st = R.get("stats") or []
        if len(st) > 4: warn("review.stats", "review.stats no longer renders; keep only what you need for the findings")
        for k, s in enumerate(st):
            p = f"review.stats[{k}]"; need(s, ["label", "value", "source", "basis"], p)
            src, basis = s.get("source"), s.get("basis")
            if src not in SOURCE_BASIS: err(f"{p}.source", "one source only: Shopify, Privy, or Merchant. Don't combine Privy and Shopify numbers")
            elif basis not in SOURCE_BASIS[src]: err(f"{p}.basis", f"{src} numbers use one of {sorted(SOURCE_BASIS[src])}")
            if MIXED_SHARE.search(f"{s.get('label','')} {s.get('caption','')}") and src == "Shopify":
                err(p, "looks like an email/text share of Shopify revenue; Privy's send-date revenue can't be divided by Shopify's order-date totals")
        for k, f in enumerate(R.get("findings") or []):
            p = f"review.findings[{k}]"; need(f, ["observation", "source", "change", "task"], p)
            if len(str(f.get("change", ""))) > 80: err(f"{p}.change", "the change is the headline: 80 characters at most")
            if len(str(f.get("observation", ""))) > 160: err(f"{p}.observation", "one line of evidence: 160 characters at most")
            for fld in ("change", "observation"):
                if re.search(r"\byet\b|\bvs\.?\b|;", str(f.get(fld, "")), re.I): warn(f"{p}.{fld}", "say how the facts connect instead of 'yet', 'vs.', or a semicolon (Writing for merchants)")
            if re.match(r"\s*(keep|rename|tidy|clean up the name|document)\b", str(f.get("change", "")), re.I):
                warn(f"{p}.change", "top recommendations are changes that move the sale; housekeeping and 'keep doing X' belong in the task list")
            if re.search(r"\b(stale|out of date|outdated|last (updated|refreshed)|hasn.t refreshed|sync (delay|lag))\b", str(f.get("change", "")) + " " + str(f.get("observation", "")), re.I):
                warn(f"{p}", "Privy-side data issues (stale counts, sync delays) aren't merchant recommendations; work around them, and if one affects a number the merchant relies on, tell them in chat and note it in basis")
            figs = re.findall(r"(?:CA\$|\$|£|€)\d[\d,.]*[KM]?|\d[\d,.]*%|\b\d{1,3}(?:,\d{3})+\b", str(f.get("observation", "")))
            if len(figs) > 2: warn(f"{p}.observation", f"{len(figs)} figures in one line of evidence; keep it to two")
            if f.get("task_label") and len(f["task_label"]) > 40: err(f"{p}.task_label", "40 characters at most")
            if f.get("task") and f["task"] not in step_ids: err(f"{p}.task", f"no task with id {f['task']!r}; every finding must point to a task")
        if len(R.get("findings") or []) > 3: warn("review.findings", "more than 3; keep the ones that change the plan")
        pass
    elif M.get("profile") != "new_store":
        warn("review", "no 2025 review; include one when Shopify history exists")

    # exclusions named in the sale terms (e.g. "Refills and gift cards excluded", "Excludes bundles")
    terms = str((data.get("sale") or {}).get("terms", "")).lower()
    EXCLUDED = []
    for mm in re.finditer(r"([a-z ,'-]+?)\s+(?:are |is )?excluded|excludes?\s+([a-z ,'-]+)", terms):
        chunk = mm.group(1) or mm.group(2) or ""
        chunk = re.split(r"[.;]", chunk)[0]
        for part in re.split(r",|\band\b|\bor\b", chunk):
            w = part.strip().removeprefix("the ").strip()
            if w and len(w) > 2 and w not in ("all", "some"): EXCLUDED.append(w)
    LIVE = re.compile(r"\b(is live|now live|starts now|sale is on|is here|shop now)\b")
    # ---- sends
    S = data.get("sends", {});
    _rows = S.get("rows") or []; _words = {"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"ten":10,"eleven":11,"twelve":12,"thirteen":13,"fourteen":14,"fifteen":15,"sixteen":16,"seventeen":17,"eighteen":18,"nineteen":19,"twenty":20}
    _counts = {"email": sum(r.get("channel") == "email" for r in _rows), "sms": sum(r.get("channel") == "sms" for r in _rows)}
    _counts["send"] = _counts["email"] + _counts["sms"]
    for _n, _k in re.findall(r"\b(\d+|[A-Za-z]+)\s+(emails?|SMS|sends?)\b(?!\s+a\s+(?:day|week))", str(S.get("title", ""))):
        _v = int(_n) if _n.isdigit() else _words.get(_n.lower())
        _key = "email" if _k.lower().startswith("email") else "sms" if _k == "SMS" else "send"
        if _v is not None and _v != _counts[_key]: err("sends.title", f"says {_n} {_k}, but the calendar has {_counts[_key]}")
    if data.get("sends") or not DISPLAYS_ONLY:
        need(S, ["title", "rows"], "sends"); claim(S.get("title"), "sends.title")
    for i, r in enumerate(S.get("rows") or []):
        p = f"sends.rows[{i}]"; ch = r.get("channel")
        need(r, ["date", "channel", "message"] + (["time", "campaign", "audience"] if ch != "none" else []), p)
        if ch not in ("email", "sms", "none"): err(f"{p}.channel", "email, sms, or none (a deliberately quiet day)")
        day = inwin(r.get("date"), f"{p}.date")
        if ch == "none": continue
        try: hh, mm = map(int, str(r.get("time")).split(":")); when = dt.datetime.combine(day, dt.time(hh, mm)) if day else None
        except Exception: err(f"{p}.time", "use 24h HH:MM"); when = None
        if ch == "sms" and when and not M.get("timezone_sending"):
            try:
                z = ZoneInfo(M.get("timezone") or "America/New_York"); aw = when.replace(tzinfo=z)
                et, pt = aw.astimezone(ZoneInfo("America/New_York")), aw.astimezone(ZoneInfo("America/Los_Angeles"))
                if pt.time() < dt.time(9, 0) or et.time() >= dt.time(20, 0):
                    warn(f"{p}.time", f"lands at {pt:%-I:%M%p} Pacific and {et:%-I:%M%p} Eastern; Privy holds texts until quiet hours end, so some subscribers get it later than planned. Recommend timezone-based sending (meta.timezone_sending) or noon-7:59pm Eastern")
            except Exception: err("meta.timezone", "unknown time zone")
        if ch == "sms" and not re.search(r"https?://|\[link\]", str(r.get("message", ""))): warn(f"{p}.message", "add a shop link ([link] placeholder) so the SMS has somewhere to go")
        if when and end and when > end:
            if not r.get("post_sale"): err(p, "scheduled after the sale ends (mark a plain follow-up with post_sale: true)")
            else:
                cmd_ = dt.date.fromisoformat(W["black_friday"]) + dt.timedelta(days=3)
                if when.date() > cmd_: err(p, "post-sale sends go out by Cyber Monday")
                if re.search(r"\b(sale|% off|discount|deal|deals|free|code|save)\b", str(r.get("subject", "")) + " " + str(r.get("message", "")), re.I):
                    err(p, "a post-sale send can't mention a sale, discount, deal, or free gift; the offer has ended")
        if r.get("channel") == "sms" and re.search(r"\b(reply|text) stop\b", str(r.get("message", "")), re.I):
            warn(p, "Privy adds opt-out language to SMS automatically; remove \"Reply STOP\" from the copy so it doesn't appear twice")
        text = " ".join(str(r.get(k) or "") for k in ("subject", "message", "campaign"))
        m = DEADLINE.search(text)
        if m and when:
            ref = dtm(r["deadline_ref"], f"{p}.deadline_ref") if r.get("deadline_ref") else end
            if r.get("deadline_ref") and ref and end and ref != end and not r.get("distinct_offer"):
                err(f"{p}.deadline_ref", "points to an end that isn't the sale end; set distinct_offer or remove the deadline language")
            if ref and (when > ref or ref - when > dt.timedelta(hours=24)):
                err(p, f"deadline language (\"{m.group(0)}\") must go out in the 24 hours before the sale ends, which is {ref.strftime('%a, %b')} {ref.day} at {ref.strftime('%I:%M%p').lstrip('0').lower()} (window.offer_end, or the extension's end). This send is {when.strftime('%a, %b')} {when.day}. Move it, drop the deadline wording, or fix offer_end if the sale really ends sooner")
            if ref and cm and W.get("extension") and ref.date() == cm and not r.get("distinct_offer"):
                err(p, "the sale continues after Cyber Monday, so Monday sends can't say it's ending")
        if ch == "sms":
            gsm = set("@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞÆæßÉ !\"#¤%&'()*+,-./0123456789:;<=>?¡ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ§¿abcdefghijklmnopqrstuvwxyzäöñüà^{}\\[~]|€")
            bad = sorted({c for c in str(r.get("message", "")) if c not in gsm})
            if bad: warn(f"{p}.message", f"characters {''.join(bad)!r} switch the text to UCS-2, which cuts one message from 160 to 70 characters; use straight quotes and plain punctuation")
        if M.get("timezone_sending") and when and end and exposure and exposure <= when.date() <= end.date() and not r.get("store_time"):
            err(p, "sale-day sends go out on the store's clock (store_time: true), so everyone hears the sale is live at the same moment; time-zone sending is for pre-sale sends only")
        copy = (str(r.get("subject") or "") + " " + str(r.get("message") or "")).lower()
        for item in EXCLUDED:
            stem = item[:-1] if item.endswith("s") else item
            if stem and re.search(r"\b" + re.escape(stem), copy): err(p, f"the copy mentions {item}, which the sale terms exclude")
        if [x for x in EXCLUDED if "gift card" not in x] and re.search(r"\beverything\b", copy):
            warn(p, "says 'everything' while the terms exclude items; say what's included or 'sitewide' with the exclusions shown")
        _ea = dt.date.fromisoformat(str(W["early_access_start"])[:10]) if W.get("early_access_start") else None
        if when and start and when < start and LIVE.search(copy) and not (_ea and when.date() >= _ea):
            err(p, f"says the sale is live, but it's scheduled before the sale starts ({start}); move it or send it to early access only")
        m = SCARCITY.search(text)
        if m and not r.get("inventory_backed"): err(p, f"scarcity claim (\"{m.group(0)}\") needs inventory_backed: true, checked against live stock at send time")

    # ---- scope: which segments and flows are in the plan (not rendered as tables; used for names and checks)
    X = data.get("scope", {}); need(X, ["segments", "flows"], "scope")
    def rows(sec, letter):
        Y = X.get(sec, {}); inc, sk = set(), set()
        for i, r in enumerate(Y.get("included") or []):
            need(r, ["id", "name"], f"scope.{sec}.included[{i}]")
            if cid(r.get("id"), f"scope.{sec}.included[{i}].id", (letter,)): inc.add(r["id"])
        for i, r in enumerate(Y.get("skipped") or []):
            need(r, ["id", "name", "reason"], f"scope.{sec}.skipped[{i}]")
            if cid(r.get("id"), f"scope.{sec}.skipped[{i}].id", (letter,)): sk.add(r["id"])
        for x in inc & sk: err(f"scope.{sec}", f"{x} is both included and skipped")
        return inc, sk
    si, ss = rows("segments", "S"); fi, fs = rows("flows", "F")
    send_text = " ".join(str(r.get("audience", "")) + " " + str(r.get("suppress", "")) for r in S.get("rows") or [])
    used = refs | set(re.findall(r"\bS\d\d\b", send_text))
    for x in (ss | fs) & used: err("tasks", f"{x} is skipped, so no task or send can use it")
    for x in (si | fi) - used: warn("scope", f"{x} is in scope but no task or send uses it")
    if "S20" not in si and not DISPLAYS_ONLY: warn("scope.segments", "S20 (unengaged suppression) is Core; include it or its new-to-Privy substitute")
    first_sale = None
    for k, r in enumerate(S.get("rows") or []):
        w = dtm(f"{r.get('date')}T{r.get('time')}", "_") if r.get("date") and r.get("time") else None
        if w and start and w >= start and r.get("channel") == "email" and (first_sale is None or w < first_sale[1]): first_sale = (k, w)
    for k, r in enumerate(S.get("rows") or []):
        if re.search(r"\bS19\b", str(r.get("suppress", ""))) and (not first_sale or k != first_sale[0]):
            err(f"sends.rows[{k}].suppress", "recent buyers are good people to include; leave out 7-day buyers (S19) only on the launch email")
    for core in (() if DISPLAYS_ONLY else ("F01", "F05", "F12")):
        if core not in fi: warn("scope.flows", f"{core} is a Core flow and isn't included")
    unknown = set(re.findall(r"\bS\d\d\b", send_text)) - si - ss
    for x in unknown: err("sends", f"{x} is used in sends but isn't in scope.segments, so the page can't show its name")

    # ---- custom sections
    if data.get("custom_sections"): err("custom_sections", "replaced: use sale.margin, review.store_totals, review.top_sellers, or popups")
    MG = (data.get("sale") or {}).get("margin")
    if MG:
        for k_, m in enumerate(MG.get("rows") or []):
            if not str(m.get("tier", "")).strip() or not str(m.get("keep", "")).strip(): err(f"sale.margin.rows[{k_}]", "tier and keep are both required")
        if not MG.get("rows"): err("sale.margin.rows", "at least one tier")
        if MG.get("note") and len(str(MG["note"])) > 140: err("sale.margin.note", "140 characters at most: one line, no caveats")
    STT = (R or {}).get("store_totals")
    if STT:
        need(STT, ["total", "orders", "from", "to", "source"], "review.store_totals")
        if (R or {}).get("daily"): warn("review.store_totals", "the daily chart already shows last year; the store card only appears without one")
    TSL = (R or {}).get("top_sellers") or []
    if len(TSL) > 5: err("review.top_sellers", "5 at most")
    for k_, t_ in enumerate(TSL): need(t_, ["product", "in_stock", "sold_last_bfcm"], f"review.top_sellers[{k_}]")
    PU = data.get("popups")
    if PU:
        if not DISPLAYS_ONLY: warn("popups", "the popup calendar is for popups-only merchants; other plans put popups in tasks")
        rows_ = PU.get("rows") or []
        for k_, r_ in enumerate(rows_): need(r_, ["start", "name", "offer", "audience"], f"popups.rows[{k_}]")
        m_ = re.search(r"\b(\d+)\s+popups?\b", str(PU.get("title", "")))
        n_popups = sum(1 for r_ in rows_ if r_.get("kind", "popup") == "popup")
        if m_ and int(m_.group(1)) != n_popups: err("popups.title", f"says {m_.group(1)} popups, but the calendar has {n_popups}")

    # ---- sources, closing
    C = data.get("closing", {}); need(C, ["title", "lede"], "closing")
    if C.get("cta"):
        need(C["cta"], ["label", "url"], "closing.cta")
        if not re.match(r"^https://(www\.)?privy\.com(/|$)", str(C["cta"].get("url", ""))): err("closing.cta.url", "call-to-action links must go to privy.com")

    if not HAS_CSM:
        if C.get("cta") and re.search(r"csm|coach|session", str(C["cta"].get("label", "")) + " " + str(C.get("lede", "")), re.I): warn("closing.cta", "a call to action to book a Privy CSM, but meta.has_csm isn't true")
        for t in TK:
            if str(t.get("owner", "")).lower() == "your privy csm": warn(f"tasks.{t.get('id')}", "a task is owned by \"Your Privy CSM\", but meta.has_csm isn't true")

    BS = data.get("basis")
    if BS is not None: need(BS, ["data"], "basis")  # kept for internal review; not shown on the page

    for i, r in enumerate(data.get("resources") or []):
        need(r, ["name", "url", "text"], f"resources[{i}]")
        if not re.match(r"^https://(www\.|help\.)?privy\.com(/|$)", str(r.get("url", ""))): err(f"resources[{i}].url", "resources link to privy.com or help.privy.com only")
    if len(data.get("resources") or []) > 3: warn("resources", "more than 3 extra resources; the Hub, Playbook, and Resource Center are already listed")

    # ---- text-wide guards
    for path, s in walk(data):
        low = s.lower()
        shopper = path.startswith("sends.rows") and path.rsplit(".", 1)[-1] in ("subject", "message")
        for c in COMPETITORS:
            if c in low: err(path, f"mentions a competing platform ({c}); remove it")
        if not path.startswith("sources.industry") and FORECAST_TEXT.search(s): err(path, f"forecast language (\"{FORECAST_TEXT.search(s).group(0)}\")")
        if EMAIL_RE.search(s): err(path, "contains an email address; keep customer data out of the plan")
        if PHONE_RE.search(s): err(path, "contains a phone number; keep customer data out of the plan")
        if not shopper:
            for h in HYPE:
                if re.search(rf"\b{re.escape(h)}\b", low): err(path, f"hype word \"{h}\" (DESIGN.md voice rules)")
            if "!" in s and not path.endswith("url"): err(path, "no exclamation points in Privy copy")
        if "\u2014" in s: err(path, "no em dashes; use a period or a comma (Writing for merchants)")
        if re.search(r"(?<!day),\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}\s+(?:to|through)\s+", s) and not path.startswith(("basis", "sources", "sends.rows", "window", "meta")):
            warn(path, "put the date range in parentheses after the figure it qualifies: \"(Jul 3 to Sep 30)\" (comma-attached dates)")
        if re.search(r"\bsms (delivery )?failures\b", s, re.I) and not path.startswith(("basis", "sources", "review")): err(path, "don't ask merchants to watch SMS failures; they're often landlines and can't be seen or removed. Monitor SMS opt-outs")
        if re.search(r"of (new )?visitors (sign|signed) up|(convert|converts|converted) [\d.]+% of (new )?visitors", s, re.I): err(path, "the signup rate is per popup view, not per visitor: say \"of popup views lead to a signup\"")
        if re.search(r"\bcoach(es|ing)?\b", own_words(s), re.I) and not path.startswith(("basis", "sources")): err(path, "say Privy CSM, never coach")
        if re.search(r"\b\d[\d,]*(\s+to\s+\d[\d,]*)?\s+unsubscribes?\b", s, re.I) and not path.startswith(("basis", "sources")): err(path, "give unsubscribes as a rate (for example 0.2%), never a count")
        if ";" in s and not path.startswith(("sends.rows", "basis", "sources")) and not path.endswith((".id", ".ref")): warn(path, "no semicolons in plan wording; use two sentences")
        if re.search(r"\btexts?\b", own_words(s), re.I) and not path.endswith((".id", ".ref", ".category", ".status", ".priority", ".evidence", ".channel")) and not path.startswith(("meta.proper_names", "scope", "already_set")):
            err(path, "say SMS, never text or texts (merchant names listed in meta.proper_names are exempt)")
        if (DEADLINE.search(s) or SCARCITY.search(s)) and not path.startswith(("sends.rows", "sources")):
            warn(path, "deadline or scarcity wording outside the send calendar; make sure it describes rather than claims")

    if "--previous" in sys.argv:
        import difflib
        prev = json.loads(Path(sys.argv[sys.argv.index("--previous") + 1]).read_text())
        old_t = {t.get("id"): t for t in prev.get("tasks") or []}
        new_t = {t.get("id"): t for t in data.get("tasks") or []}
        for tid, t in old_t.items():
            if tid not in new_t:
                warn(f"tasks.{tid}", f"removed since the last version (\"{t.get('text', '')[:60]}\"); its checkmark is orphaned. Keep the ID if the task still applies")
            else:
                n = new_t[tid]
                same_cat = t.get("category") == n.get("category")
                sim = difflib.SequenceMatcher(None, str(t.get("text", "")).lower(), str(n.get("text", "")).lower()).ratio()
                if not same_cat or sim < 0.35:
                    err(f"tasks.{tid}", f"this ID now points to a different task (was \"{t.get('text', '')[:50]}\"); give the new task a new ID so progress isn't misattributed")
    if _bad_owner: err("tasks", f"{len(_bad_owner)} task owner(s) aren't in meta.team {sorted(team)}: {', '.join(_bad_owner[:12])}{' ...' if len(_bad_owner) > 12 else ''}")
    if _you_owner: warn("tasks", f"the merchant named a team, but {len(_you_owner)} task(s) are owned by \"You\": {', '.join(_you_owner[:12])}{' ...' if len(_you_owner) > 12 else ''}. Assign owners from meta.team, or meta.area_owners for standard tasks")
    _e = list(dict.fromkeys(errors)); _w = list(dict.fromkeys(warnings))
    if _e:
        print(f"Fix these first ({len(_e)}):")
        for e in _e: print(e)
    if _w:
        _cap = len(_w) if "--all-warnings" in sys.argv else 8
        print(f"\nWarnings ({len(_w)}), use judgment:")
        for w in _w[:_cap]: print(w)
        if len(_w) > _cap: print(f"... and {len(_w) - _cap} more (run with --all-warnings to see them)")
    print(f"\n{len(_e)} error(s), {len(_w)} warning(s)")
    errors[:] = _e
    if errors: sys.exit(1)
    if sys.argv[2] == "--check": return
    html = RENDERER.read_text()
    if "/*PLAN_DATA*/" not in html: print("renderer placeholder missing"); sys.exit(1)
    out = Path(sys.argv[2])
    out.write_text(html.replace("/*PLAN_DATA*/", json.dumps(data, ensure_ascii=False).replace("</", "<\\/")))
    print(f"Built {out}")
    if "--pdf" in sys.argv:
        pdf = Path(sys.argv[sys.argv.index("--pdf") + 1])
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            print("PDF skipped: Playwright isn't installed. Open the HTML and use Print > Save as PDF instead."); return
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page(color_scheme="light")
            page.goto(out.resolve().as_uri())
            page.wait_for_timeout(800)
            page.evaluate("() => document.documentElement.setAttribute('data-theme','light')")
            page.pdf(path=str(pdf), format="Letter", print_background=True, prefer_css_page_size=True)
            browser.close()
        print(f"PDF {pdf}")

if __name__ == "__main__":
    main()
