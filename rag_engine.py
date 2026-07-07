import os
from dotenv import load_dotenv
from pypdf import PdfReader
import chromadb
from chromadb.utils import embedding_functions
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

chroma_client = chromadb.PersistentClient(path="./chroma_db")

embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = chroma_client.get_or_create_collection(
    name="study_docs",
    embedding_function=embedding_function
)


def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def store_chunks(chunks, source_name="sample.pdf"):
    # Check if first chunk ID already exists
    first_id = f"{source_name}_chunk_0"
    existing = collection.get(ids=[first_id])
    
    if existing["ids"]:
        print(f"'{source_name}' already exists. Skipping.")
        return

    ids = [f"{source_name}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"source": source_name, "chunk_index": i} for i in range(len(chunks))]

    collection.add(
        documents=chunks,
        ids=ids,
        metadatas=metadatas
    )
    print(f"Stored {len(chunks)} chunks in ChromaDB.")


def search(query, n_results=3):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results["documents"][0]


def generate_answer(query):
    relevant_chunks = search(query, n_results=3)
    context = "\n\n".join(relevant_chunks)

    prompt = f"""You are a helpful study assistant. Answer the question using ONLY the context below.
If the answer isn't in the context, say "I couldn't find that in the document."

Context:
{context}

Question: {query}

Answer:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    text = extract_text_from_pdf("sample.pdf")
    chunks = chunk_text(text)
    store_chunks(chunks)

    test_query = "What is a live node?"
    answer = generate_answer(test_query)
    print(f"\nQuestion: {test_query}")
    print(f"Answer: {answer}")