import time
from search import search_papers
from memory import save_search, get_search_history, save_preference, get_preference, get_suggestions
from summarizer import summarize_paper
from database import init_db

def run_search(keyword, limit=10, year_start=None, year_end=None, sort="citationCount", lang="id"):
    init_db()
    save_search(keyword)
    
    print(f"Mencari paper: '{keyword}'...")
    papers = search_papers(keyword, limit=limit, year_start=year_start, year_end=year_end, sort=sort)
    
    if not papers:
        return []
    
    results = []
    for i, paper in enumerate(papers):
        title = paper.get("title", "Tanpa Judul")
        abstract = paper.get("abstract", "")
        year = paper.get("year", "N/A")
        citations = paper.get("citationCount", 0)
        pdf_info = paper.get("openAccessPdf")
        url = paper.get("url", "")
        
        summary = summarize_paper(title, abstract, lang=lang)
        
        badge = "Free PDF" if pdf_info else "Abstract Only"
        pdf_url = pdf_info.get("url", "") if pdf_info else ""
        
        results.append({
            "title": title,
            "year": year,
            "citations": citations,
            "badge": badge,
            "pdf_url": pdf_url,
            "url": url,
            "summary": summary,
            "abstract": abstract
        })
        
        time.sleep(1)
    
    return results
