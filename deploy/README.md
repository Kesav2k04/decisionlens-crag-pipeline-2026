# Deploy DecisionLens (Production)

**Live UI:** [decisionlens-june-2026.vercel.app](https://decisionlens-june-2026.vercel.app)

**Infrastructure:** Vercel (Frontend) → GCP Compute Engine VM (NVIDIA L4, `northamerica-northeast2`) running Ollama + FastAPI.

---

## Architecture

```text
Browser → https://decisionlens-june-2026.vercel.app
              ↓  web/vercel.json rewrites /api/*
         http://<GCP_STATIC_IP>:8077 (GCP VM, port 8077)
              ↓
         Ollama (granite3.1-dense:8b + nomic-embed-text)
              ↓
         pipeline/agent.py via api/main.py
```


