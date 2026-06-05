# DecisionLens Evidence Register

Purpose: every public claim in README, demo video, project page, resume bullets, and presentation must be backed by evidence. If a claim is not in this register or in code/test output, it is not ready for submission.

Status values:

- Verified
- User-provided
- Pending
- Rejected
- Needs update

## Core Challenge Evidence

| ID | Claim | Status | Evidence / Source | Owner | Notes |
|---|---|---|---|---|---|
| CH-001 | June challenge is about soccer, AI, and World Cup understanding. | User-provided | June Challenge Details pasted by Kesav on May 28, 2026. | Kesav | Use soccer/World Cup wording in README, not racing. |
| CH-002 | Submission deadline is June 30, 2026 at 11:59 PM ET. | User-provided | Official challenge text and rules pasted by Kesav. | Kesav | In IST this is July 1, 2026 at 9:29 AM. |
| CH-003 | Project page submissions open after June 3 kickoff webinar. | User-provided | June Challenge Details pasted by Kesav. | Kesav | Recheck after webinar. |
| CH-004 | Required submission items: public GitHub repo, functioning prototype/POC, README, project/team details, repo link, up to 3-minute video. | User-provided | Official challenge text pasted by Kesav. | Kesav | Must be verified on platform before final submission. |
| CH-005 | Judging criteria: Technical Execution, Innovation, Challenge Fit, Implementation and Feasibility. | User-provided | Official rules pasted by Kesav. | Kesav | Each criterion scored 1 to 5, max 20 points. |
| CH-006 | Eligible team size is 1 to 5 participants, one project per monthly challenge. | User-provided | Official rules pasted by Kesav. | Kesav | Make sure every member is individually registered. |
| CH-007 | Repo naming guidance: `teamname-challengemonth-2026`. | User-provided | `D:\Downloads\README (9).md`. | Kesav | Proposed repo: `decisionlens-june-2026` or team-name variant. |
| CH-008 | Current downloaded hands-on lab README is May/TORCS focused and says June lab is coming. | Verified local file | `D:\Downloads\README (8).md`. | Kesav | Recheck GitHub June 1. |

## IBM Tool Evidence

| ID | Claim | Status | Evidence / Source | Owner | Notes |
|---|---|---|---|---|---|
| IBM-001 | IBM Granite is an allowed IBM AI-supported technology. | User-provided | June Challenge Details pasted by Kesav. | Kesav | Exact version pending June lab/webinar. |
| IBM-002 | Docling is an allowed IBM AI-supported technology for knowledge and data handling. | User-provided | June Challenge Details pasted by Kesav. | Kesav | Use for document ingestion. |
| IBM-003 | LangFlow/LangChain is allowed for orchestration. | User-provided | June Challenge Details pasted by Kesav. | Karthi | Use only if it improves clarity. |
| IBM-004 | Context Forge is listed as a gateway/proxy/MCP registry tool. | User-provided | June Challenge Details pasted by Kesav. | Karthi | Stretch until core works. |
| IBM-005 | IBM Bob is listed as a code assistant. | User-provided | June Challenge Details pasted by Kesav. | Kesav | Ask whether Bob counts as runtime or dev assistance. |
| IBM-006 | Granite model/version for final demo. | Pending | Ask June 3 kickoff or IBM tech webinar. | Kesav | Do not hardcode README claim yet. |
| IBM-007 | watsonx.ai is required or optional. | Pending | Ask organizers. | Kesav | Avoid claiming cloud deployment until verified. |

## Product Claims

| ID | Claim | Status | Evidence / Source | Owner | Notes |
|---|---|---|---|---|---|
| PRD-001 | DecisionLens focuses on VAR/decision transparency, not prediction. | Verified | Audited project plan and challenge "Trust and Transparency" category. | Kesav | Product direction locked. |
| PRD-002 | System retrieves official rule/protocol evidence before answering. | Pending | Needs implemented ingestion/retrieval code. | Kesav | README claim only after prototype works. |
| PRD-003 | System cites source snippets. | Pending | Needs UI output and tests. | Kesav | Required for explainability. |
| PRD-004 | System abstains or lists missing evidence when facts are insufficient. | Pending | Needs generation and tests. | Kesav | Critical anti-hallucination feature. |
| PRD-005 | System explains handball, offside, penalty, red card, and VAR reviewability. | Pending | Needs test set coverage. | Kesav/Karthi | Do not claim all categories until tested. |




| ID | Claim | Status | Evidence / Source | Owner | Notes |
|---|---|---|---|---|---|
| DATA-001 | IFAB/FIFA laws can be used as official rule source if public and allowed. | Verified | Laws of the Game 2025/26 Document: https://downloads.theifab.com/downloads/laws-of-the-game-2025-26-single-pages?l=en (Downloaded: 2026-06-05) | Kesav | Extracted size: 2,376,657 bytes. Generated 80 discrete contextual chunks. |
| DATA-002 | VAR protocol source is available and parseable. | Verified | IFAB VAR Official Updates: https://theifab.com (Downloaded: 2026-06-05) | Kesav | Extracted size: 81,221 bytes. Generated 5 discrete contextual chunks. |
| DATA-003 | football-data.org is usable for live metadata. | Pending | Need account, docs, and endpoint test. | Karthi | Do not treat as VAR truth source. |
| DATA-004 | StatsBomb open data can support historical event examples. | Pending | Need license check and sample data test. | Kesav | Not live 2026 data. |
| DATA-005 | ESPN or undocumented APIs are safe for submission. | Rejected | Unsupported and risky as a required dependency. | Kesav | Can be future work only if legal/allowed. |





## Evaluation Evidence

| ID | Claim | Status | Evidence / Source | Owner | Notes |
|---|---|---|---|---|---|
| EVAL-001 | 30-50 golden questions exist. | Pending | Create evaluation file. | Priya/Kesav | Track source section for each answer. |
| EVAL-002 | Citation accuracy score. | Pending | Implement deterministic test. | Kesav | More important than RAGAS alone. |
| EVAL-003 | RAGAS metrics. | Pending | Optional after deterministic checks. | Priya/Kesav | Do not fake scores. |
| EVAL-004 | Latency metric. | Pending | Measure locally and record machine details. | Karthi | Do not claim production latency unless measured. |
| EVAL-005 | Manual fan-understanding review. | Pending | Priya UI review notes. | Priya | Useful for human-centered challenge fit. |

## Team Evidence

| ID | Claim | Status | Evidence / Source | Owner | Notes |
|---|---|---|---|---|---|
| TEAM-001 | Kesav and Karthi are free during vacation and can build heavily. | User-provided | Kesav message on May 28, 2026. | Kesav | Still track actual weekly hours. |
| TEAM-002 | Priya has 2-3 hours/day and C# internship. | User-provided | Priya reply shared by Kesav. | Priya | Plan around limited availability. |
| TEAM-003 | Priya's RAG/LLM project used pretrained Llama and her work was more UI/org/presentation/docs. | User-provided | Priya reply shared by Kesav. | Priya | Do not assign her primary model coding. |
| TEAM-004 | Priya owns README/demo/evaluation support. | Pending | Confirm directly with Priya. | Kesav | Ask now. |
| TEAM-005 | Karthi owns UI/integration support. | Pending | Confirm directly with Karthi. | Kesav | Ask now. |

## Documentation Evidence

| ID | Claim | Status | Evidence / Source | Owner | Notes |
|---|---|---|---|---|---|
| DOC-001 | README includes problem, AI/technical approach, and why it matters in soccer/World Cup context. | Pending | Final README review. | Priya/Kesav | Mandatory. |
| DOC-002 | Demo video is 3 minutes or less. | Pending | Final video timestamp. | Priya | Mandatory. |
| DOC-003 | README avoids unsupported hype and fake metrics. | Pending | Codex review. | Kesav | Use documentation checklist. |
| DOC-004 | Project page text reviewed before publish. | Pending | Codex review. | Kesav | Required before June 28. |

## Daily Evidence Log

### 2026-06-05 (Day 1 Milestone Achieved)

* **Kesav (RAG Pipeline Lead):** 
  - Mitigated a runtime thread-lock bug inside the local environment configuration.
  - Developed and ran a custom zero-dependency layout parsing pipeline to unpack the official IFAB rulesets.
  - Successfully ran `pipeline/chunk_documents.ps1`, generating 80 discrete text blocks for the primary rules manual and 5 discrete blocks for the VAR guidelines.
  - Initialized a brand new Git system baseline locally and forced synchronization to the public GitHub repository layout `Kesav2k04/decisionlens-crag-pipeline-2026`.

* **Karthi (Agent Loop Lead):** 
  - Bypassed international credit card verification e-mandate blocks by moving development to local offline infrastructure.
  - Installed Ollama locally on Windows and successfully cached the `granite3.1-dense:2b` model weights.
  - Designed and ran `pipeline/test_local_granite.py` with an increased 300-second timeout threshold to safely allow model initialization into memory.
  - Verified perfect programmatic output processing the four official VAR review categories (Goals, Penalty kicks, Direct red cards, Mistaken identity).

### 2026-05-28

- Created audited control strategy from original master plan, downloaded README files, pasted official rules, and team constraints.
- Pending: June lab contents, exact Granite path, organizer answers.

