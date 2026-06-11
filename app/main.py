# app/main.py — DecisionLens VAR Transparency
# Production UI with Anthropic + Fable 5 design principles
# Icon-based, professional typography, measured color hierarchy

import streamlit as st
import sys
import os

# Dynamically append the pipeline directory path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "pipeline"))
)

# Configure page
st.set_page_config(
    page_title="DecisionLens | VAR Transparency",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Load Phosphor Icons (professional, modern icon set)
st.markdown(
    '<link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.0.0/index.css">',
    unsafe_allow_html=True,
)

# Load system fonts (Anthropic typography inspiration)
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Fraunces:opsz@9..144;wght@400;500;600;700&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True,
)

# ============================================================================
# PROFESSIONAL DESIGN TOKENS — Extracted from your color theory reference
# ============================================================================
st.markdown(
    """
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    /* DESIGN TOKENS */
    :root {
        /* Typography */
        --font-display: 'Fraunces', serif;
        --font-body: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        --font-mono: 'Fira Code', 'Courier New', monospace;
        
        /* Brand Colors */
        --color-brand-blue: #63A4F2;
        --color-brand-orange: #CC795C;
        --color-error-red: #8F4043;
        --color-neutral-white: #FFFFFF;
        --color-neutral-black: #000000;
        
        /* Slate (Background) */
        --color-slate-dark: #191919;
        --color-slate-med: #262625;
        --color-slate-light: #48483E;
        
        /* Cloud (Borders/Dividers) */
        --color-cloud-dark: #666683;
        --color-cloud-med: #919BA8;
        --color-cloud-light: #BFB8BA;
        
        /* Ivory (Secondary) */
        --color-ivory-dark: #E5E5DF;
        --color-ivory-med: #F8F8F7;
        --color-ivory-light: #FAFAF7;
        
        /* Semantic */
        --color-success: #2D6E4D;
        --color-warning: #D8924A;
        --color-focus: #63A4F2;
        --color-error: #8F4043;
        
        /* Spacing */
        --space-xs: 4px;
        --space-sm: 8px;
        --space-md: 12px;
        --space-lg: 16px;
        --space-xl: 24px;
        --space-2xl: 32px;
        
        /* Border Radius */
        --radius-sm: 4px;
        --radius-md: 8px;
        --radius-lg: 12px;
        
        /* Shadows */
        --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* PAGE STRUCTURE */
    body { font-family: var(--font-body); color: #111827; background: #FFFFFF; }
    .block-container { padding: var(--space-2xl) var(--space-lg); max-width: 1100px; }
    
    /* ========== HERO SECTION ========== */
    .hero-container {
        padding-bottom: var(--space-2xl);
        border-bottom: 1px solid #E5E7EB;
        margin-bottom: var(--space-2xl);
    }
    
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: var(--space-sm);
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: #0D4A8A;
        background: #E7F3FF;
        padding: var(--space-sm) var(--space-md);
        border-radius: 20px;
        margin-bottom: var(--space-lg);
    }
    
    .hero-title {
        font-family: var(--font-display);
        font-size: 42px;
        font-weight: 700;
        line-height: 1.15;
        margin-bottom: var(--space-md);
        color: #111827;
        letter-spacing: -0.02em;
    }
    
    .hero-title .accent { color: var(--color-brand-blue); }
    
    .hero-subtitle {
        font-size: 16px;
        line-height: 1.6;
        color: #4B5563;
        max-width: 600px;
        margin-bottom: 0;
    }
    
    /* ========== ARCHITECTURE SECTION ========== */
    .section-label {
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #6B7280;
        margin-bottom: var(--space-lg);
        margin-top: var(--space-2xl);
    }
    
    .architecture-flow {
        display: flex;
        gap: var(--space-sm);
        overflow-x: auto;
        padding-bottom: var(--space-sm);
        margin-bottom: var(--space-2xl);
    }
    
    .arch-step {
        flex: 0 0 auto;
        min-width: 140px;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: var(--space-md) var(--space-lg);
        border: 1px solid #E5E7EB;
        border-radius: var(--radius-md);
        background: #F9FAFB;
        transition: all 0.2s ease;
    }
    
    .arch-step:hover {
        border-color: var(--color-brand-blue);
        background: #F0F7FE;
    }
    
    .arch-step.active {
        border-color: var(--color-brand-blue);
        background: #E7F3FF;
    }
    
    .arch-step-number {
        font-size: 13px;
        font-weight: 700;
        color: #6B7280;
        margin-bottom: var(--space-xs);
    }
    
    .arch-step-name {
        font-size: 12px;
        font-weight: 600;
        text-align: center;
        color: #111827;
    }
    
    .arch-step-tool {
        font-size: 10px;
        color: #6B7280;
        margin-top: var(--space-xs);
        text-align: center;
    }
    
    .arch-step.active .arch-step-name,
    .arch-step.active .arch-step-number {
        color: var(--color-brand-blue);
    }
    
    /* ========== QUERY INPUT SECTION ========== */
    .query-section {
        margin-bottom: var(--space-2xl);
    }
    
    .input-container {
        position: relative;
    }
    
    .stTextInput > div > div > input {
        font-family: var(--font-body) !important;
        font-size: 14px !important;
        border: 1px solid #D1D5DB !important;
        border-radius: var(--radius-md) !important;
        padding: 12px 14px !important;
        background: #FFFFFF !important;
        color: #111827 !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #9CA3AF !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--color-brand-blue) !important;
        box-shadow: 0 0 0 3px rgba(99, 164, 242, 0.1) !important;
    }
    
    /* ========== PIPELINE STATUS TRACKER ========== */
    .pipeline-tracker {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: var(--space-lg);
        margin: var(--space-2xl) 0;
        padding: var(--space-lg);
        background: #F9FAFB;
        border-radius: var(--radius-lg);
        border: 1px solid #E5E7EB;
    }
    
    .pipeline-stage {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        position: relative;
    }
    
    .pipeline-dot {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        border: 2px solid #E5E7EB;
        background: #FFFFFF;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        color: #9CA3AF;
        margin-bottom: var(--space-md);
        transition: all 0.3s ease;
    }
    
    .pipeline-dot.running {
        border-color: var(--color-brand-blue);
        background: #E7F3FF;
        color: var(--color-brand-blue);
        animation: pulse-glow 1.2s ease-in-out infinite;
    }
    
    .pipeline-dot.complete {
        border-color: #2D6E4D;
        background: #E6F6F2;
        color: #2D6E4D;
    }
    
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 0 0 rgba(99, 164, 242, 0.2); }
        50% { box-shadow: 0 0 0 8px rgba(99, 164, 242, 0); }
    }
    
    .pipeline-label {
        font-size: 11px;
        font-weight: 600;
        text-align: center;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .pipeline-label.running {
        color: var(--color-brand-blue);
        font-weight: 700;
    }
    
    .pipeline-label.complete {
        color: #2D6E4D;
    }
    
    /* ========== RESULT CARDS ========== */
    .result-card {
        border: 1px solid #E5E7EB;
        border-radius: var(--radius-lg);
        background: #FFFFFF;
        overflow: hidden;
        box-shadow: var(--shadow-sm);
        margin-top: var(--space-2xl);
    }
    
    .result-header {
        padding: var(--space-lg);
        background: #F9FAFB;
        border-bottom: 1px solid #E5E7EB;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .result-title {
        font-size: 13px;
        font-weight: 600;
        color: #111827;
        display: flex;
        align-items: center;
        gap: var(--space-sm);
    }
    
    .result-badge {
        display: inline-flex;
        align-items: center;
        gap: var(--space-xs);
        font-size: 10px;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 20px;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    
    .badge-pending {
        background: #FEF3C7;
        color: #925C0E;
    }
    
    .badge-success {
        background: #E6F6F2;
        color: #0A4D3C;
    }
    
    .badge-error {
        background: #FEE8E8;
        color: #8F4043;
    }
    
    .result-body {
        padding: var(--space-lg);
    }
    
    .answer-section {
        margin-bottom: var(--space-xl);
    }
    
    .answer-section-title {
        font-size: 11px;
        font-weight: 700;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: var(--space-md);
    }
    
    .answer-text {
        font-size: 14px;
        line-height: 1.7;
        color: #1F2937;
        background: #FAFBFC;
        padding: var(--space-lg);
        border-left: 3px solid var(--color-brand-blue);
        border-radius: var(--radius-sm);
    }
    
    /* ========== CITATIONS & EVIDENCE ========== */
    .citations-container {
        margin-top: var(--space-xl);
        padding-top: var(--space-xl);
        border-top: 1px solid #E5E7EB;
    }
    
    .citation-item {
        padding: var(--space-md);
        background: #F9FAFB;
        border-left: 2px solid #63A4F2;
        border-radius: var(--radius-sm);
        margin-bottom: var(--space-md);
    }
    
    .citation-source {
        font-size: 11px;
        font-weight: 700;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: var(--space-xs);
    }
    
    .citation-law {
        font-size: 12px;
        font-weight: 600;
        color: #111827;
        margin-bottom: var(--space-xs);
    }
    
    .citation-text {
        font-size: 13px;
        line-height: 1.5;
        color: #4B5563;
        font-style: italic;
    }
    
    /* ========== CONFIDENCE & MISSING EVIDENCE ========== */
    .metadata-row {
        display: flex;
        gap: var(--space-xl);
        margin-top: var(--space-xl);
        padding-top: var(--space-xl);
        border-top: 1px solid #E5E7EB;
    }
    
    .metadata-block {
        flex: 1;
    }
    
    .metadata-label {
        font-size: 11px;
        font-weight: 700;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: var(--space-md);
        display: flex;
        align-items: center;
        gap: var(--space-xs);
    }
    
    .confidence-meter {
        width: 100%;
        height: 6px;
        background: #E5E7EB;
        border-radius: 3px;
        overflow: hidden;
        margin-bottom: var(--space-sm);
    }
    
    .confidence-fill {
        height: 100%;
        background: linear-gradient(90deg, #2D6E4D 0%, #63A4F2 50%, #D8924A 100%);
        transition: width 0.3s ease;
    }
    
    .confidence-text {
        font-size: 12px;
        color: #4B5563;
    }
    
    .missing-evidence-list {
        list-style: none;
    }
    
    .missing-evidence-item {
        font-size: 13px;
        line-height: 1.6;
        color: #4B5563;
        padding-left: 20px;
        position: relative;
        margin-bottom: var(--space-sm);
    }
    
    .missing-evidence-item::before {
        content: "—";
        position: absolute;
        left: 4px;
        color: #D8924A;
        font-weight: 700;
    }
    
    /* ========== JSON DEBUG SECTION ========== */
    .json-section {
        margin-top: var(--space-xl);
        padding-top: var(--space-xl);
        border-top: 1px solid #E5E7EB;
    }
    
    .json-label {
        font-size: 10px;
        font-weight: 700;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: var(--space-md);
    }
    
    /* ========== UTILITY ========== */
    .divider { height: 1px; background: #E5E7EB; margin: var(--space-xl) 0; }
    
    .text-small { font-size: 12px; color: #6B7280; }
    
    .text-muted { color: #9CA3AF; }
    
    .icon-inline {
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }

</style>
""",
    unsafe_allow_html=True,
)

# ============================================================================
# UI RENDERING
# ============================================================================

# HERO SECTION
st.markdown(
    """
<div class="hero-container">
    <div class="hero-badge">
        <i class="ph ph-soccer-ball"></i>
        FIFA WORLD CUP 2026 TRANSIT
    </div>
    <h1 class="hero-title">DecisionLens: <span class="accent">VAR Transparency</span></h1>
    <p class="hero-subtitle">
        Retrieves official FIFA Laws of the Game and explains controversial soccer decisions 
        in plain language with citations, confidence levels, and missing-evidence warnings.
    </p>
</div>
""",
    unsafe_allow_html=True,
)

# ARCHITECTURE SECTION
st.markdown('<div class="section-label"><i class="ph ph-diagram-icon"></i> System Architecture</div>', unsafe_allow_html=True)
st.markdown(
    """
<div class="architecture-flow">
    <div class="arch-step">
        <div class="arch-step-number">1</div>
        <div class="arch-step-name">Input Stream</div>
        <div class="arch-step-tool">Streamlit UI</div>
    </div>
    <div class="arch-step">
        <div class="arch-step-number">2</div>
        <div class="arch-step-name">Retrieval</div>
        <div class="arch-step-tool">Rank-BM25</div>
    </div>
    <div class="arch-step active">
        <div class="arch-step-number">3</div>
        <div class="arch-step-name">Correction</div>
        <div class="arch-step-tool">Evaluator Loop</div>
    </div>
    <div class="arch-step">
        <div class="arch-step-number">4</div>
        <div class="arch-step-name">Generation</div>
        <div class="arch-step-tool">Granite 2B</div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# QUERY INPUT SECTION
st.markdown('<div class="section-label"><i class="ph ph-chat-dots"></i> Ask a Question</div>', unsafe_allow_html=True)
question = st.text_input(
    "Ask about a VAR decision or football rule:",
    placeholder="e.g., According to the VAR Protocol, what can the referee review?",
    label_visibility="collapsed",
)

# PIPELINE STATUS (when question is submitted)
if question:
    st.markdown(
        """
    <div class="pipeline-tracker">
        <div class="pipeline-stage">
            <div class="pipeline-dot complete">
                <i class="ph ph-check"></i>
            </div>
            <div class="pipeline-label complete">Query Parsed</div>
        </div>
        <div class="pipeline-stage">
            <div class="pipeline-dot running">
                <i class="ph ph-gear"></i>
            </div>
            <div class="pipeline-label running">Processing</div>
        </div>
        <div class="pipeline-stage">
            <div class="pipeline-dot">
                <i class="ph ph-robot"></i>
            </div>
            <div class="pipeline-label">Generation</div>
        </div>
        <div class="pipeline-stage">
            <div class="pipeline-dot">
                <i class="ph ph-check-circle"></i>
            </div>
            <div class="pipeline-label">Response</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
    
    # RESULT CARD
    st.markdown(
        """
    <div class="result-card">
        <div class="result-header">
            <div class="result-title">
                <i class="ph ph-lightning-bold"></i>
                System Response
            </div>
            <span class="result-badge badge-pending">
                <i class="ph ph-timer"></i>
                In Progress
            </span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
    
    # PLACEHOLDER MESSAGE
    st.info(
        "Pipeline integration launching Day 3. Your question has been received and will be processed through the CRAG system."
    )
    
    # MOCK RESULT STRUCTURE (for demo)
    result = {
        "question": question,
        "status": "awaiting_pipeline_connection",
        "engine": "granite3.1-dense:2b",
        "retrieval_strategy": "hybrid_bm25_vector",
        "decision_steps": [],
    }
    
    # RESULT BODY (when data is ready)
    st.markdown(
        """
    <div class="result-body">
        <div class="answer-section">
            <div class="answer-section-title">Answer</div>
            <div class="answer-text">
                Pipeline is being configured. Once connected, this section will display the grounded answer 
                with citations to official FIFA Laws of the Game.
            </div>
        </div>
        
        <div class="citations-container">
            <div class="answer-section-title">Supporting Evidence</div>
            <div class="citation-item">
                <div class="citation-source">IFAB Laws of the Game 2025/26</div>
                <div class="citation-law">Law 5 – The Referee</div>
                <div class="citation-text">
                    "The referee is empowered to enforce the Laws of the Game in connection with the match 
                    to which he has been appointed."
                </div>
            </div>
        </div>
        
        <div class="metadata-row">
            <div class="metadata-block">
                <div class="metadata-label">
                    <i class="ph ph-gauge"></i>
                    Confidence
                </div>
                <div class="confidence-meter">
                    <div class="confidence-fill" style="width: 75%;"></div>
                </div>
                <div class="confidence-text">75% — Sufficient evidence available</div>
            </div>
            <div class="metadata-block">
                <div class="metadata-label">
                    <i class="ph ph-warning"></i>
                    Missing Evidence
                </div>
                <ul class="missing-evidence-list">
                    <li class="missing-evidence-item">Real-time VAR incident video</li>
                    <li class="missing-evidence-item">Referee communication protocol</li>
                </ul>
            </div>
        </div>
        
        <div class="json-section">
            <div class="json-label">Debug Payload</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
    
    # Raw JSON for debugging
    st.json(result)