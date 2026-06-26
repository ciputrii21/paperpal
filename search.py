import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

S2_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")

def search_papers(keyword, limit=10, year_start=None, year_end=None, sort="citationCount"):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    headers = {"x-api-key": S2_API_KEY}
    params = {
        "query": keyword,
        "limit": limit,
        "fields": "title,year,citationCount,abstract,openAccessPdf,url,authors"
    }
    
    if year_start and year_end:
        params["year"] = f"{year_start}-{year_end}"
    
    time.sleep(1)
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.json()}")
        return []
    
    data = response.json()
    papers = data.get("data", [])
    
    if sort == "year_desc":
        papers.sort(key=lambda x: x.get("year") or 0, reverse=True)
    elif sort == "year_asc":
        papers.sort(key=lambda x: x.get("year") or 0)
    elif sort == "citationCount":
        papers.sort(key=lambda x: x.get("citationCount") or 0, reverse=True)
    
    return papers

if __name__ == "__main__":
    results = search_papers("machine learning", limit=5)
    for p in results:
        print(f"\n- {p['title']}")
        print(f"  Tahun: {p.get('year', 'N/A')}")
        print(f"  Sitasi: {p.get('citationCount', 0)}")
        pdf = p.get('openAccessPdf')
        print(f"  PDF: {'Free PDF' if pdf else 'Abstract Only'}")
