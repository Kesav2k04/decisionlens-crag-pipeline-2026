#!/usr/bin/env bash
# Start DecisionLens API inside tmux (survives SSH disconnect).
# Run after GCP VM Start: bash deploy/gcp-start.sh
set -euo pipefail

SESSION=dl
ROOT="${HOME}/decisionlens-june-2026"
ORIGIN="${ALLOWED_ORIGINS:-https://decisionlens-june-2026.vercel.app}"

if tmux has-session -t "$SESSION" 2>/dev/null; then
  echo "Session '$SESSION' already exists. Attach: tmux attach -t $SESSION"
  exit 0
fi

tmux new-session -d -s "$SESSION" -c "$ROOT" \
  "source .venv/bin/activate && export ALLOWED_ORIGINS='$ORIGIN' && export OLLAMA_HOST=127.0.0.1:11434 && uvicorn api.main:app --host 0.0.0.0 --port 8077"

echo "Started DecisionLens in tmux session '$SESSION'."
echo "  Attach:  tmux attach -t $SESSION"
echo "  Logs:    tmux attach -t $SESSION  (Ctrl+B D to detach)"
echo "  Health:  curl http://127.0.0.1:8077/api/health"
