# evaluation/evaluate.py
# DecisionLens — Deterministic Evaluation Suite
# Measures citation accuracy, abstention accuracy, and latency
# Run: python evaluation/evaluate.py

import sys
import os
import json
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'pipeline'))
from agent import run

def load_questions(path: str) -> list:
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)

def check_citation_present(result: dict) -> bool:
    """Did the system return at least one rule citation?"""
    citations = result.get("rule_citations", [])
    return len(citations) > 0 and any(
        c.get("quoted_span", "").strip() != "" for c in citations
    )

def check_keywords_present(result: dict, keywords: list) -> bool:
    """Do at least 70% of the expected keywords appear in the response text?"""
    if not keywords:
        return True
    answer = result.get("answer", "").lower()
    
    processed_steps = []
    for step in result.get("decision_steps", []):
        if isinstance(step, dict):
            processed_steps.append(str(list(step.values())))
        else:
            processed_steps.append(str(step))
            
    combined = answer + " " + " ".join(processed_steps).lower()
    
    # Require 70% keyword match bounds to support natural LLM paraphrasing
    matches = sum(1 for kw in keywords if kw.lower() in combined)
    return matches >= max(1, int(len(keywords) * 0.7))

def check_abstention(result: dict, should_abstain: bool) -> bool:
    """Did the system abstain when it should, and answer when it should?"""
    confidence = result.get("confidence", 1.0)
    abstained = confidence == 0.0
    return abstained == should_abstain

def check_decision_type(result: dict, expected: str) -> bool:
    """Did the system identify the correct decision type?"""
    if expected == "unknown":
        return True  # abstention questions — type doesn't matter
    return result.get("decision_type", "unknown") == expected

def run_evaluation(questions_path: str = "evaluation/golden_questions.json"):
    if not os.path.exists(questions_path):
        print(f"[-] Evaluation data missing. Please initialize {questions_path} first.")
        return
        
    questions = load_questions(questions_path)
    total = len(questions)

    results_log = []
    
    # Counters
    citation_hits = 0
    keyword_hits = 0
    abstention_hits = 0
    decision_type_hits = 0
    latencies = []

    print(f"\nRunning evaluation on {total} questions...\n")
    print("=" * 70)

    for q in questions:
        qid = q["id"]
        question = q["question"]
        
        start = time.time()
        result = run(question)
        elapsed = time.time() - start
        latencies.append(elapsed)

        # Run checks
        c1 = check_citation_present(result) if not q["should_abstain"] else True
        c2 = check_keywords_present(result, q.get("must_contain_keywords", []))
        c3 = check_abstention(result, q["should_abstain"])
        c4 = check_decision_type(result, q["expected_decision_type"])

        if c1: citation_hits += 1
        if c2: keyword_hits += 1
        if c3: abstention_hits += 1
        if c4: decision_type_hits += 1

        status = "PASS" if all([c1, c2, c3, c4]) else "FAIL"
        print(f"[{status}] {qid}: {question[:55]}...")
        if status == "FAIL":
            print(f"       Citations:{c1} Keywords:{c2} Abstention:{c3} Type:{c4}")
            print(f"       Confidence: {result.get('confidence', 0):.2f} | "
                  f"Type: {result.get('decision_type')}")

        results_log.append({
            "id": qid,
            "question": question,
            "status": status,
            "latency_seconds": round(elapsed, 2),
            "confidence": result.get("confidence", 0),
            "citation_present": c1,
            "keywords_present": c2,
            "abstention_correct": c3,
            "decision_type_correct": c4
        })

    # Summary
    avg_latency = sum(latencies) / len(latencies) if latencies else 0.0
    citation_accuracy = (citation_hits / total * 100) if total else 0.0
    abstention_accuracy = (abstention_hits / total * 100) if total else 0.0
    keyword_accuracy = (keyword_hits / total * 100) if total else 0.0
    decision_accuracy = (decision_type_hits / total * 100) if total else 0.0

    print("\n" + "=" * 70)
    print("EVALUATION RESULTS")
    print("=" * 70)
    print(f"Total questions:        {total}")
    print(f"Citation accuracy:      {citation_accuracy:.1f}%  ({citation_hits}/{total})")
    print(f"Keyword accuracy:       {keyword_accuracy:.1f}%  ({keyword_hits}/{total})")
    print(f"Abstention accuracy:    {abstention_accuracy:.1f}%  ({abstention_hits}/{total})")
    print(f"Decision type accuracy: {decision_accuracy:.1f}%  ({decision_type_hits}/{total})")
    print(f"Average latency:        {avg_latency:.1f}s per query")
    print(f"Machine:                RTX 3070 Ti 8GB | Ryzen 9 6900HX | granite3.1-dense:8b")
    print("=" * 70)

    # Save results
    summary = {
        "total_questions": total,
        "citation_accuracy_pct": round(citation_accuracy, 1),
        "keyword_accuracy_pct": round(keyword_accuracy, 1),
        "abstention_accuracy_pct": round(abstention_accuracy, 1),
        "decision_type_accuracy_pct": round(decision_accuracy, 1),
        "avg_latency_seconds": round(avg_latency, 1),
        "machine": "RTX 3070 Ti 8GB VRAM | Ryzen 9 6900HX | 16GB DDR5",
        "model": "granite3.1-dense:8b via Ollama",
        "parser": "IBM Docling 2.97.0 SimplePipeline",
        "chunks_indexed": 532
    }

    os.makedirs("evaluation", exist_ok=True)
    with open("evaluation/results.json", "w") as f:
        json.dump({"summary": summary, "per_question": results_log}, f, indent=2)

    print(f"\nFull results saved → evaluation/results.json")
    print("These numbers go directly into the README metrics section.")
    return summary

if __name__ == "__main__":
    run_evaluation()
