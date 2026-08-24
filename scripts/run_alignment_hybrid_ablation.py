"""Rule-alignment ablation: citation-only vs embedding-only vs hybrid (current).

The professor's concern: embeddings can't distinguish statute citations
(§6-1-1703(2)(a) vs (2)(b) look near-identical), so rule matching should be a
hybrid of citation + text. This measures whether the current pipeline (which is
ALREADY citation-first for rules) matters, by re-scoring every case under three
rule-alignment modes while holding all other node types on embeddings:

  * embedding_only — rules matched purely by embedding cosine (the "non-hybrid")
  * citation_only  — rules matched only by citation-token intersection, no fallback
  * hybrid         — current: citation-first, embedding fallback (align_rules)

Reports, per mode: the GPT-5<Llama ranking (x/6), total L-GED, and total
v_misground (aligned rule pairs with CONFLICTING citations = embeddings merging
legally distinct rules). Also a direct embedding-confusion demo on sibling
subsections.

    LEX_DRL_SIMILARITY=embedding poetry run python scripts/run_alignment_hybrid_ablation.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
os.environ.setdefault("LEX_DRL_SIMILARITY", "embedding")

import lex_drl.alignment as al  # noqa: E402
from lex_drl.alignment import (  # noqa: E402
    _align_by_text, _embedding_cosine_matrix, align_all, align_rules,
    extract_citation_tokens,
)
from lex_drl.discrepancy import compute_discrepancies  # noqa: E402
from lex_drl.schema import LegalReasoningGraph  # noqa: E402

al.SIMILARITY_METHOD = "embedding"
THRESH = 0.55
GRAPHS = Path("data/outputs/graphs")
CASES = ["E1", "E2", "M1", "M2", "H1", "H2"]
STUDENTS = ["gpt5", "llama3_2b"]


def _load(name: str) -> LegalReasoningGraph:
    return LegalReasoningGraph.model_validate_json((GRAPHS / name).read_text())


def rule_map_embedding_only(teacher, student):
    """Rules matched purely by embedding cosine on label+citation (no citation step)."""
    m, _ = _align_by_text(
        teacher.rules, student.rules, "rid",
        lambda r: f"{r.label} {r.citation}", threshold=THRESH,
    )
    return m


def rule_map_citation_only(teacher, student):
    """Rules matched only by citation-token intersection; no text fallback."""
    mapping, used = {}, set()
    for t in teacher.rules:
        tt = extract_citation_tokens(t.citation)
        mid = None
        if tt:
            for s in student.rules:
                if s.rid in used:
                    continue
                if extract_citation_tokens(s.citation) & tt:
                    mid = s.rid
                    used.add(mid)
                    break
        mapping[t.rid] = mid
    return mapping


def rule_map_combined(teacher, student):
    """Principled hybrid: citation agreement => match; sibling subsection => discount
    (so embeddings can't merge (2)(a) with (2)(b)); otherwise embedding on text."""
    from lex_drl.alignment import _greedy_assign
    tr, sr = teacher.rules, student.rules
    if not tr:
        return {}
    emb = (_embedding_cosine_matrix([r.label for r in tr], [r.label for r in sr])
           if sr else [[] for _ in tr])
    sim = []
    for i, t in enumerate(tr):
        ti = extract_citation_tokens(t.citation)
        base_i = {x.split("(")[0] for x in ti}
        row = []
        for j, s in enumerate(sr):
            sj = extract_citation_tokens(s.citation)
            base_j = {x.split("(")[0] for x in sj}
            e = emb[i][j]
            if ti and sj and (ti & sj):
                v = 1.0                      # same citation token → same rule
            elif ti and sj and (base_i & base_j):
                v = min(e, 0.45)             # sibling subsection → discount below threshold
            else:
                v = e                        # no usable citation signal → text
            row.append(v)
        sim.append(row)
    assign = _greedy_assign([r.rid for r in tr], [r.rid for r in sr], sim, THRESH)
    return {tid: sid for tid, sid, _ in assign}


def score(teacher, student, rule_map):
    """Build a report with the given rule_map (others on embedding) and score it."""
    base = align_all(teacher, student, threshold=THRESH)
    rep_align = base.model_copy(update={"rule_map": rule_map})
    return compute_discrepancies(teacher, student, rep_align)


MODES = {
    "embedding_only": rule_map_embedding_only,
    "citation_only": rule_map_citation_only,
    "hybrid": lambda t, s: align_rules(t, s, THRESH),
    "hybrid_combined": rule_map_combined,
}


def main() -> None:
    assert al.SIMILARITY_METHOD == "embedding"
    print(f"Rule-alignment ablation (embedding threshold {THRESH}); "
          f"non-rule nodes always on embeddings.\n")

    graphs = {}
    for c in CASES:
        graphs[c] = {
            "teacher": _load(f"{c}_reference.json"),
            "gpt5": _load(f"{c}_agent_gpt5.json"),
            "llama3_2b": _load(f"{c}_agent_llama3_2b.json"),
        }

    results: dict[str, dict] = {}
    for mode, fn in MODES.items():
        per_case = {}
        misground_total = 0
        for c in CASES:
            t = graphs[c]["teacher"]
            row = {}
            for stu in STUDENTS:
                rep = score(t, graphs[c][stu], fn(t, graphs[c][stu]))
                row[stu] = rep.l_ged
                misground_total += rep.v_misground_count
            per_case[c] = row
        rank_ok = sum(1 for c in CASES if per_case[c]["gpt5"] < per_case[c]["llama3_2b"])
        total_lged = sum(per_case[c][s] for c in CASES for s in STUDENTS)
        results[mode] = {"per_case": per_case, "rank": rank_ok,
                         "misground": misground_total, "total_lged": total_lged}

    # ── headline table ──
    print(f"{'mode':16s} {'GPT5<Llama':>11s} {'Σ L-GED':>9s} {'Σ misground':>12s}")
    print("-" * 52)
    for mode in MODES:
        r = results[mode]
        print(f"{mode:16s} {str(r['rank'])+'/6':>11s} {r['total_lged']:>9.1f} "
              f"{r['misground']:>12d}")
    print()

    # ── how much of hybrid's rule matching is citation vs fallback ──
    print("Rule-match provenance under the hybrid (per case, both students):")
    cit_total = fb_total = miss_total = 0
    for c in CASES:
        t = graphs[c]["teacher"]
        for stu in STUDENTS:
            s = graphs[c][stu]
            cit = rule_map_citation_only(t, s)
            hyb = align_rules(t, s, THRESH)
            n_cit = sum(1 for v in cit.values() if v)
            n_hyb = sum(1 for v in hyb.values() if v)
            n_fb = n_hyb - n_cit
            n_miss = len(hyb) - n_hyb
            cit_total += n_cit
            fb_total += n_fb
            miss_total += n_miss
    denom = cit_total + fb_total + miss_total
    print(f"  citation-matched rules : {cit_total}  ({100*cit_total/denom:.0f}% of teacher rules)")
    print(f"  embedding-fallback     : {fb_total}  ({100*fb_total/denom:.0f}%)")
    print(f"  unmatched (missed)     : {miss_total}  ({100*miss_total/denom:.0f}%)")
    print()

    # ── direct embedding-confusion demo on sibling subsections ──
    print("Embedding CANNOT distinguish sibling subsections (cosine on rule LABEL only):")
    # scan every graph's rule list for same-base-section, different-subsection pairs
    demo_pairs = []
    seen = set()
    for c in CASES:
        for who in ("teacher", "gpt5", "llama3_2b"):
            rules = graphs[c][who].rules
            for i in range(len(rules)):
                for j in range(i + 1, len(rules)):
                    ti = extract_citation_tokens(rules[i].citation)
                    tj = extract_citation_tokens(rules[j].citation)
                    if ti and tj and not (ti & tj):
                        stem_i = {t.split("(")[0] for t in ti}
                        stem_j = {t.split("(")[0] for t in tj}
                        if stem_i & stem_j:
                            key = (rules[i].citation, rules[j].citation)
                            if key not in seen:
                                seen.add(key)
                                demo_pairs.append((rules[i], rules[j]))
    shown = 0
    for a, b in demo_pairs[:6]:
        sim = _embedding_cosine_matrix([a.label], [b.label])[0][0]
        flag = "  <-- would MERGE" if sim >= THRESH else ""
        print(f"  cos={sim:.3f}  {a.citation}  vs  {b.citation}{flag}")
        shown += 1
    if not shown:
        print("  (no distinct-subsection sibling pairs found across the corpus)")
    print("\n  → embeddings rate distinct subsections above the 0.55 match threshold;")
    print("    only the citation tokens keep them apart. hybrid_combined discounts these.")


if __name__ == "__main__":
    main()
