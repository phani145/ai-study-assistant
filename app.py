import streamlit as st
from dotenv import load_dotenv

from components.pdf_uploader import (
    render_pdf_uploader,
)

from components.summary_view import (
    render_summary_view,
    render_study_tools,
)

from components.chat_interface import (
    render_chat_interface,
)

from components.voice_interface import (
    render_voice_interface,
)

from services.ollama_service import (
    check_ollama,
    is_model_available,
    get_available_models,
    OLLAMA_MODEL,
)


load_dotenv()


st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="🎓",
    layout="wide"
)


def initialize_session_state():
    """Initialize Streamlit session state."""

    if "document" not in st.session_state:
        st.session_state.document = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


def render_sidebar():
    """Render sidebar information."""

    with st.sidebar:

        st.title("🎓 AI Study Assistant")

        st.markdown(
            """
            Your local GenAI study companion.

            **Features**
            - 📚 PDF extraction
            - 📝 AI summaries
            - 💬 PDF Q&A
            - 🎤 Voice questions
            - 🔊 AI voice answers
            - 🧠 Study tools
            """
        )

        st.divider()

        st.subheader("🤖 AI Model")

        st.write(
            f"Model: `{OLLAMA_MODEL}`"
        )

        if check_ollama():

            st.success(
                "Ollama is running"
            )

            try:

                models = get_available_models()

                if is_model_available():

                    st.success(
                        f"`{OLLAMA_MODEL}` available"
                    )

                else:

                    st.error(
                        f"`{OLLAMA_MODEL}` not found"
                    )

                    if models:
                        st.caption(
                            "Available models:"
                        )

                        for model in models:
                            st.code(model)

            except Exception as exc:

                st.warning(str(exc))

        else:

            st.error(
                "Ollama is not running."
            )

            st.caption(
                "Start Ollama before using AI features."
            )

        st.divider()

        st.subheader("⚙️ Settings")

        st.caption(
            "LLM processing uses your local Ollama server."
        )

        st.caption(
            "PDF text is processed inside this application."
        )


def main():
    """Main application."""

    initialize_session_state()

    render_sidebar()

    st.title("🎓 AI Study Assistant")

    st.markdown(
        """
        **Learn from your own study material using local GenAI.**

        Upload a PDF, generate summaries, ask questions,
        or use your microphone.
        """
    )

    st.divider()

    document = render_pdf_uploader()

    if document is not None:

        # Update document only when a new upload exists.
        st.session_state.document = document

    document = st.session_state.document

    if document is None:

        st.info(
            "👆 Upload a study-material PDF to get started."
        )

        return

    st.divider()

    st.subheader("📄 Document Information")

    st.write(
        f"**File:** {document['filename']}"
    )

    if not document["chunks"]:

        st.warning(
            "This document does not contain extractable text."
        )

        st.info(
            "For this version, use a text-based PDF. "
            "OCR for scanned PDFs can be added later."
        )

        return

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "📝 Summary",
            "💬 Ask PDF",
            "🎤 Voice",
            "🧠 Study Tools",
            "🔍 Extracted Text",
        ]
    )

    with tab1:

        render_summary_view(
            document
        )

    with tab2:

        render_chat_interface(
            document
        )

    with tab3:

        render_voice_interface(
            document
        )

    with tab4:

        render_study_tools(
            document
        )

    with tab5:

        st.subheader(
            "🔍 Extracted PDF Text"
        )

        with st.expander(
            "Show extracted text"
        ):

            for page in document["pages"]:

                if page.text.strip():

                    st.markdown(
                        f"### Page {page.page_number}"
                    )

                    st.text(
                        page.text
                    )


if __name__ == "__main__":
    main()