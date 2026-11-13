"""Anthropic Messages API access (stdlib only) and offline-fixture mode."""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from .config import API_URL
from .prompts import CV_SYSTEM, CV_TOOL, REQ_SYSTEM, REQ_TOOL


def call_tool(system: str, user: str, tool: dict, model: str, retries: int = 4) -> dict:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        sys.exit("ANTHROPIC_API_KEY is not set (or use --fixtures for an offline run).")
    body = json.dumps({
        "model": model,
        "max_tokens": 8000,
        "temperature": 0,
        "system": system,
        "messages": [{"role": "user", "content": user}],
        "tools": [tool],
        "tool_choice": {"type": "tool", "name": tool["name"]},
    }).encode()
    headers = {"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"}
    for attempt in range(retries):
        req = urllib.request.Request(API_URL, data=body, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data = json.load(r)
            for block in data["content"]:
                if block["type"] == "tool_use":
                    return block["input"]
            raise RuntimeError("model returned no tool call")
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 529) and attempt < retries - 1:
                time.sleep(2 ** attempt * 2)
                continue
            sys.exit(f"API error {e.code}: {e.read().decode()[:500]}")
    sys.exit("API retries exhausted")


def get_requirements(job_text: str, args) -> dict:
    if args.requirements:
        return json.loads(Path(args.requirements).read_text())
    if args.fixtures:
        return json.loads((Path(args.fixtures) / "requirements.json").read_text())
    return call_tool(REQ_SYSTEM, f"<job_description>\n{job_text}\n</job_description>", REQ_TOOL, args.model)


def get_assessment(cv_text: str, reqs: list[dict], cv_name: str, args) -> dict:
    if args.fixtures:
        return json.loads((Path(args.fixtures) / f"{Path(cv_name).stem}.analysis.json").read_text())
    req_list = "\n".join(f"- {r['name']} [{r['priority']}]" + (f" (min {r['min_years']} years)" if r.get("min_years") else "")
                         for r in reqs)
    user = f"<requirements>\n{req_list}\n</requirements>\n\n<cv>\n{cv_text}\n</cv>"
    return call_tool(CV_SYSTEM, user, CV_TOOL, args.model)
