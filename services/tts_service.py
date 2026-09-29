from io import BytesIO

from gtts import gTTS


def text_to_speech(text: str, language: str = "en") -> bytes:
    """
    Convert text to speech and return MP3 audio as bytes.
    """
    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    audio_buffer = BytesIO()

    tts = gTTS(
        text=text,
        lang=language,
        slow=False
    )

    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)

    return audio_buffer.read()