import os

import pytest

try:
    from openai import OpenAI

    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Brak OPENAI_API_KEY w środowisku")
@pytest.mark.skipif(not OPENAI_AVAILABLE, reason="Brak pakietu openai")
def test_openai_chat_live():
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Test integracji live"}]
    )
    from src.security.api_key_audit import log_api_key_usage

    log_api_key_usage("openai", os.getenv("OPENAI_API_KEY", "none"))
    assert response.choices[0].message.content, "Brak odpowiedzi od OpenAI (live)"
