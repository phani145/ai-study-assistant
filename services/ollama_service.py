import os
from typing import Optional

import requests
from dotenv import load_dotenv


load_dotenv()


OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434"
).rstrip("/")

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "gemma3:1b"
)


class OllamaError(Exception):
    """Custom Ollama exception."""


def check_ollama() -> bool:
    """Check whether Ollama server is running."""

    try:
        response = requests.get(
            f"{OLLAMA_BASE_URL}/api/tags",
            timeout=5
        )

        return response.ok

    except requests.RequestException:
        return False


def get_available_models():
    """Return models available in Ollama."""

    try:
        response = requests.get(
            f"{OLLAMA_BASE_URL}/api/tags",
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        return [
            model.get("name", "")
            for model in data.get("models", [])
        ]

    except requests.RequestException as exc:
        raise OllamaError(
            "Ollama is not running or cannot be reached."
        ) from exc


def is_model_available(model_name: Optional[str] = None) -> bool:
    """Check whether the requested model exists."""

    model_name = model_name or OLLAMA_MODEL

    models = get_available_models()

    return any(
        model == model_name
        or model.split(":")[0] == model_name.split(":")[0]
        for model in models
    )


def generate_response(
    prompt: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.2
) -> str:
    """
    Send a prompt to Ollama and return generated text.
    """

    if not check_ollama():
        raise OllamaError(
            "Ollama is not running. Start Ollama and try again."
        )

    if not is_model_available():
        raise OllamaError(
            f"Model '{OLLAMA_MODEL}' was not found in Ollama."
        )

    messages = []

    if system_prompt:
        messages.append(
            {
                "role": "system",
                "content": system_prompt
            }
        )

    messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": temperature
        }
    }

    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json=payload,
            timeout=300
        )

        if response.status_code != 200:
            raise OllamaError(
                f"Ollama returned HTTP {response.status_code}: "
                f"{response.text}"
            )

        data = response.json()

        message = data.get("message", {})
        content = message.get("content", "").strip()

        if not content:
            raise OllamaError(
                "Ollama returned an empty response."
            )

        return content

    except requests.Timeout as exc:
        raise OllamaError(
            "Ollama took too long to respond."
        ) from exc

    except requests.RequestException as exc:
        raise OllamaError(
            f"Could not communicate with Ollama: {exc}"
        ) from exc