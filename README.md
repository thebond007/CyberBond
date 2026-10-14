# 🛡️ CyberBond

A cybersecurity and digital forensics assistant built with Streamlit and LangChain. CyberBond answers questions from a private knowledge base of course notes (RAG) and calls forensic tools when the task needs one.

https://cyberbond-7v2te4eqyipfz7vxoqq9zq.streamlit.app/

## Features

- **RAG over your notes:** PDF, DOCX, TXT and MD files are chunked, embedded locally and stored in Chroma. Answers cite the source file and page.
- **Tool-calling agent:** the model decides when to search the notes or run a tool.
- **Forensic tools:**
  - Hash calculator (MD5, SHA-1, SHA-256)
  - Timestamp converter (Unix epoch and Windows FILETIME to UTC)
  - IOC extractor (IPs, URLs, domains, emails, hashes)
  - File signature checker (magic bytes)
- **Chat UI:** multi-session sidebar, streaming responses, chat export.
- **Honest answers:** if the notes don't cover a topic, the answer is labelled as general knowledge.

## Architecture

```
User question
     |
     v
 Agent loop (agent.py) ---> Tools (tools.py)
     |                         |- search_notes -> Chroma retriever (rag/)
     |                         |- calculate_hashes
     |                         |- convert_timestamp
     |                         |- extract_iocs
     |                         `- check_file_signature
     v
 Streamed answer + tool caption + sources
```

## Tech stack

Python, Streamlit, LangChain, Chroma, sentence-transformers (`all-MiniLM-L6-v2`), Groq API (`openai/gpt-oss-20b`).

## Setup

```bash
git clone https://github.com/thebond007/CyberBond.git
cd CyberBond
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_key_here
```

Get a free key at [console.groq.com](https://console.groq.com). The model name lives in `models.py`; if Groq retires it, pick another from your account's model list.

## Build the knowledge base

Put your PDF, DOCX, TXT or MD files in `data/docs/`, then run:

```bash
python -m rag.ingest
```

Run this again whenever you add or change documents. The vector store (`data/vectorstore/`) is generated locally and not committed.

## Run

```bash
python -m streamlit run app.py
```

## Smoke tests

```bash
python test_tools.py   # offline tool checks
python test_rag.py     # retrieval + LLM
python test_agent.py   # full agent behaviour
```

## Project structure

```
app.py          Streamlits