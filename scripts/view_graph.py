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


def node_label_index(graph: dict) -> dict[str, str]:
    """{node_id: label} across all six node types, for resolving edge endpoints."""
    return {n["id"]: n["label"] for n in collect_nodes(graph)}


def _derive_edge_justification(edge: dict, apps_by_id: dict, obls_by_id: dict) -> str | None:
    """Fall back to related node's text when an edge has no own justification.

    Many models (e.g. Qwen) leave ``edge.justification`` null but still populate
    ``application.reasoning`` and ``obligation.label``. This walks the canonical
    edge-type → adjacent-node-field mapping to surface that text, tagged so the
    reader knows it isn't the edge's own justification.
    """
    src, dst = edge.get("src", ""), edge.get("dst", "")
    etype = edge.get("type", "")

    # Edges pointing into an application — the app's reasoning explains it.
    if dst in apps_by_id and etype in {"applies-to", "supports", "contradicts"}:
        r = apps_by_id[dst].get("reasoning")
        if r:
            return f"*(from {dst}'s reasoning)* {r}"

    # Edges out of an application into a conclusion — app reasoning + result.
    if src in apps_by_id and etype in {"satisfies-element", "fails-element", "supports"}:
        a = apps_by_id[src]
        r = a.get("reasoning")
        result = a.get("result", "")
        if r:
            return f"*(from {src} — result={result})* {r}"

    if etype == "triggers":
        # F → I: find an application that subsumes this (fact, issue) pair.
        for aid, a in apps_by_id.items():
            if src in (a.get("fact_refs") or []) and a.get("issue_ref") == dst:
                r = a.get("reasoning")
                if r:
                    return f"*(from {aid} which subsumes {src} under {dst})* {r}"
        # R → O: use the obligation's own label.
        if dst in obls_by_id:
            o = obls_by_id[dst]
            label = o.get("label", "")
            if label:
                return f"*(from obligation {dst})* {label}"

    return None


def build_edge_table(graph: dict) -> pd.DataFrame:
    """One row per edge with src/dst node labels and the LLM's justification.

    When the edge has no ``justification`` of its own, fall back to the
    reasoning carried on adjacent nodes (application.reasoning,
    obligation.label) so the column is informative even for terse models.
    """
    labels = node_label_index(graph)
    apps_by_id = {a.get("aid", ""): a for a in graph.get("applications", [])}
    obls_by_id = {o.get("oid", ""): o for o in graph.get("obligations", [])}
    rows = []
    for e in graph.get("edges", []):
        src, dst = e.get("src", ""), e.get("dst", "")
        justification = e.get("justification")
        if not justification:
            justification = _derive_edge_justification(e, apps_by_id, obls_by_id) or "—"
        rows.append({
            "Edge": e.get("eid", ""),
            "Source": f"{src} — {labels.get(src, '(missing)')[:60]}",
            "Type": e.get("type", ""),
            "Target": f"{dst} — {labels.get(dst, '(missing)')[:60]}",
            "Justification": justification,
        })
    return pd.DataFrame(rows)


def build_application_traces(graph: dict) -> list[dict]:
    """One trace per application: rule + facts + issue + result + reasoning."""
    labels = node_label_index(graph)
    traces = []
    for a in graph.get("applications", []):
        rule_id = a.get("rule_ref", "")
        issue_id = a.get("issue_ref", "")
        fact_ids = a.get("fact_refs", []) or []
        traces.append({
            "aid": a.get("aid", ""),
            "rule": f"{rule_id}: {labels.get(rule_id, '(missing)')}",
            "facts": [f"{fid}: {labels.get(fid, '(missing)')}" for fid in fact_ids],
            "issue": f"{issue_id}: {labels.get(issue_id, '(missing)')}",
            "result": a.get("result", ""),
            "reasoning": a.get("reasoning", "") or "",
        })
    return traces


ANALYSIS_DIR = Path("data/outputs/analysis")


def raw_response_path(graph: dict) -> Path:
    """Derive the analysis file path from a graph's source/agent_id metadata."""
    case_id = graph.get("case_id", "")
    if graph.get("source") == "reference":
        label = "reference"
    else:
        label = f"agent_{graph.get('agent_id', 'unknown')}"
    return ANALYSIS_DIR / f"{case_id}_{label}_raw.txt"


def load_raw_response(graph: dict) -> tuple[str | None, str | None]:
    """Return (prose, json_text) from the saved LLM response.

    Splits on the "=== JSON GRAPH ===" marker. If the marker is absent (agent
    prompt strictly emitted JSON), prose is None.
    """
    path = raw_response_path(graph)
    if not path.is_file():
        return None, None
    text = path.read_text(encoding="utf-8")
    marker = "=== JSON GRAPH ==="
    if marker in text:
        prose, json_text = text.split(marker, 1)
        # Some models wrap the marker (e.g. **=== JSON GRAPH ===**), leaving
        # trailing markdown chars before the actual JSON. Drop everything
        # before the first '{' so the JSON block is clean.
        json_text = json_text.lstrip()
        brace = json_text.find("{")
        if brace > 0:
            json_text = json_text[brace:]
        return prose.strip() or None, json_text.strip() or None
    # No marker: try to detect prose-only (no JSON block) vs JSON-only output.
    stripped = text.strip()
    if stripped.startswith("{"):
        return None, stripped
    return stripped, None


def _edges_by_target(graph: dict) -> dict[str, list[dict]]:
    """Group edges by their destination node id."""
    by_target: dict[str, list[dict]] = {}
    for e in graph.get("edges", []):
        by_target.setdefault(e.get("dst", ""), []).append(e)
    return by_target


def _format_inbound_edges(node_id: str, edges_by_target: dict[str, list[dict]]) -> list[str]:
    """Render inbound edges with justifications as Markdown sub-bullets.

    Skips edges whose ``justification`` is empty. For applications, the
    ``reasoning`` field carries the why-connected information already, so an
    edge without its own justification is structural noise and we drop it.
    """
    inbound = [e for e in edges_by_target.get(node_id, []) if e.get("justification")]
    if not inbound:
        return []
    lines = ["    - *Why connected:*"]
    for e in inbound:
        src = e.get("src", "?")
        etype = e.get("type", "?")
        lines.append(
            f"        - **{src}** →[*{etype}*]→ **{node_id}**: {e['justification']}"
        )
    return lines


def synthesize_narrative(graph: dict) -> str:
    """Build a prose-style F-I-R-A-C-O narrative from the structured JSON.

    Used when the LLM emitted JSON only (no PART 1 prose). Walks each section
    in canonical order, folds the structured fields into readable Markdown,
    and attaches every node's inbound edges (with their justifications) so the
    reader sees *why* each component connects to its neighbours.
    """
    labels = node_label_index(graph)
    edges_in = _edges_by_target(graph)
    parts: list[str] = []

    facts = graph.get("facts", [])
    if facts:
        parts.append("**F — Facts**")
        parts.append("*(Source nodes — facts don't have inbound edges in the canonical flow.)*")
        for f in facts:
            polarity = f.get("polarity") or "present"
            tag = "" if polarity == "present" else f" *({polarity})*"
            parts.append(f"- **{f.get('fid', '')}**{tag}: {f.get('label', '')}")
        parts.append("")

    issues = graph.get("issues", [])
    if issues:
        parts.append("**I — Issues**")
        for i in issues:
            iid = i.get("iid", "")
            status = i.get("status") or ""
            tag = f" *({status})*" if status else ""
            parts.append(f"- **{iid}**{tag}: {i.get('label', '')}")
            parts.extend(_format_inbound_edges(iid, edges_in))
        parts.append("")

    rules = graph.get("rules", [])
    if rules:
        parts.append("**R — Rules**")
        for r in rules:
            rid = r.get("rid", "")
            authority = r.get("authority") or ""
            jurisdiction = r.get("jurisdiction") or ""
            meta = ", ".join(x for x in [authority, jurisdiction] if x)
            citation = r.get("citation") or ""
            parts.append(
                f"- **{rid}** ({meta}) — *{citation}*: {r.get('label', '')}"
            )
            parts.extend(_format_inbound_edges(rid, edges_in))
        parts.append("")

    apps = graph.get("applications", [])
    if apps:
        parts.append("**A — Application**")
        for a in apps:
            aid = a.get("aid", "")
            rule_id = a.get("rule_ref", "")
            issue_id = a.get("issue_ref", "")
            fact_ids = a.get("fact_refs", []) or []
            facts_inline = ", ".join(fact_ids) if fact_ids else "(no facts cited)"
            result = a.get("result", "")
            parts.append(
                f"- **{aid}** [*{result}*]: "
                f"Rule **{rule_id}** ({labels.get(rule_id, '?')[:60]}) "
                f"applied to facts **{facts_inline}** "
                f"for issue **{issue_id}** ({labels.get(issue_id, '?')[:60]})"
            )
            reasoning = a.get("reasoning") or ""
            if reasoning:
                parts.append(f"    - *Reasoning:* {reasoning}")
            parts.extend(_format_inbound_edges(aid, edges_in))
        parts.append("")

    concs = graph.get("conclusions", [])
    if concs:
        parts.append("**C — Conclusions**")
        for c in concs:
            cid = c.get("cid", "")
            det = c.get("determination", "")
            conf = c.get("confidence", "")
            support = ", ".join(c.get("support_refs", []) or []) or "(no support refs)"
            parts.append(
                f"- **{cid}** — *{det}* (confidence: {conf}); "
                f"supported by {support}"
            )
            parts.extend(_format_inbound_edges(cid, edges_in))
        parts.append("")

    obls = graph.get("obligations", [])
    if obls:
        parts.append("**O — Obligations**")
        for o in obls:
            oid = o.get("oid", "")
            jurisdiction = o.get("jurisdiction") or ""
            status = o.get("status") or ""
            deadline = o.get("deadline") or ""
            meta = ", ".join(x for x in [status, jurisdiction, deadline] if x)
            required_by = o.get("required_by") or ""
            parts.append(
                f"- **{oid}** ({meta}) — {o.get('label', '')}"
                + (f" *(required by {required_by})*" if required_by else "")
            )
            parts.extend(_format_inbound_edges(oid, edges_in))

    return "\n".join(parts)


def render_generation_reasoning(graph: dict):
    """Show the LLM's own prose narrative that produced this graph."""
    st.subheader("Generation reasoning")
    st.caption(
        "The LLM's prose write-up that produced this graph — its actual "
        "thought process before emitting the JSON."
    )

    path = raw_response_path(graph)
    prose, json_text = load_raw_response(graph)

    if prose:
        tab_prose, tab_synth = st.tabs(["LLM prose (as emitted)", "Reconstructed narrative (from JSON)"])
        with tab_prose:
            st.caption(f"Source: `{path}` (LLM-emitted prose)")
            with st.container(height=500, border=True):
                st.markdown(prose)
        with tab_synth:
            st.caption(
                "Walks the JSON in F-I-R-A-C-O order and inlines each node's "
                "incoming edge justifications."
            )
            with st.container(height=500, border=True):
                st.markdown(synthesize_narrative(graph))
        with st.expander(f"Raw JSON (PART 2 only) — `{path}`"):
            if json_text:
                st.code(json_text, language="json")
            else:
                st.info("No JSON block found after the marker in this raw file.")
    elif path.is_file():
        agent_id = graph.get("agent_id")
        st.caption(
            f"`{agent_id}` emitted JSON only (per "
            f"[configs/prompts/agent_firaco.txt:99](configs/prompts/agent_firaco.txt#L99)). "
            f"Reconstructed F-I-R-A-C-O narrative below from the structured fields."
        )
        with st.container(height=500, border=True):
            st.markdown(synthesize_narrative(graph))
        with st.expander(f"Raw response (JSON only) — `{path}`"):
            st.code(path.read_text(encoding="utf-8"), language="json")
    else:
        st.warning(f"Raw response file not found: `{path}`")


def render_reasoning_panel(graph: dict):
    """Show why nodes are connected: edge justifications + application traces."""
    edges = graph.get("edges", [])
    apps = graph.get("applications", [])

    st.subheader("Reasoning trace")
    st.caption(
        "Why these nodes are connected. Edge **justifications** explain each "
        "individual link; **application traces** show the rule-to-facts "
        "subsumption that drives each conclusion."
    )

    apps_by_id = {a.get("aid", ""): a for a in graph.get("applications", [])}
    obls_by_id = {o.get("oid", ""): o for o in graph.get("obligations", [])}
    edge_count = len(edges)
    edges_with_own = sum(1 for e in edges if e.get("justification"))
    edges_derived = sum(
        1 for e in edges
        if not e.get("justification")
        and _derive_edge_justification(e, apps_by_id, obls_by_id)
    )
    edges_unknown = edge_count - edges_with_own - edges_derived

    c1, c2, c3 = st.columns(3)
    c1.metric("Edges", edge_count)
    c2.metric("With own justification", edges_with_own,
              help="The LLM populated edge.justification directly.")
    c3.metric("Derived from adjacent nodes", edges_derived,
              help="Edge.justification was null but text was reconstructed "
                   "from application.reasoning or obligation.label.")
    if edges_unknown:
        st.caption(f"⚠ {edges_unknown} edge(s) have neither own nor derivable justification.")

    with st.expander(f"Edge justifications ({edge_count})", expanded=True):
        if not edges:
            st.info("No edges in this graph.")
        else:
            st.dataframe(build_edge_table(graph), use_container_width=True, hide_index=True)

    with st.expander(f"Application traces ({len(apps)})", expanded=False):
        if not apps:
            st.info("No applications in this graph.")
        else:
            for trace in build_application_traces(graph):
                result_color = {
                    "satisfied": "#229954", "violated": "#C0392B",
                    "partial": "#D4AC0D", "requires-fact": "#7D3C98",
                }.get(trace["result"], "#888")
                st.markdown(
                    f"**{trace['aid']}** — "
                    f"<span style='color:{result_color};font-weight:600;'>"
                    f"{trace['result']}</span>",
                    unsafe_allow_html=True,
                )
                st.markdown(f"- **Rule applied:** {trace['rule']}")
                st.markdown(f"- **Issue:** {trace['issue']}")
                if trace["facts"]:
                    st.markdown("- **Facts:**")
                    for fact in trace["facts"]:
                        st.markdown(f"    - {fact}")
                if trace["reasoning"]:
                    st.markdown(f"- **Reasoning:** {trace['reasoning']}")
                st.divider()


# ── Renderers ──

NODE_LAYER = {"F": 0, "I": 1, "R": 2, "A": 3, "C": 4, "O": 5}


def render_with_plotly(nodes: list[dict], edges: list[dict], highlights: set[str] | None = None):
    """Layered Plotly+NetworkX graph: F → I → R → A → C → O top-to-bottom."""
    try:
        import networkx as nx
        import plotly.graph_objects as go
    except ImportError:
        return False

    highlights = highlights or set()
    valid_ids = {n["id"] for n in nodes}

    g = nx.DiGraph()
    for n in nodes:
        g.add_node(n["id"], **n, layer=NODE_LAYER.get(n["type"], 6))
    for e in edges:
        if e.get("src") in valid_ids and e.get("dst") in valid_ids:
            g.add_edge(e["src"], e["dst"], **e)

    if not g.nodes:
        return False

    pos = nx.multipartite_layout(g, subset_key="layer", align="horizontal")
    pos = {n: (p[0], -p[1]) for n, p in pos.items()}

    edge_x: list[float | None] = []
    edge_y: list[float | None] = []
    for src, dst in g.edges():
        x0, y0 = pos[src]
        x1, y1 = pos[dst]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    traces = [go.Scatter(
        x=edge_x, y=edge_y, mode="lines",
        line=dict(width=1, color="rgba(140,140,140,0.35)"),
        hoverinfo="none", showlegend=False,
    )]

    for t, color in NODE_COLORS.items():
        ids = [nid for nid, data in g.nodes(data=True) if data.get("type") == t]
        if not ids:
            continue
        xs, ys, texts, hovers, sizes, borders, border_widths = [], [], [], [], [], [], []
        for nid in ids:
            x, y = pos[nid]
            xs.append(x); ys.append(y)
            data = g.nodes[nid]
            full = data.get("label", "") or ""
            texts.append(nid)
            hovers.append(f"<b>{nid}</b> ({NODE_NAMES.get(t, t)})<br>{full[:200]}")
            is_hi = nid in highlights
            sizes.append(46 if is_hi else 36)
            borders.append("#FF1744" if is_hi else "rgba(30,30,30,0.65)")
            border_widths.append(3 if is_hi else 1.5)
        traces.append(go.Scatter(
            x=xs, y=ys, text=texts, hovertext=hovers, hoverinfo="text",
            mode="markers+text", name=f"{t} — {NODE_NAMES[t]}",
            marker=dict(
                color=color, size=sizes, opacity=0.95,
                line=dict(color=borders, width=border_widths),
            ),
            textposition="middle center",
            textfont=dict(size=11, color="white", family="Arial Black"),
        ))

    annotations = []
    for src, dst in g.edges():
        x0, y0 = pos[src]
        x1, y1 = pos[dst]
        annotations.append(dict(
            ax=x0, ay=y0, x=x1, y=y1,
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=1.1,
            arrowcolor="rgba(100,100,100,0.55)",
            standoff=20,
        ))

    # Layer band labels on the left margin
    layer_xs = [p[0] for p in pos.values()]
    left_x = (min(layer_xs) - 0.1) if layer_xs else 0
    for t in "FIRACO":
        ys_in_layer = [p[1] for nid, p in pos.items()
                       if g.nodes[nid].get("type") == t]
        if ys_in_layer:
            annotations.append(dict(
                x=left_x, y=sum(ys_in_layer) / len(ys_in_layer),
                xref="x", yref="y", showarrow=False,
                text=f"<b>{t}</b>",
                font=dict(size=20, color=NODE_COLORS[t]),
                xanchor="right",
            ))

    fig = go.Figure(data=traces, layout=go.Layout(
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    xanchor="center", x=0.5),
        hovermode="closest",
        margin=dict(b=20, l=40, r=10, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        paper_bgcolor="white",
        plot_bgcolor="rgba(247,249,252,1)",
        annotations=annotations,
        height=680,
    ))

    st.plotly_chart(fig, use_container_width=True)
    return True


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
    if render_with_plotly(nodes, edges, highlights):
        return
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

        st.divider()
        render_generation_reasoning(graph)

        st.divider()
        render_reasoning_panel(graph)

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

        st.divider()
        st.subheader("Generation reasoning — side by side")
        col_a, col_b = st.columns(2)
        with col_a:
            render_generation_reasoning(ga)
        with col_b:
            render_generation_reasoning(gb)

        st.divider()
        st.subheader("Reasoning trace — side by side")
        col_a, col_b = st.columns(2)
        with col_a:
            render_reasoning_panel(ga)
        with col_b:
            render_reasoning_panel(gb)

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
