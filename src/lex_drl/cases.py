"""Load and parse case files from data/cases/.

Each case is a markdown file with structured sections:
  # {CASE_ID} — {title}
  ## Metadata
  ## Facts
  ## Question
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

CASES_DIR = Path("data/cases")


@dataclass
class Case:
    case_id: str                          # e.g., "E1"
    title: str
    facts: str
    question: str
    jurisdiction_tags: list[str] = field(default_factory=list)
    doctrinal_area: str = ""
    tier: str = ""                        # "easy" | "medium" | "hard"
    role: str = ""                        # "training" | "test"


def load_case(case_id: str) -> Case:
    """Parse a case markdown file by case_id prefix (e.g., 'E1')."""
    matches = list(CASES_DIR.glob(f"{case_id}_*.md"))
    if not matches:
        raise FileNotFoundError(
            f"No case file matching '{case_id}_*.md' in {CASES_DIR}"
        )
    path = matches[0]
    raw = path.read_text(encoding="utf-8")

    # Parse sections
    sections: dict[str, str] = {}
    title = ""
    current_section: str | None = None
    buf: list[str] = []

    for line in raw.splitlines():
        if line.startswith("# ") and not title:
            title = line[2:].strip()
            continue
        if line.startswith("## "):
            if current_section:
                sections[current_section] = "\n".join(buf).strip()
            current_section = line[3:].strip()
            buf = []
        else:
            buf.append(line)
    if current_section:
        sections[current_section] = "\n".join(buf).strip()

    meta = sections.get("Metadata", "")
    return Case(
        case_id=case_id,
        title=title,
        facts=sections.get("Facts", ""),
        question=sections.get("Question", ""),
        jurisdiction_tags=_extract_list(meta, "jurisdiction"),
        doctrinal_area=_extract_scalar(meta, "doctrinal_area"),
        tier=_extract_scalar(meta, "tier"),
        role=_extract_scalar(meta, "role"),
    )


def load_all_cases() -> list[Case]:
    """Load all cases from the cases directory, sorted by ID."""
    ids = sorted(
        {p.name.split("_")[0] for p in CASES_DIR.glob("*.md")},
    )
    return [load_case(cid) for cid in ids]


def _extract_scalar(meta: str, key: str) -> str:
    for line in meta.splitlines():
        if key in line.lower():
            return line.split(":", 1)[1].strip().strip("`").strip('"')
    return ""


def _extract_list(meta: str, key: str) -> list[str]:
    raw = _extract_scalar(meta, key)
    if not raw:
        return []
    return [t.strip() for t in raw.replace("+", ",").split(",") if t.strip()]
