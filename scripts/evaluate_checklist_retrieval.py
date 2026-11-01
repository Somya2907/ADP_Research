"""C1, offline: which way of picking checklist items covers the most of a new case's gap?

No model is run. Items are mined from the 15 training cases' unpatched answers;
each ranking method picks k items for each of the 15 test cases, and the pick
is scored against that test case's real missing Rules/Obligations (the teacher
is used for scoring only). Methods:

    bm25         the Phase 5 retrieval (BM25 over patch keywords) — the baseline
    support      items most often missed across training cases first
    similarity   items whose label is closest to the case text first
    combined     similarity + support
    store_best   the best k items the store holds for this case (upper bound:
                 what perfect retrieval from the training knowledge could give)

Also a tier-transfer table: items mined from one tier's training cases, scored
on each tier's test cases.

Outputs results/c1/retrieval_eval.csv, transfer.csv, RETRIEVAL.md.

    poetry run python scripts/evaluate_checklist_retrieval.py
"""
from __future__ import annotations

import csv
import json
import os
import sys
from pathlib import Path
from statistics import mean

os.environ.setdefault("LEX_DRL_SIMILARITY", "embedding")
os.environ.setdefault("LEX_DRL_RULE_ALIGN", "combined")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import lex_drl.alignment as alignment_module  # noqa: E402
from lex_drl.cases import TIERS, load_all_cases  # noqa: E402
from lex_drl.checklist import (  # noqa: E402
    Cluster, Item, cluster, coverage, missed_items, rank, test_gaps,
)
from lex_drl.injection import training_party_names  # noqa: E402
from lex_drl.loop import LoopConfig, _retrieve, empty_graph, score  # noqa: E402
from lex_drl.patch_generator import canonical_citation  # noqa: E402
from lex_drl.patch_store import Patch, PatchStore  # noqa: E402
from lex_drl.schema import LegalReasoningGraph  # noqa: E402
from lex_drl.statute_index import load_statute_index  # noqa: E402

STUDENT = "llama3_2b"
GRAPHS = Path("data/outputs/graphs")
ROUND0 = Path("data/outputs/loop/full/round_0")
BM25_STORE = Path("results/loop/full/store_round_1.json")   # mined from the same round-0 answers
OUT = Path("results/c1")
KS = (3, 5, 10)
METHODS = ("bm25", "support", "similarity", "combined", "store_best")


def _embed(texts):
    return alignment_module._get_embed_model().encode(texts, normalize_embeddings=True,
                                                      show_progress_bar=False)


def _student(cid):
    p = ROUND0 / f"{cid}_agent_{STUDENT}.json"
    return LegalReasoningGraph.model_validate_json(p.read_text()) if p.exists() else empty_graph(cid)


def _bm25_clusters(store: PatchStore, case, k) -> list[Cluster]:
    """The Phase 5 retrieval, as clusters so it is scored the same way."""
    out = []
    for p in _retrieve(store, case, LoopConfig(k=k)):
        kind = "O" if p.patch_family == "missing_obligation" else "R"
        it = Item(kind=kind, citation=p.controlling_authority, jurisdiction=p.jurisdiction,
                  label=p.prevention_step, weight=0.0,
                  sections=canonical_citation(p.controlling_authority, p.jurisdiction),
                  source_case=(p.source_cases or [""])[0])
        out.append(Cluster(kind=kind, sections=it.sections, jurisdiction=p.jurisdiction, items=[it]))
    return out


def _store_best(clusters, gaps, k, embed) -> list[Cluster]:
    """Greedy: repeatedly add the cluster that fills the most remaining gap weight."""
    chosen: list[Cluster] = []
    for _ in range(k):
        base = coverage(chosen, gaps, len(chosen), embed=embed)["weight"] if chosen else 0.0
        best, gain = None, 0.0
        for c in clusters:
            if c in chosen:
                continue
            g = coverage(chosen + [c], gaps, len(chosen) + 1, embed=embed)["weight"] - base
            if g > gain:
                best, gain = c, g
        if best is None:
            break
        chosen.append(best)
    return chosen


def _pick(method, clusters, case, k, gaps, store, embed):
    if method == "bm25":
        return _bm25_clusters(store, case, k)
    if method == "store_best":
        return _store_best([c for c in rank(clusters, case, "support")], gaps, k, embed)
    return rank(clusters, case, method, embed=embed)[:k]


def main() -> None:
    if alignment_module.SIMILARITY_METHOD != "embedding":
        raise SystemExit("scorer must be embedding + combined")
    cases = load_all_cases()
    train = [c for c in cases if c.role == "training"]
    test = [c for c in cases if c.role == "test"]
    teachers = {c.case_id: LegalReasoningGraph.model_validate_json(
        (GRAPHS / f"{c.case_id}_reference.json").read_text()) for c in cases}
    index = load_statute_index()
    names = training_party_names()
    reports = {c.case_id: score(teachers[c.case_id], _student(c.case_id))[0] for c in cases}

    items = {c.case_id: missed_items(c, reports[c.case_id], teachers[c.case_id],
                                     index=index, party_names=names) for c in train}
    clusters = cluster(i for its in items.values() for i in its)
    gaps = {c.case_id: test_gaps(reports[c.case_id], teachers[c.case_id], index=index) for c in test}
    store = PatchStore()
    for p in json.loads(BM25_STORE.read_text()):
        store.add(Patch.model_validate(p))

    rows = []
    for c in test:
        for k in KS:
            for method in METHODS:
                picked = _pick(method, clusters, c, k, gaps[c.case_id], store, _embed)
                for strict in (True, False):
                    cov = coverage(picked, gaps[c.case_id], k, embed=_embed if strict else None)
                    rows.append({"case": c.case_id, "tier": c.tier, "k": k, "method": method,
                                 "match": "section+label" if strict else "section", **cov})
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "retrieval_eval.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)

    # tier transfer: items from one tier's training cases, k=10, combined ranking
    transfer = []
    for src in TIERS:
        src_clusters = cluster(i for c in train if c.tier == src for i in items[c.case_id])
        for dst in TIERS:
            for method in ("combined", "store_best"):
                covs = []
                for c in test:
                    if c.tier != dst:
                        continue
                    picked = _pick(method, src_clusters, c, 10, gaps[c.case_id], store, _embed)
                    covs.append(coverage(picked, gaps[c.case_id], 10, embed=_embed))
                transfer.append({"from": src, "to": dst, "method": method,
                                 "useful_per_case": round(mean(x["useful"] for x in covs), 2),
                                 "weight_per_case": round(mean(x["weight"] for x in covs), 2)})
    with (OUT / "transfer.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(transfer[0]))
        w.writeheader(); w.writerows(transfer)

    # summary
    gap_w = mean(sum(g.weight for g in gs) for gs in gaps.values())
    lines = ["# C1 — choosing checklist items without looking at the answer", "",
             f"Items: {sum(len(v) for v in items.values())} missed teacher Rules/Obligations from "
             f"{len(train)} training cases, grouped into {len(clusters)} clusters "
             f"(same kind of node + same statute section). Test cases: {len(test)}; their mean "
             f"missing R/O weight is {gap_w:.1f}.", "",
             "An item is **useful** if it is the same kind of node as a missing teacher node "
             "in the test case, cites the same section and has a similar label "
             "(embedding similarity ≥ 0.5). **Fillable weight** is the L-GED those useful items "
             "would remove if the student wrote them correctly.", "",
             "| Method | k | Useful items per case | Precision | Fillable L-GED per case | "
             "Useful (section match only) |", "|---|--:|--:|--:|--:|--:|"]
    for k in KS:
        for method in METHODS:
            s = [r for r in rows if r["k"] == k and r["method"] == method and r["match"] == "section+label"]
            l = [r for r in rows if r["k"] == k and r["method"] == method and r["match"] == "section"]
            given = sum(r["given"] for r in s)
            lines.append(f"| {method} | {k} | {mean(r['useful'] for r in s):.1f} | "
                         f"{100 * sum(r['useful'] for r in s) / given:.0f}% | "
                         f"{mean(r['weight'] for r in s):.1f} | {mean(r['useful'] for r in l):.1f} |"
                         if given else f"| {method} | {k} | 0 | – | 0 | 0 |")
    lines += ["", "## Tier transfer (k=10, section+label match)", "",
              "Fillable L-GED per test case when items come only from one tier's training cases.", "",
              "| Items from ↓ / test tier → | " + " | ".join(TIERS) + " |",
              "|---|" + "--:|" * len(TIERS)]
    for src in TIERS:
        cells = []
        for dst in TIERS:
            a = next(t for t in transfer if t["from"] == src and t["to"] == dst and t["method"] == "combined")
            b = next(t for t in transfer if t["from"] == src and t["to"] == dst and t["method"] == "store_best")
            cells.append(f"{a['weight_per_case']:.1f} (best {b['weight_per_case']:.1f})")
        lines.append(f"| {src} | " + " | ".join(cells) + " |")
    (OUT / "RETRIEVAL.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
