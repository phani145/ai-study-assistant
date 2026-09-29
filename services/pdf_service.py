from dataclasses import dataclass
from typing import List

import fitz


@dataclass
class PageText:
    page_number: int
    text: str


@dataclass
class TextChunk:
    text: str
    page_numbers: List[int]


def extract_pdf_text(pdf_bytes: bytes) -> List[PageText]:
    """
    Extract text from every page of a PDF.

    Returns:
        List[PageText]
    """

    pages = []

    try:
        document = fitz.open(stream=pdf_bytes, filetype="pdf")

        for page_index, page in enumerate(document):
            text = page.get_text("text").strip()

            pages.append(
                PageText(
                    page_number=page_index + 1,
                    text=text
                )
            )

        document.close()

    except Exception as exc:
        raise RuntimeError(f"Could not read PDF: {exc}") from exc

    return pages


def get_total_text_length(pages: List[PageText]) -> int:
    """Return total extracted character count."""

    return sum(len(page.text) for page in pages)


def has_extractable_text(pages: List[PageText]) -> bool:
    """Check whether the PDF contains usable text."""

    return any(page.text.strip() for page in pages)


def create_chunks(
    pages: List[PageText],
    chunk_size: int = 3500,
    overlap: int = 400
) -> List[TextChunk]:
    """
    Create page-aware text chunks.

    The overlap helps preserve context between chunks.
    """

    chunks = []

    for page in pages:
        text = page.text.strip()

        if not text:
            continue

        start = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    TextChunk(
                        text=chunk_text,
                        page_numbers=[page.page_number]
                    )
                )

            if end >= len(text):
                break

            start = max(end - overlap, start + 1)

    return chunks


def get_full_text(pages: List[PageText]) -> str:
    """Combine all extracted page text."""

    sections = []

    for page in pages:
        if page.text.strip():
            sections.append(
                f"[Page {page.page_number}]\n{page.text.strip()}"
            )

    return "\n\n".join(sections)


def retrieve_relevant_chunks(
    question: str,
    chunks: List[TextChunk],
    top_k: int = 5
) -> List[TextChunk]:
    """
    Simple local retrieval based on word overlap.

    This avoids adding FAISS/Chroma in the first version.
    """

    stop_words = {
        "the", "is", "a", "an", "and", "or", "of", "to",
        "in", "on", "for", "what", "why", "how", "when",
        "where", "which", "who", "are", "was", "were",
        "with", "from", "this", "that", "about"
    }

    question_words = {
        word.lower().strip(".,?!:;()[]{}")
        for word in question.split()
        if len(word) > 2
    }

    question_words -= stop_words

    scored_chunks = []

    for chunk in chunks:
        chunk_words = {
            word.lower().strip(".,?!:;()[]{}")
            for word in chunk.text.split()
        }

        score = len(question_words.intersection(chunk_words))

        scored_chunks.append((score, chunk))

    scored_chunks.sort(
        key=lambda item: item[0],
        reverse=True
    )

    selected = [
        chunk
        for score, chunk in scored_chunks[:top_k]
        if score > 0
    ]

    # If no keyword matches exist, provide the first chunks
    # rather than pretending that nothing exists.
    if not selected:
        selected = chunks[:top_k]

    return selected


def format_chunks_for_prompt(chunks: List[TextChunk]) -> str:
    """Format chunks with their page references."""

    sections = []

    for chunk in chunks:
        pages = ", ".join(
            str(page)
            for page in chunk.page_numbers
        )

        sections.append(
            f"[Source: Page {pages}]\n{chunk.text}"
        )

    return "\n\n".join(sections)