import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")

def search_papers(keyword):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    headers = {"x-api-key": API_KEY}
    params = {
        "query": keyword,
        "limit": 5,
        "fields": "title,year,citationCount,abstract,openAccessPdf,url"
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    print(f"Status: {response.status_code}")
    print(f"\nHasil pencarian: '{keyword}'")
    print("=" * 50)
    
    for paper in data["data"]:
        print(f"\n- {paper['title']}")
        print(f"  Tahun: {paper.get('year', 'N/A')}")
        print(f"  Sitasi: {paper.get('citationCount', 0)}")
        pdf = paper.get('openAccessPdf')
        print(f"  PDF: {'Free PDF' if pdf else 'Abstract Only'}")

search_papers("machine learning")
