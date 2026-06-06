import os
import json
from pypdf import PdfReader

def extract_true_pdf_text(pdf_path):
    if not os.path.exists(pdf_path):
        return ""
    try:
        reader = PdfReader(pdf_path)
        pages_content = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages_content.append(text)
        return "\n".join(pages_content)
    except Exception as e:
        print(f"[-] Error reading {pdf_path}: {str(e)}")
        return ""

def run_ingestion():
    targets = [
        {"input": "data/raw/Laws of the Game 2025_26_single pages.pdf", "source": "IFAB Laws of the Game 2025/26"},
        {"input": "data/raw/Video Assistant Referee (VAR) protocol _ IFAB.pdf", "source": "IFAB VAR Protocol Guidelines"}
    ]
    all_chunks = []
    chunk_idx = 0
    chunk_size = 600
    overlap = 100
    
    print("[+] Extracting visual layer rule text safely from PDF elements using pypdf...")
    for item in targets:
        if not os.path.exists(item["input"]):
            print(f"[-] Missing file source: {item['input']}")
            continue
            
        print(f"    -> Extracting visible layout layers from: {os.path.basename(item['input'])}")
        raw_text = extract_true_pdf_text(item["input"])
        sanitized_text = " ".join(raw_text.split())
        
        start = 0
        while start < len(sanitized_text):
            end = start + chunk_size
            segment = sanitized_text[start:end].strip()
            if len(segment) > 50:
                all_chunks.append({
                    "chunk_id": chunk_idx,
                    "source": item["source"],
                    "text": segment
                })
                chunk_idx += 1
            start += (chunk_size - overlap)
            
    output_path = "data/chunks/chunks.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)
    print(f"[Success] Data refreshed! Total clean rule chunks saved: {chunk_idx}")

if __name__ == "__main__":
    run_ingestion()
