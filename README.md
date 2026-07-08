---
title: AI Study Assistant
emoji: 🎓
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# AI Study Assistant

A RAG-based AI assistant that answers questions from your own PDF notes using semantic search and LLM generation.

## How It Works

1. Upload any PDF (lecture notes, textbook chapters, research papers)
2. The system chunks the text and stores embeddings in a local vector database (ChromaDB)
3. When you ask a question, it retrieves the most relevant chunks using semantic similarity
4. Llama 3.3 (via Groq API) generates a grounded answer using only your document as context

## Tech Stack

- Python — core language
- ChromaDB — vector database for semantic search
- Sentence Transformers — local embedding model (all-MiniLM-L6-v2)
- Groq API — LLM inference (Llama 3.3 70B)
- Streamlit — web interface
- pypdf — PDF text extraction

## Architecture

PDF → Text Extraction → Chunking → Embeddings → ChromaDB

Question → Embedding → Similarity Search → Top 3 Chunks → Llama 3.3 → Answer

## Known Limitations and Future Improvements

- Retrieval always returns top-k regardless of relevance score
- Fixed chunk size may split definitions across boundaries
- No conversation memory for follow-up questions

## Setup

Clone and install:

    git clone https://github.com/Aditya1546/ai-study-assistant
    cd ai-study-assistant
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt

Add a .env file:

    GROQ_API_KEY=your_key_here

Run:

    streamlit run app.py---

    GROQ_API_KEY=your_key_here

Run:

    streamlit run app.py
