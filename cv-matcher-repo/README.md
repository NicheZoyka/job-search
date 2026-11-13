# cv-matcher

An LLM agent that checks how well a CV matches a job description and prints an
**AI CV Summary**: per-requirement match (✔ / ~ / ✘), priority, evidence with employer,
period and duration, and an overall score.

Example vacancy: *Data and Financial Engineering* ([`examples/job.txt`](examples/job.txt)).
Example result for a synthetic candidate: [`examples/sample_output.txt`](examples/sample_output.txt).

## How it works
1. **LLM** turns the job description into requirements with priorities (Critical / High / Medium / Low).
2. **LLM** judges each requirement against the CV (Yes / Partial / No) and returns role references and **verbatim quotes**.
3. **Code** verifies every quote exists in the CV, computes durations (overlaps counted once), scores and renders the report.

Models are weak at date arithmetic and invent evidence, so they only *point* at evidence; code checks and computes.
Details: [`docs/architecture.md`](docs/architecture.md). Rules for coding agents: [`AGENTS.md`](AGENTS.md).

## Quick start

You need Python 3.10+ and an [Anthropic API key](https://console.anthropic.com/) (the two LLM steps call the API).

**1. Get the code**
```bash
git clone https://github.com/<your-user>/cv-matcher.git
cd cv-matcher
```

**2. (Optional) create a virtual environment and install the one dependency**
```bash
python -m venv .venv
source .venv/bin/activate            # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install python-docx              # only needed for .docx CVs; .txt works without it
```
(`.pdf` CVs need the `pdftotext` tool from poppler.)

**3. Set your API key** (once per terminal session; never commit it)
```bash
export ANTHROPIC_API_KEY=sk-ant-...          # Windows PowerShell: $env:ANTHROPIC_API_KEY="sk-ant-..."
```

**4. Run it on a CV and a vacancy**
```bash
# macOS / Linux
PYTHONPATH=src python -m cv_matcher --cv path/to/candidate.docx --job examples/job.txt
```
```powershell
# Windows PowerShell
$env:PYTHONPATH="src"; python -m cv_matcher --cv path\to\candidate.docx --job examples\job.txt
```
- `--cv` – the CV file (`.docx`, `.pdf` or `.txt`); `--job` – a text file with the vacancy description.
- `PYTHONPATH=src` tells Python that the `cv_matcher` package lives in the `src` folder (it is not pip-installed).
- `python -m cv_matcher` runs the package as a program.

The report is printed to the console and saved as `reports/<cv-name>.txt` and `reports/<cv-name>.json`.

### Other ways to run
```bash
# many CVs at once: one report each + reports/ranking.json
PYTHONPATH=src python -m cv_matcher --cv-dir ./cvs --job my_job.txt --out reports

# keep the requirements/priorities fixed between runs (reuse reports/requirements.json or edit it)
PYTHONPATH=src python -m cv_matcher --cv cv.docx --job my_job.txt --requirements reports/requirements.json

# choose another model (default claude-sonnet-5-5; or set env CVM_MODEL)
PYTHONPATH=src python -m cv_matcher --cv cv.docx --job my_job.txt --model claude-opus-5-5
```

## Try it without an API key (offline demo)
Uses recorded model outputs from `tests/fixtures/`, makes no API calls and reproduces `examples/sample_output.txt`:
```bash
PYTHONPATH=src python -m cv_matcher --cv examples/sample_cv.txt --job examples/job.txt \
    --fixtures tests/fixtures --today 2026-07-15
```

## Run the tests
Tests are automatic checks of the code itself (duration maths, rejection of invented quotes, report layout, a full
offline run). They need no API key and no real CVs. Use them after changing the code.
```bash
pip install pytest
PYTHONPATH=src python -m pytest -q          # Windows PowerShell: $env:PYTHONPATH="src"; python -m pytest -q
```
Expected: all tests pass (`14 passed`).

## Notes
- Durations: end month inclusive, overlapping roles merged, `Present` = today.
- `Partial` is a judgement call – review manually. This is a screening aid, not a hiring decision.
- **Privacy:** CVs are personal data. `.gitignore` excludes `.env`, `reports/` and `*.docx`, but check `git status`
  before every commit and check GDPR obligations before sending CVs to any API.

## License
MIT – see [LICENSE](LICENSE).
