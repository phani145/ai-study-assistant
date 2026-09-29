from pathlib import Path
import tempfile

from faster_whisper import WhisperModel


_model = None


def get_whisper_model():
    """
    Load Whisper only when needed.

    This avoids loading the model during every Streamlit rerun.
    """

    global _model

    if _model is None:
        _model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8"
        )

    return _model


def transcribe_audio(audio_bytes: bytes) -> str:
    """
    Transcribe WAV/audio bytes using local Whisper.
    """

    if not audio_bytes:
        raise ValueError("No audio data was provided.")

    temporary_path = None

    try:
        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        ) as temp_file:

            temp_file.write(audio_bytes)
            temporary_path = Path(temp_file.name)

        model = get_whisper_model()

        segments, _ = model.transcribe(
            str(temporary_path),
            beam_size=5
        )

        transcript = " ".join(
            segment.text.strip()
            for segment in segments
        ).strip()

        if not transcript:
            raise RuntimeError(
                "Whisper could not detect any speech."
            )

        return transcript

    except Exception as exc:
        raise RuntimeError(
            f"Speech-to-text failed: {exc}"
        ) from exc

    finally:
        if temporary_path and temporary_path.exists():
            temporary_path.unlink(missing_ok=True)