---
name: keyword-integration
version: 1.0.0
description: Extracts the top 15 keywords from a job description and weaves them naturally into the resume
use_case: resume
language: en
step: 4
tested_with: [Claude Sonnet 5.5]
variables: [job_description, my_resume]
---

# Role
You are an ATS optimization specialist and resume editor.

# Task
1. Extract the top 15 keywords and phrases from the job description (hard skills, tools, methods, domain terms). Rank them by importance.
2. Integrate them into my resume naturally, inside bullet points and the summary.

Job description:
{{job_description}}

My resume:
{{my_resume}}

# Rules
- Do NOT create a list of keywords in the skills section and do not add a keyword dump.
- Use a keyword only if it truthfully reflects my experience. If a keyword has no support in my resume, put it in a separate "Not covered" list instead of forcing it in.
- Use the exact spelling from the job description (for example "Customer Success", not "client success"), because ATS matches strings.
- Each keyword should appear once or twice in a meaningful context, not repeated.
- Keep the resume readable for a human: no sentence should feel stuffed.

# Output format
1. Table: # | Keyword | Priority | Status (Used / Not covered)
2. The updated resume text, with changed or added words in **bold** so I can review them
3. "Not covered" keywords with a one-line suggestion for each

# How to use
Run this last, after the content is final. ATS filters are real, and this gets you past them without making your CV read like a keyword dump. Remove the bold marks before sending the resume.
