#!/usr/bin/env bash
set -euo pipefail

ollama serve &
OLLAMA_PID=$!

echo "Waiting for Ollama..."
for i in $(seq 1 60); do
  if curl -sf http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

echo "Pulling models (first boot may take several minutes)..."
ollama pull granite3.1-dense:8b
ollama pull nomic-embed-text

echo "Starting DecisionLens API on port ${PORT:-7860}..."
exec uvicorn api.main:app --host 0.0.0.0 --port "${PORT:-7860}"
