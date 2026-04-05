import pandas as pd
from typing import Dict, Any, List
from openpyxl import load_workbook

class ExcelMetadataParser:
    def __init__(self, file):
        self.df = pd.read_excel(file)
        self.wb = load_workbook(file)
    
    def parse_dynamic(self) -> List[Dict[str, Any]]:
        """Dynamically map Excel columns without hardcoding"""
        records = []
        
        # Auto-detect metadata columns (common patterns)
        metadata_patterns = {
            'title': ['title', 'Title', 'TITLE', 'book_title'],
            'author': ['author', 'Author', 'AUTHOR', 'editor'],
            'isbn': ['isbn', 'ISBN', 'eisbn'],
            'year': ['year', 'Year', 'YEAR', 'publication_year']
        }
        
        for idx, row in self.df.iterrows():
            record = {}
            
            # Map all columns dynamically
            for col in self.df.columns:
                # Find best matching metadata field
                matched_field = None
                for field, patterns in metadata_patterns.items():
                    if any(pattern in col.lower() for pattern in patterns):
                        matched_field = field
                        break
                
                if matched_field:
                    record[matched_field] = str(row[col]).strip()
                else:
                    # Store as custom field
                    record[f"custom_{col.lower()}"] = str(row[col]).strip()
            
            records.append(record)
        
        return records
