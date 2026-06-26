import time
from search import search_papers
from memory import save_search, get_search_history, save_preference, get_preference, get_suggestions
from summarizer import summarize_paper
from database import init_db

def run_search(keyword, limit=10, year_start=None, year_end=None, sort="citationCount", lang="id"):
    # Init database
    init_db()
    
    # Simpan ke memory
    save_search(keyword)
    
    # Cari papers
    print(f"\nMencari paper: '{keyword}'...")
    papers = search_papers(keyword, limit=limit, year_start=year_start, year_end=year_end, sort=sort)
    
    if not papers:
        print("Tidak ada hasil ditemukan.")
        return []
    
    # Proses setiap paper
    results = []
    for i, paper in enumerate(papers):
        print(f"Memproses paper {i+1}/{len(papers)}...")
        
        title = paper.get("title", "Tanpa Judul")
        abstract = paper.get("abstract", "")
        year = paper.get("year", "N/A")
        citations = paper.get("citationCount", 0)
        pdf_info = paper.get("openAccessPdf")
        url = paper.get("url", "")
        
        # Summarize
        summary = summarize_paper(title, abstract, lang=lang)
        
        # Badge
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

if __name__ == "__main__":
    results = run_search(
        keyword="deep learning",
        limit=3,
        lang="id"
    )
    
    print("\n" + "="*60)
    print("HASIL PENCARIAN PAPERPAL")
    print("="*60)
    
    for paper in results:
        print(f"\nJudul: {paper['title']}")
        print(f"Tahun: {paper['year']} | Sitasi: {paper['citations']}")
        print(f"Badge: {paper['badge']}")
        print(f"Ringkasan: {paper['summary']}")
        print("-"*40)
    
    print(f"\nSuggestions: {get_suggestions()}")
