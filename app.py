import streamlit as st
from pipeline import run_search
from memory import get_search_history, get_suggestions, save_preference, get_preference
from database import init_db

init_db()

st.set_page_config(
    page_title="PaperPal - Research Assistant",
    page_icon="📚",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}
.paper-card {
    background: #f8f9fa;
    border-left: 4px solid #667eea;
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1rem;
}
.badge-free {
    background: #28a745;
    color: white;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 12px;
}
.badge-abstract {
    background: #6c757d;
    color: white;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>📚 PaperPal</h1>
    <p>Asisten Riset Pribadi dengan Memori AI | Personal Research Assistant with AI Memory</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/books.png", width=80)
    st.header("⚙️ Pengaturan")
    
    lang = st.selectbox(
        "Bahasa Ringkasan",
        ["id", "en"],
        format_func=lambda x: "🇮🇩 Bahasa Indonesia" if x == "id" else "🇬🇧 English"
    )
    
    sort = st.selectbox(
        "Urutkan Berdasarkan",
        ["citationCount", "year_desc", "year_asc"],
        format_func=lambda x: {
            "citationCount": "📊 Paling Banyak Dikutip",
            "year_desc": "🆕 Terbaru",
            "year_asc": "📅 Terlama"
        }[x]
    )
    
    col1, col2 = st.columns(2)
    with col1:
        year_start = st.number_input("Dari Tahun", min_value=1900, max_value=2026, value=2020)
    with col2:
        year_end = st.number_input("Sampai Tahun", min_value=1900, max_value=2026, value=2026)
    
    limit = st.slider("Jumlah Paper", min_value=5, max_value=20, value=10)
    
    st.divider()
    st.subheader("🕐 Riwayat Pencarian")
    history = get_search_history(limit=5)
    if history:
        for row in history:
            if st.button(f"🔍 {row[0]}", key=f"hist_{row[0]}_{row[1]}"):
                st.session_state.search_keyword = row[0]
                st.rerun()
    else:
        st.caption("Belum ada riwayat")
    
    st.divider()
    st.subheader("💡 Saran Topik")
    suggestions = get_suggestions()
    if suggestions:
        for s in suggestions:
            if st.button(f"✨ {s}", key=f"sug_{s}"):
                st.session_state.search_keyword = s
                st.rerun()

# Search bar
col1, col2 = st.columns([4, 1])
with col1:
    keyword = st.text_input(
        "Cari topik riset",
        value=st.session_state.get("search_keyword", ""),
        placeholder="contoh: machine learning, climate change, quantum computing...",
        label_visibility="collapsed"
    )
with col2:
    search_btn = st.button("🚀 Cari", type="primary", use_container_width=True)

if search_btn and keyword:
    save_preference("last_sort", sort)
    
    with st.spinner(f"🔍 Mencari paper tentang '{keyword}'..."):
        results = run_search(
            keyword=keyword,
            limit=limit,
            year_start=year_start,
            year_end=year_end,
            sort=sort,
            lang=lang
        )
    
    if results:
        st.success(f"✅ Ditemukan {len(results)} paper untuk **'{keyword}'**")
        st.divider()
        
        for i, paper in enumerate(results):
            with st.expander(f"{'📄' if paper['badge'] == 'Abstract Only' else '📥'} {paper['title']}", expanded=(i < 2)):
                
                col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
                with col1:
                    st.metric("📅 Tahun", paper['year'])
                with col2:
                    st.metric("📊 Sitasi", f"{paper['citations']:,}")
                with col3:
                    if paper['badge'] == "Free PDF":
                        st.success("✅ Free PDF")
                    else:
                        st.info("📋 Abstract Only")
                with col4:
                    if paper['pdf_url']:
                        st.link_button("📥 PDF", paper['pdf_url'], use_container_width=True)
                    elif paper['url']:
                        st.link_button("🔗 Lihat", paper['url'], use_container_width=True)
                
                st.write("**🤖 Ringkasan AI:**")
                st.info(paper['summary'])
                
                if paper['abstract']:
                    with st.expander("📖 Lihat Abstrak Asli"):
                        st.write(paper['abstract'])
    else:
        st.warning("⚠️ Tidak ada hasil. Coba kata kunci lain!")

elif search_btn and not keyword:
    st.error("❌ Masukkan kata kunci terlebih dahulu!")

# Footer
st.divider()
st.caption("📚 PaperPal — Built with Qwen AI & Semantic Scholar | Global AI Hackathon 2026")
