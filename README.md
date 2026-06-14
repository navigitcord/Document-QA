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

* OCR support for scanned PDFs.
* Persistent vector storage.
* Hybrid Retrieval (BM25 + Semantic Search).
* Section-aware citations.
* Streaming responses.
* Authentication and multi-user support.
* Docker containerization.
* Automated evaluation and testing.


## Known Limitations

* Supports text-based PDFs only.
* OCR is not implemented for scanned/image PDFs.
* Vector index is stored in memory and rebuilt on each application restart.
* Citations currently provide document name and page number rather than exact section headings.
* Optimized for small document collections (1-3 PDFs) as required by the assignment.