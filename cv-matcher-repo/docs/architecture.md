# Architecture

## Flow
```
job.txt ──► [LLM step 1] ──► requirements.json ─┐
                                                ├─► [LLM step 2] ─► assessment (roles + matches + quotes)
cv.docx ──► readers.read_document ──────────────┘                          │
                                                                           ▼
                                   scoring.process: verify quotes, compute durations, score
                                                                           ▼
                                          render.render_text  ──►  <cv>.txt / <cv>.json / ranking.json
```

## Why the LLM does not do everything
| Weakness of LLMs | Mitigation |
|---|---|
| Date arithmetic / overlapping jobs | Model returns `YYYY-MM` dates only; `scoring.union_months` computes totals |
| Invented evidence | Each evidence item needs a verbatim quote; `process()` checks it against the CV text |
| Inferring skills from seniority or industry | Prompt forbids it; `No` is the default when nothing is quoted |
| Non-determinism | `temperature=0`, forced tool call (structured JSON), requirements can be pinned with `--requirements` |

## Data contracts
**Requirements** (step 1 output / `--requirements` input)
```json
{"job_title": "...", "requirements": [
  {"name": "SQL", "short": "SQL", "priority": "Critical|High|Medium|Low", "min_years": 3}]}
```
**Assessment** (step 2 output)
```json
{"candidate_name": "...", "stated_experience": "5 years",
 "roles": [{"company": "...", "title": "...", "start": "2022-06", "end": "2023-11|present"}],
 "assessments": [{"requirement": "SQL", "match": "Yes|Partial|No", "note": null,
   "evidence": [{"role_index": 0, "what": "Used SQL", "quote": "verbatim fragment"}]}]}
```
`role_index` is `null` for evidence outside the work history (education, languages, certificates); such evidence has no duration.

**Result** (`<cv>.json`): candidate, `score_pct`, `missing_critical`, per-requirement `match`,
`evidence[{company, period, months, quote}]`, `total_months`, `warnings`.

## Scoring
Weights Critical 5 / High 3 / Medium 2 / Low 1; Yes = 1, Partial = 0.5, No = 0;
`score_pct` = weighted sum / max. Batch ranking sorts by fewest missing Critical skills, then score.

## Durations
Month granularity, end month inclusive, overlapping roles merged, `present` = today (`--today` overrides for tests).

## Extending
- **New input format:** add a branch in `readers.read_document`.
- **Another LLM provider:** implement `call_tool(system, user, tool, model)` in `llm.py` returning the tool-call dict.
- **New output:** add a renderer next to `render_text` and call it from `cli.main`.
- **Prompt changes:** edit `prompts.py`, regenerate fixtures, update `examples/sample_output.txt`.

## Privacy
CVs are personal data. The tool keeps no state: texts go only to the configured LLM API and results are written
to the local `--out` directory. Do not commit real CVs or reports; review retention terms of your API provider.
