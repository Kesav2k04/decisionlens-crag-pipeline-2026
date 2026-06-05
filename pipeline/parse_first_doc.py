import os
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat

def run_ingestion():
    source_pdf = os.path.join("data", "raw", "Laws of the Game 2025_26_single pages.pdf")
    output_txt = os.path.join("data", "processed", "laws_of_the_game_parsed.txt")
    
    print(f"[+] Launching Light-Weight Memory Guarded Docling against: {source_pdf}")
    if not os.path.exists(source_pdf):
        print(f"[-] Error: Source file not found at {source_pdf}")
        return

    # Turn off heavy AI model weights to protect system RAM
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = False               
    pipeline_options.do_table_structure = False   
    pipeline_options.num_threads = 1              

    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )
    
    result = converter.convert(source_pdf)
    exported_text = result.document.export_to_markdown()
    
    os.makedirs(os.path.dirname(output_txt), exist_ok=True)
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(exported_text)
        
    print(f"[+] Execution successful! Text layout extracted to: {output_txt}")

if __name__ == '__main__':
    run_ingestion()
