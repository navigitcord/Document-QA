from flask import (
    Flask,
    render_template,
    request
)

import os

from services.pdf_processor import extract_pdf_text
from services.chunker import create_chunks

from services.embeddings import (
    embed_documents
)

from services.vector_store import (
    FAISSVectorStore
)

from services.rag_pipeline import (
    answer_question
)

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

vector_store = None
# Home Route
@app.route("/")
def home():

    return render_template(
        "index.html"
    )
# Upload Route
@app.route( "/upload", methods=["POST"])
def upload():
    # Get Files
    files = request.files.getlist("pdfs")

    # Validate files uploaded
    if not files or all(file.filename == "" for file in files):
        return render_template(
            "index.html",
            error="Please upload at least one PDF."
        )

    # Assignment requirement: 1-3 PDFs
    if len(files) > 3:
        return render_template(
            "index.html",
            error="Maximum 3 PDF files are allowed."
        )
    #Process PDFs
    all_chunks = []

    for file in files:

        # PDF File Validation
        if not file.filename.lower().endswith(".pdf"):
            return render_template(
                "index.html",
                error=f"{file.filename} is not a PDF file."
            )
        filepath = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )
        
        file.save(filepath)

        pages = extract_pdf_text(
            filepath
        )

        chunks = create_chunks(
            pages
        )

        all_chunks.extend(
            chunks
        )
        print(f"Total chunks: {len(all_chunks)}")

    # Create Embeddings

    embedded_chunks = embed_documents(
        all_chunks
    )

    # Create FAISS Index

    global vector_store

    vector_store = FAISSVectorStore()

    vector_store.create_index(
        embedded_chunks
    )

    print(
        f"Created vector store with {len(embedded_chunks)} chunks"
    )
    print("FAISS index created successfully")
    return render_template(
        "index.html",
        upload_success=True,
        total_chunks=len(all_chunks)
    )
    

# Ask Question Route
@app.route(
"/ask",
methods=["POST"]
)
def ask():
    # print("Ask route called")
    # print(vector_store)
    # Validation
    if vector_store is None:

        return render_template(
            "index.html",
            error="Please upload PDFs first."
        )
    # Get Question
    question = request.form.get(
        "question"
    )
    if not question.strip():
        return render_template(
            "index.html",
            error="Please enter a question."
        )
    # RAG
    result = answer_question(
        question,
        vector_store
    )
    return render_template(
        "index.html",
        answer=result["answer"],
        citations=result["citations"]
    )
    
# Run App
if __name__ == "__main__":

    app.run(
        debug=True
    )
