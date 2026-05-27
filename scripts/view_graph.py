"""Streamlit F-I-R-A-C-O graph viewer.

Launch:
    poetry run streamlit run scripts/view_graph.py
    poetry run streamlit run scripts/view_graph.py -- --graph data/outputs/graphs/E1_reference.json

Features:
  - Load a graph by path argument, sidebar picker, or file upload
  - Header with case_id, source, model_name, agent_id
  - Node-type bar chart (F/I/R/A/C/O totals)
  - Interactive node-link diagram colored by node type
  - Side-by-side comparison mode highlighting alignment-style diffs
  - Alignment method comparison: TF-IDF vs sentence-embedding results
  - Collapsible raw JSON

Requires: streamlit, streamlit-agraph (preferred) OR pyvis (fallback), pandas.
Install with: poetry add streamlit streamlit-agraph pandas
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))


# ── Project color scheme (per onboarding spec) ──
NODE_COLORS = {
    "F": "#2E86C1",   # Facts        — blue
    "I": "#16A085",   # Issues       — teal
    "R": "#7D3C98",   # Rules        — purple
    "A": "#C0392B",   # Application  — red
    "C": "#D4AC0D",   # Conclusion   — amber
    "O": "#229954",   # Obligations  — green
}
NODE_NAMES = {
    "F": "Facts", "I": "Issues", "R": "Rules",
    "A": "Application", "C": "Conclusion", "O": "Obligations",
}
NODE_FIELDS = ["facts", "issues", "rules", "applications", "conclusions", "obligations"]
ID_FIELDS = {
    "facts": "fid", "issues": "iid", "rules": "rid",
    "applications": "aid", "conclusions": "cid", "obligations": "oid",
}
LABEL_FIELDS = {
    "facts": "label", "issues": "label", "rules": "label",
    "applications": "reasoning", "conclusions": "determination", "obligations": "label",
}


def node_type_of(node_id: str) -> str:
    """Return F/I/R/A/C/O based on the leading capital letter of the ID."""
    if not node_id:
        return "?"
    return node_id[0].upper()


def collect_nodes(graph: dict) -> list[dict[str, Any]]:
    """Flatten all six node lists into a single list of {id, label, type, raw}."""
    out: list[dict[str, Any]] = []
    for field in NODE_FIELDS:
        id_key = ID_FIELDS[field]
        label_key = LABEL_FIELDS[field]
        for n in graph.get(field, []):
            nid = n.get(id_key, "")
            out.append({
                "id": nid,
                "type": node_type_of(nid),
                "label": str(n.get(label_key, "") or ""),
                "raw": n,
            })
    return out


def node_counts(graph: dict) -> dict[str, int]:
    return {label: len(graph.get(field, [])) for label, field in zip("FIRACO", NODE_FIELDS)}


# ── Renderers ──

def render_with_agraph(nodes: list[dict], edges: list[dict], highlights: set[str] | None = None):
    """Try streamlit-agraph; return True on success."""
    try:
        from streamlit_agraph import Config, Edge as AEdge, Node as ANode, agraph
    except ImportError:
        return False

    highlights = highlights or set()
    a_nodes = []
    for n in nodes:
        base_color = NODE_COLORS.get(n["type"], "#888")
        is_hi = n["id"] in highlights
        a_nodes.append(ANode(
            id=n["id"],
            label=f"{n['id']}: {n['label'][:40]}",
            size=22 if is_hi else 16,
            color={"background": base_color, "border": "#FF1744" if is_hi else "#222",
                   "highlight": {"background": base_color, "border": "#FF1744"}},
            shape="dot",
        ))
    a_edges = [
        AEdge(source=e["src"], target=e["dst"], label=e["type"], type="CURVE_SMOOTH")
        for e in edges
    ]
    config = Config(width=900, height=600, directed=True, physics=True, hierarchical=False)
    agraph(nodes=a_nodes, edges=a_edges, config=config)
    return True


def render_with_pyvis(nodes: list[dict], edges: list[dict], highlights: set[str] | None = None):
    """Fallback: pyvis-rendered HTML embedded via st.components."""
    try:
        from pyvis.network import Network
    except ImportError:
        st.error(
            "Neither `streamlit-agraph` nor `pyvis` is installed. "
            "Install one with: `poetry add streamlit-agraph` "
            "(or `poetry add pyvis`)."
        )
        return False

    highlights = highlights or set()
    net = Network(height="600px", width="100%", directed=True, notebook=False, cdn_resources="in_line")
    for n in nodes:
        color = NODE_COLORS.get(n["type"], "#888")
        net.add_node(
            n["id"],
            label=f"{n['id']}: {n['label'][:40]}",
            title=n["label"],
            color={"background": color, "border": "#FF1744" if n["id"] in highlights else "#222"},
            size=22 if n["id"] in highlights else 16,
        )
    for e in edges:
        if e["src"] in {n["id"] for n in nodes} and e["dst"] in {n["id"] for n in nodes}:
            net.add_edge(e["src"], e["dst"], label=e["type"])
    html = net.generate_html(notebook=False)
    import streamlit.components.v1 as components
    components.html(html, height=620, scrolling=True)
    return True


def render_graph(graph: dict, highlights: set[str] | None = None):
    nodes = collect_nodes(graph)
    edges = graph.get("edges", [])
    if render_with_agraph(nodes, edges, highlights):
        return
    render_with_pyvis(nodes, edges, highlights)


# ── Loading ──

def load_graph_file(path: Path) -> dict:
    return json.loads(Path(path).read_text())


def list_graph_files(graphs_dir: Path) -> list[Path]:
    if not graphs_dir.is_dir():
        return []
    return sorted(graphs_dir.glob("*.json"))


# ── Header / charts ──

def show_header(graph: dict, prefix: str = ""):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(f"{prefix}case_id", graph.get("case_id", "?"))
    c2.metric(f"{prefix}source", graph.get("source", "?"))
    c3.metric(f"{prefix}model", str(graph.get("model_name", "?"))[:24])
    c4.metric(f"{prefix}agent_id", str(graph.get("agent_id") or "—"))


def show_counts_chart(graph: dict, label: str = "Node types"):
    counts = node_counts(graph)
    df = pd.DataFrame({
        "Type": [f"{k} ({NODE_NAMES[k]})" for k in counts],
        "Count": list(counts.values()),
    })
    st.caption(label)
    st.bar_chart(df, x="Type", y="Count", color="#2E86C1")


# ── Alignment-method comparison helpers ──

TFIDF_SNAPSHOT_DIR = Path("data/snapshots/tfidf_v1")
EMBED_SNAPSHOT_DIR = Path("data/snapshots/embedding_v1")
TIER_FROM_PREFIX = {"E": "easy", "M": "medium", "H": "hard"}


def load_summary_csv(path: Path) -> pd.DataFrame | None:
    if not path.is_file():
        return None
    df = pd.read_csv(path)
    df["tier"] = df["case_id"].str[0].map(TIER_FROM_PREFIX).fillna("?")
    return df


def merge_methods(tfidf: pd.DataFrame, embed: pd.DataFrame) -> pd.DataFrame:
    """Wide-format join on (case_id, student) with one suffix per method."""
    return tfidf.merge(
        embed, on=["case_id", "student", "tier"],
        suffixes=("_tfidf", "_embed"),
    )


def ranking_per_case(df_method: pd.DataFrame) -> pd.DataFrame:
    """For each case, return GPT-5 L-GED, Qwen L-GED, and whether GPT-5 < Qwen."""
    pivot = df_method.pivot_table(
        index=["case_id", "tier"], columns="student", values="l_ged_score",
    ).reset_index()
    pivot["correct"] = pivot["gpt5"] < pivot["qwen3_4b"]
    return pivot


def render_method_comparison():
    st.header("Alignment method comparison")
    st.caption(
        "Compares the **TF-IDF baseline** against the **sentence-embedding** "
        "alignment under `BAAI/bge-small-en-v1.5`. The discrepancy scorer is "
        "identical; only the similarity backend changes."
    )

    tfidf_df = load_summary_csv(TFIDF_SNAPSHOT_DIR / "results" / "discrepancy_summary.csv")
    embed_df = load_summary_csv(EMBED_SNAPSHOT_DIR / "results" / "discrepancy_summary.csv")
    if tfidf_df is None or embed_df is None:
        st.error(
            "Snapshot CSVs not found. Expected:\n"
            f"- `{TFIDF_SNAPSHOT_DIR / 'results' / 'discrepancy_summary.csv'}`\n"
            f"- `{EMBED_SNAPSHOT_DIR / 'results' / 'discrepancy_summary.csv'}`"
        )
        return

    # ── Headline: ranking correctness ──
    tfidf_rank = ranking_per_case(tfidf_df)
    embed_rank = ranking_per_case(embed_df)
    tfidf_ok = int(tfidf_rank["correct"].sum())
    embed_ok = int(embed_rank["correct"].sum())
    total = len(tfidf_rank)

    c1, c2, c3 = st.columns(3)
    c1.metric("TF-IDF: GPT-5 < Qwen", f"{tfidf_ok}/{total}", help="Number of cases where GPT-5 L-GED is lower than Qwen.")
    c2.metric("Embedding: GPT-5 < Qwen", f"{embed_ok}/{total}", delta=embed_ok - tfidf_ok)
    c3.metric("Ranking improvement", f"+{embed_ok - tfidf_ok}", help="Cases flipped from incorrect to correct.")

    # ── Side-by-side L-GED table ──
    st.subheader("L-GED side-by-side")
    merged = merge_methods(tfidf_df, embed_df)
    merged_view = merged[[
        "case_id", "tier", "student",
        "l_ged_score_tfidf", "l_ged_score_embed",
    ]].copy()
    merged_view["Δ (embed − tfidf)"] = (
        merged_view["l_ged_score_embed"] - merged_view["l_ged_score_tfidf"]
    ).round(2)
    merged_view = merged_view.rename(columns={
        "case_id": "Case", "tier": "Tier", "student": "Student",
        "l_ged_score_tfidf": "L-GED (TF-IDF)",
        "l_ged_score_embed": "L-GED (embed)",
    }).sort_values(["Case", "Student"])
    st.dataframe(merged_view, use_container_width=True, hide_index=True)

    # ── Ranking grid ──
    st.subheader("Per-case ranking correctness")
    rank_view = tfidf_rank.merge(
        embed_rank, on=["case_id", "tier"], suffixes=("_tfidf", "_embed"),
    )
    rank_view["TF-IDF ✓"] = rank_view["correct_tfidf"].map({True: "✓", False: "✗"})
    rank_view["Embed ✓"] = rank_view["correct_embed"].map({True: "✓", False: "✗"})
    rank_view = rank_view.rename(columns={
        "case_id": "Case", "tier": "Tier",
        "gpt5_tfidf": "GPT-5 (tfidf)", "qwen3_4b_tfidf": "Qwen (tfidf)",
        "gpt5_embed": "GPT-5 (embed)", "qwen3_4b_embed": "Qwen (embed)",
    })[["Case", "Tier",
        "GPT-5 (tfidf)", "Qwen (tfidf)", "TF-IDF ✓",
        "GPT-5 (embed)", "Qwen (embed)", "Embed ✓"]]
    st.dataframe(rank_view, use_container_width=True, hide_index=True)

    # ── L-GED bar chart ──
    st.subheader("L-GED per case, grouped by method × student")
    long = pd.concat([
        tfidf_df.assign(method="TF-IDF"),
        embed_df.assign(method="Embedding"),
    ], ignore_index=True)
    long["series"] = long["student"] + " — " + long["method"]
    chart_df = long.pivot_table(
        index="case_id", columns="series", values="l_ged_score",
    ).reset_index().sort_values("case_id")
    st.bar_chart(chart_df, x="case_id", y=[c for c in chart_df.columns if c != "case_id"])

    # ── Component breakdown (v_miss / v_halluc / e_diff) ──
    st.subheader("Component breakdown")
    comp_tabs = st.tabs(["v_miss", "v_halluc", "e_diff"])
    for tab, col in zip(comp_tabs, ["v_miss_count", "v_halluc_count", "e_diff_count"]):
        with tab:
            comp = merged[["case_id", "tier", "student", f"{col}_tfidf", f"{col}_embed"]].copy()
            comp["Δ"] = comp[f"{col}_embed"] - comp[f"{col}_tfidf"]
            comp = comp.rename(columns={
                "case_id": "Case", "tier": "Tier", "student": "Student",
                f"{col}_tfidf": f"{col} (tfidf)",
                f"{col}_embed": f"{col} (embed)",
            }).sort_values(["Case", "Student"])
            st.dataframe(comp, use_container_width=True, hide_index=True)

    # ── Method explainer ──
    with st.expander("Why embedding wins"):
        st.markdown(
            "- **TF-IDF** scores paraphrases like *\"based in Austin\"* vs *\"operates "
            "out of Austin\"* near zero because the n-grams don't overlap, so GPT-5's "
            "verbose paraphrases are counted as hallucinations (`v_halluc` inflated).\n"
            "- **Sentence embeddings** assign such paraphrases ≈0.95 cosine — they align "
            "as the same node, so `v_halluc` drops and GPT-5 (a more capable, more "
            "verbose model) finally scores below Qwen.\n"
            "- Toggle at runtime via `LEX_DRL_SIMILARITY=embedding|tfidf` before running "
            "`scripts/run_discrepancy_analysis.py`."
        )


# ── Comparison helpers ──

def compute_diff_highlights(g1: dict, g2: dict) -> tuple[set[str], set[str]]:
    """Naive label-based alignment for visual highlighting.

    For each node in g1, find a node in g2 with the same node-type and an
    identical lowercased label. Nodes without a match are 'differences'.
    This is a viewer aid, not the real alignment algorithm — that lives in
    src/lex_drl/alignment.py.
    """
    def index(graph):
        idx: dict[tuple[str, str], str] = {}
        for n in collect_nodes(graph):
            idx[(n["type"], n["label"].strip().lower())] = n["id"]
        return idx

    idx1, idx2 = index(g1), index(g2)
    keys1, keys2 = set(idx1), set(idx2)
    only1 = {idx1[k] for k in keys1 - keys2}
    only2 = {idx2[k] for k in keys2 - keys1}
    return only1, only2


# ── Main app ──

def parse_cli_args() -> argparse.Namespace:
    # Streamlit forwards args after `--`. argparse needs them isolated.
    if "--" in sys.argv:
        argv = sys.argv[sys.argv.index("--") + 1:]
    else:
        argv = []
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("--graph", default=None)
    p.add_argument("--graphs-dir", default="data/outputs/graphs")
    args, _ = p.parse_known_args(argv)
    return args


def pick_graph(label: str, graph_files: list[Path], default_idx: int = 0,
               key_prefix: str = "") -> dict | None:
    """Render selectbox + optional uploader. Returns the parsed graph or None."""
    options = ["(upload)"] + [p.name for p in graph_files]
    idx = min(default_idx + 1, len(options) - 1) if graph_files else 0
    choice = st.selectbox(label, options, index=idx, key=f"{key_prefix}_choice")
    if choice == "(upload)":
        uploaded = st.file_uploader(f"Upload {label}", type=["json"], key=f"{key_prefix}_upload")
        if uploaded:
            return json.loads(uploaded.getvalue())
        return None
    return load_graph_file(graph_files[options.index(choice) - 1])


def main():
    st.set_page_config(page_title="F-I-R-A-C-O Graph Viewer", layout="wide")
    st.title("F-I-R-A-C-O Graph Viewer")

    args = parse_cli_args()
    graphs_dir = Path(args.graphs_dir)
    graph_files = list_graph_files(graphs_dir)

    with st.sidebar:
        st.header("Mode")
        mode = st.radio(
            "View",
            ["Single graph", "Side-by-side comparison", "Alignment method comparison"],
            index=0,
        )
        st.caption(f"Graphs dir: `{graphs_dir}` ({len(graph_files)} files)")
        st.markdown("**Legend**")
        for k in "FIRACO":
            st.markdown(
                f"<span style='display:inline-block;width:12px;height:12px;"
                f"background:{NODE_COLORS[k]};margin-right:6px;border-radius:2px;'></span>"
                f"{k} — {NODE_NAMES[k]}",
                unsafe_allow_html=True,
            )

    if mode == "Alignment method comparison":
        render_method_comparison()
        return

    if mode == "Single graph":
        if args.graph:
            graph = load_graph_file(Path(args.graph))
            st.caption(f"Loaded from CLI: `{args.graph}`")
        else:
            graph = pick_graph("Graph file", graph_files, key_prefix="single")
        if not graph:
            st.info("Pick or upload a graph to begin.")
            return

        show_header(graph)
        st.divider()
        left, right = st.columns([1, 2])
        with left:
            show_counts_chart(graph)
            st.metric("Edges", len(graph.get("edges", [])))
        with right:
            st.caption("Reasoning graph")
            render_graph(graph)

        with st.expander("Raw JSON"):
            st.json(graph)

    else:  # side-by-side
        st.caption("Compare two graphs — usually teacher vs student for the same case.")
        col_a, col_b = st.columns(2)
        with col_a:
            ga = pick_graph("Graph A (e.g. teacher)", graph_files, default_idx=0, key_prefix="cmp_a")
        with col_b:
            gb_default_idx = 1 if len(graph_files) > 1 else 0
            gb = pick_graph("Graph B (e.g. student)", graph_files, default_idx=gb_default_idx,
                            key_prefix="cmp_b")

        if not ga or not gb:
            st.info("Pick or upload both graphs to compare.")
            return

        only_a, only_b = compute_diff_highlights(ga, gb)

        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("Graph A")
            show_header(ga, prefix="A · ")
            show_counts_chart(ga, label="A · Node types")
            st.caption(f"Highlighted (no match in B): {len(only_a)}")
            render_graph(ga, highlights=only_a)
        with col_b:
            st.subheader("Graph B")
            show_header(gb, prefix="B · ")
            show_counts_chart(gb, label="B · Node types")
            st.caption(f"Highlighted (no match in A): {len(only_b)}")
            render_graph(gb, highlights=only_b)

        with st.expander("Diff summary"):
            cnts_a = node_counts(ga)
            cnts_b = node_counts(gb)
            df = pd.DataFrame(OrderedDict([
                ("Type", list(cnts_a.keys())),
                ("A count", list(cnts_a.values())),
                ("B count", list(cnts_b.values())),
                ("Δ (B−A)", [cnts_b[k] - cnts_a[k] for k in cnts_a]),
            ]))
            st.dataframe(df, use_container_width=True)

        with st.expander("Raw JSON (A | B)"):
            tab_a, tab_b = st.tabs(["A", "B"])
            with tab_a:
                st.json(ga)
            with tab_b:
                st.json(gb)


if __name__ == "__main__":
    main()
