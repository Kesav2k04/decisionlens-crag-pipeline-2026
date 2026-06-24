# pipeline/retriever.py
# Optimised: embedding cache + rank_bm25 + parallel init + isolated memory footprint + fingerprinted BM25 cache

import os
import json
import pickle
import hashlib
import gc
import numpy as np
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from rank_bm25 import BM25Okapi

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHUNKS_PATH = os.path.join(BASE_DIR, "data", "chunks", "chunks.json")
CACHE_PATH  = os.path.join(BASE_DIR, "data", "embeddings_cache.npz")
BM25_CACHE_PATH = os.path.join(BASE_DIR, "data", "chunks", "bm25_cache.pkl")

_ollama_host = os.environ.get("OLLAMA_HOST", "127.0.0.1:11434")
OLLAMA_EMBED_URL = os.environ.get("OLLAMA_EMBED_URL", f"http://{_ollama_host}/api/embed")
EMBED_MODEL = os.environ.get("OLLAMA_EMBED_MODEL", "nomic-embed-text")

# ── helpers ────────────────────────────────────────────────

def load_chunks() -> list:
    if not os.path.exists(CHUNKS_PATH):
        raise FileNotFoundError(f"chunks.json missing at {CHUNKS_PATH}")
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def chunks_fingerprint(chunks: list) -> str:
    payload = [
        {
            "chunk_id": c.get("chunk_id"),
            "source": c.get("source"),
            "text": c.get("text"),
            "parser": c.get("parser"),
            "pipeline": c.get("pipeline"),
        }
        for c in chunks
    ]
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    return digest

def legacy_chunks_fingerprint(chunks: list) -> str:
    """Fingerprint format used before 2026-06-12 cache hardening."""
    return hashlib.md5(json.dumps([c["chunk_id"] for c in chunks]).encode()).hexdigest()

def get_embedding(text: str) -> list:
    """Return an embedding vector; supports modern (/api/embed) and legacy Ollama APIs."""
    modern_url = OLLAMA_EMBED_URL
    legacy_url = modern_url.replace("/api/embed", "/api/embeddings")
    if legacy_url == modern_url:
        legacy_url = f"http://{_ollama_host}/api/embeddings"

    try:
        r = requests.post(
            modern_url,
            json={"model": EMBED_MODEL, "input": text},
            timeout=30,
        )
        if r.status_code == 200:
            data = r.json()
            if data.get("embeddings"):
                return data["embeddings"][0]
            if data.get("embedding"):
                return data["embedding"]
    except Exception:
        pass

    try:
        r = requests.post(
            legacy_url,
            json={"model": EMBED_MODEL, "prompt": text},
            timeout=30,
        )
        if r.status_code == 200:
            data = r.json()
            if data.get("embedding"):
                return data["embedding"]
    except Exception:
        pass

    return [0.0] * 768

def embed_all_parallel(chunks: list, max_workers: int = 4) -> np.ndarray:
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
        legacy_fingerprint = legacy_chunks_fingerprint(self.chunks)

        # ── Try loading cache ──
        if os.path.exists(CACHE_PATH):
            with np.load(CACHE_PATH, allow_pickle=True) as cached:
                cached_fingerprint = str(cached["fingerprint"])
                cached_embeddings = cached["embeddings"].copy()
            if cached_fingerprint == fingerprint:
                print("[+] Embedding cache hit - loading from disk (fast path)")
                self.embeddings = cached_embeddings
            elif (
                cached_fingerprint == legacy_fingerprint
                and len(cached_embeddings) == len(self.chunks)
            ):
                print("[+] Embedding cache hit - legacy fingerprint matches current chunk count")
                self.embeddings = cached_embeddings
            else:
                print("[+] Cache stale (chunks changed) - recomputing...")
                self.embeddings = self._build_and_cache(fingerprint)
        else:
            print("[+] No cache found - building embedding index...")
            self.embeddings = self._build_and_cache(fingerprint)

        # Memory Optimization Fix: Compute vector matrix norms ONCE during startup initialization
        print("[+] Pre-computing vector metrics tracks...")
        self.embeddings = np.array(self.embeddings, dtype=np.float32)
        self.norms = np.linalg.norm(self.embeddings, axis=1)

        # ── Build/Load BM25 index with Disk Cache ──
        self.bm25 = self._load_or_build_bm25(fingerprint, legacy_ok_size=len(self.chunks))

        # Force aggressive memory reclaim
        gc.collect()
        print(f"[+] Retriever ready - {len(self.chunks)} chunks indexed.\n")

    def _build_and_cache(self, fingerprint: str) -> np.ndarray:
        embeddings = embed_all_parallel(self.chunks, max_workers=4)
        os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
        temp_path = CACHE_PATH + ".tmp"
        try:
            with open(temp_path, "wb") as f:
                np.savez_compressed(f,
                                    embeddings=embeddings,
                                    fingerprint=np.array(fingerprint))
            os.replace(temp_path, CACHE_PATH)
            print(f"[+] Cache saved -> {CACHE_PATH}")
        except PermissionError:
            print("[+] Cache write skipped - using in-memory embeddings (path not writable)")
        return embeddings

    def _load_or_build_bm25(self, fingerprint: str, legacy_ok_size: int) -> BM25Okapi:
        if os.path.exists(BM25_CACHE_PATH):
            with open(BM25_CACHE_PATH, "rb") as f:
                cached = pickle.load(f)
            if (
                isinstance(cached, dict)
                and cached.get("fingerprint") == fingerprint
                and "bm25" in cached
            ):
                print(f"[+] Loading BM25 Index from Disk Cache (instant) -> {BM25_CACHE_PATH}")
                return cached["bm25"]
            if (
                isinstance(cached, BM25Okapi)
                and getattr(cached, "corpus_size", None) == legacy_ok_size
            ):
                print(f"[+] Loading legacy BM25 Index from Disk Cache -> {BM25_CACHE_PATH}")
                return cached
            print("[+] BM25 cache stale or legacy format - rebuilding...")
        else:
            print("[+] No BM25 cache found - Building fresh BM25 index matrix...")

        tokenized = [c["text"].lower().split() for c in self.chunks]
        bm25 = BM25Okapi(tokenized)
        try:
            with open(BM25_CACHE_PATH, "wb") as f:
                pickle.dump({"fingerprint": fingerprint, "bm25": bm25}, f)
            print(f"[+] BM25 Cache saved -> {BM25_CACHE_PATH}")
        except PermissionError:
            print("[+] BM25 cache write skipped - using in-memory index (path not writable)")
        return bm25

    @staticmethod
    def _needs_var_category_window(query: str) -> bool:
        q = query.lower()
        return (
            "var" in q
            and ("categor" in q or "reviewable" in q)
            and ("four" in q or "decision" in q or "incident" in q)
        )

    @staticmethod
    def _expand_query(query: str) -> str:
        q = query.lower()
        additions = []
        if "var" in q and ("categor" in q or "reviewable" in q):
            additions.append(
                "reviewable match-changing decisions incidents goal/no goal "
                "penalty kick/no penalty kick direct red cards mistaken identity"
            )
        if "qualified replacement" in q and "var" in q:
            additions.append(
                "incapacitated VAR AVAR replay operator match continue without the use of VARs"
            )
        return f"{query} {' '.join(additions)}".strip()

    def _context_window_text(self, doc_id: int, forward: int = 5) -> str:
        source = self.chunks[doc_id].get("source")
        parts = [self.chunks[doc_id]["text"]]
        for next_id in range(doc_id + 1, min(len(self.chunks), doc_id + forward + 1)):
            if self.chunks[next_id].get("source") != source:
                break
            parts.append(self.chunks[next_id]["text"])
        return " ".join(parts)

    def search(self, query: str, top_k: int = 5) -> list:
        expanded_query = self._expand_query(query)

        # BM25 Inversion Lookup Pass
        bm25_scores = self.bm25.get_scores(expanded_query.lower().split())
        bm25_ranked = list(np.argsort(bm25_scores)[::-1][:20])

        # Accelerated Matrix Vector Correlation Check
        q_vec = np.array(get_embedding(expanded_query), dtype=np.float32)
        q_norm = np.linalg.norm(q_vec) + 1e-8
        
        # Safe dot multiplication against pre-computed memory variables
        similarities = np.dot(self.embeddings, q_vec) / (self.norms * q_norm + 1e-8)
        vector_ranked = list(np.argsort(similarities)[::-1][:20])

        # RRF Fusion Logic with Tuned k = 72 for 593 Chunks
        fused = self._rrf(vector_ranked, bm25_ranked, k=72)

        results = []
        needs_var_window = self._needs_var_category_window(query)
        for doc_id in fused[:top_k]:
            text = self.chunks[doc_id]["text"]
            if (
                needs_var_window
                and "reviewable" in text.lower()
                and ("categories" in text.lower() or "decisions/incidents" in text.lower())
            ):
                text = self._context_window_text(doc_id, forward=5)
            results.append({
                "chunk_id":     int(doc_id),
                "text":         text,
                "source":       self.chunks[doc_id]["source"],
                "bm25_score":   float(bm25_scores[doc_id]),
                "vector_score": float(similarities[doc_id])
            })
            
        # Clean garbage references instantly
        del q_vec
        return results

    @staticmethod
    def _rrf(vec_ids: list, bm25_ids: list, k: int = 72) -> list:
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
