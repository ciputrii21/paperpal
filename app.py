import streamlit as st
from pipeline import run_search
from memory import get_search_history, get_suggestions, save_preference, get_preference
from database import init_db

# Init
init_db()

# Page config
st.set_page_config(
    page_title="PaperPal - Research Assistant",
    page_icon="📚",
    layout="wide"
)

# Header
st.title("📚 PaperPal")
st.caption("Asisten Riset Pribadi dengan Memori | Personal Research Assistant with Memory")

# Sidebar
with st.sidebar:
    st.header("⚙️ Pengaturan | Settings")
    
    lang = st.selectbox(
        "Bahasa Ringkasan | Summary Language",
        ["id", "en"],
        format_func=lambda x: "🇮🇩 Bahasa Indonesia" if x == "id" else "🇬🇧 English"
    )
    
    sort = st.selectbox(
        "Urutkan | Sort By",
        ["citationCount", "year_desc", "year_asc"],
        format_func=lambda x: {
            "citationCount": "📊 Paling Banyak Dikutip",
            "year_desc": "🆕 Terbaru",
            "year_asc": "📅 Terlama"
        }[x]
    )
    
    col1, col2 = st.columns(2)
    with col1:
        year_start = st.number_input("Tahun Dari", min_value=1900, max_value=2026, value=2020)
    with col2:
        year_end = st.number_input("Tahun Sampai", min_value=1900, max_value=2026, value=2026)
    
    limit = st.slider("Jumlah Paper", min_value=5, max_value=20, value=10)
    
    st.divider()
    
    # Riwayat pencarian
    st.header("🕐 Riwayat | History")
    history = get_search_history(limit=5)
    if history:
        for row in history:
            st.text(f"• {row[0]}")
    else:
        st.text("Belum ada riwayat")
    
    st.divider()
    
    # Suggestions
    st.header("💡 Saran Topik | Suggestions")
    suggestions = get_suggestions()
    if suggestions:
        for s in suggestions:
            if st.button(f"🔍 {s}", key=f"sug_{s}"):
                st.session_state.search_keyword = s

# Main search
keyword = st.text_input(
    "🔍 Cari topik riset | Search research topic",
    value=st.session_state.get("search_keyword", ""),
    placeholder="contoh: machine learning, climate change, quantum computing..."
)

search_btn = st.button("🚀 Cari Paper | Search Papers", type="primary")

if search_btn and keyword:
    save_preference("last_sort", sort)
    save_preference("last_lang", lang)
    
    with st.spinner(f"Mencari paper tentang '{keyword}'..."):
        results = run_search(
            keyword=keyword,
            limit=limit,
            year_start=year_start,
            year_end=year_end,
            sort=sort,
            lang=lang
        )
    
    if results:
        st.success(f"✅ Ditemukan {len(results)} paper untuk '{keyword}'")
        st.divider()
        
        for i, paper in enumerate(results):
            with st.expander(f"📄 {paper['title']}", expanded=(i < 3)):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.write(f"**Tahun:** {paper['year']}")
                with col2:
                    st.write(f"**Sitasi:** {paper['citations']}")
                with col3:
                    if paper['badge'] == "Free PDF":
                        st.success("✅ Free PDF")
                    else:
                        st.info("📋 Abstract Only")
                
                st.write("**Ringkasan:**")
                st.write(paper['summary'])
                
                if paper['pdf_url']:
                    st.link_button("📥 Download PDF", paper['pdf_url'])
                elif paper['url']:
                    st.link_button("🔗 Lihat di Semantic Scholar", paper['url'])
    else:
        st.warning("Tidak ada hasil. Coba kata kunci lain.")

elif search_btn and not keyword:
    st.error("Masukkan kata kunci terlebih dahulu!")
