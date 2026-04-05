import re
from bs4 import BeautifulSoup

class TableFormatter:
    @staticmethod
    def format_tables_for_epub(html_content: str) -> str:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        for table in soup.find_all('table'):
            # Add grid borders (hairline 0.25pt)
            table['style'] = getattr(table, 'style', '') + '; border-collapse: collapse;'
            
            for row in table.find_all('tr'):
                for cell in row.find_all(['td', 'th']):
                    cell['style'] = (getattr(cell, 'style', '') + 
                                   '; border: 0.25pt solid black; padding: 8px;')
        
        return str(soup)
