"""Reading CV / job files and text normalisation."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path



def read_document(path: Path) -> str:
    ext = path.suffix.lower()
    if ext == ".docx":
        import docx  # python-docx

        d = docx.Document(str(path))
        parts = [p.text for p in d.paragraphs if p.text.strip()]
        for t in d.tables:
            for row in t.rows:
                parts.append(" | ".join(c.text.strip() for c in row.cells))
        return "\n".join(parts)
    if ext == ".pdf":
        out = subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True, text=True, check=True)
        return out.stdout
    return path.read_text(encoding="utf-8", errors="replace")


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("’", "'").replace("–", "-").replace("—", "-")).strip().lower()
