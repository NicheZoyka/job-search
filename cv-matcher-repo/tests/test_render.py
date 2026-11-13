from cv_matcher.render import build_summary, render_text

P = {
    "candidate_name": "A B", "stated_experience": "5 years", "score_pct": 50, "missing_critical": ["X"],
    "results": [
        {"requirement": "SQL", "short": "SQL", "priority": "Critical", "match": "Yes", "total_months": 38,
         "evidence": [{"what": "Used SQL", "company": "Co", "period": "Jan 2020 – Mar 2023", "months": 38}], "note": None},
        {"requirement": "X", "short": None, "priority": "Critical", "match": "No", "total_months": 0, "evidence": [], "note": None},
    ],
}


def test_summary_mentions_strengths_and_gaps():
    s = build_summary(P)
    assert "5 years of IT experience" in s and "SQL (3 years 2 months)" in s
    assert "no evidence of X (required)" in s


def test_render_layout():
    t = render_text(P)
    assert t.splitlines()[0] == "AI CV Summary"
    assert "✘\nX\nCritical\nMatching: No" in t
    assert "Match score: 50% | Missing critical: X" in t


def test_evidence_without_company_renders_plain():
    p = {**P, "results": [{"requirement": "Degree", "short": "Degree", "priority": "Medium", "match": "Yes", "total_months": 0,
                           "evidence": [{"what": "MSc Finance", "company": None, "period": None, "months": 0}], "note": None}]}
    assert "Evidence: MSc Finance." in render_text(p)
