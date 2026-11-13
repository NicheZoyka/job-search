"""Command line interface."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

from .config import DEFAULT_MODEL
from .llm import get_assessment, get_requirements
from .readers import read_document
from .render import render_text
from .scoring import process


def main() -> None:
    ap = argparse.ArgumentParser(description="Check how well CVs match a job description.")
    ap.add_argument("--cv", action="append", default=[], help="CV file (.docx/.pdf/.txt); repeatable")
    ap.add_argument("--cv-dir", help="Directory with CVs (batch mode)")
    ap.add_argument("--job", required=True, help="Job description file or '-' for stdin")
    ap.add_argument("--requirements", help="Pre-defined requirements JSON (skips step 1)")
    ap.add_argument("--fixtures", help="Offline mode: read LLM outputs from this dir")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--out", default="reports")
    ap.add_argument("--today", help="YYYY-MM-DD, override 'present' date (for reproducible tests)")
    args = ap.parse_args()

    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    cvs = [Path(c) for c in args.cv]
    if args.cv_dir:
        cvs += sorted(p for p in Path(args.cv_dir).iterdir() if p.suffix.lower() in (".docx", ".pdf", ".txt"))
    if not cvs:
        sys.exit("No CVs given (--cv / --cv-dir).")

    job_text = sys.stdin.read() if args.job == "-" else read_document(Path(args.job))
    reqs_doc = get_requirements(job_text, args)
    reqs = reqs_doc["requirements"]
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "requirements.json").write_text(json.dumps(reqs_doc, ensure_ascii=False, indent=2))

    ranking = []
    for cv in cvs:
        cv_text = read_document(cv)
        assess = get_assessment(cv_text, reqs, cv.name, args)
        p = process(assess, reqs, cv_text, today)
        (out / f"{cv.stem}.json").write_text(json.dumps(p, ensure_ascii=False, indent=2))
        (out / f"{cv.stem}.txt").write_text(render_text(p))
        print(render_text(p), "\n")
        for w in p["warnings"]:
            print("WARNING:", w, file=sys.stderr)
        ranking.append({"cv": cv.name, "candidate": p["candidate_name"], "score_pct": p["score_pct"],
                        "missing_critical": p["missing_critical"]})
    if len(ranking) > 1:
        ranking.sort(key=lambda r: (len(r["missing_critical"]), -r["score_pct"]))
        (out / "ranking.json").write_text(json.dumps(ranking, ensure_ascii=False, indent=2))
        print("RANKING:")
        for i, r in enumerate(ranking, 1):
            print(f"{i}. {r['candidate']} — {r['score_pct']}%  missing critical: {r['missing_critical'] or '-'}")
