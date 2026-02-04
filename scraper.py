import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_business_description(url):
    try:
        # 1. fetch
        headers = {'User-Agent': 'Mozilla/5.0...'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        html_content = response.text 
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 2. extract text
        paragraphs = [p.get_text() for p in soup.find_all('p')]
        text_content = " ".join(paragraphs[:5])
        
        return text_content, ""
        
    except Exception as e:
        return f"fetch failure: {str(e)}", ""