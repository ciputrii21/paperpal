import requests
import time
import os

try:
    import streamlit as st
    S2_API_KEY = st.secrets.get("SEMANTIC_SCHOLAR_API_KEY", os.getenv("SEMANTIC_SCHOLAR_API_KEY"))
    HAS_STREAMLIT = True
except:
    from dotenv import load_dotenv
    load_dotenv()
    S2_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
    HAS_STREAMLIT = False

def _do_search(keyword, limit=10, year_start=None, year_end=None, sort="citationCount"):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    headers = {"x-api-key": S2_API_KEY}
    params = {
        "query": keyword,
        "limit": limit,
        "fields": "title,year,citationCount,abstract,openAccessPdf,url,authors"
    }
    if year_start and year_end:
        params["year"] = f"{year_start}-{year_end}"

    max_retries = 3
    for attempt in range(max_retries):
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            break
        elif response.status_code == 429:
            print(f"[DEBUG] Rate limited (attempt {attempt+1}/{max_retries}), waiting...")
            time.sleep(2 * (attempt + 1))  # backoff: 2s, 4s, 6s
        else:
            print(f"[DEBUG] Error {response.status_code}: {response.text[:300]}")
            return []
    else:
        print("[DEBUG] Gagal setelah retry, rate limit terus.")
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

# Kalau jalan di Streamlit, bungkus dengan cache biar gak spam API
if HAS_STREAMLIT:
    @st.cache_data(ttl=600, show_spinner=False)
    def search_papers(keyword, limit=10, year_start=None, year_end=None, sort="citationCount"):
        return _do_search(keyword, limit, year_start, year_end, sort)
else:
    def search_papers(keyword, limit=10, year_start=None, year_end=None, sort="citationCount"):
        return _do_search(keyword, limit, year_start, year_end, sort)
