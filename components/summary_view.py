import streamlit as st

from prompts.summary_prompts import (
    SHORT_SUMMARY_PROMPT,
    DETAILED_SUMMARY_PROMPT,
    MCQ_PROMPT,
    FLASHCARD_PROMPT,
    EXAM_QUESTIONS_PROMPT,
)

from services.ollama_service import (
    generate_response,
    OllamaError,
)


def _build_context(document, max_characters=18000):
    """Create a safe LLM context from document chunks."""

    chunks = document["chunks"]

    if not chunks:
        return ""

    selected = []
    total = 0

    for chunk in chunks:
        pages = ", ".join(
            str(page)
            for page in chunk.page_numbers
        )

        text = (
            f"[Page {pages}]\n"
            f"{chunk.text}\n\n"
        )

        if total + len(text) > max_characters:
            break

        selected.append(text)
        total += len(text)

    return "".join(selected)


def render_summary_view(document):
    """Render PDF summary and study tools."""

    st.subheader("📝 PDF Summaries")

    if not document["chunks"]:
        st.warning(
            "There is no extractable text to summarize."
        )
        return

    context = _build_context(document)

    tab1, tab2 = st.tabs(
        [
            "Short Summary",
            "Detailed Summary",
        ]
    )

    with tab1:

        if st.button(
            "Generate Short Summary",
            key="short_summary_button"
        ):

            prompt = SHORT_SUMMARY_PROMPT.format(
                context=context
            )

            with st.spinner(
                "Gemma 3:1B is creating your summary..."
            ):

                try:
                    result = generate_response(prompt)
                    st.markdown(result)

                except OllamaError as exc:
                    st.error(str(exc))

    with tab2:

        if st.button(
            "Generate Detailed Summary",
            key="detailed_summary_button"
        ):

            prompt = DETAILED_SUMMARY_PROMPT.format(
                context=context
            )

            with st.spinner(
                "Generating detailed exam notes..."
            ):

                try:
                    result = generate_response(prompt)
                    st.markdown(result)

                except OllamaError as exc:
                    st.error(str(exc))


def render_study_tools(document):
    """Render optional study tools."""

    st.subheader("🧠 Study Tools")

    if not document["chunks"]:
        st.warning(
            "Upload a text-based PDF first."
        )
        return

    context = _build_context(
        document,
        max_characters=16000
    )

    difficulty = st.selectbox(
        "Difficulty",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "Generate MCQs",
            key="mcq_button"
        ):

            prompt = MCQ_PROMPT.format(
                count=5,
                context=(
                    f"Difficulty: {difficulty}\n\n"
                    f"{context}"
                )
            )

            with st.spinner("Generating MCQs..."):

                try:
                    st.markdown(
                        generate_response(prompt)
                    )

                except OllamaError as exc:
                    st.error(str(exc))

    with col2:

        if st.button(
            "Generate Flashcards",
            key="flashcard_button"
        ):

            prompt = FLASHCARD_PROMPT.format(
                context=context
            )

            with st.spinner(
                "Generating flashcards..."
            ):

                try:
                    st.markdown(
                        generate_response(prompt)
                    )

                except OllamaError as exc:
                    st.error(str(exc))

    with col3:

        if st.button(
            "Important Questions",
            key="exam_questions_button"
        ):

            prompt = EXAM_QUESTIONS_PROMPT.format(
                context=context
            )

            with st.spinner(
                "Generating exam questions..."
            ):

                try:
                    st.markdown(
                        generate_response(prompt)
                    )

                except OllamaError as exc:
                    st.error(str(exc))