\# AI Study Assistant



A RAG-based AI assistant that answers questions from your own PDF notes using semantic search and LLM generation.



\## How It Works



1\. Upload any PDF (lecture notes, textbook chapters, research papers)

2\. The system chunks the text and stores embeddings in a local vector database (ChromaDB)

3\. When you ask a question, it retrieves the most relevant chunks using semantic similarity

4\. Llama 3.3 (via Groq API) generates a grounded answer using only your document as context



\## Tech Stack



\- \*\*Python\*\* — core language

\- \*\*ChromaDB\*\* — vector database for semantic search

\- \*\*Sentence Transformers\*\* — local embedding model (all-MiniLM-L6-v2)

\- \*\*Groq API\*\* — LLM inference (Llama 3.3 70B)

\- \*\*Streamlit\*\* — web interface

\- \*\*pypdf\*\* — PDF text extraction



\## Architecture



PDF → Text Extraction → Chunking (500 chars, 50 overlap) → Embeddings → ChromaDB



Question → Embedding → Similarity Search → Top 3 Chunks → Llama 3.3 → Answer



\## Known Limitations and Future Improvements



\- Retrieval always returns top-k results regardless of relevance score — a similarity threshold would improve precision

\- Fixed chunk size may split definitions across boundaries — dynamic chunking based on document structure would help

\- No conversation memory — follow-up questions lose prior context



\## Setup



Clone the repo and install dependencies:



&#x20;   git clone https://github.com/Aditya1546/ai-study-assistant

&#x20;   cd ai-study-assistant

&#x20;   python -m venv venv

&#x20;   venv\\Scripts\\activate

&#x20;   pip install -r requirements.txt



Add a .env file with your Groq API key:



&#x20;   GROQ\_API\_KEY=your\_key\_here



Run the app:



&#x20;   streamlit run app.py

