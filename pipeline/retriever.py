import json
import numpy as np
import requests

CHUNKS_PATH = "data/chunks/chunks.json"

def load_chunks():
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_embedding(text: str) -> list:
    """Retrieves local embedding vector via Ollama's nomic service pipeline."""
    try:
        url = "http://localhost:11434/api/embeddings"
        response = requests.post(url, json={"model": "nomic-embed-text", "prompt": text}, timeout=10)
        if response.status_code == 200:
            return response.json()["embedding"]
    except Exception:
        pass
    return [0.0] * 768

def calculate_local_bm25(query: str, document_text: str) -> float:
    import re
    words = re.findall(r'\w+', query.lower())
    doc_text_lower = document_text.lower()
    score = 0.0
    for word in words:
        occurrences = doc_text_lower.count(word)
        if occurrences > 0:
            score += (occurrences / (len(doc_text_lower.split()) + 1e-5)) * 10.0 + 1.5
    return score

def reciprocal_rank_fusion(vector_ranked_ids: list, bm25_ranked_ids: list, k: int = 60) -> list:
    rrf_scores = {}
    for rank, doc_id in enumerate(vector_ranked_ids):
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + 1.0 / (k + rank + 1)
    for rank, doc_id in enumerate(bm25_ranked_ids):
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + 1.0 / (k + rank + 1)
    return sorted(rrf_scores.keys(), key=lambda x: rrf_scores[x], reverse=True)

class HybridRetriever:
    def __init__(self):
        print("[+] Loading purified text database...")
        self.chunks = load_chunks()
        
        print(f"[+] Vectorizing KNOWLEDGE BASE across ALL {len(self.chunks)} elements via local GPU...")
        raw_embeddings = []
        
        # FIX: Loop through every single available chunk without truncation boundaries
        total_chunks = len(self.chunks)
        for i in range(total_chunks):
            vector = get_embedding(self.chunks[i]["text"])
            raw_embeddings.append(vector)
            if i % 50 == 0 or i == total_chunks - 1:
                print(f"    -> Progress: Indexed embedding nodes {i+1}/{total_chunks}")
                
        self.embeddings = np.array(raw_embeddings)
        print(f"[+] Hybrid Retriever online. Total index capacity: {len(self.chunks)} items.")

    def search(self, query: str, top_k: int = 2) -> list:
        bm25_scores = [calculate_local_bm25(query, chunk["text"]) for chunk in self.chunks]
        bm25_ranked = list(np.argsort(bm25_scores)[::-1][:20])
        
        query_vector = np.array(get_embedding(query))
        dot_products = np.dot(self.embeddings, query_vector)
        matrix_norms = np.linalg.norm(self.embeddings, axis=1)
        query_norm = np.linalg.norm(query_vector)
        
        similarities = dot_products / (matrix_norms * query_norm + 1e-8)
        vector_ranked = list(np.argsort(similarities)[::-1][:20])
        
        fused_identifiers = reciprocal_rank_fusion(vector_ranked, bm25_ranked)
        
        top_results = []
        for doc_id in fused_identifiers[:top_k]:
            top_results.append({
                "chunk_id": doc_id,
                "text": self.chunks[doc_id]["text"],
                "source": self.chunks[doc_id]["source"],
                "bm25_score": float(bm25_scores[doc_id]),
                "vector_score": float(similarities[doc_id])
            })
        return top_results

if __name__ == "__main__":
    search_engine = HybridRetriever()
    test_suite = [
        "What is the handball rule?",
        "When can VAR review a decision?",
        "What constitutes an offside position?"
    ]
    
    for query in test_suite:
        print(f"\n{'-'*70}\nQuery: {query}")
        hits = search_engine.search(query, top_k=2)
        for rank, match in enumerate(hits):
            print(f"  Match {rank+1} [Chunk ID: {match['chunk_id']}] -> Source: {match['source']}")
            print(f"  Scores -> Keyword Weight: {match['bm25_score']:.3f} | Vector Cosine: {match['vector_score']:.3f}")
            print(f"  Excerpt: {match['text'][:250]}...\n")
