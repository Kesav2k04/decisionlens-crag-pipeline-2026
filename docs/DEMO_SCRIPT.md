# DecisionLens — 3-Minute Demo Script

Total runtime: 3:00. Record screen + voiceover. The Streamlit app must already be running
(`streamlit run app/main.py`) with Ollama serving `granite3.1-dense:8b` before recording starts.
Every claim below is traceable to the evidence register (IDs in brackets).

---

## 0:00–0:25 — Problem

**On screen:** A still of a World Cup VAR review (referee at the monitor), then cut to the IFAB Laws of the Game PDF scrolling — hundreds of pages.

**Say:**
> "When VAR overturns a goal, fans see the signal but never the reasoning. The rule that decided it is buried somewhere in 200-plus pages of the IFAB Laws of the Game and a separate VAR Protocol. Chatbots will happily explain the call — and routinely invent the rule. DecisionLens answers from the official text only, shows its citations, and refuses when the evidence isn't there." [PRD-001, CH-001]

## 0:25–1:25 — Live prototype

**On screen:** The DecisionLens app. Type question 1 and submit:

**Question 1:** `What are the four categories of decisions that VAR can review?`

**Expected output:** A cited answer listing goal/no goal, penalty/no penalty, direct red card, and mistaken identity; the brass dial shows evidence sufficiency around 74%; citation cards quote the IFAB VAR Protocol; "Documents Consulted" shows the VAR Protocol accession label. [PRD-002, PRD-003]

**Say (while it generates, ~10 seconds):**
> "Every answer is built from retrieved rule text — here it finds the VAR Protocol's review categories, quotes the exact span, and shows a confidence score that measures evidence sufficiency, not certainty."

**Then type question 2:**

**Question 2:** `Was Neymar's handball in the 2026 World Cup final against Argentina deliberate?`

**Expected output:** Immediate abstention — confidence 0%, the red wax seal panel "Evidence Not Before the Register" listing "Specific incident details not available in rule documents" and "Video evidence cannot be processed by text system". [PRD-004]

**Say:**
> "Ask about a specific incident, and it refuses. It has no video and no match data, and it says so instead of guessing. This abstention behavior is tested, not accidental."

## 1:25–2:05 — Architecture walkthrough

**On screen:** The architecture diagram from the README, then 5 seconds of the LangFlow Playground running the DecisionLens CRAG Agent component.

**Say:**
> "Under the hood: IBM Docling parses the two official IFAB PDFs into 593 section chunks. A hybrid retriever combines BM25 keyword search and nomic-embed-text vectors through Reciprocal Rank Fusion. A corrective-RAG evaluator scores the evidence — above 0.75 it answers, below 0.65 it abstains. IBM Granite 3.1 8B, running locally through Ollama, generates the structured answer in strict JSON, using only the retrieved chunks. The same pipeline is exposed as a LangFlow custom component." [IBM-001, IBM-002, DATA-001, DATA-002]

## 2:05–2:35 — Evaluation results

**On screen:** `evaluation/results.json` summary block, or the metrics table from the README.

**Say:**
> "We test with 50 golden questions and deterministic checks. Citation accuracy: 100 percent — all 50 answers cite real rule text. Abstention accuracy: 100 percent — every incident-specific trap question was refused. Keyword accuracy 100 percent, decision-type classification 100 percent, average latency 9.3 seconds per question on an RTX 3070 Ti. All numbers are in results.json in the repo." [EVAL-001 through EVAL-004]

## 2:35–3:00 — Impact and limitations

**On screen:** The app idle on the crest header.

**Say:**
> "DecisionLens makes the rule basis of refereeing decisions inspectable for any fan — which is what trust in officiating actually requires. Its limits are deliberate: it explains rules, it does not judge officials; it cannot see video, so it never claims to know what happened in an incident; and confidence means evidence sufficiency, not correctness. Built with IBM Granite, IBM Docling, and LangFlow for the IBM SkillsBuild AI Builders Challenge." [PRD-001, limitations per checklist]

---

## Recording notes

- Do not show code files or long terminal scrolls; the architecture section uses the diagram only.
- If question 1's latency exceeds 15 seconds in the take, re-record — warm up Ollama with one query before recording.
- Verify final video length ≤ 3:00 before upload (DOC-002).

