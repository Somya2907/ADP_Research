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
import json
from pathlib import Path

from dotenv import load_dotenv

from lex_drl.cases import load_case
from lex_drl.patch_generator import _canon_jurisdiction
from lex_drl.patch_store import Patch, PatchStore
from lex_drl.schema import GraphSource
# Reused from extraction.py (module-level, importable):
from lex_drl.extraction import PROMPT_DIR, _parse_response, _save_raw_response
from lex_drl.clients import get_agent_client

load_dotenv()  # load OPENAI_API_KEY / OPENROUTER_API_KEY from .env (handoff draft omitted this)

TEST_CASES = ["E2", "M2", "H2"]
PATCH_STORE_PATH = Path("data/patches/patches.json")
PATCHED_DIR = Path("data/outputs/graphs")
RETRIEVAL_LOG = Path("results/retrieval_log.json")

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


def run_patched(case, model_key: str, store: PatchStore, k: int, *,
                allowed: set[str], variant: str, jfilter: bool, run_tag: str = ""):
    query = f"{case.facts}\n{case.question}"
    juris = {_canon_jurisdiction(t) for t in (getattr(case, "jurisdiction_tags", []) or [])}
    if jfilter and juris:
        patches = store.retrieve(query, k=k, allowed=allowed, jurisdictions=juris)
        if not patches:  # fall back to unfiltered top-k (on the allowed set)
            patches = store.retrieve(query, k=k, allowed=allowed)
    else:
        patches = store.retrieve(query, k=k, allowed=allowed)

    system = build_patched_system(case, render_notes_block(patches))
    client = get_agent_client(model_key)
    gen_kwargs = {"run_tag": run_tag} if run_tag else {}
    resp = client.generate(system=system, user="Begin your analysis now.", **gen_kwargs)
    _save_raw_response(case.case_id, f"agent_{model_key}_patched", resp)
    graph = _parse_response(
        resp.text, case_id=case.case_id, source=GraphSource.AGENT,
        model=resp.model, agent_id=model_key,
    )
    tag = f"_{run_tag}" if run_tag else ""
    suffix = f"_patched_k{k}" if variant == "dirty" else f"_patched_{variant}{tag}_k{k}"
    out = PATCHED_DIR / f"{case.case_id}_agent_{model_key}{suffix}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(graph.model_dump_json(indent=2), encoding="utf-8")

    off = sum(1 for p in patches if p.jurisdiction not in juris) if juris else 0
    log = {
        "case": case.case_id, "student": model_key, "k": k, "variant": variant,
        "run_tag": run_tag, "case_jurisdictions": sorted(juris),
        "n_retrieved": len(patches),
        "off_jurisdiction_pct": round(100.0 * off / len(patches), 1) if patches else 0.0,
        "retrieved": [{"patch_id": p.patch_id, "jurisdiction": p.jurisdiction,
                       "verification": p.verification,
                       "authority": p.controlling_authority,
                       "off_jurisdiction": bool(juris) and p.jurisdiction not in juris}
                      for p in patches],
    }
    print(f"  {case.case_id}/{model_key} (k={k}, {variant}): {len(patches)} patches, "
          f"{log['off_jurisdiction_pct']}% off-juris → {out.name}")
    return out, log


def _append_log(entries: list[dict]) -> None:
    RETRIEVAL_LOG.parent.mkdir(parents=True, exist_ok=True)
    existing = json.loads(RETRIEVAL_LOG.read_text()) if RETRIEVAL_LOG.exists() else []
    # de-dupe by (case, student, k, variant, run_tag): a re-run replaces its rows
    keyed = {(e["case"], e["student"], e["k"], e["variant"], e.get("run_tag", "")): e
             for e in existing + entries}
    RETRIEVAL_LOG.write_text(json.dumps(list(keyed.values()), indent=2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=3, help="patches retrieved per case (ablate {1,3,5})")
    ap.add_argument("--students", nargs="+", default=["gpt5", "llama3_2b"])
    ap.add_argument("--patch-store", default=str(PATCH_STORE_PATH))
    ap.add_argument("--cases", nargs="+", default=TEST_CASES)
    ap.add_argument("--allowed", default="verified",
                    help="comma-sep verification statuses to retrieve (default: verified)")
    ap.add_argument("--variant", default="dirty",
                    choices=["dirty", "clean", "clean_jfilter"],
                    help="store variant → output suffix; clean_jfilter adds a jurisdiction pre-filter")
    ap.add_argument("--run-tag", default="", help="salt the cache key (variance repeats)")
    ap.add_argument("--allow-party-leaks", action="store_true",
                    help="do NOT drop patches that name a training-case party (default: drop)")
    args = ap.parse_args()

    allowed = {s.strip() for s in args.allowed.split(",") if s.strip()}
    jfilter = args.variant == "clean_jfilter"

    store = PatchStore.from_file(args.patch_store)
    if not args.allow_party_leaks:
        store, dropped = filter_leaks(store)
        if dropped:
            print(f"Leakage guard: dropped {len(dropped)} patch(es) naming a training-case "
                  f"party (use --allow-party-leaks to keep): "
                  f"{', '.join(sorted({p.controlling_authority[:24] for p in dropped}))}")
    print(f"Injecting top-{args.k} (variant={args.variant}, allowed={sorted(allowed)}, "
          f"jfilter={jfilter}) of {len(store)} patches per (case, student).")

    ok, failed, logs = [], [], []
    for cid in args.cases:
        case = load_case(cid)
        for model_key in args.students:
            try:
                _, log = run_patched(case, model_key, store, args.k,
                                     allowed=allowed, variant=args.variant,
                                     jfilter=jfilter, run_tag=args.run_tag)
                logs.append(log)
                ok.append(f"{cid}/{model_key}")
            except Exception as e:  # one 429 / parse error must not abort the rest
                failed.append(f"{cid}/{model_key}")
                print(f"  [FAIL] {cid}/{model_key}: {type(e).__name__}: {str(e)[:160]}")

    if logs:
        _append_log(logs)
        print(f"  retrieval log → {RETRIEVAL_LOG}")
    print(f"\nDone: {len(ok)} ok, {len(failed)} failed.")
    if failed:
        print("  failed:", ", ".join(failed))


if __name__ == "__main__":
    main()
