import subprocess
import pandoc
from pandoc import Document
from .ocr import OCRProcessor
from .ai_processor import AIProcessor
from .table_formatter import TableFormatter
from pathlib import Path

class EbookPipeline:
    def __init__(self, config):
        self.ocr = OCRProcessor()
        self.ai = AIProcessor(config.openai_key)
        self.templates_dir = config.templates_dir
    
    def process_batch(self, file_paths: List[str], metadata: List[Dict], 
                     work_dir: str, rewrite_percent: int, generate_content: bool):
        
        results = []
        
        for file_path, meta in zip(file_paths, metadata):
            try:
                # 1. Content Extraction
                content = self.extract_content(file_path)
                
                # 2. AI Processing
                if generate_content:
                    title = self.ai.generate_title(content)
                    preface = self.ai.generate_preface(meta)
                    content = f"{preface}\n\n{content}"
                    meta['title'] = title
                
                if rewrite_percent != 0:
                    content = self.ai.rewrite_content(content, rewrite_percent)
                
                # 3. Format tables
                content = TableFormatter.format_tables_for_epub(content)
                
                # 4. Generate structured EPUB
                epub_path = self.generate_epub(content, meta, work_dir)
                
                results.append({
                    'input': file_path,
                    'output': epub_path,
                    'status': 'success'
                })
                
            except Exception as e:
                results.append({
                    'input': file_path,
                    'status': 'error',
                    'error': str(e)
                })
        
        return results
    
    def generate_epub(self, content: str, metadata: Dict, work_dir: str) -> str:
        # Load EPUB template
        template_path = Path(self.templates_dir) / "epub_template.html"
        template = template_path.read_text()
        
        # Replace metadata variables
        for key, value in metadata.items():
            template = template.replace(f"{{{{{key.upper()}}}}}", value)
        
        # Insert content
        final_html = template.replace("{{CONTENT}}", content)
        
        # Convert with Pandoc
        doc = Document()
        doc.content = final_html
        epub_path = f"{work_dir}/output.epub"
        doc.save(epub_path)
        
        return epub_path
