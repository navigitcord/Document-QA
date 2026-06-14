from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_chunks(page_data):
    """
    Split extracted PDF pages into chunks while
    preserving metadata.

    Input:
    [
        {
            "text": "...",
            "page": 1,
            "source": "file.pdf"
        }
    ]

    Output:
    [
        {
            "text": "...chunk...",
            "page": 1,
            "source": "file.pdf"
        }
    ]
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    chunks = []
    chunk_id = 0

    for page in page_data:

        split_chunks = splitter.split_text(page["text"])

        for chunk in split_chunks:

            chunks.append(
                {
                    "id": chunk_id,
                    "text": chunk,
                    "page": page["page"],
                    "source": page["source"]
                }
            )

            chunk_id += 1
        return chunks