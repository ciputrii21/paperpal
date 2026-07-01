import os
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

def summarize_paper(title, abstract, lang="id"):
    if not abstract:
        if lang == "id":
            return "📋 Abstrak tidak tersedia untuk paper ini."
        return "📋 No abstract available for this paper."
    
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
        # Placeholder mode - tampilkan abstrak yang sudah dipotong rapi
        if abstract:
            sentences = abstract.split('. ')
            short = '. '.join(sentences[:2]) + '.'
            if lang == "id":
                return f"⚡ {short}"
            return f"⚡ {short}"
        if lang == "id":
            return "📋 Ringkasan tidak tersedia."
        return "📋 Summary not available."
