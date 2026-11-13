"""Deterministic part: dates, evidence validation, scoring. No LLM, no I/O."""
from __future__ import annotations

import datetime as dt

from .config import WEIGHTS
from .readers import norm


def ym_to_idx(s: str, today: dt.date) -> int:
    s = s.strip().lower()
    if s in ("present", "now", "current", "ongoing"):
        return today.year * 12 + today.month - 1
    y, m = s.split("-")[:2]
    return int(y) * 12 + int(m) - 1


def union_months(intervals: list[tuple[int, int]]) -> int:
    """Total months covered by [start, end) intervals, overlaps counted once."""
    total, cur_s, cur_e = 0, None, None
    for s, e in sorted(i for i in intervals if i[1] > i[0]):
        if cur_e is None or s > cur_e:
            if cur_e is not None:
                total += cur_e - cur_s
            cur_s, cur_e = s, e
        else:
            cur_e = max(cur_e, e)
    if cur_e is not None:
        total += cur_e - cur_s
    return total


def fmt_dur(m: int) -> str:
    if m <= 0:
        return "less than 1 month"
    y, mo = divmod(m, 12)
    parts = []
    if y:
        parts.append(f"{y} year{'s' if y != 1 else ''}")
    if mo:
        parts.append(f"{mo} month{'s' if mo != 1 else ''}")
    return " ".join(parts)


MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def fmt_period(start: str, end: str) -> str:
    def one(s):
        if s.strip().lower() in ("present", "now", "current", "ongoing"):
            return "Present"
        y, m = s.split("-")[:2]
        return f"{MON[int(m) - 1]} {y}"
    return f"{one(start)} – {one(end)}"




def process(assess: dict, reqs: list[dict], cv_text: str, today: dt.date) -> dict:
    cv_norm = norm(cv_text)
    roles = assess["roles"]
    by_req = {norm(a["requirement"]): a for a in assess["assessments"]}
    warnings, results = [], []

    for r in reqs:
        a = by_req.get(norm(r["name"])) or {"match": "No", "evidence": [], "note": None}
        match, note = a["match"], a.get("note")
        ev_ok, intervals = [], []
        for e in a.get("evidence", []):
            i = e.get("role_index")  # None = evidence outside work history (education, languages, certificates)
            if i is not None and (not isinstance(i, int) or not (0 <= i < len(roles))):
                warnings.append(f"[{r['name']}] invalid role_index {i} - evidence dropped")
                continue
            if norm(e["quote"]) not in cv_norm:
                warnings.append(f"[{r['name']}] quote not found in CV, dropped: “{e['quote'][:70]}”")
                continue
            if i is None:
                ev_ok.append({"company": None, "title": None, "what": e["what"], "period": None, "months": 0,
                              "quote": e["quote"]})
                continue
            role = roles[i]
            s, en = ym_to_idx(role["start"], today), ym_to_idx(role["end"], today) + 1  # end month inclusive
            months = max(en - s, 0)
            intervals.append((s, en))
            ev_ok.append({"company": role["company"], "title": role.get("title"), "what": e["what"],
                          "period": fmt_period(role["start"], role["end"]), "months": months, "quote": e["quote"]})
        # de-duplicate the same role cited twice
        seen, uniq = set(), []
        for e in ev_ok:
            k = (e["company"], e["period"]) if e["company"] else ("", e["what"])
            if k not in seen:
                seen.add(k)
                uniq.append(e)
        ev_ok = uniq
        total = union_months(intervals)

        if match in ("Yes", "Partial") and not ev_ok:
            warnings.append(f"[{r['name']}] {match} without verifiable evidence -> No")
            match = "No"
        min_y = r.get("min_years")
        if match == "Yes" and min_y and total < min_y * 12:
            match = "Partial"
            note = (note + "; " if note else "") + f"evidenced {fmt_dur(total)} < required {min_y:g} years"
        results.append({"requirement": r["name"], "short": r.get("short"), "priority": r["priority"], "match": match,
                        "evidence": ev_ok, "total_months": total if ev_ok else 0, "note": note})

    got = sum(WEIGHTS[x["priority"]] * {"Yes": 1, "Partial": .5, "No": 0}[x["match"]] for x in results)
    max_ = sum(WEIGHTS[x["priority"]] for x in results) or 1
    missing_critical = [x["requirement"] for x in results if x["priority"] == "Critical" and x["match"] == "No"]
    return {
        "candidate_name": assess["candidate_name"],
        "stated_experience": assess.get("stated_experience"),
        "score_pct": round(100 * got / max_),
        "missing_critical": missing_critical,
        "results": results,
        "warnings": warnings,
    }
