# PaperPal

AI-powered research assistant built with **Qwen Cloud** for searching, analyzing, and chatting with academic papers.

## Features

- 🔍 Search academic papers using Semantic Scholar
- 📄 Generate concise AI summaries
- 💬 Chat with papers using Qwen
- 🧠 Persistent conversation memory
- 📚 Compare multiple papers
- ⚡ Fast Streamlit interface

---

# Requirements

Before you begin, install:

- Python 3.10+
- Git

Verify your installation:

```bash
python --version
git --version
```

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/ciputrii21/paperpal.git
cd paperpal
```

---

## 2. Create a virtual environment

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# Configure Environment Variables

The project already includes a `.env.example` file.

Copy it to `.env`.

### Windows

```powershell
copy .env.example .env
```

or

```powershell
Copy-Item .env.example .env
```

### Linux / macOS

```bash
cp .env.example .env
```

Open the `.env` file and replace the placeholder values with your own API keys.

Example:

```env
QWEN_API_KEY="your_qwen_api_key_here"
SEMANTIC_SCHOLAR_API_KEY="your_semantic_scholar_api_key_here"
```

### Required API Keys

#### Qwen Cloud

Create an API key:

https://modelstudio.console.alibabacloud.com

#### Semantic Scholar

Create an API key:

https://www.semanticscholar.org/product/api

---

# Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

Then open your browser:

```
http://localhost:8501
```

---

# How to Use

1. Enter a research topic or keyword.
2. Search for relevant papers.
3. Select a paper from the results.
4. Generate an AI summary.
5. Ask follow-up questions.
6. Continue the conversation with memory across the session.

---



# Project Structure

<img width="1536" height="1024" alt="Project_Diagram" src="https://github.com/user-attachments/assets/bf148539-0f59-47d0-a2f0-cfbd744882bf" />

# Architecture Diagram

<img width="1122" height="1402" alt="Architecture_Diagram" src="https://github.com/user-attachments/assets/52035d0e-e5d5-4c6c-af42-c79592166cae" />



---

# Troubleshooting

### Missing API Key

Make sure `.env` exists and contains valid API keys.

### ModuleNotFoundError

Reinstall dependencies:

```bash
pip install -r requirements.txt
```

### Streamlit command not found

Run:

```bash
python -m streamlit run app.py
```
### PowerShell blocks virtual environment activation

If you see an error similar to:

```text
running scripts is disabled on this system
```

Run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
```

Then activate the virtual environment again:

```powershell
.venv\Scripts\activate
```



---

# Technologies

- Qwen Cloud
- Alibaba Cloud DashScope
- Semantic Scholar API
- Streamlit
- Python

---

# License

This project is released under the MIT License.
