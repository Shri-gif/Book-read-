import pytesseract
from PIL import Image
import pdf2image
import PyPDF2
from pathlib import Path
from typing import List

class OCRProcessor:
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
    
    def is_scanned_pdf(self, pdf_path: str) -> bool:
        """Detect if PDF is scanned (image-based)"""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            page = reader.pages[0]
            return len(page.images) > 0 or page.extract_text().strip() == ""
    
    def process_pdf(self, pdf_path: str) -> str:
        """OCR scanned PDFs, pass-through digital PDFs"""
        if not self.is_scanned_pdf(pdf_path):
            # Digital PDF - extract text directly
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            return text
        
        # Scanned PDF - OCR
        images = pdf2image.convert_from_path(pdf_path)
        full_text = ""
        for img in images:
            text = pytesseract.image_to_string(img)
            full_text += text + "\n"
        return full_text
    
    def process_file(self, file_path: str) -> str:
        path = Path(file_path)
        if path.suffix.lower() == '.pdf':
            return self.process_pdf(file_path)
        # Add other formats as needed
        return Path(file_path).read_text()
