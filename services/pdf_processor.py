from pypdf import PdfReader
import os


def extract_pdf_text(pdf_path):
    """
    Extract text from a PDF page-by-page.

    Returns:
    [
        {
            "text": "...",
            "page": 1,
            "source": "document.pdf"
        }
    ]
    """

    reader = PdfReader("JD Engineer AIML.pdf")

    pages = []

    filename = os.path.basename(pdf_path)

    for page_num, page in enumerate(reader.pages, start=1):

        text = page.extract_text()

        if text and text.strip():

            pages.append(
                {
                    "text": text.strip(),
                    "page": page_num,
                    "source": filename
                }
            )

    return pages