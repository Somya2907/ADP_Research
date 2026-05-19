"""End-to-end graph extraction: case + prompt template → LegalReasoningGraph.

The core pipeline:
  1. Load case facts and question
  2. Render the appropriate prompt template (teacher or agent)
  3. Call the model
  4. Parse the two-part response (written analysis + JSON graph)
  5. Validate against F-I-R-A-C-O schema
  6. Save to data/outputs/graphs/
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from pydantic import ValidationError
from rich import print as rprint

from .cases import Case
from .clients import AgentClient, LLMResponse, TeacherClient
from .schema import GraphSource, LegalReasoningGraph

PROMPT_DIR = Path("configs/prompts")
OUTPUT_DIR = Path("data/outputs/graphs")
ANALYSIS_DIR = Path("data/outputs/analysis")


def _ensure_dirs():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)


def load_statutes() -> str:
    """Concatenate all statute text files for teacher context injection."""
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
    """Run teacher model (Claude Opus 4.6) with statutory context."""
    client = TeacherClient()
    template = (PROMPT_DIR / "teacher_firaco.txt").read_text(encoding="utf-8")
    system = template.format(
        statutes=load_statutes(),
        case_facts=case.facts,
        case_question=case.question,
    )
    resp = client.generate(system=system, user="Begin your analysis now.")
    _save_raw_response(case.case_id, "reference", resp)
    return _parse_response(
        resp.text,
        case_id=case.case_id,
        source=GraphSource.REFERENCE,
        model=resp.model,
    )


def extract_agent_graph(case: Case) -> LegalReasoningGraph:
    """Run agent model (GPT-5) WITHOUT statutory context."""
    client = AgentClient()
    template = (PROMPT_DIR / "agent_firaco.txt").read_text(encoding="utf-8")
    system = template.format(
        case_facts=case.facts,
        case_question=case.question,
    )
    resp = client.generate(system=system, user="Begin your analysis now.")
    _save_raw_response(case.case_id, "agent", resp)
    return _parse_response(
        resp.text,
        case_id=case.case_id,
        source=GraphSource.AGENT,
        model=resp.model,
    )


def _save_raw_response(case_id: str, source: str, resp: LLMResponse):
    """Save full raw response for debugging and analysis."""
    _ensure_dirs()
    out = ANALYSIS_DIR / f"{case_id}_{source}_raw.txt"
    out.write_text(resp.text, encoding="utf-8")


def _parse_response(
    text: str,
    case_id: str,
    source: GraphSource,
    model: str,
) -> LegalReasoningGraph:
    """Parse two-part LLM response into a validated LegalReasoningGraph.

    Expected format:
      [written FIRACO analysis]
      === JSON GRAPH ===
      { ... valid JSON ... }
    """
    marker = "=== JSON GRAPH ==="

    if marker not in text:
        # Fallback: try to find a JSON block anywhere in the response
        json_match = re.search(r"\{[\s\S]*\}", text)
        if json_match:
            rprint(f"[yellow]Warning: {case_id} missing '{marker}' delimiter, "
                   f"attempting JSON extraction from response body[/yellow]")
            json_blob = json_match.group()
        else:
            raise ValueError(
                f"Response for {case_id} missing '{marker}' delimiter "
                f"and no JSON block found.\n"
                f"First 500 chars: {text[:500]}"
            )
    else:
        _analysis, json_blob = text.split(marker, 1)
        json_blob = json_blob.strip()

    # Strip markdown fences if present
    if json_blob.startswith("```"):
        # Remove opening fence line and closing fence
        lines = json_blob.split("\n")
        start = 1  # skip the ``` line
        end = len(lines)
        for i in range(len(lines) - 1, 0, -1):
            if lines[i].strip().startswith("```"):
                end = i
                break
        json_blob = "\n".join(lines[start:end])

    try:
        raw = json.loads(json_blob)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"JSON parse failed for {case_id}: {e}\n\n"
            f"First 500 chars of JSON blob:\n{json_blob[:500]}"
        )

    # Inject metadata that the LLM may not have included
    raw.setdefault("case_id", case_id)
    raw["source"] = source.value
    raw["model_name"] = model

    try:
        graph = LegalReasoningGraph.model_validate(raw)
    except ValidationError as e:
        raise ValueError(
            f"Schema validation failed for {case_id} ({source.value}):\n{e}\n\n"
            f"Raw JSON keys: {list(raw.keys())}"
        )

    return graph


def save_graph(graph: LegalReasoningGraph) -> Path:
    """Save validated graph as JSON."""
    _ensure_dirs()
    suffix = graph.source.value
    out = OUTPUT_DIR / f"{graph.case_id}_{suffix}.json"
    out.write_text(graph.model_dump_json(indent=2), encoding="utf-8")
    return out
