# DecisionLens — Master Project Plan
## IBM SkillsBuild BeMyApp June Challenge 2026
### Team: [You], Karthi, Priya | Deadline: June 30, 2026 @ 11:59 PM ET

---

## PART 0: AUDIT OF THE PREVIOUS PLAN — MISTAKES FOUND

This section documents every flaw in the Gemini-generated plan and the prior response. 
Do not skip this. Understanding why the previous plan was wrong IS part of the deep learning.

---

### MISTAKE 1 — Wrong Timeline (Critical)
**What was said:** "30-day plan"  
**Reality:** May 28 to June 30 is 33 days. Small difference but your weekly phases were miscounted, causing overlap with IBM's own webinar schedule.  
**Fix:** The roadmap below is date-accurate to the day.

---

### MISTAKE 2 — Problem Statement Was Too Generic (Critical for Prizes)
**What was said:** "Tactical Explainer" — explain why substitutions worked, why momentum shifted.  
**Reality:** Every team at this hackathon will build a tactical explainer. The challenge document explicitly lists it as the first example under "Understanding & Explanation." You will drown in a sea of identical projects.  
**Fix:** The correct category to target is "Trust & Transparency — Explainable VAR companions, decision reconstruction tools." This is the hardest, most novel category. Most teams will avoid it because VAR requires understanding FIFA Laws of the Game deeply. That difficulty is your moat.  
**The new problem:** Billions of fans watch VAR reviews and have no idea what is happening or why. The decision takes 4 minutes on screen, nobody explains it, trust in referees collapses. Your system reconstructs the decision step-by-step with exact rule citations. This wins Most Innovative.

---

### MISTAKE 3 — Priya Was Reduced to a Documentation Role (Severe)
**What was said:** "Priya leads documentation, README, demo video. She is not a passenger."  
**Reality:** Priya has a published IEEE paper (DOI: 10.1109/ICAECA63854.2025.11012384, ICAECA 2025) on RAG/LLM systems. She has implemented a full RAG pipeline at the level required to publish in a peer-reviewed venue. Assigning her documentation is a catastrophic waste of your best technical asset. She understands RAG evaluation, which neither of you likely know deeply yet.  
**Fix:** Priya owns the evaluation framework (RAGAS metrics). She also co-owns the RAG retrieval layer. Her IEEE paper IS your secret weapon — the approach in that paper should inform your architecture, not sit in her portfolio unused.

---

### MISTAKE 4 — Cohere Reranker Recommended Without Noting It's Paid
**What was said:** "Pass top 25 results through a Cohere Reranker"  
**Reality:** Cohere's reranker API requires paid access beyond free tier limits. For a hackathon build over 33 days with heavy testing, you will hit the limit or be charged.  
**Fix:** Use `cross-encoder/ms-marco-MiniLM-L-6-v2` from HuggingFace. It is free, runs on CPU in under 200ms per batch, and achieves near-identical reranking quality. Your RTX 3070 Ti makes this trivially fast.

---

### MISTAKE 5 — Hardware Was Completely Ignored
**What was said:** "Set up IBM watsonx.ai API" — implied cloud-only workflow  
**Reality:** You have an RTX 3070 Ti with 8GB VRAM. You can run IBM Granite 3.1 8B Instruct at Q4_K_M quantization (approximately 5.5GB VRAM) fully locally via Ollama. Karthi with 4GB VRAM can run Granite 3B Q4 locally.  
**Why this matters:**
1. During development you do not burn IBM API credits on every test call
2. Your demo can show "this runs locally, data never leaves your machine" — a genuine enterprise selling point IBM judges care about
3. Embedding models (nomic-embed-text, all-minilm) are tiny and run on CPU — cost zero API calls
**Fix:** Development uses local Granite via Ollama. Final demo uses IBM watsonx.ai API to demonstrate cloud scalability. Both paths in the README.

---

### MISTAKE 6 — LangFlow Was Listed as a Tool but the Plan Said "Avoid Frameworks" — Contradiction
**What was said:** "Use IBM tools minimally. Wrap your custom logic in LangFlow at the end."  
**Reality:** The challenge judges are IBM employees. LangFlow is explicitly listed as a required core tool. "Minimally using it at the end" signals to judges you do not understand it.  
**Fix:** LangFlow serves a specific purpose in your architecture: it is the visual orchestration layer. Your CRAG agent logic stays in pure Python. LangFlow wraps and visualizes the flow for the demo. Judges see a beautiful flow diagram. You understand the internals. This is not a contradiction — it is layered architecture.

---

### MISTAKE 7 — Context Forge Was Ignored
**What was said:** One passing mention, no role defined  
**Reality:** Context Forge is IBM's MCP (Model Context Protocol) gateway and proxy. It lets you define your tools (live match data API, FIFA rules search, VAR protocol lookup) as MCP-compatible endpoints that Granite can call natively. This is the correct IBM-native way to implement the "tool use" part of your CRAG agent. Using it properly demonstrates you understand IBM's agentic stack at the infrastructure level.  
**Fix:** Your three agent tools (live_match_data, fifa_rules_lookup, var_protocol_search) are exposed through Context Forge as MCP tools. Granite calls them through the gateway. This is the correct architecture.

---

### MISTAKE 8 — No RAG Evaluation Framework Mentioned
**What was said:** "Track retrieval precision manually"  
**Reality:** "Manually" is not scientific and has zero resume value. RAGAS (Retrieval Augmented Generation Assessment) is the standard evaluation framework for production RAG systems. It measures faithfulness (did the answer come from context?), answer relevancy, context precision, context recall. These metrics are what separates a "student project" from a "production RAG pipeline" in an interview.  
**Fix:** Priya owns this. She almost certainly used evaluation metrics in her IEEE paper. RAGAS numbers go in the README and the demo.

---

### MISTAKE 9 — No Live Data API Strategy
**What was said:** "Collect 10-15 PDFs of tactical analysis"  
**Reality:** The World Cup starts June 11. That means from Week 2 of your project there are real live matches happening. Your system should be able to fetch live match event data, not just static PDFs.  
**Fix:** football-data.org has a free tier (10 calls/minute, sufficient for hackathon). StatsBomb has open-data on GitHub (historical match data, detailed event data). These are your live and historical data sources respectively. Static knowledge base: FIFA documents. Dynamic: live match APIs.

---

### MISTAKE 10 — The CRAG Evaluator Architecture Was Wrong
**What was said:** "Use IBM Granite to evaluate whether retrieved context is relevant"  
**Reality:** Calling a full 8B parameter LLM just to decide "is this relevant?" wastes tokens, increases latency, and increases cost. The correct architecture uses a dedicated cross-encoder (small model, fast) for relevance scoring. Save the large LLM call for the final synthesis step only.  
**Fix:** Cross-encoder for relevance evaluation (CPU, free, fast). IBM Granite only for final answer synthesis. This reduces your LLM API calls by 60-70%, which is a quantifiable metric for your resume.

---

### MISTAKE 11 — World Cup Timeline Not Integrated Into Project Plan
**What was said:** Nothing about live matches  
**Reality:** World Cup group stage runs June 11 - June 26. Round of 32 runs June 27 - July 3. Your submission deadline is June 30. This means during your final week, there are live Round of 32 matches and active VAR decisions happening in real time. Your demo can use REAL matches that just happened. This is a massive advantage. Build it in.

---

### MISTAKE 12 — No Mention of RAGAS or Automated Testing Pipeline
**What was said:** "Run 20 real questions and log results"  
**Reality:** Logging manually is fine for Week 3. But for the submission, you need an automated evaluation script that runs a test set, computes RAGAS metrics, and produces a results table. That table is what you put in your README. Judges see numbers, not claims.

---

## PART 1: THE CORRECT PROBLEM STATEMENT (LOCKED)

### Project Name: DecisionLens

**Problem:**  
VAR (Video Assistant Referee) is the most controversial technology in modern soccer. During the FIFA World Cup 2026, when a VAR review happens — an offside check, a handball decision, a penalty review — billions of fans watch a black screen for 3-5 minutes and receive only a one-word verdict: "Overturned" or "Confirmed." No explanation. No rule reference. No transparency.

This is not a minor fan experience problem. It is a trust problem. Fans who do not understand the decision feel cheated regardless of whether it was correct. Referees receive death threats over misunderstood decisions. Broadcasters cannot explain the decision in real time because they do not have a system to do it.

**Your solution:**  
DecisionLens is a retrieval-grounded reasoning engine that reconstructs any VAR decision or tactical shift in plain language, with exact FIFA rule citations, step-by-step reasoning, and a confidence score — in under 10 seconds.

**User asks:**  
"Why was Messi's goal disallowed in the 67th minute? The VAR took 4 minutes. Was the arm in an unnatural position?"

**System does:**  
1. Identifies entities: player, minute, match, decision type (handball/offside/penalty)  
2. Retrieves from FIFA Laws of the Game (Law 12 — handball definition, natural vs unnatural position)  
3. Retrieves from VAR protocol document (steps for handball review)  
4. Retrieves from match event data (what actually happened at minute 67)  
5. CRAG evaluator: Is this context sufficient to explain the decision? If not, triggers live data fallback  
6. Synthesizes explanation with exact rule citations and a confidence score  

**Output:**  
"Under FIFA Law 12, a handball is considered deliberate if the arm is in an unnatural position. In the 67th minute, the VAR reviewed whether [player]'s arm created an unnatural silhouette. The review process involves [X steps per VAR protocol]. The decision was confirmed/overturned because [rule condition met/not met]. Confidence: 87% (based on retrieved rule text match)."

---

### Why This Wins All Three Prize Categories

**1st Place (Technical Execution):**  
Hybrid search + CRAG loop + cross-encoder reranker + IBM Granite + Docling parsing of FIFA PDFs + Context Forge MCP tools + RAGAS evaluation. This is a complete, measurable, production-grade pipeline.

**Most Innovative:**  
No team will build VAR transparency. It requires understanding FIFA law at a document level, not just soccer statistics. Your combination of legal document retrieval + live event data + self-correcting RAG is genuinely novel.

**Best Use of Technology:**  
Docling parses FIFA's complex multi-column PDFs and table-heavy documents accurately. Granite generates grounded explanations. LangFlow visualizes the flow. Context Forge exposes live match tools as MCP endpoints. You are using every IBM tool for a real purpose, not decoration.

---

## PART 2: FULL SYSTEM ARCHITECTURE

```
                        [ User Query ]
                        "Why was the goal disallowed?"
                               │
                               ▼
                    [ Query Processor ]
                    ├── Entity extraction (player, minute, match, decision type)
                    ├── Sub-question decomposition
                    │   ├── "What is the Law 12 handball rule?"
                    │   ├── "What is the VAR review process for handball?"
                    │   └── "What happened in that specific match at that minute?"
                    └── Query expansion for hybrid search
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
          [ Dense Vector Search ]  [ Sparse BM25 Search ]
          (semantic meaning:        (exact keywords:
           "unnatural arm            "Law 12", "handball",
            position", "VAR")        "natural silhouette")
                    └──────────┬──────────┘
                               ▼
               [ Reciprocal Rank Fusion ]
               (merges both ranked lists mathematically)
                               │
                               ▼
              [ Cross-Encoder Reranker ]
              (ms-marco-MiniLM-L-6-v2, runs on CPU)
              Input: top 20 fused results
              Output: top 5 truly relevant chunks
                               │
                               ▼
           ┌─────────[ CRAG Evaluator ]─────────┐
           │   "Is this context sufficient?"    │
           │   Uses cross-encoder relevance     │
           │   scoring, NOT a full LLM call     │
           └────────────────────────────────────┘
                    │                │
              SUFFICIENT        INSUFFICIENT
                    │                │
                    ▼                ▼
          [ Context Compressor ]  [ Context Forge MCP Tools ]
          Strip irrelevant        ├── live_match_data(match_id, minute)
          sentences before        ├── fifa_rules_lookup(law_number)
          LLM call                └── var_protocol_search(decision_type)
                    │                │
                    └──────┬─────────┘
                           ▼
              [ IBM Granite 3.1 8B Instruct ]
              (via watsonx.ai API for production,
               Ollama GGUF Q4_K_M for development)
              System prompt: "You are a FIFA rules
              expert. Answer ONLY from provided context.
              Always cite the specific Law or protocol
              section. Include a confidence score."
                           │
                           ▼
              [ Response with Citations ]
              ├── Plain language explanation
              ├── Exact FIFA rule references
              ├── Decision reconstruction steps
              └── Confidence score (0-100%)
                           │
                           ▼
              [ RAGAS Evaluation Layer ]
              (Priya owns this)
              ├── Faithfulness score
              ├── Answer relevancy score
              ├── Context precision
              └── Context recall
```

---

## PART 3: TECHNOLOGY STACK (LOCKED, NO CHANGES)

### IBM Tools (Required — All Four Used Properly)

| Tool | Role in DecisionLens | Why This Impresses Judges |
|------|----------------------|---------------------------|
| IBM Granite 3.1 8B | Final answer synthesis, grounded explanation generation | Used for actual reasoning, not just decoration |
| Docling | Parsing FIFA Laws of the Game PDF, VAR protocol documents, referee manuals | Handles complex multi-column PDFs perfectly |
| LangFlow | Visual orchestration of the entire CRAG pipeline | Judges see the flow visually; you understand the internals |
| Context Forge | MCP gateway exposing live_match_data, fifa_rules_lookup, var_protocol_search as tool endpoints | Shows understanding of IBM's agentic infrastructure |

### Non-IBM Tools (Supporting Layer)

| Tool | Role | Cost |
|------|------|------|
| rank_bm25 | Keyword search for exact FIFA law terms | Free, pip install |
| cross-encoder/ms-marco-MiniLM-L-6-v2 | Reranking and CRAG relevance evaluation | Free, HuggingFace |
| ChromaDB (local file mode) | Vector store during development | Free, local file |
| nomic-embed-text via Ollama | Embedding model during development | Free, local |
| IBM Watson embedding API | Embedding in production (watsonx.ai) | Free tier via IBM access |
| football-data.org API | Live match event data (free tier: 10 calls/min) | Free |
| StatsBomb open-data (GitHub) | Historical detailed match event data | Free, open source |
| RAGAS library | Automated RAG evaluation | Free, pip install |
| Streamlit | Demo frontend | Free |
| GCP $300 credits | Backup LLM calls, additional embedding API | Already have |

---

## PART 4: KNOWLEDGE BASE STRUCTURE

Your knowledge base has two layers: static and dynamic.

### Static Layer (Docling-Parsed Documents)
Collect and parse these with Docling before June 8:

1. FIFA Laws of the Game 2025/26 (official PDF, free download from FIFA.com)
   — Law 12 (Handball), Law 11 (Offside), Law 13 (Free kicks), Law 16 (Goal kicks)
   — This is your primary source for VAR decision explanations
   
2. VAR Protocol and Guidelines (FIFA IFAB document, publicly available)
   — Step-by-step VAR review process
   — Which decisions can be reviewed and which cannot
   — Time limits and communication protocols
   
3. Referee Handbook / Additional Instructions for Match Officials (FIFA)
   — Interpretation of handball "natural silhouette" rule
   — Offside geometry (arm position, shoulder, etc.)

4. World Cup 2026 Tournament Regulations (FIFA)
   — Group stage, knockout format, tiebreaker rules

5. Historical match reports (StatsBomb open data)
   — Past World Cup finals, key controversial decisions
   — Structured event data: every pass, shot, foul by minute

### Dynamic Layer (Live APIs)
During the World Cup (June 11 onwards):

- football-data.org free tier: match events, lineups, goals, cards by match ID
- ESPN public API (undocumented but usable): live match commentary text
- Optionally: web search via Context Forge for post-match referee statements

---

## PART 5: TEAM ROLES (FINAL, NON-NEGOTIABLE)

### [You] — RAG Pipeline Lead
Own the retrieval layer:
- Docling document parsing pipeline
- Semantic chunking implementation  
- ChromaDB vector store setup
- BM25 keyword index setup
- Reciprocal Rank Fusion implementation
- Context compression module

### Karthi — Agent Loop Lead
Own the agentic layer:
- CRAG evaluator (cross-encoder based, not LLM-based)
- Context Forge MCP tool definitions (live_match_data, fifa_rules_lookup, var_protocol_search)
- LangFlow orchestration setup
- Streamlit frontend integration
- IBM Granite API integration (both local Ollama and watsonx.ai)

### Priya — Evaluation + Technical Depth Lead
Own what she actually knows from her IEEE paper:
- RAGAS evaluation framework setup and test suite
- Test question set (minimum 50 questions with ground truth answers from FIFA laws)
- Evaluation results table for README
- Architecture documentation (she understands what she's documenting because she built it in her paper)
- Demo video scripting and narration
- README writing (but technically informed, not generic)

**Critical note about Priya:**  
Her IEEE paper on RAG/LLM means she has seen a production RAG system fail and succeed. In Week 2 when you are debugging retrieval quality, she is the person who knows what good retrieval looks like. Ask her about her paper's methodology. Whatever chunking or retrieval strategy she used there is directly applicable here.

---

## PART 6: LOCAL DEVELOPMENT SETUP (Hardware-Specific)

### Your Machine (RTX 3070 Ti, 8GB VRAM)

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull IBM Granite 3.1 8B Instruct (fits in 8GB VRAM at Q4_K_M)
ollama pull granite3.1-dense:8b

# Pull embedding model (CPU, tiny)
ollama pull nomic-embed-text

# Verify Granite runs
ollama run granite3.1-dense:8b "Explain FIFA Law 12 on handball in 2 sentences"
```

During development, all your LLM calls hit localhost:11434. Zero API costs while learning and testing.

For production/demo: swap the base URL from localhost to IBM watsonx.ai endpoint. The code does not change, only the endpoint and API key.

### Karthi's Machine (RTX 3050, 4GB VRAM)

```bash
# Pull Granite 3B (fits in 4GB VRAM)
ollama pull granite3-dense:2b

# OR run Granite 8B with CPU offloading (slower but works)
OLLAMA_NUM_GPU=20 ollama run granite3.1-dense:8b  # offloads some layers to CPU
```

Karthi should own Context Forge setup and LangFlow, which are less GPU-intensive.

### Cross-Encoder Reranker (Both Machines, CPU)

```python
from sentence_transformers import CrossEncoder

# Downloads once, runs on CPU in milliseconds
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def rerank(query, passages, top_k=5):
    pairs = [[query, passage] for passage in passages]
    scores = reranker.predict(pairs)
    ranked = sorted(zip(passages, scores), key=lambda x: x[1], reverse=True)
    return [passage for passage, score in ranked[:top_k]]
```

---

## PART 7: CORE MATHEMATICAL CONCEPTS (What You Must Understand, Not Just Use)

This section is your learning curriculum. You cannot skip this. Understanding these makes you dangerous in interviews.

### 7.1 — Cosine Similarity (Foundation of Vector Search)

Two text chunks are "similar" if the angle between their embedding vectors is small. 

```python
import numpy as np

def cosine_similarity(vec_a, vec_b):
    """
    Geometrically: measures the cosine of the angle between two vectors.
    Result: 1.0 = identical direction, 0.0 = perpendicular, -1.0 = opposite
    For text embeddings, values typically range from 0.3 to 0.99
    """
    dot_product = np.dot(vec_a, vec_b)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    return dot_product / (norm_a * norm_b)

# What this means intuitively:
# "natural body position handball" and "arm in normal playing position"
# will have cosine similarity ~0.82 (same legal concept, different words)
# "handball rule" and "offside trap formation" will have ~0.31 (unrelated)
```

Run this yourself. Compute similarities between three FIFA rule excerpts. See which ones cluster together. This is the geometry that drives your entire retrieval system.

### 7.2 — BM25 (Why You Need It Alongside Vector Search)

BM25 (Best Match 25) scores documents based on term frequency, normalized by document length. It is algebraically defined as:

```
BM25(q, d) = Σ IDF(qi) × (f(qi,d) × (k1+1)) / (f(qi,d) + k1×(1 - b + b×|d|/avgdl))
```

In plain English: a chunk gets a high BM25 score if it contains your query's exact words frequently, adjusted so long documents are not unfairly favored. Vector search misses "Law 12" and "Article 45" because they are rare exact strings. BM25 finds them instantly. You need both.

### 7.3 — Reciprocal Rank Fusion

When you have two ranked lists (vector search gave you ranks 1-20, BM25 gave you ranks 1-20), how do you merge them? RRF:

```python
def reciprocal_rank_fusion(vector_ranked, bm25_ranked, k=60):
    """
    k=60 is the standard constant. Higher k reduces the influence of top ranks.
    Each document gets score: Σ 1/(k + rank_in_each_list)
    A document ranked #1 in both lists gets: 1/61 + 1/61 = 0.0328
    A document ranked #1 in vector and #5 in BM25 gets: 1/61 + 1/65 = 0.0317
    """
    scores = {}
    for rank, doc_id in enumerate(vector_ranked):
        scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
    for rank, doc_id in enumerate(bm25_ranked):
        scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)
```

### 7.4 — Semantic Chunking (Why Naive Chunking Destroys Context)

```python
def semantic_chunk(text, embedding_fn, similarity_threshold=0.65):
    """
    Split a document at points where meaning shifts,
    not at arbitrary character counts.
    
    Step 1: Split into sentences
    Step 2: Embed each sentence  
    Step 3: Compute similarity between consecutive sentences
    Step 4: Where similarity drops below threshold, start new chunk
    """
    sentences = split_sentences(text)
    embeddings = [embedding_fn(s) for s in sentences]
    
    chunks = []
    current_chunk = [sentences[0]]
    
    for i in range(1, len(sentences)):
        similarity = cosine_similarity(embeddings[i-1], embeddings[i])
        if similarity < similarity_threshold:
            # Topic boundary detected
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentences[i]]
        else:
            current_chunk.append(sentences[i])
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks
```

Test this on FIFA Law 12 (handball). You will see it correctly separates the "deliberate handball" section from the "accidental handball" section as distinct chunks.

### 7.5 — The ReAct Loop (The Agent's Brain)

```python
def crag_agent(user_query, knowledge_base, mcp_tools):
    conversation_history = []
    max_iterations = 5
    
    for iteration in range(max_iterations):
        # Step 1: Retrieve
        vector_results = knowledge_base.vector_search(user_query, top_k=20)
        bm25_results = knowledge_base.bm25_search(user_query, top_k=20)
        fused = reciprocal_rank_fusion(vector_results, bm25_results)
        reranked = rerank(user_query, fused[:20], top_k=5)
        
        # Step 2: Evaluate relevance (cross-encoder, NOT a full LLM call)
        relevance_scores = [reranker.predict([user_query, chunk]) for chunk in reranked]
        avg_relevance = sum(relevance_scores) / len(relevance_scores)
        
        # Step 3: Route
        if avg_relevance > 0.7:
            # Context is good. Compress and synthesize.
            context = compress_context(user_query, reranked)
            answer = granite_synthesize(user_query, context, conversation_history)
            return answer, reranked  # return sources for display
            
        elif avg_relevance < 0.3:
            # Context is bad. Trigger MCP tool fallback.
            entities = extract_entities(user_query)  # match_id, minute, decision_type
            live_data = mcp_tools.call("live_match_data", entities)
            reranked = reranked + [live_data]  # augment context
            # Loop again with richer context
            
        else:
            # Ambiguous. Augment and synthesize.
            entities = extract_entities(user_query)
            web_supplement = mcp_tools.call("fifa_rules_lookup", entities)
            context = compress_context(user_query, reranked + [web_supplement])
            answer = granite_synthesize(user_query, context, conversation_history)
            return answer, reranked
    
    # If we exhausted iterations, return best effort
    return granite_synthesize(user_query, reranked, conversation_history), reranked
```

Every line of this loop is something you must be able to explain in an interview.

---

## PART 8: 33-DAY ROADMAP (MAY 28 — JUNE 30)

All dates are hard. No slippage allowed past one day.

---

### WEEK 1: May 28 – June 3 — Environment and Foundation

**Goal by end of week:** Every team member can make a raw IBM Granite API call AND a raw Ollama call. Priya has parsed at least one FIFA PDF with Docling. GitHub repo exists with folder structure.

#### May 28 (Today) — Setup Day
**[You]:**
- Create GitHub repository: `decisionlens-wc2026`
- Folder structure: `/data/raw`, `/data/chunks`, `/pipeline`, `/agents`, `/evaluation`, `/app`, `/notebooks`
- Add Karthi and Priya as collaborators
- Install Ollama, pull `granite3.1-dense:8b` and `nomic-embed-text`
- Write `test_granite_local.py`: one raw Ollama API call, print response. Commit it.

**Karthi:**
- Install Python environment (Python 3.11, pip, venv)
- Install: `pip install langflow chromadb rank_bm25 sentence-transformers ragas requests streamlit docling`
- Write `test_granite_api.py`: one raw HTTP request to IBM watsonx.ai (get API key from IBM Cloud), print response. Commit it.

**Priya:**
- Download FIFA Laws of the Game 2025/26 PDF from FIFA.com (free, public document)
- Download VAR Protocol document from FIFA IFAB
- Install Docling: `pip install docling`
- Run Docling on the FIFA Laws PDF. Look at what comes out. Note which sections parse well and which don't.
- Register on football-data.org for free API key

#### May 29-30 — Tokenization and Prompt Engineering
**Learning focus:** What does temperature actually do? How does a system prompt constrain output?

Write this experiment (everyone does it):
```python
# Run the same FIFA rule question at temperature 0.0 and temperature 1.0
# Compare the outputs. At 0.0 it is deterministic. At 1.0 it hallucinates.
# This is the entire temperature intuition in one experiment.
for temp in [0.0, 0.3, 0.7, 1.0]:
    response = call_granite(
        system="You are a FIFA rules expert. Answer only from FIFA Laws of the Game.",
        user="What is the handball rule?",
        temperature=temp
    )
    print(f"Temperature {temp}: {response[:200]}")
```

Run it. See how at temperature 0 the model says "Law 12 states..." and at temperature 1.0 it starts inventing "In the 1986 rule amendment...". This is why your production system uses temperature 0.1 maximum.

#### May 31 – June 1 — Docling Deep Dive (Priya leads, everyone participates)
Priya walks through her Docling output with the team. Together you answer:
- Which chunks are clean and embeddable?
- Which sections got mangled (tables, footnotes)?
- How does Docling handle multi-column FIFA PDF layouts?
- What pre-processing do you need before chunking?

Write the first version of `pipeline/document_parser.py` together.

**June 1: IBM Learning Lab opens. Start it immediately.**

#### June 2-3 — Structured Output and the IBM Granite System Prompt
The most important engineering challenge for VAR explanations: Granite must return structured JSON with fields: `explanation`, `rule_citations`, `decision_steps`, `confidence_score`.

```python
# This is your production system prompt. Write it, test it, lock it.
SYSTEM_PROMPT = """You are DecisionLens, an AI assistant trained on FIFA Laws of the Game and VAR protocols.

Your ONLY knowledge source is the context provided below. Never answer from general knowledge.

You MUST respond in this exact JSON format:
{
  "explanation": "plain language explanation for fans",
  "rule_citations": ["FIFA Law X, Section Y: exact rule text", ...],
  "decision_steps": ["Step 1: VAR checked...", "Step 2: The referee...", ...],
  "confidence_score": 0-100,
  "source_documents": ["document name and section", ...]
}

If the context does not contain enough information to answer, set confidence_score below 40 and explain what is missing."""
```

Test this 20 times on different VAR questions. See where it fails. Fix the prompt. This is real prompt engineering.

**June 3: Attend IBM Kickoff Webinar. Note any technical requirements or tool updates.**

---

### WEEK 2: June 4 – June 10 — The RAG Core

**Goal by end of week:** A working retrieval system. You can query your FIFA document knowledge base and get the top 5 most relevant chunks for any VAR question.

#### June 4 — Team Formation Webinar. Attend it.

#### June 4-5 — Cosine Similarity from Scratch (YOU do this before using any library)

```python
# Run this notebook before touching ChromaDB
import numpy as np
import requests

def get_embedding(text):
    # Use Ollama nomic-embed-text endpoint
    response = requests.post('http://localhost:11434/api/embeddings',
                             json={"model": "nomic-embed-text", "prompt": text})
    return np.array(response.json()['embedding'])

# Your three test sentences from FIFA Law 12
s1 = "A handball occurs when a player deliberately touches the ball with their hand or arm."
s2 = "An arm in an unnatural position that makes the body bigger constitutes a handball offense."
s3 = "A goal kick is awarded when the ball crosses the goal line last touched by an attacker."

e1, e2, e3 = get_embedding(s1), get_embedding(s2), get_embedding(s3)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print(f"s1 vs s2 (same law): {cosine_similarity(e1, e2):.4f}")  # Should be > 0.80
print(f"s1 vs s3 (different law): {cosine_similarity(e1, e3):.4f}")  # Should be < 0.50

# If you get these numbers you understand vector search.
```

This experiment IS the understanding. Do not skip it.

#### June 6-7 — Semantic Chunking Implementation

Implement `pipeline/chunker.py` using the semantic chunking algorithm from Part 7.4. Test it on:
1. FIFA Law 12 (should produce chunks for: deliberate handball, accidental handball, goal-scoring handball, natural position definition)
2. VAR Protocol (should produce chunks for: reviewable decisions, review process, communication)

Compare outputs to naive 500-character chunking. Write a short analysis in your notebook: which produces cleaner retrieval chunks and why?

#### June 8-9 — BM25 + Vector Hybrid Search

Implement `pipeline/retriever.py`:

```python
from rank_bm25 import BM25Okapi
import chromadb

class HybridRetriever:
    def __init__(self, chunks, embeddings):
        # BM25 index
        self.tokenized = [c.split() for c in chunks]
        self.bm25 = BM25Okapi(self.tokenized)
        self.chunks = chunks
        
        # ChromaDB vector store
        self.client = chromadb.Client()
        self.collection = self.client.create_collection("decisionlens")
        self.collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=[str(i) for i in range(len(chunks))]
        )
    
    def search(self, query, embedding, top_k=20):
        # Dense search
        vector_results = self.collection.query(
            query_embeddings=[embedding], n_results=top_k)
        vector_ids = vector_results['ids'][0]
        
        # Sparse search
        bm25_scores = self.bm25.get_scores(query.split())
        bm25_ids = [str(i) for i in np.argsort(bm25_scores)[-top_k:][::-1]]
        
        # Reciprocal Rank Fusion
        return reciprocal_rank_fusion(vector_ids, bm25_ids)
```

Test: Query "was the arm in unnatural position" against your FIFA Law 12 chunks. Are the top 5 results the correct sections?

#### June 10 — IBM Tech Webinar (Week of June 8). Attend it. Note anything that changes your plan.

---

### WEEK 3: June 11 – June 17 — CRAG Agent Loop

**WORLD CUP STARTS JUNE 11. Start collecting real match events for testing.**

**Goal by end of week:** A complete CRAG pipeline running end-to-end. Query in, grounded explanation out, with source citations.

#### June 11-12 — Cross-Encoder Reranker

Implement `pipeline/reranker.py`. Test it:
```python
# Before reranking: top result might be tangentially related
# After reranking: top result should be the exact rule that applies
from sentence_transformers import CrossEncoder

reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

query = "handball arm unnatural position World Cup goal disallowed"
chunks = retriever.search(query, top_k=20)

scores = reranker.predict([[query, chunk] for chunk in chunks])
reranked = [c for _, c in sorted(zip(scores, chunks), reverse=True)][:5]
# Top 5 should now be laser-focused on handball rule definition
```

#### June 13-14 — CRAG Evaluator + Context Forge MCP Tools

Implement `agents/evaluator.py` using the cross-encoder relevance score (not a separate LLM call).

Implement Context Forge MCP tool definitions:
```yaml
# context_forge_tools.yaml
tools:
  - name: live_match_data
    description: Fetch live match events from football-data.org
    endpoint: /api/matches/{match_id}/events
    parameters:
      - name: match_id
        type: string
      - name: minute
        type: integer
        
  - name: fifa_rules_lookup  
    description: Search FIFA Laws of the Game by law number or keyword
    endpoint: /api/knowledge/fifa_laws
    parameters:
      - name: law_number
        type: string
      - name: keyword
        type: string
        
  - name: var_protocol_search
    description: Search VAR protocol documents for specific decision types
    endpoint: /api/knowledge/var_protocol
    parameters:
      - name: decision_type
        enum: [handball, offside, penalty, violent_conduct]
```

#### June 15-16 — Context Compression

Implement `pipeline/compressor.py`. The logic: given 5 retrieved chunks, call Granite with a fast prompt: "From this text, extract only the sentences directly relevant to: [query]. Return only those sentences." This strips irrelevant padding before the final synthesis call.

Measure: average token count before and after compression on 10 test queries. Record the reduction percentage. This is your resume metric.

#### June 17 — Full End-to-End Integration Test

Run 10 real questions from the first week of World Cup matches through your complete pipeline. Log every step. For each query record:
- Number of chunks retrieved
- Relevance score before reranking
- Relevance score after reranking
- Which path CRAG took (sufficient/insufficient/ambiguous)
- Token count before context compression
- Token count after context compression
- Final answer quality (human judgment 1-5)

This log is Week 3's deliverable. Keep it.

---

### WEEK 4: June 18 – June 24 — Evaluation, LangFlow, and Polish

**Goal by end of week:** RAGAS evaluation numbers generated. LangFlow flow built. Streamlit app working.

#### June 18-19 — RAGAS Evaluation (Priya leads)

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from datasets import Dataset

# Your test set: 50 questions with ground truth answers from FIFA laws
# Priya builds this from her knowledge of the FIFA documents
test_data = {
    "question": ["What is the handball rule?", "Can VAR review offside?", ...],
    "ground_truth": ["Under FIFA Law 12...", "Yes, VAR can review...", ...],
    "answer": [...],  # what DecisionLens generated
    "contexts": [[...], ...]  # what was retrieved for each question
}

dataset = Dataset.from_dict(test_data)
results = evaluate(dataset, metrics=[faithfulness, answer_relevancy, 
                                      context_precision, context_recall])
print(results)
# Target: faithfulness > 0.85, answer_relevancy > 0.80
# These numbers go in your README and demo
```

#### June 20-21 — LangFlow Orchestration

Build the complete CRAG flow in LangFlow. Each node corresponds to a component you already wrote in Python:
- Document Loader → Docling parser
- Embeddings → IBM Watson embedding
- Vector Store → ChromaDB
- Retriever → Your HybridRetriever
- Reranker → Cross-encoder
- Agent → Your CRAG evaluator loop
- LLM → IBM Granite

The LangFlow diagram is your architecture diagram for the demo video. Do not skip this.

#### June 22-23 — Streamlit Frontend

```python
import streamlit as st
import json

st.set_page_config(page_title="DecisionLens", page_icon="⚽")
st.title("⚽ DecisionLens — FIFA World Cup 2026 VAR Transparency Engine")

query = st.text_input("Ask about any VAR decision or tactical moment:")

if query:
    with st.spinner("Retrieving FIFA rules and match data..."):
        result, sources = crag_agent(query)
        parsed = json.loads(result)
    
    st.markdown("### Explanation")
    st.write(parsed['explanation'])
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Confidence Score", f"{parsed['confidence_score']}%")
    with col2:
        st.metric("Sources Used", len(parsed['source_documents']))
    
    st.markdown("### Decision Reconstruction")
    for i, step in enumerate(parsed['decision_steps']):
        st.markdown(f"**Step {i+1}:** {step}")
    
    st.markdown("### FIFA Rule Citations")
    for citation in parsed['rule_citations']:
        st.info(citation)
    
    st.markdown("### Source Documents")
    for source in parsed['source_documents']:
        st.caption(source)
```

#### June 24 — Integration Test with Live World Cup Data

The Round of 32 starts June 27. By June 24 you should have 13 days of group stage VAR controversies to test with. Run your full pipeline on 5 real World Cup VAR incidents from the past two weeks. Does DecisionLens explain them correctly?

---

### WEEK 5: June 25 – June 30 — Submission Week

**Goal: Submitted and published on platform by June 28 (2 days early).**

#### June 25 — Final Bug Fix Day

No new features. Fix only what is broken. Anything that does not work by June 25 gets cut from the demo.

#### June 26-27 — Demo Video (Priya leads scripting, everyone records together)

3-minute structure:
- 0:00-0:30: Problem statement. Show a real World Cup VAR moment. "Why did nobody explain this?"
- 0:30-1:30: Live demo. Ask a real question from a real match. Show the step-by-step output. Show the CRAG fallback triggering.
- 1:30-2:30: Architecture walkthrough using LangFlow diagram. One sentence per component.
- 2:30-3:00: RAGAS numbers. Before/after context compression token reduction. Why this is production-grade.

Do not show code in the demo video. Show the system working. Show the architecture diagram.

#### June 28 — README Final Version

README structure:
1. Project title and one-sentence description
2. Problem it solves (2 paragraphs)
3. Architecture diagram (export from LangFlow)
4. IBM tools used and exactly how
5. Technical approach (CRAG, hybrid search, cross-encoder — one paragraph each)
6. RAGAS evaluation results table
7. Performance metrics (context compression reduction %, average response time)
8. Setup instructions (local Ollama + IBM watsonx.ai API)
9. Example queries and outputs
10. Why this matters for soccer fans globally

#### June 28 — Submit on Platform (DO NOT WAIT FOR JUNE 30)

Submit two days early. Then if there are technical problems with the platform you have time to fix them.

#### June 29-30 — Buffer / Final Polish

If you submitted early, use this time to write one additional technical document: a post-mortem on what the CRAG fallback triggered most often and why. This is extra material for interviews.

---

## PART 9: RESUME BULLETS (Write These Now So You Know What You Are Building Toward)

These are the exact bullets that go on your resume when this is done:

```
DecisionLens — VAR Transparency Engine for FIFA World Cup 2026
IBM SkillsBuild BeMyApp Challenge | June 2026

• Architected a Corrective RAG (CRAG) pipeline combining BM25 keyword 
  search and dense vector retrieval with Reciprocal Rank Fusion, achieving 
  [X]% improvement in context relevance over naive vector search alone.

• Implemented semantic chunking on FIFA Laws of the Game and VAR protocol 
  documents using Docling, reducing out-of-context chunk retrieval by [X]% 
  compared to fixed-size chunking.

• Engineered a self-correcting agent loop using IBM Granite 3.1 8B and 
  Context Forge MCP tools, with automatic fallback to live match data APIs 
  when internal knowledge base relevance score fell below threshold.

• Reduced per-query LLM token consumption by [X]% through cross-encoder-based 
  context compression prior to IBM Granite synthesis call.

• Evaluated system quality using RAGAS framework, achieving [X] faithfulness 
  score and [X] answer relevancy score across 50 FIFA-grounded test questions.

• Deployed locally on RTX 3070 Ti using IBM Granite GGUF Q4_K_M quantization 
  via Ollama; demonstrated identical outputs using IBM watsonx.ai cloud endpoint.
```

Fill in the [X] numbers after you run your evaluations in Week 4.

---

## PART 10: WHAT WILL KILL YOUR CHANCES (Read This Weekly)

1. **Building a score predictor** — judges explicitly said they do not want this
2. **Using LangChain as a black box** — if you cannot explain every node in your LangFlow diagram you will fail the technical Q&A
3. **No source citations in the output** — explainability is the entire challenge theme. Output without citations is opaque AI.
4. **Submitting on June 30 at 11:58 PM** — platform issues will end your project
5. **Priya only doing documentation** — you are wasting your only team member with published RAG experience
6. **Not having RAGAS numbers** — claims without metrics are meaningless to judges
7. **A demo video that shows code** — show the system, show the architecture diagram, show the numbers
8. **Skipping the cosine similarity from scratch notebook** — if you do not understand what the retrieval system is doing mathematically you cannot debug it when it fails at 2am before submission

---

## PART 11: KEY DATES CALENDAR

| Date | Event |
|------|-------|
| May 28 | Start today. GitHub repo, Ollama setup, Docling first run |
| June 1 | IBM Learning Lab opens. Start it. |
| June 3 | IBM Kickoff Webinar 10AM ET. Attend. |
| June 4 | Team Formation Webinar 10AM ET. Attend. |
| Week of June 8 | IBM Tech Webinar. Attend. Note any changes. |
| June 11 | FIFA World Cup 2026 starts. Group stage begins. |
| June 11 | Your hybrid retriever should be working by this date |
| June 17 | End-to-end CRAG pipeline working |
| June 24 | RAGAS evaluation done. LangFlow done. Streamlit done. |
| June 26 | World Cup Round of 32 starts. Use live data in demo. |
| June 28 | SUBMIT. Do not wait for June 30. |
| June 30 | Hard deadline 11:59 PM ET. |

---

## PART 12: DATA SOURCES AND FREE APIs

| Source | What It Provides | Cost | URL |
|--------|-----------------|------|-----|
| FIFA Laws of the Game | Laws 1-17, handball, offside, VAR rules | Free PDF | FIFA.com |
| FIFA/IFAB VAR Protocol | Step-by-step review process | Free PDF | IFAB.com |
| football-data.org | Live match events, goals, cards, lineups | Free (10 calls/min) | football-data.org |
| StatsBomb Open Data | Detailed historical match events (passes, shots, fouls) | Free GitHub | github.com/statsbomb/open-data |
| ESPN undocumented API | Live match commentary | Free (unofficial) | Use carefully |
| FIFA 2026 official site | Tournament regulations, group draw | Free | FIFA.com/en/tournaments/mens/worldcup/2026 |

---

*Last updated: May 28, 2026. Version 1.0 — Locked after audit.*
*Team: [You] (RAG Pipeline), Karthi (Agent Loop), Priya (Evaluation + Technical Depth)*
*Project: DecisionLens — VAR Transparency Engine for FIFA World Cup 2026*
