# Hugging Face Space entry — see deploy/README.md for Vercel + GPU setup.
FROM ollama/ollama:latest

USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY pipeline/ pipeline/
COPY api/ api/
COPY data/chunks/ data/chunks/
COPY evaluation/results.json evaluation/results.json

COPY deploy/start.sh /start.sh
RUN chmod +x /start.sh

ENV OLLAMA_HOST=127.0.0.1:11434
ENV OLLAMA_URL=http://127.0.0.1:11434/api/generate
ENV PORT=7860

EXPOSE 7860
CMD ["/start.sh"]
