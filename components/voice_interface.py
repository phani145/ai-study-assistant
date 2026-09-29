import streamlit as st

from services.stt_service import (
    transcribe_audio,
)

from services.tts_service import text_to_speech

from services.ollama_service import (
    OllamaError,
)

from components.chat_interface import (
    answer_question,
)


def render_voice_interface(document):
    """Render voice question functionality."""

    st.subheader("🎤 Voice Question")

    if not document["chunks"]:
        st.warning(
            "Upload a text-based PDF before asking a voice question."
        )
        return

    st.write(
        "Click the microphone button, ask your question, "
        "and release it when finished."
    )

    audio = st.audio_input(
        "🎤 Record your question",
        sample_rate=16000,
        key="voice_question"
    )

    if audio is None:
        return

    st.audio(
        audio,
        format="audio/wav"
    )

    if st.button(
        "Transcribe and Ask AI",
        key="transcribe_voice"
    ):

        with st.spinner(
            "Converting speech to text..."
        ):

            try:

                transcript = transcribe_audio(
                    audio.getvalue()
                )

                st.session_state.voice_transcript = (
                    transcript
                )

                st.success(
                    "Speech successfully converted to text."
                )

                st.markdown(
                    f"**Transcribed Question:** "
                    f"{transcript}"
                )

            except Exception as exc:

                st.error(
                    f"Speech recognition failed: {exc}"
                )

                return

        with st.spinner(
            "Gemma 3:1B is answering..."
        ):

            try:

                answer, sources = answer_question(
                    transcript,
                    document
                )

                st.markdown("### 🤖 AI Answer")

                st.markdown(answer)

                if sources:
                    st.caption(
                        "📖 Source: "
                        + ", ".join(
                            f"Page {page}"
                            for page in sources
                        )
                    )

                st.session_state.voice_answer = answer

            except OllamaError as exc:

                st.error(str(exc))

                return

        st.markdown("### 🔊 Listen to Answer")

        try:

            with st.spinner(
                "Generating audio..."
            ):

                audio_bytes = text_to_speech(
                    answer
                )

            st.audio(
                audio_bytes,
                format="audio/mp3"
            )

        except Exception as exc:

            st.warning(
                f"TTS could not generate audio: {exc}"
            )

            st.info(
                "The AI answer is still available as text."
            )