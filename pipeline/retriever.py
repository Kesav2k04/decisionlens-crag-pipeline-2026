# pipeline/retriever.py
# Optimised: embedding cache + rank_bm25 + parallel init + top_k=5

import os
import json
import hashlib
import numpy as np
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from rank_bm25 import BM25Okapi

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHUNKS_PATH = os.path.join(BASE_DIR, "data", "chunks", "chunks.json")
CACHE_PATH  = os.path.join(BASE_DIR, "data", "embeddings_cache.npz")

# ── helpers ────────────────────────────────────────────────

def load_chunks() -> list:
    if not os.path.exists(CHUNKS_PATH):
        raise FileNotFoundError(f"chunks.json missing at {CHUNKS_PATH}")
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def chunks_fingerprint(chunks: list) -> str:
    """Hash the chunks so we know if the cache is stale."""
    digest = hashlib.md5(
        json.dumps([c["chunk_id"] for c in chunks]).encode()
    ).hexdigest()
    return digest

def get_embedding(text: str) -> list:
    try:
        r = requests.post(
            "http://localhost:11434/api/embeddings",
            json={"model": "nomic-embed-text", "prompt": text},
            timeout=15
        )
        if r.status_code == 200:
            return r.json()["embedding"]
    except Exception:
        pass
    return [0.0] * 768

def embed_all_parallel(chunks: list, max_workers: int = 8) -> np.ndarray:
    """
    Embed all chunks in parallel using a thread pool.
    max_workers=8 sends 8 simultaneous requests to Ollama.
    Much faster than sequential on a local model.
    """
    embeddings = [None] * len(chunks)
    total = len(chunks)
    completed = 0

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        future_to_idx = {
            pool.submit(get_embedding, chunks[i]["text"]): i
            for i in range(total)
        }
        for future in as_completed(future_to_idx):
            idx = future_to_idx[future]
            embeddings[idx] = future.result()
            completed += 1
            if completed % 50 == 0 or completed == total:
                print(f"    -> Embedded {completed}/{total}")

    return np.array(embeddings, dtype=np.float32)

# ── retriever ──────────────────────────────────────────────

class HybridRetriever:
    def __init__(self):
        print("[+] Loading chunks...")
        self.chunks = load_chunks()
        fingerprint = chunks_fingerprint(self.chunks)

        # ── Try loading cache ──
        if os.path.exists(CACHE_PATH):
            cached = np.load(CACHE_PATH, allow_pickle=True)
            if str(cached["fingerprint"]) == fingerprint:
                print("[+] Embedding cache hit — loading from disk (fast path)")
                self.embeddings = cached["embeddings"]
            else:
                print("[+] Cache stale (chunks changed) — recomputing...")
                self.embeddings = self._build_and_cache(fingerprint)
        else:
            print("[+] No cache found — building embedding index...")
            self.embeddings = self._build_and_cache(fingerprint)

        # ── Build BM25 index ──
        print("[+] Building BM25 index...")
        tokenized = [c["text"].lower().split() for c in self.chunks]
        self.bm25 = BM25Okapi(tokenized)

        print(f"[+] Retriever ready — {len(self.chunks)} chunks indexed.\n")

    def _build_and_cache(self, fingerprint: str) -> np.ndarray:
        embeddings = embed_all_parallel(self.chunks, max_workers=8)
        os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
        np.savez_compressed(CACHE_PATH,
                            embeddings=embeddings,
                            fingerprint=np.array(fingerprint))
        print(f"[+] Cache saved → {CACHE_PATH}")
        return embeddings

    def search(self, query: str, top_k: int = 5) -> list:
        # BM25 (fast — pre-indexed inverted index)
        bm25_scores = self.bm25.get_scores(query.lower().split())
        bm25_ranked = list(np.argsort(bm25_scores)[::-1][:20])

        # Vector (fast — single matrix multiply)
        q_vec = np.array(get_embedding(query), dtype=np.float32)
        norms = np.linalg.norm(self.embeddings, axis=1)
        q_norm = np.linalg.norm(q_vec) + 1e-8
        similarities = np.dot(self.embeddings, q_vec) / (norms * q_norm + 1e-8)
        vector_ranked = list(np.argsort(similarities)[::-1][:20])

        # RRF fusion
        fused = self._rrf(vector_ranked, bm25_ranked)

        results = []
        for doc_id in fused[:top_k]:
            results.append({
                "chunk_id":     int(doc_id),
                "text":         self.chunks[doc_id]["text"],
                "source":       self.chunks[doc_id]["source"],
                "bm25_score":   float(bm25_scores[doc_id]),
                "vector_score": float(similarities[doc_id])
            })
        return results

    @staticmethod
    def _rrf(vec_ids: list, bm25_ids: list, k: int = 60) -> list:
        scores = {}
        for rank, doc_id in enumerate(vec_ids):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank + 1)
        for rank, doc_id in enumerate(bm25_ids):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank + 1)
        return sorted(scores.keys(), key=lambda x: scores[x], reverse=True)


if __name__ == "__main__":
    r = HybridRetriever()
    for q in ["What is the handball rule?",
               "When can VAR review a decision?",
               "What constitutes an offside position?"]:
        print(f"\n{'─'*60}\nQuery: {q}")
        for i, hit in enumerate(r.search(q, top_k=3)):
            print(f"  [{i+1}] chunk {hit['chunk_id']} | "
                  f"vec={hit['vector_score']:.3f} bm25={hit['bm25_score']:.3f}")
            print(f"       {hit['text'][:180]}...")
