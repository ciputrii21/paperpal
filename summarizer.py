import os
import re

try:
    import streamlit as st
    QWEN_API_KEY = st.secrets.get("QWEN_API_KEY", os.getenv("QWEN_API_KEY"))
except:
    from dotenv import load_dotenv
    load_dotenv()
    QWEN_API_KEY = os.getenv("QWEN_API_KEY")

from openai import OpenAI

QWEN_BASE_URL = "https://ws-7kjohtcpeqglh4nh.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1"

client = OpenAI(
    api_key=QWEN_API_KEY,
    base_url=QWEN_BASE_URL
)

# Stopword sederhana buat scoring kalimat (bahasa Inggris, karena abstrak paper akademik hampir selalu Inggris)
_STOPWORDS = set("""
a an the this that these those is are was were be been being have has had do does did
will would shall should can could may might must of in on at to for with by from as
and or but if then than so such it its it's we our us they their them he she his her
not no nor also which who whom whose what when where why how all any both each few
more most other some such only own same
""".split())


def _extractive_summary(abstract, num_sentences=2):
    """Pilih kalimat paling informatif dari abstrak berdasarkan frekuensi kata penting,
    lalu susun ulang sesuai urutan asli (biar tetap koheren dibaca)."""
    sentences = re.split(r'(?<=[.!?])\s+', abstract.strip())
    sentences = [s.strip() for s in sentences if len(s.strip()) > 15]

    if len(sentences) <= num_sentences:
        return '. '.join(s.rstrip('.') for s in sentences) + '.'

    word_freq = {}
    for sentence in sentences:
        words = re.findall(r'\b[a-zA-Z]+\b', sentence.lower())
        for w in words:
            if w not in _STOPWORDS and len(w) > 2:
                word_freq[w] = word_freq.get(w, 0) + 1

    scored = []
    for idx, sentence in enumerate(sentences):
        words = re.findall(r'\b[a-zA-Z]+\b', sentence.lower())
        score = sum(word_freq.get(w, 0) for w in words if w not in _STOPWORDS)
        score = score / (len(words) + 1)
        # Bonus kecil untuk kalimat pertama (biasanya berisi konteks/tujuan utama)
        if idx == 0:
            score *= 1.3
        scored.append((score, idx, sentence))

    top = sorted(scored, key=lambda x: x[0], reverse=True)[:num_sentences]
    top_sorted_by_position = sorted(top, key=lambda x: x[1])

    result = '. '.join(s.rstrip('.') for _, _, s in top_sorted_by_position) + '.'
    return result


def summarize_paper(title, abstract, lang="id"):
    if not abstract:
        if lang == "id":
            return "❓ Abstrak tidak tersedia untuk paper ini."
        return "❓ No abstract available for this paper."

    if lang == "id":
        prompt = f"""Ringkas paper akademik berikut dalam 2-3 kalimat bahasa Indonesia yang mudah dipahami mahasiswa:

Judul: {title}
Abstrak: {abstract}

Ringkasan:"""
    else:
        prompt = f"""Summarize this academic paper in 2-3 clear sentences for students:

Title: {title}
Abstract: {abstract}

Summary:"""

    try:
        response = client.chat.completions.create(
            model="qwen-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[DEBUG] Qwen API belum aktif ({type(e).__name__}), pakai mode ekstraktif.")
        short = _extractive_summary(abstract, num_sentences=2)
        if lang == "id":
            return f"📝 {short}\n\n_(Mode ekstraktif — ringkasan AI penuh akan aktif setelah verifikasi Qwen API selesai)_"
        return f"📝 {short}\n\n_(Extractive mode — full AI summary will activate once Qwen API verification completes)_"
