# DecisionLens in LangFlow

## What this is for

LangFlow is IBM's visual builder for AI workflows. In DecisionLens it serves one purpose: **show judges and reviewers the CRAG pipeline as a flow**, without rebuilding the engine inside LangFlow's generic nodes.

The custom component **DecisionLens CRAG Agent** does not reimplement retrieval or generation. It calls the same function the web app uses:

```text
pipeline/agent.py  →  run(question, mode, language)
```

That means one engine, three surfaces:

| Surface | Role |
|---|---|
| **React web app** (`web/`) | Primary demo UI for fans and judges |
| **FastAPI** (`api/main.py`) | HTTP wrapper for the React app |
| **LangFlow Playground** | Visual flow demo of the same `run()` call |
| **Streamlit** (`app/main.py`) | Fallback prototype UI |

If LangFlow and the web app both answer the same question, they should return the same citations and abstention behaviour, because they share `run()`.

## What LangFlow is not

- Not a second RAG stack (no LangFlow-native vector store replacing our 593 Docling chunks).
- Not required to run the product. The hackathon demo works fully with React + FastAPI + Ollama alone.
- Not connected to live match video or incident feeds.

## Showcase in the hackathon (recommended)

LangFlow is **not** part of the public live URL. Judges click **Vercel**; LangFlow appears in your **video** as proof you integrated the IBM visual stack.

| Method | Effort | Judge impact |
|---|---|---|
| **15–20 s screen clip in demo video** | Low | High — shows IBM LangFlow + same engine |
| README + architecture mention | Done | Medium |
| Deploy LangFlow online | High, not required | Low — judges rarely run LangFlow flows |

**Perfect showcase workflow:**

1. Record the main demo on **https://decisionlens-june-2026.vercel.app** (primary).
2. Locally: `python -m langflow run --components-path langflow/ --port 7860`
3. Record **one** Playground run: Text Input → DecisionLens CRAG Agent → same VAR question as the web demo.
4. Voiceover one line: *“The same `run()` function powers the web app and this LangFlow component — one engine, not two pipelines.”*

LangFlow Desktop / local server is the **standard** hackathon pattern. Online LangFlow hosting is possible (Docker Space) but unnecessary when you already have a live Vercel demo.

## Prerequisites

1. Ollama running: `ollama serve`
2. Models pulled: `granite3.1-dense:8b`, `nomic-embed-text`
3. Chunks indexed: `data/chunks/chunks.json` (593 chunks from Docling ingestion)
4. LangFlow installed in your Python environment

## Run

From your clone of the repository (the folder that contains `pipeline/agent.py`):

```powershell
cd path\to\decisionlens-june-2026
python -m langflow run --components-path langflow/ --port 7860
```

If LangFlow must be started from another working directory, point at the repo explicitly:

```powershell
$env:DECISIONLENS_ROOT = "C:\path\to\decisionlens-june-2026"
python -m langflow run --components-path path\to\decisionlens-june-2026\langflow\ --port 7860
```

If you pasted the component in **New Custom Component** (Saved), open **<> Code**, replace all code with the latest [decisionlens_component.py](decisionlens_component.py), and save.

Open `http://localhost:7860`. In the component sidebar, search for **DecisionLens CRAG Agent**. Drag it onto the canvas, connect a **Text Input** (or Chat Input) to the `question` field, and open the **Playground**.

## Sample questions

**Should answer with citations (GOOD route):**

`What are the four categories of decisions that VAR can review?`

Expected: four VAR review categories, IFAB VAR Protocol citation, confidence around 0.95.

**Should abstain (incident guard):**

`Was Neymar's handball in the 2026 World Cup final deliberate?`

Expected: confidence 0.0, missing evidence listed, no invented answer.

## Output format

Valid output is markdown with: explanation, evidence confidence, decision steps, rule citations (quoted spans), and sources. On abstention, a missing-evidence section instead of a fabricated verdict.

## Code entry point

[decisionlens_component.py](decisionlens_component.py) — LangFlow `CustomComponent` that imports `run` from `pipeline/agent.py`.
