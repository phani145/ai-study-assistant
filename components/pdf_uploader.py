import streamlit as st

from services.pdf_service import (
    extract_pdf_text,
    get_total_text_length,
    has_extractable_text,
    create_chunks,
)


def render_pdf_uploader():
    """Render PDF upload UI."""

    st.subheader("📚 Upload Study Material")

    uploaded_file = st.file_uploader(
        "Choose your study-material PDF",
        type=["pdf"],
        accept_multiple_files=False,
        help="Upload a PDF containing text-based study material."
    )

    if uploaded_file is None:
        return None

    if not uploaded_file.name.lower().endswith(".pdf"):
        st.error("Please upload a PDF file.")
        return None

    try:
        pdf_bytes = uploaded_file.getvalue()

        if not pdf_bytes:
            st.error("The uploaded PDF is empty.")
            return None

        pages = extract_pdf_text(pdf_bytes)

        if not pages:
            st.error("Could not read any pages from this PDF.")
            return None

        text_length = get_total_text_length(pages)

        st.success(
            f"PDF uploaded successfully: {uploaded_file.name}"
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Pages",
            len(pages)
        )

        col2.metric(
            "Extracted Characters",
            f"{text_length:,}"
        )

        chunks = create_chunks(pages)

        col3.metric(
            "Text Chunks",
            len(chunks)
        )

        if not has_extractable_text(pages):
            st.warning(
                "No selectable text was found. "
                "This may be a scanned/image-only PDF. "
                "OCR is not included in this first version."
            )

            return {
                "filename": uploaded_file.name,
                "pages": pages,
                "chunks": [],
                "text": "",
            }

        return {
            "filename": uploaded_file.name,
            "pages": pages,
            "chunks": chunks,
            "text": "\n\n".join(
                page.text for page in pages if page.text
            ),
        }

    except Exception as exc:
        st.error(
            f"PDF processing failed: {exc}"
        )

        return None