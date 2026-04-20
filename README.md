# RAIN Agency Chatbot

Ask questions about RAIN in plain English — get instant answers from their actual website content.

Built with: Python · LlamaIndex · Claude (Anthropic) · Streamlit

---

## Quickstart

**1. Install**
```bash
pip install -r requirements.txt
```

**2. Set API key in terminal**
```bash
# Mac / Linux
export ANTHROPIC_API_KEY=sk-ant-your-key-here

# Windows CMD
set ANTHROPIC_API_KEY=sk-ant-your-key-here

# Windows PowerShell
$env:ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

**3. Ingest documents (once only)**
```bash
python ingest.py
```
First run downloads the embedding model (~130MB). Takes 1–2 minutes.

**4. Launch**
```bash
streamlit run app.py
```
Opens at http://localhost:8501

---

## Knowledge base (4 docs, all from rainlocal.com)

| File | Content |
|---|---|
| rain_about.txt | Who RAIN is, clients, testimonials, specialties |
| rain_services.txt | Digital ads, creative, web optimization, reporting |
| rain_blog.txt | AI + compliance article, digital marketing playbook |
| rain_case_studies.txt | La Capitol ($34.3M deposits) + bank hiring (161% more applications) |

All content sourced directly from rainlocal.com — no invented data.

---

## Example questions
- "What does RAIN do?"
- "Does RAIN work with credit unions?"
- "Tell me about the La Capitol case study"
- "What results did RAIN get for the bank hiring campaign?"
- "How does RAIN handle compliance for financial ads?"
- "What channels does RAIN run campaigns on?"
- "How does RAIN use AI in marketing?"
- "Who are some of RAIN's clients?"

---

## Project structure
```
rain-knowledge-bot/
├── docs/
│   ├── rain_about.txt
│   ├── rain_services.txt
│   ├── rain_blog.txt
│   └── rain_case_studies.txt
├── storage/        ← auto-created by ingest.py
├── ingest.py
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```
