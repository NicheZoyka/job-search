# AGENTS.md

Instructions for coding agents (and humans) working in this repository.

## What this project is
`cv-matcher` checks how well a CV matches a job description with an LLM and prints an
"AI CV Summary". See `README.md` and `docs/architecture.md`.

## Commands
```bash
pip install python-docx pytest   # setup (no packaging files: always run with PYTHONPATH=src)
PYTHONPATH=src python -m pytest -q      # tests, fully offline, no API key needed
PYTHONPATH=src python -m cv_matcher --cv examples/sample_cv.txt --job examples/job.txt \
    --fixtures tests/fixtures --today 2026-07-15      # offline demo
```

## Layout
- `src/cv_matcher/prompts.py` - system prompts + tool JSON schemas (the only place prompts live)
- `readers.py` - docx/pdf/txt reading, `norm()` text normalisation
- `llm.py` - Anthropic API call (stdlib `urllib`), offline `--fixtures` mode
- `scoring.py` - deterministic: dates, quote verification, min-years, score
- `render.py` - report text; `cli.py` - arguments and orchestration
- `tests/` - pytest; `tests/fixtures/` - recorded LLM outputs for offline tests; `examples/` - vacancy, synthetic CV, expected report

## Rules that must not be broken
1. **No date/duration arithmetic by the LLM.** Models return roles with `YYYY-MM` dates; durations are computed in `scoring.py`.
2. **Every evidence quote must be verified** as a substring of the CV (via `norm()`). Unverifiable evidence is dropped and
   `Yes/Partial` without evidence becomes `No`. Never relax this.
3. **No real personal data in the repo.** Tests/examples use only synthetic CVs. Never commit real CVs, `reports/`,
   `.env` or API keys (there is no `.gitignore`, so check `git status` before every commit).
4. Keep runtime dependencies at zero beyond optional `python-docx`; use stdlib for HTTP. Evidence outside the work history
   (education, languages) uses `role_index: null` and carries no duration.
5. Changing a prompt or schema in `prompts.py` requires updating fixtures/tests and `examples/sample_output.txt`
   (regenerate with the offline demo command above, writing to `--out /tmp/out`, copy `sample_cv.txt` over it and review the diff).
6. Report layout is a contract (`render.py`, `tests/test_render.py`); change it deliberately.

## Conventions
- Python 3.10+, type hints on public functions, small pure functions in `scoring.py`.
- Add a test for every bug fix in `scoring.py` / `render.py`.
- Commit messages: imperative, one topic per commit.
