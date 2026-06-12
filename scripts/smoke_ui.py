# scripts/smoke_ui.py
# Headless smoke test: runs app/main.py through Streamlit's AppTest harness,
# asserts the script renders without exceptions, and exercises the mode
# buttons and a simulated verdict so every render path is covered.
import json
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(REPO, "pipeline"))

from streamlit.testing.v1 import AppTest

at = AppTest.from_file(os.path.join(REPO, "app", "main.py"), default_timeout=120)
at.run()

assert not at.exception, f"EXCEPTION ON FIRST RENDER: {at.exception}"
print(f"[1] first render OK — markdown blocks: {len(at.markdown)}, buttons: {len(at.button)}")

# flip to analyst mode
analyst = next(b for b in at.button if b.key == "mode_analyst")
analyst.click().run()
assert not at.exception, f"EXCEPTION AFTER MODE SWITCH: {at.exception}"
assert at.session_state["mode"] == "analyst"
print("[2] analyst mode switch OK")

# inject fake verdicts (no Ollama dependency) covering the full record paths
GOOD_ENTRY = {
        "q": "What makes a handball deliberate?",
        "r": {
            "answer": "A handball is judged deliberate when the arm makes the body unnaturally bigger.",
            "decision_type": "handball",
            "confidence": 0.87,
            "rule_citations": [
                {"source": "IFAB Laws of the Game 2025/26", "law_or_section": "Law 12",
                 "quoted_span": "touches the ball with their hand/arm when it has made their body unnaturally bigger"}
            ],
            "decision_steps": ["Step 1: the rule defines the offence.", "Step 2: it applies here."],
            "missing_evidence": [],
            "sources": ["IFAB Laws of the Game 2025/26"],
            "tactical_context": "",
            "language": "English",
            "retrieval_debug": {
                "crag_decision": "GOOD",
                "crag_score": 0.87,
                "top_chunks": [
                    {"chunk_id": 412, "bm25_score": 9.31, "vector_score": 0.88},
                    {"chunk_id": 218, "bm25_score": 7.02, "vector_score": 0.84},
                    {"chunk_id": 305, "bm25_score": 5.55, "vector_score": 0.81},
                ],
                "timings_ms": {"retrieval": 412, "generation": 8900, "total": 9350},
            },
        },
}
GATE_ENTRY = {
        "q": "Was Neymar's handball in the final deliberate?",
        "r": {
            "answer": "DecisionLens could not find sufficient rule evidence for this incident.",
            "decision_type": "unknown",
            "confidence": 0.0,
            "rule_citations": [],
            "decision_steps": [],
            "missing_evidence": ["Specific incident details not available in rule documents"],
            "sources": [],
            "tactical_context": "",
            "language": "English",
        },
}

# A) good verdict as the latest record — full record + live telemetry
at.session_state["history"] = [GATE_ENTRY, GOOD_ENTRY]
at.run()
assert not at.exception, f"EXCEPTION ON VERDICT RENDER: {at.exception}"
joined = "\n".join(str(m.value) for m in at.markdown)
for needle in ["DECISION RECORD", "The Lineage", "Colophon", "Hand of God",
               "rec-stamp", "dial-needle", "eng-ball", "folio 412", "PASSED", "ENGAGED"]:
    assert needle in joined, f"MISSING IN RENDER: {needle}"
exp_labels = "|".join(e.label for e in at.expander)
assert "Engine Room" in exp_labels and "Hypothetical" in exp_labels, f"expander labels: {exp_labels}"
print("[3] full decision record + live telemetry render OK")

# B) gate-tripped abstention as the latest record
at.session_state["history"] = [GOOD_ENTRY, GATE_ENTRY]
at.run()
assert not at.exception, f"EXCEPTION ON GATE RENDER: {at.exception}"
joined = "\n".join(str(m.value) for m in at.markdown)
for needle in ["TRIPPED", "the gate closed first", "NEVER ENGAGED", "Not in evidence"]:
    assert needle in joined, f"MISSING IN GATE RENDER: {needle}"
print("[3b] gate-tripped audit trail renders OK")

# abstention-at-tribunal path
at.session_state["history"] = [{
    "q": "What is the rule about the stadium roof?",
    "r": {
        "answer": "Insufficient evidence.",
        "decision_type": "unknown",
        "confidence": 0.3,
        "rule_citations": [], "decision_steps": [],
        "missing_evidence": ["No governing clause retrieved"],
        "sources": [], "tactical_context": "", "language": "English",
        "retrieval_debug": {
            "crag_decision": "POOR", "crag_score": 0.41,
            "top_chunks": [{"chunk_id": 12, "bm25_score": 1.2, "vector_score": 0.41}],
            "timings_ms": {"retrieval": 380, "total": 400},
        },
    },
}]
at.run()
assert not at.exception, f"EXCEPTION ON ABSTENTION RENDER: {at.exception}"
joined = "\n".join(str(m.value) for m in at.markdown)
assert "ABSTENTION SIDING" in joined, "abstention siding not rendered"
assert "NEVER ENGAGED" in joined, "scribe never-engaged state not rendered"
print("[4] tribunal abstention path renders OK")

print("ALL SMOKE TESTS PASSED")
