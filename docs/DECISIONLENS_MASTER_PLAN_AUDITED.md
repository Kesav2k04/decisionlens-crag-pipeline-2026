# DecisionLens Master Plan Audited

IBM SkillsBuild AI Builders Challenge, June 2026

Last updated: May 28, 2026, IST

This file replaces the earlier `DECISIONLENS_MASTER_PLAN.md` for planning and execution. The earlier file is useful as brainstorming history, but it contains risky assumptions and must not be followed blindly.

## 1. Executive Decision

Build DecisionLens as a focused, prize-safe advanced RAG project:

DecisionLens helps football fans understand controversial soccer decisions, especially VAR-style incidents, by retrieving official rule/protocol evidence and generating a plain-language explanation with citations, confidence, and missing-evidence warnings.

The project should optimize for four outcomes at the same time:

1. Prize competitiveness in IBM judging.
2. Deep learning for Kesav and Karthi.
3. A resume-worthy advanced RAG system.
4. A clean, honest, well-documented public GitHub repository.

The winning strategy is not "Claude builds everything." The winning strategy is controlled AI-assisted engineering: Claude teaches, drafts, codes in small increments, and reviews, while the team verifies every claim through files, tests, sources, and human judgment.

## 2. Official Challenge Fit

The June challenge asks for an AI-powered solution that helps humans understand soccer before, during, or after the match. It explicitly welcomes:

- Tactical explainability.
- Trust and transparency.
- Fan understanding.
- Human performance under pressure.

It explicitly discourages:

- Pure score or outcome prediction.
- Replacing referees, coaches, or players.
- Static dashboards with little meaningful AI.
- Fantasy-only, meme, or trivia projects.
- Non-explainable or opaque AI.
- Ignoring the emotional, cultural, or human side of the game.

DecisionLens should target the strongest category:

Trust and Transparency: explainable VAR companions, decision reconstruction, and referee-decision clarity.

This is more distinctive than a generic match explainer or score predictor, and it naturally supports the challenge's human-centered explainability theme.

## 3. Hard Corrections To The Earlier Plan

Follow these corrections before starting any build work:

1. Do not depend on live VAR data.
   - football-data.org may provide matches, scores, lineups, cards, and related competition data, but it is not a guaranteed source of live VAR incident reasoning.
   - Treat live data as optional metadata, not the core proof source.

2. Correct the World Cup timing assumption.
   - The earlier plan said the Round of 32 starts June 26 or June 27. That is unsafe. Verified public schedule information indicates the Round of 32 starts June 28, 2026.
   - The demo should not depend on knockout-stage live incidents before submission.

3. Do not assign Priya as primary RAG architect.
   - Priya said she has 2-3 hours/day, has a C# internship, worked on a RAG/LLM project, but mostly handled UI, organization, presentation, and documentation.
   - Her best role is documentation lead, demo/pitch lead, UI reviewer, evaluation dataset support, and project coordination.
   - Kesav and Karthi own core RAG implementation with Claude Code guidance.

4. Use IBM tools deeply, not decoratively.
   - The rules require at least one IBM AI-supported technology. The strategy should use Granite, Docling, and LangFlow/LangChain clearly.
   - Context Forge is a stretch goal only after the core RAG app, UI, evaluation, and README are working.

5. Do not overpromise Granite version or cloud path.
   - Prefer IBM Granite as the required LLM family.
   - Verify the exact model/version after the June lab and kickoff webinar.
   - If Granite 4.1 is available and allowed, prefer it. If the lab requires Granite 3.x, follow the lab.

6. Do not fake evaluation metrics.
   - RAGAS is useful, but deterministic citation tests are mandatory.
   - README metrics must come from committed scripts, logs, or reproducible runs.

7. Do not write "locked, no changes."
   - The product direction is locked.
   - Tool versions, APIs, and implementation details stay adaptable until the June lab and webinar clarify requirements.

8. Use Windows-first setup instructions.
   - The team is on Windows laptops. Do not paste Linux-only setup commands unless explicitly marked as WSL/Linux.

9. Do not let Claude change scope.
   - Any shift away from VAR/decision transparency needs explicit approval from Kesav after Codex review.

## 4. Final Product Scope

### In Scope For V1

- Ingest official soccer law/protocol documents with Docling.
- Chunk and index relevant rule text.
- Retrieve evidence for user questions about handball, offside, penalty, red card, and VAR reviewability.
- Generate grounded explanations using IBM Granite.
- Show citations and source snippets in the UI.
- Provide an uncertainty/missing-evidence response when the facts are not enough.
- Provide a small evaluation set of 30-50 golden questions.
- Provide deterministic checks for citation presence and source grounding.
- Provide a polished README and 3-minute demo video.

### Stretch Scope

- LangFlow visual orchestration diagram.
- RAGAS metrics.
- football-data.org metadata lookup.
- Context Forge MCP gateway.
- multilingual explanation.
- live match metadata.

### Out Of Scope

- score prediction.
- fantasy football.
- replacing referees.
- fully automated legal correctness claims.
- live VAR truth determination from video.
- undocumented ESPN scraping as a required feature.
- huge multi-agent architecture before the basic prototype works.

## 5. Architecture

Primary flow:

1. User asks a soccer decision question.
2. Query processor extracts decision type and key terms.
3. Retriever searches official document chunks using hybrid retrieval.
4. Reranker selects the strongest evidence.
5. Evidence checker decides whether enough source support exists.
6. Granite generates a structured answer using only retrieved evidence.
7. UI displays answer, citations, source snippets, confidence, and missing evidence.
8. Evaluation scripts test whether answers cite sources and abstain when needed.

Recommended response schema:

```json
{
  "answer": "Plain-language explanation for a football fan.",
  "decision_type": "handball | offside | penalty | red_card | var_reviewability | unknown",
  "rule_citations": [
    {
      "source": "IFAB Laws of the Game 2025/26",
      "law_or_section": "Law 12",
      "quoted_span": "Exact retrieved text or short source phrase"
    }
  ],
  "decision_steps": [
    "Step-by-step reasoning grounded in retrieved evidence"
  ],
  "confidence": 0.0,
  "missing_evidence": [
    "What facts are missing, if any"
  ],
  "sources": [
    "Document title, page/section/chunk id"
  ]
}
```

Rules for this schema:

- `confidence` is not a truth score. It means evidence sufficiency.
- If the retrieved context is weak, the answer must say what is missing.
- Every legal/rule claim must connect to a source snippet.
- Do not cite a rule section unless the retriever actually returned it.

## 6. Technology Strategy

### Required Core

- IBM Granite: final grounded explanation generation.
- Docling: parse official PDF/HTML rule documents into structured text.
- LangChain or simple Python orchestration: connect ingestion, retrieval, prompt, and evaluation.
- Streamlit or similar lightweight UI: demo prototype.
- GitHub public repository: clean, reproducible project.

### Recommended Supporting Tools

- ChromaDB or FAISS: vector index.
- BM25/rank_bm25: exact keyword retrieval.
- sentence-transformers reranker: reranking if time allows.
- RAGAS: optional quality metrics after deterministic tests work.
- pytest: deterministic tests.

### Stretch

- LangFlow: visual diagram for demo and judging.
- Context Forge: MCP gateway for retrieval or metadata tools.
- football-data.org: optional match metadata only.

## 7. Team Roles

### Kesav

Owner: product direction, RAG learning, ingestion/retrieval, Claude Enterprise coordination, final quality gate.

Responsibilities:

- Keep project aligned to VAR/decision transparency.
- Use Claude Enterprise for learning, design review, and documentation critique.
- Own Docling ingestion and retrieval pipeline with Karthi.
- Maintain evidence register.
- Run Codex review at milestones.
- Ensure final README and demo do not contain unsupported claims.

### Karthi

Owner: app integration and implementation support.

Responsibilities:

- Work with Kesav on Claude Code implementation.
- Own Streamlit UI or frontend integration.
- Own LangFlow/LangChain visualization if included.
- Keep daily commits or progress notes.
- Explain each module he touches in simple language.

### Priya

Owner: documentation, demo narrative, evaluation support, fan-perspective review.

Responsibilities:

- Own README draft structure after technical facts are provided.
- Build or help build 30-50 evaluation questions from official rules.
- Review UI from a non-expert fan perspective.
- Lead demo script and presentation flow.
- Attend two fixed weekly check-ins if possible.
- Do not become the bottleneck for core RAG code.

## 8. Claude Usage Strategy

### Claude Enterprise Web Project

Use for:

- Understanding RAG concepts.
- Brainstorming with uploaded project files.
- Reviewing architecture.
- Critiquing README and demo script.
- Explaining code to beginners.
- Checking documentation for unsupported claims.

Do not use for:

- Blindly generating huge codebases.
- Making final technical claims without evidence.
- Changing the product direction.
- Producing generic marketing language.

### Claude Code

Use for:

- Reading the repo.
- Planning small implementation steps.
- Editing files.
- Running tests.
- Explaining diffs.
- Updating docs with verified facts.

Mandatory rule:

Claude Code must read `CLAUDE.md` first and follow it. If Claude Code starts drifting, paste: "Stop. Re-read CLAUDE.md and DECISIONLENS_MASTER_PLAN_AUDITED.md. Return to the current milestone only."

### Karthi And Claude Enterprise

Do not share login credentials. If Karthi needs Claude Enterprise support, use pair programming, screen sharing, or paste the specific task/files into Kesav's session and send him the reviewed output.

## 9. Daily Workflow

Every build day should follow this loop:

1. Daily start.
   - What did we finish yesterday?
   - What is today's single target?
   - What files must Claude inspect?
   - What is the acceptance check?

2. Learning block.
   - Claude explains the concept in beginner language.
   - Team writes a short note in `notes/learning-log.md` or equivalent.

3. Implementation block.
   - One feature at a time.
   - Small edits.
   - Tests or manual verification.

4. Evidence update.
   - Add source, test, metric, screenshot, or log to evidence register.

5. End of day.
   - What works?
   - What failed?
   - What is blocked?
   - What must not be changed tomorrow?

## 10. Milestone Roadmap

### May 28 to June 3: Ground Truth And Setup

Deliverables:

- Public repo created with challenge naming convention.
- Official requirements copied into evidence register.
- June lab checked when available.
- IBM kickoff notes captured.
- Windows setup instructions drafted.
- First Docling parse tested.
- First Granite call tested locally or via watsonx, depending on access.
- Claude project instructions installed.

Questions to ask organizers after checking docs:

- Does June lab require a specific IBM tool path?
- Is local Granite via Ollama acceptable in demo, or must final demo call watsonx.ai?
- Are curated incident briefs acceptable when live VAR event data is unavailable?
- Does IBM Bob count only as development assistance or as submitted technology?

### June 4 to June 10: Retrieval Core

Deliverables:

- Official documents ingested.
- Chunk metadata includes source, section, page if available, and chunk id.
- BM25 plus vector search working.
- A small manual test set proves the retriever can find handball, offside, penalty, and VAR reviewability sections.
- Retrieval debug page or CLI prints top chunks.

Learning goals:

- embeddings.
- BM25.
- chunking.
- citation grounding.

### June 11 to June 17: Grounded Generation

Deliverables:

- Granite answer generation with JSON schema.
- Evidence sufficiency check.
- "I do not have enough evidence" behavior.
- 10 golden questions.
- Basic UI with answer, citations, and source snippets.

Learning goals:

- prompt design.
- structured outputs.
- hallucination control.
- source-grounded generation.

### June 18 to June 24: Evaluation And Polish

Deliverables:

- 30-50 evaluation questions.
- deterministic citation tests.
- optional RAGAS run.
- improved UI.
- README technical draft.
- LangFlow diagram if useful and stable.

Learning goals:

- evaluation.
- test design.
- UX for explainability.
- technical writing.

### June 25 to June 28: Freeze And Submit

Deliverables:

- Feature freeze on June 25.
- README final draft reviewed by Codex.
- demo video script reviewed by Codex.
- project page text reviewed by Codex.
- submit by June 28.

### June 29 to June 30: Buffer

Only fix:

- submission platform issues.
- broken setup steps.
- documentation errors.
- minor demo packaging.

Do not add new core features.

## 11. Questions To Ask Team Members

Ask Priya now:

1. Can you own README and demo script drafts if we provide the verified technical facts?
2. Can you help create 30-50 evaluation questions from official laws and protocols?
3. Can you test the UI as a non-expert fan and mark confusing outputs?
4. Can you join two fixed weekly calls until submission?
5. Which days will your internship reduce your available time?

Ask Karthi now:

1. Can you own Streamlit UI and integration?
2. Can you run Claude Code locally, or should we pair through Kesav's Claude Enterprise sessions?
3. Can you commit daily progress or send a daily update?
4. Can you explain each file you touch back to the team?
5. Can you attend the June 3 and June 4 webinars?

## 12. Documentation Standard

All documentation must pass the `DOCUMENTATION_QUALITY_CHECKLIST.md`.

Core rules:

- No generic AI language.
- No fake metrics.
- No unsupported claims.
- No repeated filler.
- No claims that hide AI assistance.
- No copied text from sources except short, attributed excerpts where permitted.
- Use clear, specific, measured language.

Preferred style:

DecisionLens retrieves official football rule evidence and explains controversial decisions in plain language. It shows what rule text was used, what facts are missing, and how confident the system is in the available evidence.

Avoid:

DecisionLens leverages cutting-edge AI to revolutionize the fan experience with seamless insights.

## 13. Review Gates

Codex review is required before:

- final architecture lock.
- first public README draft.
- demo video script.
- project page text.
- final submission.

Claude review is useful but not final. Claude can draft. Codex reviews. Humans decide.

## 14. Acceptance Criteria

The project is submission-ready only when:

- The public repo opens cleanly.
- Setup instructions work on a fresh machine or are clearly marked as tested/untested.
- The prototype runs.
- At least one strong demo query returns a cited answer.
- At least one uncertainty query abstains or lists missing evidence.
- README explains IBM tool use accurately.
- Evaluation results are reproducible or clearly marked as manual.
- Demo video is under 3 minutes.
- Project page includes the repo link and video.
- Submission is published on the platform before the deadline.

## 15. Source Basis And Pending Verifications

Known from user-provided official challenge text:

- Deadline: June 30, 2026 at 11:59 PM ET.
- Project page opens after June 3 kickoff webinar.
- Public GitHub repo required.
- Functioning prototype or proof of concept required.
- README must include problem, AI/technical approach, and why it matters in soccer/World Cup context.
- Up to 3-minute video required.
- Judging criteria: Technical Execution, Innovation, Challenge Fit, Implementation and Feasibility.
- Each criterion scored 1 to 5 for a maximum of 20 points.
- IBM-supported tools include Granite, LangFlow/LangChain, Docling, Context Forge, IBM Bob, or related tools.

Known from downloaded README files:

- `README (8).md` is mostly May lab guidance and says June lab is coming.
- `README (9).md` says team repositories should follow `teamname-challengemonth-2026` format and be public before submission.

Pending verification after June lab opens:

- exact June lab contents.
- exact recommended IBM Granite model.
- watsonx.ai access details.
- whether local Ollama Granite is acceptable for final demo.
- any required IBM Bob usage.
- whether Context Forge has a specific expected path.
- any updated official rules.

