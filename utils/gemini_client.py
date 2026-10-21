"""Optional Gemini Developer API adapter for explicit integration runs."""

import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).parents[1]
load_dotenv(PROJECT_ROOT / ".env")


@lru_cache(maxsize=1)
def _client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Set GEMINI_API_KEY in the environment or project .env file")

    from google import genai
    from google.genai import types

    return genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(
            timeout=30_000,
            retry_options=types.HttpRetryOptions(attempts=1),
        ),
    )


def generate_gemini_text(prompt: str) -> str:
    """Make one Gemini request and return generated text."""
    from google.genai import types

    response = _client().models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemini-3.8-flash"),
        contents=prompt,
        config=types.GenerateContentConfig(
            max_output_tokens=128,
            temperature=0,
            thinking_config=types.ThinkingConfig(
                thinking_level=types.ThinkingLevel.LOW,
            ),
        ),
    )
    text = response.text
    if not text:
        candidate = response.candidates[0] if response.candidates else None
        finish_reason = candidate.finish_reason if candidate else "no candidate"
        raise RuntimeError(
            f"Gemini returned no text (finish_reason={finish_reason})"
        )
    return text.strip()
