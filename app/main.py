# app/main.py
# DecisionLens — VAR Decision Transparency Engine
# Visual identity: vintage football history museum. All styling is inline
# CSS injected via st.markdown — no external images, no CDN dependencies.

import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pipeline')))
from agent import run

# ── Palette ──────────────────────────────────────────────────
PARCHMENT = "#F5F0E8"
PITCH_GREEN = "#1B4332"
AGED_GOLD = "#B8860B"
INK_NAVY = "#1A2744"

st.set_page_config(
    page_title="⚽ DecisionLens",
    layout="centered"
)

# ── Full theme override ──────────────────────────────────────
st.markdown(f"""
<style>
/* Base canvas: parchment, serif, ink */
.stApp {{
    background-color: {PARCHMENT};
    background-image:
        radial-gradient(ellipse at top left, rgba(184,134,11,0.06), transparent 60%),
        radial-gradient(ellipse at bottom right, rgba(27,67,50,0.05), transparent 60%);
    color: {INK_NAVY};
    font-family: Georgia, 'Times New Roman', serif;
}}
header[data-testid="stHeader"] {{ background: transparent; }}
#MainMenu, footer {{ visibility: hidden; }}

h1, h2, h3, h4 {{
    font-family: Georgia, 'Times New Roman', serif !important;
    color: {INK_NAVY} !important;
}}
p, li, label, .stMarkdown {{ color: {INK_NAVY}; }}

/* Embossed crest title block */
.dl-crest {{
    border-top: 3px double {AGED_GOLD};
    border-bottom: 3px double {AGED_GOLD};
    padding: 1.6rem 1rem 1.3rem 1rem;
    margin-bottom: 1.8rem;
    text-align: center;
    background: linear-gradient(180deg, rgba(27,67,50,0.04), rgba(27,67,50,0.00) 40%,
                rgba(27,67,50,0.00) 60%, rgba(27,67,50,0.04));
}}
.dl-crest .dl-title {{
    font-size: 2.4rem;
    letter-spacing: 0.35rem;
    font-variant: small-caps;
    color: {PITCH_GREEN};
    text-shadow: 0 1px 0 rgba(255,255,255,0.8), 0 -1px 0 rgba(26,39,68,0.25);
    margin: 0;
}}
.dl-crest .dl-subtitle {{
    font-size: 0.82rem;
    letter-spacing: 0.22rem;
    text-transform: uppercase;
    color: {AGED_GOLD};
    margin-top: 0.45rem;
}}
.dl-crest .dl-rule {{
    width: 120px;
    border-top: 1px solid {AGED_GOLD};
    margin: 0.7rem auto 0 auto;
}}

/* Question input: ledger entry line */
.stTextInput input {{
    background-color: #FBF8F2 !important;
    color: {INK_NAVY} !important;
    border: 1px solid {AGED_GOLD} !important;
    border-radius: 2px !important;
    font-family: Georgia, serif !important;
    font-size: 1.02rem !important;
    padding: 0.7rem !important;
}}
.stTextInput input::placeholder {{ color: rgba(26,39,68,0.45) !important; }}
.stTextInput label {{
    font-variant: small-caps;
    letter-spacing: 0.08rem;
    font-size: 1rem !important;
    color: {PITCH_GREEN} !important;
}}

/* Section plaques */
.dl-plaque {{
    font-variant: small-caps;
    letter-spacing: 0.18rem;
    font-size: 1.05rem;
    color: {PITCH_GREEN};
    border-bottom: 1px solid {AGED_GOLD};
    padding-bottom: 0.25rem;
    margin: 1.6rem 0 0.8rem 0;
}}

/* Verdict panel */
.dl-verdict {{
    background: #FBF8F2;
    border: 1px solid rgba(184,134,11,0.55);
    border-left: 4px solid {PITCH_GREEN};
    padding: 1.1rem 1.3rem;
    font-size: 1.05rem;
    line-height: 1.75;
    box-shadow: 2px 3px 0 rgba(26,39,68,0.08);
}}

/* Brass compass confidence dial */
.dl-dial-wrap {{ text-align: center; padding: 0.4rem 0 0.2rem 0; }}
.dl-dial {{
    width: 130px; height: 65px;
    margin: 0 auto;
    border-radius: 130px 130px 0 0;
    position: relative;
    background: conic-gradient(
        from 270deg at 50% 100%,
        #8B2E2E 0deg,
        {AGED_GOLD} calc(var(--conf) * 1.8deg),
        rgba(26,39,68,0.12) calc(var(--conf) * 1.8deg),
        rgba(26,39,68,0.12) 180deg,
        transparent 180deg
    );
    border: 2px solid {AGED_GOLD};
    border-bottom: 3px solid {INK_NAVY};
    box-shadow: inset 0 2px 6px rgba(26,39,68,0.25), 0 1px 0 rgba(255,255,255,0.7);
}}
.dl-dial::after {{
    content: "";
    position: absolute;
    left: 50%; bottom: -6px;
    width: 10px; height: 10px;
    margin-left: -5px;
    border-radius: 50%;
    background: radial-gradient(circle at 35% 35%, #E8C56A, {AGED_GOLD} 60%, #7A5A08);
    border: 1px solid {INK_NAVY};
}}
.dl-dial-value {{
    font-family: 'Courier New', monospace;
    font-size: 1.3rem;
    color: {PITCH_GREEN};
    margin-top: 0.4rem;
}}
.dl-dial-label {{
    font-variant: small-caps;
    letter-spacing: 0.14rem;
    font-size: 0.78rem;
    color: {AGED_GOLD};
}}

/* Decision register entries */
.dl-step {{
    border-left: 2px solid {AGED_GOLD};
    padding: 0.35rem 0 0.35rem 0.9rem;
    margin-bottom: 0.45rem;
    line-height: 1.6;
}}
.dl-step .dl-step-no {{
    font-family: 'Courier New', monospace;
    color: {AGED_GOLD};
    margin-right: 0.4rem;
}}

/* Referee's notebook citation pages: ruled lines, torn edge */
.dl-notebook {{
    background:
        repeating-linear-gradient(
            180deg,
            #FDFBF6 0px, #FDFBF6 27px,
            rgba(26,39,68,0.12) 27px, rgba(26,39,68,0.12) 28px
        );
    border: 1px solid rgba(26,39,68,0.25);
    border-left: 3px solid #8B2E2E;
    padding: 0.9rem 1.1rem 1.1rem 1.1rem;
    margin-bottom: 0.9rem;
    position: relative;
    box-shadow: 2px 3px 0 rgba(26,39,68,0.10);
    clip-path: polygon(
        0 0, 100% 0, 100% calc(100% - 7px),
        96% 100%, 90% calc(100% - 6px), 84% 100%, 78% calc(100% - 5px),
        72% 100%, 66% calc(100% - 7px), 60% 100%, 54% calc(100% - 5px),
        48% 100%, 42% calc(100% - 7px), 36% 100%, 30% calc(100% - 5px),
        24% 100%, 18% calc(100% - 7px), 12% 100%, 6% calc(100% - 5px), 0 100%
    );
}}
.dl-notebook .dl-cite-law {{
    font-family: 'Courier New', monospace;
    font-weight: bold;
    color: {PITCH_GREEN};
    font-size: 0.95rem;
}}
.dl-notebook .dl-cite-source {{
    font-family: 'Courier New', monospace;
    font-size: 0.8rem;
    color: rgba(26,39,68,0.65);
    letter-spacing: 0.04rem;
}}
.dl-notebook .dl-cite-quote {{
    font-family: 'Courier New', monospace;
    font-size: 0.88rem;
    color: {INK_NAVY};
    margin-top: 0.5rem;
    line-height: 28px;
}}

/* Aged red wax seal for missing evidence */
.dl-seal-panel {{
    border: 1px dashed #8B2E2E;
    background: rgba(139,46,46,0.05);
    padding: 1rem 1.2rem 1rem 4.6rem;
    position: relative;
    margin-bottom: 0.9rem;
}}
.dl-seal {{
    position: absolute;
    left: 0.9rem; top: 50%;
    transform: translateY(-50%) rotate(-12deg);
    width: 58px; height: 58px;
    border-radius: 50%;
    background: radial-gradient(circle at 38% 32%, #B24A4A, #8B2E2E 55%, #5E1F1F);
    box-shadow: 0 2px 5px rgba(26,39,68,0.35), inset 0 0 0 4px rgba(245,240,232,0.25);
    color: {PARCHMENT};
    font-variant: small-caps;
    font-size: 0.52rem;
    letter-spacing: 0.06rem;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
}}
.dl-seal-panel ul {{ margin: 0; padding-left: 1.1rem; }}
.dl-seal-panel li {{ color: #5E1F1F; line-height: 1.6; }}
.dl-seal-title {{
    font-variant: small-caps;
    letter-spacing: 0.12rem;
    color: #8B2E2E;
    margin-bottom: 0.3rem;
}}

/* Museum accession label cards for sources */
.dl-accession {{
    display: inline-block;
    background: #FDFBF6;
    border: 1px solid {AGED_GOLD};
    border-bottom: 3px solid {AGED_GOLD};
    padding: 0.55rem 0.9rem;
    margin: 0 0.6rem 0.6rem 0;
    font-family: 'Courier New', monospace;
    font-size: 0.82rem;
    color: {INK_NAVY};
    box-shadow: 1px 2px 0 rgba(26,39,68,0.10);
}}
.dl-accession .dl-acc-no {{
    display: block;
    font-size: 0.68rem;
    color: {AGED_GOLD};
    letter-spacing: 0.1rem;
    margin-bottom: 0.15rem;
}}

/* Decision type plate */
.dl-type-plate {{
    text-align: center;
    font-variant: small-caps;
    letter-spacing: 0.2rem;
    font-size: 1.15rem;
    color: {PARCHMENT};
    background: {PITCH_GREEN};
    border: 1px solid {AGED_GOLD};
    padding: 0.55rem 0.4rem;
    margin-top: 1.5rem;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.15), 2px 3px 0 rgba(26,39,68,0.12);
}}
.dl-type-plate .dl-type-label {{
    display: block;
    font-size: 0.68rem;
    letter-spacing: 0.16rem;
    color: rgba(245,240,232,0.7);
    margin-bottom: 0.15rem;
}}

/* Footer colophon */
.dl-colophon {{
    margin-top: 2.6rem;
    padding-top: 0.8rem;
    border-top: 1px solid {AGED_GOLD};
    text-align: center;
    font-size: 0.75rem;
    letter-spacing: 0.1rem;
    color: rgba(26,39,68,0.55);
    font-variant: small-caps;
}}

/* Spinner recolor */
.stSpinner > div {{ border-top-color: {AGED_GOLD} !important; }}
</style>
""", unsafe_allow_html=True)

# ── Crest header ─────────────────────────────────────────────
st.markdown("""
<div class="dl-crest">
    <p class="dl-title">DecisionLens</p>
    <div class="dl-rule"></div>
    <p class="dl-subtitle">Official Register of Refereeing Decisions · FIFA World Cup 2026</p>
    <p class="dl-subtitle" style="letter-spacing:0.12rem; color:rgba(26,39,68,0.55);">
        Findings drawn solely from the IFAB Laws of the Game 2025/26 and the VAR Protocol
    </p>
</div>
""", unsafe_allow_html=True)

question = st.text_input(
    "Submit an enquiry to the register",
    placeholder="e.g. What makes a handball offence under FIFA Law 12?"
)

if question:
    with st.spinner("Consulting the Laws of the Game..."):
        result = run(question)

    confidence = result.get("confidence", 0.0)
    decision_type = result.get("decision_type", "unknown")

    # ── Verdict ──────────────────────────────────────────────
    st.markdown('<div class="dl-plaque">Finding of the Register</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="dl-verdict">{result.get("answer", "No finding was recorded.")}</div>',
        unsafe_allow_html=True
    )

    # ── Compass dial + decision type plate ───────────────────
    col1, col2 = st.columns(2)
    with col1:
        pct = int(round(confidence * 100))
        st.markdown(f"""
        <div class="dl-dial-wrap">
            <div class="dl-dial" style="--conf: {pct};"></div>
            <div class="dl-dial-value">{pct}%</div>
            <div class="dl-dial-label">Evidence Sufficiency</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="dl-type-plate">
            <span class="dl-type-label">Classification of Decision</span>
            {decision_type.replace("_", " ")}
        </div>
        """, unsafe_allow_html=True)

    # ── Decision steps ───────────────────────────────────────
    steps = result.get("decision_steps", [])
    if steps:
        st.markdown('<div class="dl-plaque">Sequence of Determination</div>', unsafe_allow_html=True)
        for i, step in enumerate(steps, 1):
            st.markdown(
                f'<div class="dl-step"><span class="dl-step-no">{i:02d}.</span>{step}</div>',
                unsafe_allow_html=True
            )

    # ── Citations: referee's notebook pages ──────────────────
    citations = result.get("rule_citations", [])
    if citations:
        st.markdown('<div class="dl-plaque">Citations from the Law Book</div>', unsafe_allow_html=True)
        for citation in citations:
            law_title = citation.get('law_or_section', citation.get('law', 'Rule Reference'))
            doc_source = citation.get('source', 'IFAB Official Rules')
            quoted_phrase = citation.get('quoted_span', '')
            quote_html = (
                f'<div class="dl-cite-quote">&ldquo;{quoted_phrase}&rdquo;</div>'
                if quoted_phrase else
                '<div class="dl-cite-quote">Section consulted in full for this finding.</div>'
            )
            st.markdown(f"""
            <div class="dl-notebook">
                <span class="dl-cite-law">{law_title}</span><br>
                <span class="dl-cite-source">{doc_source}</span>
                {quote_html}
            </div>
            """, unsafe_allow_html=True)

    # ── Missing evidence: wax seal panel ─────────────────────
    missing = result.get("missing_evidence", [])
    if missing and (confidence < 0.5 or decision_type == "unknown"):
        st.markdown('<div class="dl-plaque">Evidence Not Before the Register</div>', unsafe_allow_html=True)
        items = "".join(f"<li>{m}</li>" for m in missing)
        st.markdown(f"""
        <div class="dl-seal-panel">
            <div class="dl-seal">Insufficient<br>Evidence</div>
            <div class="dl-seal-title">The following facts were not available</div>
            <ul>{items}</ul>
        </div>
        """, unsafe_allow_html=True)

    # ── Sources: museum accession labels ─────────────────────
    sources = result.get("sources", [])
    if sources:
        st.markdown('<div class="dl-plaque">Documents Consulted</div>', unsafe_allow_html=True)
        labels = "".join(
            f'<div class="dl-accession"><span class="dl-acc-no">ACC. NO. {i:03d} · IFAB</span>{s}</div>'
            for i, s in enumerate(sources, 1)
        )
        st.markdown(labels, unsafe_allow_html=True)

# ── Colophon ─────────────────────────────────────────────────
st.markdown("""
<div class="dl-colophon">
    Compiled with IBM Granite 3.1 8B · IBM Docling 2.97.0 · Hybrid BM25 + Embedding Retrieval<br>
    Confidence denotes evidence sufficiency, not the correctness of the match official.
</div>
""", unsafe_allow_html=True)
