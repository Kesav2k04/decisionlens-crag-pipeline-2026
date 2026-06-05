import requests
import json

def test_karthi_inference():
    # Local Ollama endpoint port
    url = "http://localhost:11434/api/generate"
    
    # Construct an exact rule question payload
    payload = {
        "model": "granite3.1-dense:2b",
        "prompt": "<|system|>\nYou are a professional FIFA soccer official. Be concise.\n<|user|>\nAccording to the VAR Protocol, what are the only 4 match-changing situations that a Video Assistant Referee can legally review?\n<|assistant|>\n",
        "stream": False,
        "options": {
            "temperature": 0.0,
            "num_predict": 150
        }
    }
    
    print("[+] Querying Karthi's local Granite 2B background engine...")
    try:
        response = requests.post(url, json=payload, timeout=300)
        response.raise_for_status()
        
        output = response.json()["response"]
        print("\n=== LOCAL GRANITE 2B VERIFICATION ===")
        print(output.strip())
        print("=====================================\n")
        print("[+] Success. Programmatic local inference confirmed.")
        
    except requests.exceptions.ConnectionError:
        print("[-] Connection Error: Is Ollama running in the background?")
    except Exception as e:
        print(f"[-] Execution broken: {e}")

if __name__ == "__main__":
    test_karthi_inference()
