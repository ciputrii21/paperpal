import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

QWEN_API_KEY = os.getenv("QWEN_API_KEY")
QWEN_BASE_URL = "https://ws-7kjohtcpeqglh4nh.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1"

client = OpenAI(
    api_key=QWEN_API_KEY,
    base_url=QWEN_BASE_URL
)

def summarize_paper(title, abstract, lang="id"):
    if not abstract:
        return "Abstrak tidak tersedia."
    
    if lang == "id":
        prompt = f"""Ringkas paper akademik berikut dalam 2-3 kalimat bahasa Indonesia yang mudah dipahami:

Judul: {title}
Abstrak: {abstract}

Ringkasan:"""
    else:
        prompt = f"""Summarize this academic paper in 2-3 clear sentences:

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
        # Placeholder kalau Qwen belum aktif
        return f"[Ringkasan otomatis belum tersedia. Abstrak: {abstract[:200]}...]"

if __name__ == "__main__":
    test_title = "Machine Learning for Beginners"
    test_abstract = "This paper introduces machine learning concepts for beginners, covering supervised and unsupervised learning methods with practical examples."
    
    print("Test summarizer:")
    print(summarize_paper(test_title, test_abstract, lang="id"))
