from pypdf import PdfReader
from chunker import chunk_text


def process_pdf(file_path):

    reader = PdfReader(file_path)

    chunks = []

    chunk_number = 1

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text() or ""

        text = text.strip()

        if not text:
            continue

        # Ignore reference/bibliography pages
        lower_text = text.lower()

        if "references" in lower_text and page_number >= len(reader.pages) - 2:
            continue

        page_chunks = chunk_text(
            text,
            chunk_size=1500,
            overlap=300
        )

        for chunk in page_chunks:

            chunk = chunk.strip()

            # Ignore extremely small chunks
            if len(chunk) < 100:
                continue

            chunks.append({
                "chunk_number": chunk_number,
                "page_number": page_number,
                "text": chunk
            })

            chunk_number += 1

    return chunks