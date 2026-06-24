# Deploy DecisionLens (judges / live demo)

**Live UI:** [decisionlens-june-2026.vercel.app](https://decisionlens-june-2026.vercel.app)

**Stack:** Vercel (React) → proxy `/api/*` → GCP Compute Engine VM (NVIDIA L4, `us-central1`) running Ollama + FastAPI.

---

## Architecture

```
Browser → https://decisionlens-june-2026.vercel.app
              ↓  web/vercel.json rewrites /api/*
         http://34.41.120.32:8077  (GCP VM, port 8077)
              ↓
         Ollama (granite3.1-dense:8b + nomic-embed-text)
              ↓
         pipeline/agent.py via api/main.py
```

No `VITE_API_BASE` env var is required — the frontend uses same-origin `/api/...` and Vercel proxies to the VM.

---

## Operations schedule (June–July 2026)

| Period | VM | Backend |
|--------|-----|---------|
| **Now → demo recorded** | **Stop** when not recording | Saves GCP trial credit |
| **June 28** | Start for BeMyApp submit smoke test | Start API, verify live URL |
| **July 1–14** (judge review) | **Run 24/7** | `tmux` session keeps uvicorn alive |
| **After July 14** | **Stop** or delete VM | Avoid further charges |

The Vercel frontend stays online always; `/api/*` returns errors when the VM is stopped — expected during credit-saving windows.

---

## GCP VM reference

| Item | Value |
|------|--------|
| Project | `decisionlens-prod` |
| Instance | `decisionlens-api` |
| Zone | `us-central1-a` |
| GPU | NVIDIA L4 |
| External IP | `34.41.120.32` (static — update [web/vercel.json](../web/vercel.json) if it changes) |
| API port | `8077` |
| Repo on VM | `~/decisionlens-june-2026` |

---

## Start backend (after VM Start)

SSH into the VM, then:

```bash
# Ensure Ollama is running
sudo systemctl start ollama

# One-command start in tmux (recommended)
cd ~/decisionlens-june-2026
bash deploy/gcp-start.sh
```

Or manually:

```bash
tmux new -s dl
cd ~/decisionlens-june-2026
source .venv/bin/activate
export ALLOWED_ORIGINS=https://decisionlens-june-2026.vercel.app
export OLLAMA_HOST=127.0.0.1:11434
uvicorn api.main:app --host 0.0.0.0 --port 8077
# Ctrl+B then D to detach
```

First boot after fresh clone indexes 593 chunks (~5–10 min). Subsequent starts load caches in ~30s.

**Verify:**

```bash
curl http://127.0.0.1:8077/api/health
curl https://decisionlens-june-2026.vercel.app/api/health
```

Both must return JSON with `"status":"ok"`.

---

## Stop backend (save credit)

1. **GCP Console** → Compute Engine → VM instances → `decisionlens-api` → **Stop**
2. GPU billing stops; disk and static IP remain (small storage charge only)

Do **not** delete the VM unless you intend to rebuild.

---

## July 1–14: 24/7 judge window

1. **Start** VM in GCP Console
2. SSH → `bash deploy/gcp-start.sh`
3. Confirm health URLs above
4. Leave VM **running** until July 14
5. Reattach anytime: `tmux attach -t dl`

If SSH drops, uvicorn keeps running inside tmux.

---

## Firewall

Ingress TCP **8077** from `0.0.0.0/0` (rule: `allow-decisionlens-api`).

---

## Vercel

Root directory: `web/`. Proxy config in [web/vercel.json](../web/vercel.json):

```json
{ "source": "/api/:path*", "destination": "http://34.41.120.32:8077/api/:path*" }
```

Vercel proxied request timeout: **120 seconds** (sufficient for Granite generation).

After changing the VM IP, push `vercel.json` and redeploy.

---

## Troubleshooting

### All questions return DECLINED (vector_score 0.0)

Newer Ollama on Linux uses `POST /api/embed` with an `input` field (not legacy `/api/embeddings`). After pulling a fix for [pipeline/retriever.py](../pipeline/retriever.py), rebuild the index on the VM:

```bash
cd ~/decisionlens-june-2026
git pull
rm -f data/embeddings_cache.npz
bash deploy/gcp-start.sh
```

Wait for `Application startup complete`, then re-test a quick ask.

---

```powershell
$env:ALLOWED_ORIGINS="http://localhost:5173"
uvicorn api.main:app --host 127.0.0.1 --port 8077
cd web; npm run dev
```

---

## Alternatives (not used in production demo)

| Option | Notes |
|--------|--------|
| Hugging Face Space Docker | [Dockerfile](../Dockerfile) in repo |
| RunPod GPU pod | Same Docker image; stop when idle |
| Home PC + Cloudflare Tunnel | Unreliable for judges (power cuts) |

---

## Opponent deploy patterns (reference)

| Project | Live URL |
|---------|----------|
| FirstTouch | first-touch-phi.vercel.app |
| MatchMind | matchmind-ai-deshraj.vercel.app |
| PitchIQ AI | pitch-iq-ai.vercel.app (watsonx API) |

DecisionLens keeps **IBM Granite via Ollama** on a dedicated GPU VM — stronger “Best Use of Technology” story than watsonx-only wrappers.
