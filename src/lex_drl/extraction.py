"""End-to-end graph extraction: case + prompt template → LegalReasoningGraph.

Supports three model tiers:
  Teacher:  Claude Opus 4.6 + statutes → G_ref
  Student1: GPT-5, no statutes → G_agent (agent_id="gpt5")
  Student2: Qwen3-4B, no statutes → G_agent (agent_id="qwen3_4b")

Fixes (v3):
  - case_id forced from code, not from LLM output (was overwriting all to E1)
  - Graph sanitizer maps unknown enum values to safe defaults instead of crashing
    (handles LLM-invented edge types like "leads-to", missing support_refs, etc.)
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from pydantic import ValidationError
from rich import print as rprint

from .cases import Case
from .clients import TeacherClient, get_agent_client, LLMResponse
from .schema import GraphSource, LegalReasoningGraph

PROMPT_DIR = Path("configs/prompts")
OUTPUT_DIR = Path("data/outputs/graphs")
ANALYSIS_DIR = Path("data/outputs/analysis")

VALID_EDGE_TYPES = {
    "supports", "contradicts", "applies-to", "triggers",
    "satisfies-element", "fails-element", "preempts", "distinguishes",
}
VALID_CONFIDENCE = {"high", "medium", "low"}
VALID_AUTHORITY = {"binding", "persuasive", "advisory", "overruled"}
VALID_DETERMINATION = {"compliant", "non-compliant", "conditional"}
VALID_APP_RESULT = {"satisfied", "violated", "requires-fact", "partial"}


def _ensure_dirs():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)


def load_statutes() -> str:
    statutes_dir = Path("data/statutes")
    if not statutes_dir.exists():
        return "(No statute files found in data/statutes/)"
    chunks = []
    for fp in sorted(statutes_dir.glob("*.txt")):
        chunks.append(f"--- {fp.stem} ---\n{fp.read_text(encoding='utf-8')}\n")
    if not chunks:
        return "(No .txt files found in data/statutes/)"
    return "\n".join(chunks)


def extract_teacher_graph(case: Case) -> LegalReasoningGraph:
    """Run teacher (Claude Opus 4.6) with statutory context → G_ref."""
    client = TeacherClient()
    template = (PROMPT_DIR / "teacher_firaco.txt").read_text(encoding="utf-8")
    system = (
        template
        .replace("<<STATUTES>>", load_statutes())
        .replace("<<CASE_FACTS>>", case.facts)
        .replace("<<CASE_QUESTION>>", case.question)
    )
    resp = client.generate(system=system, user="Begin your analysis now.")
    _save_raw_response(case.case_id, "reference", resp)
    return _parse_response(
        resp.text,
        case_id=case.case_id,
        source=GraphSource.REFERENCE,
        model=resp.model,
        agent_id=None,
    )


def extract_agent_graph(case: Case, model_key: str = "gpt5") -> LegalReasoningGraph:
    """Run a student model WITHOUT statutory context → G_agent.

    Args:
        case:      The case to analyze.
        model_key: "gpt5" or "qwen3_4b"
    """
    client = get_agent_client(model_key)
    template = (PROMPT_DIR / "agent_firaco.txt").read_text(encoding="utf-8")
    system = (
        template
        .replace("<<CASE_FACTS>>", case.facts)
        .replace("<<CASE_QUESTION>>", case.question)
    )
    resp = client.generate(system=system, user="Begin your analysis now.")
    _save_raw_response(case.case_id, f"agent_{model_key}", resp)
    return _parse_response(
        resp.text,
        case_id=case.case_id,
        source=GraphSource.AGENT,
        model=resp.model,
        agent_id=model_key,
    )


def _save_raw_response(case_id: str, source_label: str, resp: LLMResponse):
    _ensure_dirs()
    out = ANALYSIS_DIR / f"{case_id}_{source_label}_raw.txt"
    out.write_text(resp.text, encoding="utf-8")


def _sanitize_raw_graph(raw: dict, case_id: str, source_label: str) -> dict:
    """Sanitize LLM output before schema validation.

    LLMs commonly produce:
      - Edge types not in our enum (e.g. "leads-to", "implies")
      - Missing required fields after truncation (e.g. missing support_refs)
      - Invalid enum values for confidence/authority/etc.

    Strict schema validation crashes the whole graph. This sanitizer maps
    unknown values to safe defaults and logs every change so we can review
    them in the raw response files later.
    """
    changes = []

    # ── Edges ──
    for edge in raw.get("edges", []):
        if isinstance(edge, dict) and "type" in edge:
            et = edge["type"]
            if et not in VALID_EDGE_TYPES:
                edge["type"] = "supports"  # safest default
                changes.append(f"edge {edge.get('eid', '?')}: type '{et}' → 'supports'")

    # ── Conclusions ──
    for conc in raw.get("conclusions", []):
        if not isinstance(conc, dict):
            continue
        cid = conc.get("cid", "?")
        # Missing support_refs (common when response truncated)
        if "support_refs" not in conc:
            conc["support_refs"] = []
            changes.append(f"conclusion {cid}: added missing support_refs=[]")
        # Invalid confidence
        if "confidence" in conc and conc["confidence"] not in VALID_CONFIDENCE:
            old = conc["confidence"]
            conc["confidence"] = "medium"
            changes.append(f"conclusion {cid}: confidence '{old}' → 'medium'")
        elif "confidence" not in conc:
            conc["confidence"] = "medium"
            changes.append(f"conclusion {cid}: added missing confidence='medium'")
        # Invalid determination
        if "determination" in conc and conc["determination"] not in VALID_DETERMINATION:
            old = conc["determination"]
            conc["determination"] = "conditional"
            changes.append(f"conclusion {cid}: determination '{old}' → 'conditional'")

    # ── Rules ──
    for rule in raw.get("rules", []):
        if not isinstance(rule, dict):
            continue
        rid = rule.get("rid", "?")
        if "authority" in rule and rule["authority"] not in VALID_AUTHORITY:
            old = rule["authority"]
            rule["authority"] = "binding"
            changes.append(f"rule {rid}: authority '{old}' → 'binding'")

    # ── Applications ──
    for app in raw.get("applications", []):
        if not isinstance(app, dict):
            continue
        aid = app.get("aid", "?")
        if "result" in app and app["result"] not in VALID_APP_RESULT:
            old = app["result"]
            app["result"] = "partial"
            changes.append(f"application {aid}: result '{old}' → 'partial'")

    if changes:
        rprint(f"[yellow]Note: {case_id}/{source_label} sanitized "
               f"{len(changes)} field(s):[/yellow]")
        for c in changes[:5]:  # cap log noise
            rprint(f"  [yellow]· {c}[/yellow]")
        if len(changes) > 5:
            rprint(f"  [yellow]· (+ {len(changes) - 5} more)[/yellow]")

    return raw


def _parse_response(
    text: str,
    case_id: str,
    source: GraphSource,
    model: str,
    agent_id: str | None,
) -> LegalReasoningGraph:
    """Parse two-part LLM response into a validated LegalReasoningGraph."""
    marker = "=== JSON GRAPH ==="
    source_label = f"agent_{agent_id}" if agent_id else "reference"

    if marker not in text:
        json_match = re.search(r"\{[\s\S]*\}", text)
        if json_match:
            rprint(f"[yellow]Warning: {case_id} missing '{marker}' delimiter, "
                   f"attempting JSON extraction from response body[/yellow]")
            json_blob = json_match.group()
        else:
            raise ValueError(
                f"Response for {case_id} missing '{marker}' delimiter "
                f"and no JSON block found.\nFirst 500 chars: {text[:500]}"
            )
    else:
        _analysis, json_blob = text.split(marker, 1)
        json_blob = json_blob.strip()

    # Strip markdown fences
    if json_blob.startswith("```"):
        lines = json_blob.split("\n")
        start = 1
        end = len(lines)
        for i in range(len(lines) - 1, 0, -1):
            if lines[i].strip().startswith("```"):
                end = i
                break
        json_blob = "\n".join(lines[start:end])

    try:
        raw = json.loads(json_blob)
    except json.JSONDecodeError as e:
        try:
            from json_repair import repair_json
            repaired = repair_json(json_blob)
            raw = json.loads(repaired)
            rprint(f"[yellow]Note: {case_id} JSON required repair — "
                   f"original error was: {e}[/yellow]")
        except Exception:
            raise ValueError(
                f"JSON parse failed for {case_id}: {e}\n\n"
                f"First 500 chars:\n{json_blob[:500]}\n\n"
                f"Full response saved to data/outputs/analysis/{case_id}_*_raw.txt"
            )

    # Force metadata from code (case_id bug fix)
    raw["case_id"] = case_id
    raw["source"] = source.value
    raw["model_name"] = model
    raw["agent_id"] = agent_id

    # Sanitize before validation — maps unknown enums to safe defaults
    raw = _sanitize_raw_graph(raw, case_id, source_label)

    try:
        graph = LegalReasoningGraph.model_validate(raw)
    except ValidationError as e:
        raise ValueError(
            f"Schema validation failed for {case_id} ({source.value}) "
            f"AFTER sanitization:\n{e}\n\nRaw JSON keys: {list(raw.keys())}"
        )

    return graph


def save_graph(graph: LegalReasoningGraph) -> Path:
    _ensure_dirs()
    out = Path(graph.save_path())
    out.write_text(graph.model_dump_json(indent=2), encoding="utf-8")
    return out
