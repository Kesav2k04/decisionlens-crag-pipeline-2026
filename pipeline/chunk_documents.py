import os
import json

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
    """
    Split text into overlapping chunks.
    chunk_size: target characters per chunk
    overlap: characters shared between consecutive chunks
    """
    chunks = []
    if chunk_size <= 0:
        return chunks
    step = chunk_size - overlap
    if step <= 0:
        # Fallback if overlap is equal or larger than chunk_size
        step = max(1, chunk_size // 2)
    
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start += step
    return chunks

def main():
    processed_dir = os.path.join("data", "processed")
    output_json = os.path.join(processed_dir, "chunks.json")
    
    # Files to process
    files_to_process = [
        ("laws_of_the_game_parsed.txt", "Laws of the Game 2025_26_single pages.pdf"),
        ("var_protocol_parsed.txt", "Video Assistant Referee (VAR) protocol _ IFAB.pdf")
    ]
    
    all_chunks = []
    
    print("[+] Launching Python sliding-window chunking engine...")
    for filename, source_name in files_to_process:
        filepath = os.path.join(processed_dir, filename)
        if not os.path.exists(filepath):
            print(f"[-] Warning: Parsed file not found at {filepath}, skipping.")
            continue
            
        print(f"    -> Chunking document: {filename} (Source: {source_name})")
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
            
        chunks = chunk_text(text, chunk_size=500, overlap=50)
        print(f"       Generated {len(chunks)} chunks.")
        
        for chunk in chunks:
            all_chunks.append({
                "text": chunk,
                "source": source_name
            })
            
    # Save all chunks as JSON
    os.makedirs(os.path.dirname(output_json), exist_ok=True)
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)
        
    print(f"[+] Successfully saved {len(all_chunks)} chunks to {output_json}")

if __name__ == "__main__":
    main()
