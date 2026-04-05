import openai
from typing import Dict, List
import json

class AIProcessor:
    def __init__(self, api_key: str):
        openai.api_key = api_key
    
    def generate_title(self, content: str) -> str:
        prompt = f"""
        Generate a compelling book title based on this content.
        Content preview: {content[:1000]}...
        
        Return ONLY the title, no explanations:
        """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=20
        )
        return response.choices[0].message.content.strip()
    
    def generate_preface(self, metadata: Dict) -> str:
        prompt = f"""
        Write a professional preface for a book with this metadata:
        Title: {metadata.get('title', 'Unknown')}
        Author: {metadata.get('author', 'Unknown')}
        
        Keep it 150-200 words. Professional academic tone.
        """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    
    def rewrite_content(self, content: str, percent_change: int) -> str:
        """Rewrite content preserving structure"""
        if percent_change == 0:
            return content
        
        direction = "expand" if percent_change > 0 else "reduce"
        target_length = len(content) * (1 + abs(percent_change) / 100)
        
        prompt = f"""
        Rewrite this content {direction}ing it by {abs(percent_change)}%.
        Original length: {len(content)} chars
        Target length: ~{int(target_length)} chars
        
        PRESERVE:
        - All tables, equations, figures
        - Headings and structure
        - Technical accuracy
        
        Content:
        {content}
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=int(target_length//4)
        )
        return response.choices[0].message.content.strip()
