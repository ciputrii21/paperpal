import os
try:
    import streamlit as st
    QWEN_API_KEY = st.secrets.get("QWEN_API_KEY", os.getenv("QWEN_API_KEY"))
    S2_API_KEY = st.secrets.get("SEMANTIC_SCHOLAR_API_KEY", os.getenv("SEMANTIC_SCHOLAR_API_KEY"))
except:
    from dotenv import load_dotenv
    load_dotenv()
    QWEN_API_KEY = os.getenv("QWEN_API_KEY")
    S2_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")

from openai import OpenAI

QWEN_BASE_URL = "https://ws-7kjohtcpeqglh4nh.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1"

client = OpenAI(
    api_key=QWEN_API_KEY,
    base_url=QWEN_BASE_URL
)

def summarize_paper(title, abstract, lang="id"):
    if not abstract:
        return "Abstrak tidak tersedia."
    
    if lang == "id":
        prompt = f"""Ringkas paper akademik berikut dalam 2-3 kalimat bahasa Indonesia:

Judul: {title}
Abstrak: {abstract}

Ringkasan:"""
    else:
        prompt = f"""Summarize this academic paper in 2-3 sentences:

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
        return f"[Ringkasan belum tersedia. Abstrak: {abstract[:200]}...]"
