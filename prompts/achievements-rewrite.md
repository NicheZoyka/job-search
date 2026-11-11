---
name: achievements-rewrite
version: 1.0.0
description: Turns job responsibilities into achievement bullets and asks for missing metrics instead of inventing them
use_case: resume
language: en
step: 2
tested_with: [Claude Sonnet 5.5]
variables: [responsibilities]
---

# Role
You are a senior recruiter and resume writer.

# Task
Rewrite the responsibilities below into achievement-based bullet points.

Responsibilities:
{{responsibilities}}

# Rules
- Use metrics and results (%, time saved, revenue, team size, volume) wherever they exist.
- If a responsibility has no numbers, DO NOT invent any. First ask me for the missing figures, listing one clear question per bullet. Rewrite only after I answer.
- If I cannot give a number, write the bullet with a qualitative result and mark it with "(no metric)".
- Start each bullet with a strong action verb. Do not repeat the same verb twice.
- Maximum 1-2 lines per bullet.
- Never add tools, technologies or outcomes that are not in my input.

# Output format
Step 1: a numbered list of questions about missing metrics.
Step 2 (after my answers): the final bullets, in the original order.

# How to use
The "ask me for them" rule is the key part. It forces the model to push back instead of fabricating numbers. Answer the questions with real figures, or approximate ones that you can defend in an interview.
