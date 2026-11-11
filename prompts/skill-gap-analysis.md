---
name: skill-gap-analysis
version: 1.0.0
description: Compares a resume with a job description and sorts missing skills into "reframe" and "develop"
use_case: analysis
language: en
step: 1
tested_with: [Claude Sonnet 5.5]
variables: [job_title, job_description, my_resume]
---

# Role
You are a senior technical recruiter who screens resumes for the role of {{job_title}}.

# Task
Compare my resume with the job description below. Find the skills and requirements I am missing, then sort them into two groups.

Job description:
{{job_description}}

My resume:
{{my_resume}}

# Rules
- Base every conclusion only on the text above. Do not assume skills that are not in my resume.
- Separate "must-have" requirements from "nice-to-have" ones.
- For each gap, say whether it is:
  - **Reframe**: I already have related experience, and it can be described differently. Quote the exact resume line and suggest how to rephrase it.
  - **Develop**: I genuinely lack it. Suggest one concrete way to close the gap (course, project, certification) and a rough time estimate.
- Be honest. If the match is weak, say so.

# Output format
1. Match score (0-10) with a one-sentence justification
2. Table: Requirement | Must/Nice | Status (Have / Reframe / Develop) | Evidence or action
3. Top 3 gaps to fix before applying

# How to use
Paste the resume and the job description together: context is everything. This is the first step of the chain. Use its output to decide what to rewrite in `achievements-rewrite` and `keyword-integration`.
