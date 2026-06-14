import os

from dotenv import load_dotenv
from google import genai

from services.embeddings import embed_query

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def build_context(retrieved_chunks):
    """
    Convert retrieved chunks into context
    for Gemini prompt.
    """
    
    context_parts = []

    for chunk in retrieved_chunks:

        context_parts.append(
            f"""
            Source: {chunk['source']}
            Page: {chunk['page']}

            Content:
            {chunk['text']}
            """
        )
        
    return "\n\n".join(context_parts)

def answer_question(
    question,
    vector_store,
    top_k=5
):

    # Step 1: Embed Question
    query_embedding = embed_query(
        question
    )

    # Step 2: Retrieve Relevant Chunks
    retrieved_chunks = vector_store.search(
        query_embedding,
        top_k=top_k
    )

    # Step 3: Build Context
    context = build_context(
        retrieved_chunks
    )

    # Step 4: Create Prompt
    prompt = f"""
You are a helpful assistant answering questions only from the provided documents.

Instructions:
- Answer only using the provided context.
- If the answer is not found, say:
  "I could not find this information in the uploaded documents."
- Keep answers concise.
- Do not make up information.

Context:
{context}

Question:
{question}

Answer:
"""

    # Step 5: Ask Gemini
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
    except Exception as e:
        return {
            "answer": f"Error generating answer: {str(e)}",
            "citations": []
        }

    # Step 6: Build Citations
    citations = []

    seen = set()

    for chunk in retrieved_chunks:

        citation = (
            chunk["source"],
            chunk["page"]
        )

        if citation not in seen:

            seen.add(citation)

            citations.append(
                {
                    "source": chunk["source"],
                    "page": chunk["page"],
                    "score": round(
                        chunk.get("score", 0),3)
                }
            )

    # Step 7: Return Final Response
    return {
        "answer": response.text,
        "citations": citations
    }