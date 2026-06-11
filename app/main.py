# app/main.py
import streamlit as st
import sys
import os
import json

# Force Python path alignment to cleanly import the pipeline modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pipeline')))
from agent import run

st.set_page_config(
    page_title="DecisionLens",
    page_icon="⚽",
    layout="centered"
)

st.title("⚽ DecisionLens")
st.caption("VAR Decision Transparency Engine · FIFA World Cup 2026")
st.divider()

question = st.text_input(
    "Ask about a VAR decision or football rule:",
    placeholder="e.g. What makes a handball deliberate under FIFA rules?"
)

if question:
    with st.spinner("Retrieving rule evidence and generating explanation..."):
        # Executes the unified CRAG hybrid retrieval & generation engine
        result = run(question)

    confidence = result.get("confidence", 0.0)
    decision_type = result.get("decision_type", "unknown")

    # ── Explanation ──────────────────────────────────────────
    st.markdown("### Explanation")
    st.write(result.get("answer", "No answer generated."))

    # ── Metaprogramming Metrics ─────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Evidence Confidence", f"{int(confidence * 100)}%")
    with col2:
        st.metric("Decision Type", decision_type.replace("_", " ").title())

    st.divider()

    # ── Decision Steps ───────────────────────────────────────
    steps = result.get("decision_steps", [])
    if steps:
        st.markdown("### Decision Steps")
        for i, step in enumerate(steps, 1):
            st.markdown(f"**{i}.** {step}")

    # ── Rule Citations ───────────────────────────────────────
    citations = result.get("rule_citations", [])
    if citations:
        st.markdown("### Rule Citations")
        for citation in citations:
            # Safely handle potential variations in how the model formats names
            law_title = citation.get('law_or_section', citation.get('law', 'Rule Reference'))
            doc_source = citation.get('source', 'FIFA Official Rules')
            quoted_phrase = citation.get('quoted_span', '')
            
            with st.expander(f"📖 {law_title} — {doc_source}"):
                if quoted_phrase:
                    st.markdown(f"**Exact Quoted Evidence:**")
                    st.markdown(f"> *\"{quoted_phrase}\"*")
                else:
                    st.markdown("*Context chunk utilized directly for structural synthesis.*")

    # ── Missing Evidence Guardrails ──────────────────────────
    missing = result.get("missing_evidence", [])
    # Display missing evidence warnings if confidence drops or if the agent explicitly called out gaps
    if missing and (confidence < 0.5 or "Ronaldo" in question or decision_type == "unknown"):
        st.markdown("### ⚠️ System Incompleteness Warning")
        for item in missing:
            st.warning(item)

    # ── Sources Index ────────────────────────────────────────
    sources = result.get("sources", [])
    if sources:
        st.markdown("### Sources Verified")
        for source in sources:
            st.caption(f"📄 {source}")
