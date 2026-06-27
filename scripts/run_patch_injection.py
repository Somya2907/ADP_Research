"""Phase-2 inference: inject retrieved patches into the student prompt.

For each TEST case (E2/M2/H2) and each student, retrieve the top-k patches from
the store, render them as a POLICY REASONING NOTES block, prepend that block to
the agent system prompt (before the CASE section), re-run the student, and save
``{case}_agent_{student}_patched.json``.

Run order: this script runs AFTER (1) Phase-1 lands `v_misground` + patch_store,
and (2) a mining step has produced ``data/patches/patches.json`` from the
TRAINING cases via ``patch_generator.generate_all``. Budget (k, token cap) is a
parameter to ABLATE, not a constant — see docs/PATCH_GENERATOR_DESIGN.md §9.

    python scripts/run_patch_injection.py --k 3 --students gpt5 llama3_2b

Extraction imports below were verified against extraction.py (PROMPT_DIR,
_parse_response, _save_raw_response present and signature-compatible).
"""
from __future__ import annotations

import argparse
from pathlib import Path

from dotenv import load_dotenv

from lex_drl.cases import load_case
from lex_drl.patch_store import Patch, PatchStore
from lex_drl.schema import GraphSource
# Reused from extraction.py (module-level, importable):
from lex_drl.extraction import PROMPT_DIR, _parse_response, _save_raw_response
from lex_drl.clients import get_agent_client

load_dotenv()  # load OPENAI_API_KEY / OPENROUTER_API_KEY from .env (handoff draft omitted this)

TEST_CASES = ["E2", "M2", "H2"]
PATCH_STORE_PATH = Path("data/patches/patches.json")
PATCHED_DIR = Path("data/outputs/graphs")

# Train→test leakage guard (deterministic-phase). The design's firewall relies on
# the InsightWriter prose-rewrite to keep patches party-free, but that step is
# deferred this phase (insight=None), so a few missing_obligation patches embed
# training-case (E1/M1/H1) party/product names in their prevention_step. Injecting
# those into the test prompts would be train→test contamination, so we drop any
# patch whose text names a training-case party. Disable with --allow-party-leaks.
TRAIN_PARTY_NAMES = [
    "HireFlow", "Greenleaf", "ResumeRank", "TalentMetrics",   # E1
    "LoanScore", "Denver",                                    # M1
    "PeopleScore",                                            # H1
]


def _has_party_leak(patch: Patch) -> bool:
    text = f"{patch.prevention_step} {patch.contraindication}".lower()
    return any(name.lower() in text for name in TRAIN_PARTY_NAMES)


def filter_leaks(store: PatchStore) -> tuple[PatchStore, list[Patch]]:
    """Return (clean_store, dropped) — patches naming a training-case party removed."""
    clean, dropped = PatchStore(), []
    for p in store.all():
        (dropped.append(p) if _has_party_leak(p) else clean.add(p))
    return clean, dropped


def render_notes_block(patches: list[Patch]) -> str:
    """Render retrieved patches as a compact POLICY REASONING NOTES block."""
    if not patches:
        return ""
    lines = ["POLICY REASONING NOTES (apply only where the facts trigger them):"]
    for i, p in enumerate(patches, 1):
        note = f"{i}. {p.prevention_step}"
        if p.contraindication:
            note += f" [Caveat: {p.contraindication}]"
        lines.append(note)
    lines.append("")  # trailing blank line before CASE
    return "\n".join(lines)


def build_patched_system(case, notes_block: str) -> str:
    template = (PROMPT_DIR / "agent_firaco.txt").read_text(encoding="utf-8")
    system = (
        template
        .replace("<<CASE_FACTS>>", case.facts)
        .replace("<<CASE_QUESTION>>", case.question)
    )
    if notes_block:
        # Insert before the CASE section so the persona/intro stays first.
        system = system.replace("CASE:", notes_block + "\nCASE:", 1)
    return system


def run_patched(case, model_key: str, store: PatchStore, k: int):
    query = f"{case.facts}\n{case.question}"
    patches = store.retrieve(query, k=k)
    system = build_patched_system(case, render_notes_block(patches))
    client = get_agent_client(model_key)
    resp = client.generate(system=system, user="Begin your analysis now.")
    _save_raw_response(case.case_id, f"agent_{model_key}_patched", resp)
    graph = _parse_response(
        resp.text, case_id=case.case_id, source=GraphSource.AGENT,
        model=resp.model, agent_id=model_key,
    )
    out = PATCHED_DIR / f"{case.case_id}_agent_{model_key}_patched.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(graph.model_dump_json(indent=2), encoding="utf-8")
    print(f"  {case.case_id}/{model_key}: retrieved {len(patches)} patches → {out.name}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=3, help="patches retrieved per case (ablate {1,3,5})")
    ap.add_argument("--students", nargs="+", default=["gpt5", "llama3_2b"])
    ap.add_argument("--patch-store", default=str(PATCH_STORE_PATH))
    ap.add_argument("--cases", nargs="+", default=TEST_CASES)
    ap.add_argument("--allow-party-leaks", action="store_true",
                    help="do NOT drop patches that name a training-case party (default: drop)")
    args = ap.parse_args()

    store = PatchStore.from_file(args.patch_store)
    if not args.allow_party_leaks:
        store, dropped = filter_leaks(store)
        if dropped:
            print(f"Leakage guard: dropped {len(dropped)} patch(es) naming a training-case "
                  f"party (use --allow-party-leaks to keep): "
                  f"{', '.join(sorted({p.controlling_authority[:24] for p in dropped}))}")
    print(f"Injecting top-{args.k} of {len(store)} patches per (case, student).")

    ok, failed = [], []
    for cid in args.cases:
        case = load_case(cid)
        for model_key in args.students:
            try:
                run_patched(case, model_key, store, args.k)
                ok.append(f"{cid}/{model_key}")
            except Exception as e:  # one 429 / parse error must not abort the rest
                failed.append(f"{cid}/{model_key}")
                print(f"  [FAIL] {cid}/{model_key}: {type(e).__name__}: {str(e)[:160]}")

    print(f"\nDone: {len(ok)} ok, {len(failed)} failed.")
    if failed:
        print("  failed:", ", ".join(failed))


if __name__ == "__main__":
    main()
