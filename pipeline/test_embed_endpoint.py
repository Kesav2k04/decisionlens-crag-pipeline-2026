import requests
import json

url = "http://localhost:11434/api/embeddings"
payload = {"model": "nomic-embed-text", "prompt": "test"}

try:
    print("[+] Sending request to Ollama endpoint...")
    r = requests.post(url, json=payload, timeout=10)
    print(f"[+] HTTP Status Code: {r.status_code}")
    data = r.json()
    if "embedding" in data:
        print(f"[+] Success! Embedding dimensions caught: {len(data['embedding'])}")
        print(f"[+] Sample data dimensions preview: {data['embedding'][:5]}...")
    else:
        print(f"[-] Missing embedding key. Full Response payload: {data}")
except Exception as e:
    print(f"[-] CRITICAL EXCEPTION CAUGHT: {str(e)}")
