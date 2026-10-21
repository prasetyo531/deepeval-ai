"""One-request Gemini API connectivity smoke test; not the agent quality gate."""

import os

import pytest

from utils.gemini_client import generate_gemini_text


HAS_GEMINI_API_KEY = bool(os.getenv("GEMINI_API_KEY"))


@pytest.mark.integration
@pytest.mark.skipif(not HAS_GEMINI_API_KEY, reason="Set GEMINI_API_KEY in .env or the shell")
def test_gemini_api_returns_smoke_marker() -> None:
    result = generate_gemini_text("Return exactly this marker and nothing else: QA_AGENT_SMOKE_OK")
    print(f"Gemini response: {result}", flush=True)

    assert "QA_AGENT_SMOKE_OK" in result
