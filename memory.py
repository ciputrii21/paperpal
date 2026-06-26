import sqlite3
from database import init_db, DB_PATH

def save_search(keyword):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO search_history (keyword) VALUES (?)
    """, (keyword,))
    conn.commit()
    conn.close()

def get_search_history(limit=10):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT keyword, searched_at FROM search_history
        ORDER BY searched_at DESC LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def save_preference(key, value):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO preferences (key, value) VALUES (?, ?)
    """, (key, value))
    conn.commit()
    conn.close()

def get_preference(key, default=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM preferences WHERE key = ?", (key,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else default

def get_suggestions():
    history = get_search_history(limit=5)
    if not history:
        return []
    keywords = [row[0] for row in history]
    return list(set(keywords))

if __name__ == "__main__":
    init_db()
    save_search("machine learning")
    save_search("deep learning")
    save_search("natural language processing")
    save_preference("sort", "citationCount")
    save_preference("year_start", "2020")
    
    print("Riwayat pencarian:")
    for row in get_search_history():
        print(f"  - {row[0]} ({row[1]})")
    
    print(f"\nSuggestions: {get_suggestions()}")
    print(f"Sort preference: {get_preference('sort')}")
