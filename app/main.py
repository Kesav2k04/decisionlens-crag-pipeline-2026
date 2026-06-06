# app/main.py — Day 2 Skeleton with Custom Template Styles
import streamlit as st
import sys
import os

# Dynamically append the pipeline directory path relative to this file
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "pipeline"))
)

# Configure parent layout container
st.set_page_config(
    page_title="DecisionLens | VAR Transparency", page_icon="⚽", layout="wide"
)

# Inject Custom CSS Styling Blocks directly into the Streamlit app context
st.markdown(
    """
<style>
    /* Scope out default Streamlit framing margins */
    .block-container { padding-top: 2rem; max-width: 1000px; }
    
    :root {
      --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      --color-background-primary: #ffffff;
      --color-background-secondary: #f8f9fa;
      --color-background-info: #e7f3ff;
      --color-background-success: #e6f6f2;
      --color-background-warning: #fff8e6;
      --color-text-primary: #111827;
      --color-text-secondary: #4b5563;
      --color-text-tertiary: #6b7280;
      --color-text-info: #0d4a8a;
      --color-text-success: #0a4d3c;
      --color-text-warning: #925c0e;
      --color-border-secondary: #e5e7eb;
      --color-border-tertiary: #f3f4f6;
      --border-radius-md: 8px;
      --border-radius-lg: 12px;
    }

    /* ---- LANDING HERO ---- */
    .hero { padding: 24px 0px 32px 0px; border-bottom: 0.5px solid var(--color-border-secondary); }
    .badge { display: inline-flex; align-items: center; gap: 6px; background: var(--color-background-info); color: var(--color-text-info); font-size: 11px; font-weight: 500; padding: 4px 10px; border-radius: 20px; margin-bottom: 14px; letter-spacing: .4px; }
    .hero h1 { font-size: 34px; font-weight: 500; line-height: 1.2; margin-bottom: 12px; color: var(--color-text-primary); }
    .hero h1 span { color: #3B8BD4; }
    .hero p { font-size: 15px; color: var(--color-text-secondary); max-width: 580px; line-height: 1.7; }

    /* ---- ARCHITECTURE STRIP ---- */
    .arch-strip { padding: 20px 0px; border-bottom: 0.5px solid var(--color-border-secondary); margin-bottom: 24px; }
    .arch-label { font-size: 11px; font-weight: 500; color: var(--color-text-tertiary); letter-spacing: .6px; margin-bottom: 12px; text-transform: uppercase; }
    .arch-flow { display: flex; align-items: center; gap: 8px; overflow-x: auto; }
    .arch-step { display: flex; flex-direction: column; align-items: center; padding: 10px 12px; border: 0.5px solid var(--color-border-tertiary); border-radius: var(--border-radius-md); background: var(--color-background-secondary); min-width: 120px; }
    .arch-step.active-step { border-color: #185FA5; background: var(--color-background-info); }
    .arch-step .step-name { font-size: 11px; font-weight: 600; text-align: center; color: var(--color-text-primary); }
    .arch-step .step-tool { font-size: 10px; color: var(--color-text-tertiary); margin-top: 2px; text-align: center; }
    .arch-step.active-step .step-name { color: var(--color-text-info); }
    .arch-step.active-step .step-tool { color: var(--color-text-info); }
    
    /* ---- PIPELINE STATUS TRACKER ---- */
    .pipeline { display: flex; justify-content: space-between; margin: 20px 0px; align-items: flex-start; width: 100%; }
    .pipe-stage { flex: 1; display: flex; flex-direction: column; align-items: center; position: relative; }
    .pipe-dot { width: 32px; height: 32px; border-radius: 50%; border: 0.5px solid var(--color-border-secondary); background: var(--color-background-primary); display: flex; align-items: center; justify-content: center; font-size: 14px; color: var(--color-text-tertiary); z-index: 1; position: relative; }
    .pipe-dot.running { border-color: #185FA5; background: var(--color-background-info); color: var(--color-text-info); animation: pulse-ring .8s ease-in-out infinite; }
    @keyframes pulse-ring { 0%,100% { box-shadow: 0 0 0 0 rgba(24,95,165,.2); } 50% { box-shadow: 0 0 0 5px rgba(24,95,165,0); } }
    .pipe-name { font-size: 11px; color: var(--color-text-tertiary); margin-top: 6px; text-align: center; font-weight: 500; }
    .pipe-name.active { color: var(--color-text-info); font-weight: bold; }

    /* ---- RESULT CARD ---- */
    .result-card { border: 0.5px solid var(--color-border-secondary); border-radius: var(--border-radius-lg); background: var(--color-background-primary); overflow: hidden; margin-top: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    .result-header { padding: 14px 18px; border-bottom: 0.5px solid var(--color-border-secondary); display: flex; align-items: center; justify-content: space-between; background: var(--color-background-secondary); }
    .decision-type-badge { font-size: 11px; font-weight: 600; padding: 3px 10px; border-radius: 20px; background: var(--color-background-warning); color: var(--color-text-warning); }
</style>
""",
    unsafe_allow_html=True,
)

# ---- RENDER HERO SECTION ----
st.markdown(
    """
<div class="hero">
    <div class="badge">⚽ FIFA WORLD CUP 2026 TRANSIT</div>
    <h1>DecisionLens: <span>VAR Transparency</span></h1>
    <p>Corrective Retrieval-Augmented Generation (CRAG) system built to parse and evaluate official FIFA Laws of the Game applications instantly.</p>
</div>
""",
    unsafe_allow_html=True,
)

# ---- RENDER ARCHITECTURE STRIP ----
st.markdown(
    """
<div class="arch-strip">
    <div class="arch-label">System Architecture Mapping</div>
    <div class="arch-flow">
        <div class="arch-step"><span class="step-name">1. Input Stream</span><span class="step-tool">Streamlit UI</span></div>
        <div class="arch-step"><span class="step-name">2. Retrieval</span><span class="step-tool">Rank-BM25</span></div>
        <div class="arch-step active-step"><span class="step-name">3. Correction</span><span class="step-tool">Evaluator Loop</span></div>
        <div class="arch-step"><span class="step-name">4. Generation</span><span class="step-tool">Granite 2B</span></div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# ---- NATIVE STREAMLIT INTERACTION INPUTS ----
st.markdown(
    '<div class="arch-label">Query Submission Engine</div>', unsafe_allow_html=True
)
question = st.text_input(
    "Ask about a VAR decision or football rule:",
    placeholder="e.g., According to the VAR Protocol, what can the referee review?",
)

if question:
    # ---- PIPELINE TRACKER ANIMATION STRIP ----
    st.markdown(
        f"""
    <div class="pipeline">
        <div class="pipe-stage"><div class="pipe-dot">🔍</div><div class="pipe-name">Parsed</div></div>
        <div class="pipe-stage"><div class="pipe-dot running">⚙️</div><div class="pipe-name active">CRAG Processing</div></div>
        <div class="pipe-stage"><div class="pipe-dot" style="opacity: 0.4;">🤖</div><div class="pipe-name" style="opacity: 0.4;">LLM Response</div></div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.info(
        "Pipeline integration coming Day 3 — paste your question above to test routing."
    )

    # ---- RENDER THE RAW RESPONSE CARD ----
    st.markdown(
        """
    <div class="result-card">
        <div class="result-header">
            <span style="font-weight:600; font-size:13px; color:#111827;">System Intercept Payload</span>
            <span class="decision-type-badge">AGENT_PENDING</span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Render the requested agent raw json structure inside the custom container frame
    st.json(
        {
            "question": question,
            "status": "agent not yet connected",
            "engine": "granite3.1-dense:2b",
            "retrieval_strategy": "CRAG-pending",
        }
    )
