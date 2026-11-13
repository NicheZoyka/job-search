"""Text rendering of the "AI CV Summary"."""
from __future__ import annotations

from .config import PRIORITIES, SYMBOL
from .scoring import fmt_dur


def short(x) -> str:
    return x.get("short") or x["requirement"].split("(")[0].strip()


def build_summary(p: dict) -> str:
    res = p["results"]
    first = p["candidate_name"]
    head = f"{first} has {p['stated_experience']} of IT experience" if p.get("stated_experience") else f"{first} — CV summary"
    yes = [f"{short(x)} ({fmt_dur(x['total_months'])})" for x in res if x["match"] == "Yes" and x["total_months"]]
    s = head + (", with strong skills in " + ", ".join(yes) if yes else "") + "."
    part = [short(x) for x in res if x["match"] == "Partial"]
    if part:
        s += " Partial evidence: " + ", ".join(part) + "."
    gaps = [short(x) + f" ({'required' if x['priority'] in ('Critical', 'High') else 'optional'})"
            for x in res if x["match"] == "No" and x["priority"] in ("Critical", "High")]
    if gaps:
        s += " However, there is no evidence of " + ", ".join(gaps) + "."
    return s


def render_text(p: dict) -> str:
    out = ["AI CV Summary", build_summary(p), "Skills:"]
    order = {k: i for i, k in enumerate(PRIORITIES)}
    for x in sorted(p["results"], key=lambda x: order[x["priority"]]):
        out += [SYMBOL[x["match"]], x["requirement"], x["priority"], f"Matching: {x['match']}"]
        if x["evidence"]:
            parts = [f"{e['what']} at {e['company']} ({e['period']}), {fmt_dur(e['months'])}" if e["company"] else e["what"]
                     for e in x["evidence"]]
            ev = "; ".join(parts)
            if len(x["evidence"]) > 1:
                ev += f"; total {fmt_dur(x['total_months'])}"
            out.append(f"Evidence: {ev}.")
        if x.get("note"):
            out.append(f"Note: {x['note']}")
    out.append(f"\nMatch score: {p['score_pct']}%"
               + (f" | Missing critical: {', '.join(p['missing_critical'])}" if p["missing_critical"] else ""))
    return "\n".join(out)
