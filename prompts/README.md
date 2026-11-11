# Job Search Prompts

A small, tested collection of LLM prompts for job hunting: resume review, gap analysis, achievement bullets, ATS keywords and a LinkedIn About section.

Each prompt is a standalone Markdown file with YAML frontmatter, so it is easy to read on GitHub, copy into any chat model, or parse with a script.

## Prompts

| Step | Prompt | What it does | Variables |
|------|--------|--------------|-----------|
| 1 | [skill-gap-analysis](prompts/analysis/skill-gap-analysis.md) | Compares resume vs. job description, separates skills to reframe from skills to develop | `job_title`, `job_description`, `my_resume` |
| 2 | [achievements-rewrite](prompts/resume/achievements-rewrite.md) | Turns responsibilities into achievements, asks for missing metrics instead of inventing them | `responsibilities` |
| 3 | [resume-review](prompts/resume/resume-review.md) | Reviews the resume for a target role, fixes weak bullets, flags ATS risks | `job_title`, `job_description`, `my_resume` |
| 4 | [keyword-integration](prompts/resume/keyword-integration.md) | Extracts the top 15 keywords and weaves them in naturally, no keyword dump | `job_description`, `my_resume` |
| - | [about-section](prompts/linkedin/about-section.md) | Writes 3 versions of a LinkedIn About section (formal, conversational, bold) | `background`, `problems_i_solve`, `target_audience` |

## Recommended workflow

The first four prompts work as a chain:

```
skill-gap-analysis  ->  achievements-rewrite  ->  resume-review  ->  keyword-integration
   (what is missing)     (strong content)         (polish + ATS)      (final keyword pass)
```

`about-section` is independent and can be used at any time.

## How to use a prompt

1. Open a prompt file and copy the text from `# Role` to `# Output format`.
2. Replace every `{{variable}}` with your own text. Paste the resume and the job description in the same message, because context is everything.
3. Send it to a chat model.
4. Check the result against [tests/checklist.md](tests/checklist.md), especially the "no invented facts" items.

## Design principles

- **Never invent facts.** Every prompt forbids made-up experience and numbers, and where data is missing the model must ask.
- **One task per file.** Each prompt has its own version, variables and notes.
- **Explicit output format.** The result is predictable and easy to compare between runs and models.
- **Human in the loop.** The output is a draft for you to edit, not a final document.

## Testing

Before each release the prompts are run on several fictional inputs and on more than one model, then checked against [tests/checklist.md](tests/checklist.md). The `tested_with` field in each frontmatter lists the models that passed.

## What I learned while testing

> Fill this in with your own findings. 

## Privacy

This repository contains templates only. Real resumes, contact details and employer names are never committed.

## License

MIT.
