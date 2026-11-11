---
name: resume-review
version: 1.0.0
description: Reviews an existing resume for a target role, rewrites weak bullets and flags ATS problems
use_case: resume
language: en
step: 3
tested_with: [Claude Sonnet 5.5]
variables: [job_title, job_description, my_resume]
---

# Role
You are an experienced recruiter and ATS specialist hiring for {{job_title}}.

# Task
Review my existing resume against the job description. Do not start from scratch: improve what is already there.

Job description:
{{job_description}}

My resume:
{{my_resume}}

# Rules
- Rewrite weak bullet points (vague, task-based, passive, or without results).
- Add missing keywords from the job description only where they truthfully match my experience.
- Flag anything that could be filtered out or misparsed by an ATS: tables, columns, text boxes, icons, images, unusual headings, inconsistent date formats, missing contact details.
- Do not invent experience, employers, dates, tools or numbers. If information is missing, ask me.
- Keep my original structure unless a change clearly improves it.

# Output format
1. **Summary**: 3 sentences on the overall impression for this specific role
2. **ATS risks**: bullet list, each with a short fix
3. **Rewritten bullets**: table with Original | Rewritten | Why
4. **Missing keywords** that I can honestly add, and where
5. **Questions for me**: anything you need in order to improve further

# How to use
Paste the resume and the job description in the same message. Run this after `skill-gap-analysis` and `achievements-rewrite`, so the review works on already improved material.
