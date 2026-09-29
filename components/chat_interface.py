import streamlit as st

from prompts.qa_prompts import (
    QA_PROMPT,
    QA_SYSTEM_PROMPT,
)

from services.pdf_service import (
    retrieve_relevant_chunks,
    format_chunks_for_prompt,
)

from services.ollama_service import (
    generate_response,
    OllamaError,
)


def initialize_chat_history():
    """Initialize conversation history."""

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


def clear_chat():
    """Clear conversation history."""

    st.session_state.chat_history = []


def answer_question(
    question: str,
    document
) -> tuple[str, list[int]]:
    """
    Retrieve relevant PDF chunks and answer the question.
    """

    chunks = retrieve_relevant_chunks(
        question,
        document["chunks"],
        top_k=5
    )

    if not chunks:
        return (
            "I couldn't find this information in the uploaded PDF.",
            []
        )

    context = format_chunks_for_prompt(chunks)

    prompt = QA_PROMPT.format(
        context=context,
        question=question
    )

    answer = generate_response(
        prompt=prompt,
        system_prompt=QA_SYSTEM_PROMPT,
        temperature=0.1
    )

    source_pages = sorted(
        {
            page
            for chunk in chunks
            for page in chunk.page_numbers
        }
    )

    return answer, source_pages


def render_chat_interface(document):
    """Render PDF question-answering chat."""

    st.subheader("💬 Ask Questions From Your PDF")

    initialize_chat_history()

    col1, col2 = st.columns([5, 1])

    with col2:

        if st.button(
            "Clear Chat",
            use_container_width=True
        ):
            clear_chat()
            st.rerun()

    for message in st.session_state.chat_history:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

            if message.get("sources"):
                st.caption(
                    "📖 Source: "
                    + ", ".join(
                        f"Page {page}"
                        for page in message["sources"]
                    )
                )

    question = st.chat_input(
        "Ask something about your PDF..."
    )

    if question:

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": question,
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):

            with st.spinner(
                "Searching the PDF and asking Gemma..."
            ):

                try:

                    answer, sources = answer_question(
                        question,
                        document
                    )

                    st.markdown(answer)

                    if sources:
                        st.caption(
                            "📖 Source: "
                            + ", ".join(
                                f"Page {page}"
                                for page in sources
                            )
                        )

                    st.session_state.chat_history.append(
                        {
                            "role": "assistant",
                            "content": answer,
                            "sources": sources,
                        }
                    )

                except OllamaError as exc:

                    error_message = str(exc)

                    st.error(error_message)

                    st.session_state.chat_history.append(
                        {
                            "role": "assistant",
                            "content": error_message,
                        }
                    )