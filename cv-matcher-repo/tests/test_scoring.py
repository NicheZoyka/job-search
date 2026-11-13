import datetime as dt
import json
from pathlib import Path

from cv_matcher.scoring import fmt_dur, process, union_months, ym_to_idx

ROOT = Path(__file__).parent.parent
TODAY = dt.date(2026, 7, 15)


def test_union_counts_overlap_once():
    assert union_months([(0, 10), (5, 12), (20, 24)]) == 16


def test_union_adjacent_and_empty():
    assert union_months([(0, 5), (5, 8)]) == 8
    assert union_months([]) == 0


def test_fmt_dur():
    assert fmt_dur(0) == "less than 1 month"
    assert fmt_dur(1) == "1 month"
    assert fmt_dur(12) == "1 year"
    assert fmt_dur(29) == "2 years 5 months"


def test_present_resolves_to_today():
    assert ym_to_idx("present", TODAY) == 2026 * 12 + 6


def _data():
    reqs = json.loads((ROOT / "tests/fixtures/requirements.json").read_text())["requirements"]
    assess = json.loads((ROOT / "tests/fixtures/sample_cv.analysis.json").read_text())
    cv = (ROOT / "examples/sample_cv.txt").read_text()
    return reqs, assess, cv


def _res(p, name):
    return next(x for x in p["results"] if x["requirement"].startswith(name))


def _ass(assess, name):
    return next(a for a in assess["assessments"] if a["requirement"].startswith(name))


def test_valid_evidence_passes_and_durations_merge():
    reqs, assess, cv = _data()
    p = process(assess, reqs, cv, TODAY)
    assert not p["warnings"]
    # Jul 2019 - Dec 2022 (42 months) + Jan 2023 - Jul 2026 (43 months), adjacent roles
    assert _res(p, "SQL")["total_months"] == 85
    assert p["missing_critical"] == []


def test_evidence_outside_work_history_has_no_duration():
    reqs, assess, cv = _data()
    p = process(assess, reqs, cv, TODAY)
    degree = _res(p, "University degree")
    assert degree["match"] == "Yes" and degree["total_months"] == 0
    assert degree["evidence"][0]["company"] is None


def test_fabricated_quote_is_dropped_and_downgraded():
    reqs, assess, cv = _data()
    _ass(assess, "Product Control")["match"] = "Yes"
    _ass(assess, "Product Control")["evidence"] = [{"role_index": 0, "what": "x", "quote": "Ran Product Control for desk"}]
    p = process(assess, reqs, cv, TODAY)
    pc = _res(p, "Product Control")
    assert pc["match"] == "No" and pc["evidence"] == []
    assert any("not found in CV" in w for w in p["warnings"])


def test_invalid_role_index_dropped():
    reqs, assess, cv = _data()
    _ass(assess, "Python")["evidence"] = [{"role_index": 99, "what": "x", "quote": "Python"}]
    p = process(assess, reqs, cv, TODAY)
    assert _res(p, "Python")["match"] == "No"


def test_min_years_downgrades_yes_to_partial():
    reqs, assess, cv = _data()
    next(r for r in reqs if r["name"] == "SQL")["min_years"] = 20
    p = process(assess, reqs, cv, TODAY)
    assert _res(p, "SQL")["match"] == "Partial"
    assert "required 20 years" in _res(p, "SQL")["note"]


def test_missing_assessment_defaults_to_no():
    reqs, assess, cv = _data()
    assess["assessments"] = []
    p = process(assess, reqs, cv, TODAY)
    assert all(x["match"] == "No" for x in p["results"])
    assert p["score_pct"] == 0 and "Python" in p["missing_critical"]
