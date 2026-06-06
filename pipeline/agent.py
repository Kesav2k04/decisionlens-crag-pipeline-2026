# pipeline/agent.py
# DecisionLens CRAG Agent
# Connects retriever → evaluator → Granite generation

import json
import requests
import re
from retriever import HybridRetriever

# ── Configuration ──────────────────────────────────────────
OLLAMA_URL = "http://localhost:11434/api/generate"
GRANITE_MODEL = "granite3.1-dense:8b"  # Optimized for Kesav's RTX 3070 Ti

# Relevance thresholds - Tuned for nomic-embed-text inflated cosines
GOOD_THRESHOLD = 0.75   # Above this: answer confidently from context
POOR_THRESHOLD = 0.65   # Below this: safely abstain from answering

# ── Response Schema ─────────────────────────────────────────
RESPONSE_SCHEMA = {
    "answer": "",
    "decision_type": "unknown",
    "rule_citations": [],
    "decision_steps": [],
    "confidence": 0.0,
    "missing_evidence": [],
    "sources": []
}

# ── Prompts ─────────────────────────────────────────────────
SYSTEM_PROMPT = """You are DecisionLens, an assistant that explains FIFA VAR and referee decisions to football fans.

STRICT RULES:
1. Answer ONLY from the provided rule context. Never use general knowledge.
2. Every factual claim must reference a specific Law or section from the context.
3. If the context does not contain enough information, say so clearly.
4. Always respond in valid JSON matching the exact schema provided.
5. Keep the answer field in plain language a non-expert fan can understand.
6. confidence is evidence sufficiency (0.0 to 1.0), not factual certainty.
7. 'decision_steps' MUST be a flat list of strings. Do not nest objects inside it."""

def build_generation_prompt(question: str, chunks: list, confidence: float) -> str:
    context_text = ""
    sources = []
    for i, chunk in enumerate(chunks):
        context_text += f"\n[Source {i+1}: {chunk.get('source', 'FIFA Rules')}]\n{chunk['text']}\n"
        sources.append(chunk.get("source", "FIFA Rules"))

    return f"""Answer this football fan question using ONLY the rule context below.

QUESTION: {question}

RULE CONTEXT:
{context_text}

Respond in this exact JSON format:
{{
  "answer": "Plain language explanation for a football fan",
  "decision_type": "handball | offside | penalty | red_card | var_reviewability | unknown",
  "rule_citations": [
    {{
      "source": "document name",
      "law_or_section": "Law X or Section Y",
      "quoted_span": "short exact phrase from the context above"
    }}
  ],
  "decision_steps": [
    "Step 1: what the rule says",
    "Step 2: how it applies to this situation"
  ],
  "confidence": {confidence:.2f},
  "missing_evidence": ["list any facts needed but not in context"],
  "sources": {json.dumps(list(set(sources)))}
}}

Important: quoted_span must be a short phrase actually present in the context above."""

def call_granite(prompt: str) -> str:
    """Send prompt to local Granite via Ollama with strict JSON enforcement."""
    payload = {
        "model": GRANITE_MODEL,
        "prompt": prompt,
        "system": SYSTEM_PROMPT,
        "stream": False,
        "format": "json",     # Forces Ollama backend to ONLY generate valid JSON tokens
        "options": {
            "temperature": 0.0,   # Absolute determinism
            "num_predict": 1024,
            "num_ctx": 4096       # Fixes token truncation
        }
    }
    response = requests.post(OLLAMA_URL, json=payload, timeout=120)
    response.raise_for_status()
    return response.json()["response"]

def evaluate_context(chunks: list) -> tuple[str, float]:
    """Evaluate whether retrieved chunks are sufficient to answer."""
    if not chunks:
        return "POOR", 0.0

    scores = [c.get("vector_score", 0.0) for c in chunks[:3]]
    avg_score = sum(scores) / len(scores) if scores else 0.0

    if avg_score >= GOOD_THRESHOLD:
        return "GOOD", min(avg_score * 1.5, 0.95)
    elif avg_score < POOR_THRESHOLD:
        return "POOR", avg_score
    else:
        return "UNSURE", avg_score

def parse_granite_response(raw: str) -> dict:
    """Extract and parse structured JSON from model response."""
    match = re.search(r'\{[\s\S]*\}', raw)
    
    if match:
        cleaned = match.group(0)
        # Prevent invalid strings caused by raw unescaped control newlines
        cleaned = cleaned.replace('\n', ' ')
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            return {
                **RESPONSE_SCHEMA,
                "answer": f"The system could not parse the JSON. Error: {str(e)}.",
                "confidence": 0.1,
                "missing_evidence": ["Model output contained invalid JSON syntax", raw[:200]]
            }
    
    return {
        **RESPONSE_SCHEMA,
        "answer": "No JSON block was found in the model's response.",
        "confidence": 0.1,
        "missing_evidence": ["Model completely failed to format output as JSON"]
    }

def build_abstention_response(question: str, chunks: list) -> dict:
    """Fallback response when context is irrelevant."""
    available_topics = [c.get("source", "unknown") for c in chunks]
    return {
        **RESPONSE_SCHEMA,
        "answer": (
            "DecisionLens could not find sufficient rule evidence to explain this specific situation. "
            "The question may involve incident details that are not contained in the official rule text."
        ),
        "confidence": 0.0,
        "missing_evidence": [
            "Specific incident details not available in rule documents",
            "Video evidence cannot be processed by text system"
        ],
        "sources": list(set(available_topics))
    }

def run(question: str, top_k: int = 3) -> dict:
    print(f"\n[AGENT] Question: {question}")

    # 1. Retrieve
    print("[AGENT] Retrieving relevant chunks...")
    chunks = retriever.search(question, top_k=top_k)
    print(f"[AGENT] Retrieved {len(chunks)} chunks")

    # 2. Evaluate
    decision, confidence = evaluate_context(chunks)
    print(f"[AGENT] Context evaluation: {decision} (confidence: {confidence:.3f})")

    # 3. Route
    if decision == "POOR":
        print("[AGENT] Insufficient context → abstaining")
        return build_abstention_response(question, chunks)

    # 4. Generate
    prompt = build_generation_prompt(question, chunks, confidence)
    print(f"[AGENT] Generating with {GRANITE_MODEL}...")
    raw_response = call_granite(prompt)

    # 5. Parse & Refine
    result = parse_granite_response(raw_response)
    if decision == "UNSURE" and result.get("confidence", 0) > 0.6:
        result["confidence"] = confidence
        result["missing_evidence"] = result.get("missing_evidence", []) + [
            "Context was partially relevant — answer may be incomplete"
        ]

    print(f"[AGENT] Done. Confidence: {result.get('confidence', 0):.2f}")
    return result

# Initialise retriever once at runtime
print("Initialising DecisionLens CRAG Agent...")
retriever = HybridRetriever()
print("Agent ready.\n")

if __name__ == "__main__":
    test_questions = [
        "What makes a handball deliberate under FIFA rules?",
        "What types of decisions can VAR review?",
        "Was Ronaldo's goal in the 67th minute against France offside?",
        "What is the offside rule in football?"
    ]
    for question in test_questions:
        print("\n" + "="*70)
        result = run(question)
        print(json.dumps(result, indent=2))
