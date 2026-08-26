"""Decompose every patch effect into WHY it moved L-GED — generalize the H2 finding.

For each (case, student, k, store) it splits the patch delta (patched - baseline)
into the three L-GED components and lists the high-weight teacher nodes the patched
output newly RECOVERS (missed at baseline, matched after the patch). The hypothesis
under test: a patch's delta is driven by the weighted teacher-node mass it recovers
(mostly Rules and Obligations), so the same mechanism should explain E2/M2 as it
does H2.

    LEX_DRL_SIMILARITY=embedding poetry run python scripts/decompose_patch_effect.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
os.environ.setdefault("LEX_DRL_SIMILARITY", "embedding")

import lex_drl.alignment as al  # noqa: E402
from lex_drl.discrepancy import compute_discrepancies  # noqa: E402
from lex_drl.schema import LegalReasoningGraph as G  # noqa: E402

GRAPHS = Path("data/outputs/graphs")
CASES = ["E2", "M2", "H2"]
KS = [1, 3, 5]


def _load(name: str):
    p = GRAPHS / name
    return G.model_validate_json(p.read_text()) if p.exists() else None


def _report(teacher, graph):
    return compute_discrepancies(teacher, graph, al.align_all(teacher, graph))


def _missed_set(rep):
    """teacher_id -> (weight, type, label) for every missed teacher node."""
    return {m.teacher_id: (m.weight, m.node_type, m.label) for m in rep.v_miss}


def _weighted(rep):
    vm = sum(m.weight for m in rep.v_miss)
    vh = sum(h.weight for h in rep.v_halluc)
    ve = sum(e.weight for e in rep.e_diff)
    return vm, vh, ve


def _patched_name(case, student, store, k):
    if store == "dirty":
        return f"{case}_agent_{student}_patched_k{k}.json"
    return f"{case}_agent_{student}_patched_{store}_k{k}.json"


def main():
    al.SIMILARITY_METHOD = "embedding"
    student = "llama3_2b"
    print(f"Patch-effect decomposition — {student}, embedding+{al.RULE_ALIGN_MODE} aligner\n")
    print(f"{'case':4} {'store':6} {'k':>2} {'base':>6} {'patched':>7} {'delta':>6} "
          f"{'Δvmiss':>7} {'Δvhal':>6} {'Δedge':>6} | recovered high-weight teacher nodes")
    print("-" * 118)

    for case in CASES:
        teacher = _load(f"{case}_reference.json")
        base = _load(f"{case}_agent_{student}.json")
        if teacher is None or base is None:
            continue
        rb = _report(teacher, base)
        base_missed = _missed_set(rb)
        vmb, vhb, veb = _weighted(rb)
        for store in ("dirty", "clean"):
            for k in KS:
                pg = _load(_patched_name(case, student, store, k))
                if pg is None:
                    continue
                rp = _report(teacher, pg)
                vmp, vhp, vep = _weighted(rp)
                delta = rp.l_ged - rb.l_ged
                # teacher nodes recovered = missed at baseline, NOT missed after patch
                patched_missed = _missed_set(rp)
                recovered = {tid: base_missed[tid] for tid in base_missed
                             if tid not in patched_missed}
                # show the high-weight ones (R/O and weight>=2)
                hi = sorted((v for v in ((tid,) + recovered[tid] for tid in recovered)
                             if v[1] >= 2.0), key=lambda x: -x[1])
                rec_str = ", ".join(f"{tid}({typ}{w:g})" for tid, w, typ, _ in hi[:8]) or "—"
                rec_wt = sum(w for _, w, _, _ in
                             ((tid,) + recovered[tid] for tid in recovered))
                print(f"{case:4} {store:6} {k:>2} {rb.l_ged:6.1f} {rp.l_ged:7.1f} "
                      f"{delta:+6.1f} {vmp-vmb:+7.1f} {vhp-vhb:+6.1f} {vep-veb:+6.1f} | "
                      f"Σrec={rec_wt:.0f}  {rec_str}")
        print()


if __name__ == "__main__":
    main()
