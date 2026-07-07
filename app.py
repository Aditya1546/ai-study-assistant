import streamlit as st
from rag_engine import extract_text_from_pdf, chunk_text, store_chunks, generate_answer, collection
import tempfile
import os

st.title("AI Study Assistant")
st.write("Upload your notes and ask questions about them.")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    with st.spinner("Processing your PDF..."):
        text = extract_text_from_pdf(tmp_path)
        chunks = chunk_text(text)
        first_id = f"{uploaded_file.name}_chunk_0"
        already_exists = bool(collection.get(ids=[first_id])["ids"])
        store_chunks(chunks, source_name=uploaded_file.name)
        os.unlink(tmp_path)

    if already_exists:
        st.info(f"'{uploaded_file.name}' already loaded. Ready to answer questions.")
    else:
        st.success(f"Loaded {len(chunks)} chunks from your PDF.")

    question = st.text_input("Ask a question about your notes:")

    if question:
        with st.spinner("Thinking..."):
            answer = generate_answer(question)
        st.markdown(f"**Answer:** {answer}")