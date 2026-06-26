import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("QWEN_API_KEY"),
    base_url="https://ws-7kjohtcpeqglh4nh.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1"
)

response = client.chat.completions.create(
    model="qwen3.7-plus-2026-05-26",
    messages=[
        {"role": "user", "content": "Say hello in one sentence!"}
    ]
)

print("Qwen API berhasil!")
print(response.choices[0].message.content)
