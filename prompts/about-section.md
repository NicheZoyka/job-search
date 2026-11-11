---
name: about-section
version: 1.0.0
description: Writes three versions of a LinkedIn About section that sound like a real person
use_case: linkedin
language: en
step: standalone
tested_with: [Claude Sonnet 5.5]
variables: [background, problems_i_solve, target_audience]
---

# Role
You are a professional writer who helps people describe their work in a clear, human voice.

# Task
Write my LinkedIn About section.

About me:
{{background}}

Problems I solve:
{{problems_i_solve}}

For whom:
{{target_audience}}

# Rules
- First person.
- No buzzwords or clichés ("passionate", "results-driven", "team player", "dynamic", "synergy").
- Focus on what problems I solve and for whom, not on a list of job titles.
- Under 200 words per version.
- Use only facts from my input. Do not invent achievements, numbers or clients.
- End with a simple, low-pressure call to action.

# Output format
Write 3 versions:
1. **Formal**
2. **Conversational**
3. **Bold**

After each version, one line on who it suits best.

# How to use
Pick the version that sounds most like you, then edit it by hand. Read it aloud: if you would not say a sentence to a colleague, change it.
