import fitz  # PyMuPDF
import re

def pdf_to_markdown(pdf_path, output_path):
    doc = fitz.open(pdf_path)
    markdown_content = ""
    
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text = page.get_text()
        
        # Basic formatting (you can enhance this)
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if line:
                # Convert headers (simple heuristic)
                if line.isupper() and len(line) < 60:
                    markdown_content += f"## {line}\n\n"
                else:
                    markdown_content += f"{line}\n\n"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    doc.close()

# Usage
pdf_to_markdown("/Users/arturmagalhaes/Documents/repos/datascience/agents/query-rewriter/apresentacao_Text-to-SQL com Sistemas Multiagentes.pdf", "apresentacao.md")