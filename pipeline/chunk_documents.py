# pipeline/chunk_documents.py
import json, re
from pathlib import Path
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend

BASE_DIR = Path(__file__).parent.parent

def run_ingestion():
    targets = [
        {"input": BASE_DIR/"data"/"raw"/"Laws of the Game 2025_26_single pages.pdf",
         "source": "IFAB Laws of the Game 2025/26"},
        {"input": BASE_DIR/"data"/"raw"/"Video Assistant Referee (VAR) protocol _ IFAB.pdf",
         "source": "IFAB VAR Protocol Guidelines"}
    ]
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = False
    pipeline_options.do_table_structure = False
    pipeline_options.generate_page_images = False
    pipeline_options.generate_picture_images = False
    pipeline_options.images_scale = 0.5

    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options,
                backend=PyPdfiumDocumentBackend
            )
        }
    )
    all_chunks = []; global_idx = 0
    for item in targets:
        if not item["input"].exists():
            print(f"[-] Missing: {item['input']}"); continue
        print(f"[Docling] Converting: {item['input'].name}")
        result = converter.convert(str(item["input"]))
        md = result.document.export_to_markdown()
        safe = item["input"].stem.replace(" ","_")
        audit = BASE_DIR/"data"/"processed"/safe
        audit.mkdir(parents=True, exist_ok=True)
        (audit/"docling_parsed.md").write_text(md, encoding="utf-8")
        chunks = chunk_markdown(md, item["source"], global_idx)
        global_idx += len(chunks); all_chunks.extend(chunks)
        print(f"[Docling] {len(chunks)} chunks from {item['source']}")
    out = BASE_DIR/"data"/"chunks"/"chunks.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out,"w",encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)
    print(f"\n[Done] Total chunks: {global_idx}")
    print(f"[Done] IBM Docling DocumentConverter (PyPdfiumBackend, v2.97.0)")

def chunk_markdown(text, source, start_idx, max_chunk=600, overlap=100):
    sections = re.split(r'(?=^#{1,3} )', text, flags=re.MULTILINE)
    chunks = []; idx = start_idx
    for sec in sections:
        sec = sec.strip()
        if len(sec) < 50: continue
        s = " ".join(sec.split())
        if len(s) <= max_chunk:
            chunks.append({"chunk_id":idx,"source":source,"text":s,"parser":"docling","docling_version":"2.97.0","pipeline":"StandardPdfPipeline+PyPdfium"}); idx+=1
        else:
            start=0
            while start < len(s):
                seg = s[start:start+max_chunk].strip()
                if len(seg)>50:
                    chunks.append({"chunk_id":idx,"source":source,"text":seg,"parser":"docling","docling_version":"2.97.0","pipeline":"StandardPdfPipeline+PyPdfium"}); idx+=1
                start+=(max_chunk-overlap)
    return chunks

if __name__ == "__main__":
    run_ingestion()