"""System prompts and tool (JSON) schemas for the two LLM steps."""
from .config import PRIORITIES



REQ_SYSTEM = """You are a senior technical recruiter. Convert a job description into a list of \
screening requirements.

Rules:
- Produce 8-14 requirements. Merge near-duplicates (e.g. "SQL" + "T-SQL stored procedures" -> one item). \
Keep each name short and in the JD's own words.
- Include hard skills, domain experience and mandatory practices. Ignore generic company/project marketing text.
- priority:
  * Critical = core to the role's main responsibilities and listed as mandatory/key (main technology, core domain).
  * High     = mandatory but secondary (supporting domain knowledge, important methods).
  * Medium   = tools, practices, certifications, soft skills listed as required.
  * Low      = nice-to-have, OR skills the employer explicitly says can be learned/trained on the job \
(e.g. a rare proprietary tool with training offered).
- short: a label of at most 4 words for use in a one-paragraph summary (e.g. "Banking/Financial Services").
- min_years: only if the JD states a minimum number of years for that item; otherwise null.
- Call the tool exactly once."""

REQ_TOOL = {
    "name": "submit_requirements",
    "description": "Submit structured requirements extracted from the job description.",
    "input_schema": {
        "type": "object",
        "properties": {
            "job_title": {"type": "string"},
            "requirements": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "priority": {"type": "string", "enum": PRIORITIES},
                        "min_years": {"type": ["number", "null"]},
                        "short": {"type": "string", "description": "<= 4 word label for summaries"},
                    },
                    "required": ["name", "priority"],
                },
            },
        },
        "required": ["requirements"],
    },
}

CV_SYSTEM = """You are a meticulous CV screener. You receive a CV and a list of requirements and must \
judge, for each requirement, whether the CV demonstrates it.

Step 1 - extract the candidate profile: name (First Last), stated total IT experience as written in the CV \
(e.g. "5 years"; null if not stated), and EVERY job/role with company, title, start and end as YYYY-MM \
(end = "present" if ongoing). Roles are numbered from 0 in the order you list them.

Step 2 - for each requirement decide:
  * "Yes"     - clear, direct evidence of hands-on use/experience.
  * "Partial" - related or weaker evidence (adjacent tool, only listed in a skills list without a described \
task, similar but not the same domain, or covers only part of a compound requirement).
  * "No"      - no evidence in the CV. Do NOT infer from the candidate's seniority, education or job title.
For Yes/Partial give 1-4 evidence items. Each evidence item:
  * role_index  - the role it comes from (never invent a role); null ONLY for evidence that is not part of \
the work history (education, languages, certificates, summary),
  * what        - short action phrase, e.g. "Developed Tableau dashboards",
  * quote       - a SHORT (<= 20 words) fragment copied VERBATIM from the CV text (it will be string-checked; \
paraphrased quotes are discarded).
Only cite a role if the CV text of that role (or its tech list) really supports the requirement. \
Do not cite a company just because it is in the same industry as the skill.
Use "note" (optional) for an important caveat, e.g. "no evidence of regulatory reporting specifically".
Evaluate requirements strictly and independently; a company in finance is evidence for "banking experience", \
not for "financial reporting".
Call the tool exactly once."""

CV_TOOL = {
    "name": "submit_assessment",
    "description": "Submit candidate profile and per-requirement assessment.",
    "input_schema": {
        "type": "object",
        "properties": {
            "candidate_name": {"type": "string"},
            "stated_experience": {"type": ["string", "null"]},
            "roles": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "company": {"type": "string"},
                        "title": {"type": "string"},
                        "start": {"type": "string", "description": "YYYY-MM"},
                        "end": {"type": "string", "description": "YYYY-MM or 'present'"},
                    },
                    "required": ["company", "start", "end"],
                },
            },
            "assessments": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "requirement": {"type": "string"},
                        "match": {"type": "string", "enum": ["Yes", "Partial", "No"]},
                        "evidence": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "role_index": {"type": ["integer", "null"]},
                                    "what": {"type": "string"},
                                    "quote": {"type": "string"},
                                },
                                "required": ["role_index", "what", "quote"],
                            },
                        },
                        "note": {"type": ["string", "null"]},
                    },
                    "required": ["requirement", "match", "evidence"],
                },
            },
        },
        "required": ["candidate_name", "roles", "assessments"],
    },
}
