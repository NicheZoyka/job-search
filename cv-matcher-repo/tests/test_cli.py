import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent


def test_offline_run_matches_sample_output(tmp_path):
    r = subprocess.run(
        [sys.executable, "-m", "cv_matcher", "--cv", str(ROOT / "examples/sample_cv.txt"),
         "--job", str(ROOT / "examples/job.txt"), "--fixtures", str(ROOT / "tests/fixtures"),
         "--out", str(tmp_path), "--today", "2026-07-15"],
        capture_output=True, text=True, cwd=ROOT, env={"PYTHONPATH": str(ROOT / "src"), "PATH": ""},
    )
    assert r.returncode == 0, r.stderr
    got = (tmp_path / "sample_cv.txt").read_text()
    assert got == (ROOT / "examples/sample_output.txt").read_text()
    assert got.startswith("AI CV Summary")
