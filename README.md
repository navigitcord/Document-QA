# Document Q&A Application

A Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask natural language questions about their content.

## Features

* Upload 1-3 PDF documents
* Semantic document search using FAISS
* Question answering using Gemini 2.5 Flash
* Source citations with document name and page number
* Simple Flask web interface

## Architecture

PDF Upload → Text Extraction → Chunking → Embeddings → FAISS Retrieval → Gemini Generation → Answer + Citations

## Tech Stack

* Python
* Flask
* PyPDF
* Sentence Transformers
* FAISS
* Gemini 2.5 Flash

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

Run:

```bash
python app.py
```

Open:

http://127.0.0.1:5000

## Design Decisions

* SentenceTransformers used for local embeddings
* FAISS used for semantic retrieval
* Gemini used only for answer generation
* Metadata preserved for citations

## Future Improvements

* OCR support
* Hybrid search
* Persistent vector storage
* Streaming responses
* Authentication and multi-user support
