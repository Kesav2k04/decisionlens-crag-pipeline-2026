# Deploy DecisionLens (judges / live demo)

Industry pattern for this hackathon: **Vercel (frontend) + GPU backend (Ollama + FastAPI)**.

## Opponents (for reference)

| Project | Live URL pattern |
|---------|------------------|
| FirstTouch | `first-touch-phi.vercel.app` |
| MatchMind | `matchmind-ai-deshraj.vercel.app` |
| PitchIQ AI | `pitch-iq-ai.vercel.app` (watsonx API — no local Ollama) |

DecisionLens keeps **IBM Granite via Ollama** — you need a GPU host for the backend, not just Vercel.

## Recommended (reliable, no home PC / power cuts)

### A. Hugging Face Space (Docker) + Vercel — best fit

1. Create a **Docker** Space on Hugging Face; copy `deploy/Dockerfile` to the Space repo root (or symlink).
2. Hardware: **T4 small** (~$0.40/hr) or apply for a **community GPU grant** in Space Settings (free if approved).
3. Set Space env: `ALLOWED_ORIGINS=https://YOUR-PROJECT.vercel.app`
4. Deploy **web/** to Vercel (root directory `web`). Set `VITE_API_BASE=https://YOUR-SPACE.hf.space`
5. **Sleep billing:** pause Space or switch to CPU when not demoing — you only need uptime during judge review (July 1–14), not 24/7 until July 14.

First cold start pulls ~8B model once (~5–10 min); after that answers match local eval latency.

### B. RunPod / similar (~$5–15 total)

Same Docker image on a GPU pod; stop the pod when idle. Turn on only for submission week + judge window.

### C. Do not rely on for judges

- Cloudflare Tunnel to your Windows PC (power cut / Windows Update kills the demo).
- HF **CPU-only** Space (Granite 8B on CPU is too slow — judges will feel lag).

## Local smoke test of production CORS

```powershell
$env:ALLOWED_ORIGINS="http://localhost:5173"
uvicorn api.main:app --host 127.0.0.1 --port 8077
cd web; npm run dev
```

## Streamlit fallback

`streamlit run app/main.py` — optional; React + Vercel is the primary judge-facing UI.
