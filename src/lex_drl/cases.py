"""Load and parse case files from data/cases/.

Each case is a markdown file with structured sections:
  # {CASE_ID} — {title}
  ## Metadata
  ## Facts
  ## Question
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

CASES_DIR = Path("data/cases")

# A case file is "{ID}_{slug}.md" where ID is a tier letter plus a number
# (E3, M10, H7). Anything else in the directory (e.g. MANIFEST.md) is ignored.
_CASE_ID = re.compile(r"^[EMH]\d+$")
TIERS = ("easy", "medium", "hard")


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
    # Named parties and products in the facts. Never shown to a model; used by
    # the train→test leakage guard to drop patches that name a training party.
    parties: list[str] = field(default_factory=list)


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
        parties=_extract_list(meta, "parties"),
    )


def _id_key(case_id: str) -> tuple[str, int]:
    return case_id[0], int(case_id[1:])


def load_all_cases() -> list[Case]:
    """Load all cases from the cases directory, sorted by tier letter then number."""
    ids = {p.name.split("_")[0] for p in CASES_DIR.glob("*.md")}
    ids = sorted((i for i in ids if _CASE_ID.match(i)), key=_id_key)
    return [load_case(cid) for cid in ids]


def cases_by_role(role: str) -> list[Case]:
    """All cases with the given role ("training" or "test")."""
    return [c for c in load_all_cases() if c.role == role]


def case_census() -> dict[str, dict[str, int]]:
    """Count of cases per tier and role, e.g. {"easy": {"training": 5, "test": 5}}."""
    census: dict[str, dict[str, int]] = {}
    for c in load_all_cases():
        census.setdefault(c.tier, {}).setdefault(c.role, 0)
        census[c.tier][c.role] += 1
    return census


def _extract_scalar(meta: str, key: str) -> str:
    """Value of the "- key: value" metadata line (exact key, not a substring)."""
    for line in meta.splitlines():
        m = re.match(r"^\s*-?\s*([A-Za-z_]+)\s*:\s*(.*)$", line)
        if m and m.group(1).lower() == key:
            return m.group(2).strip().strip("`").strip('"')
    return ""


def _extract_list(meta: str, key: str) -> list[str]:
    raw = _extract_scalar(meta, key)
    if not raw:
        return []
    return [t.strip() for t in raw.replace("+", ",").split(",") if t.strip()]
