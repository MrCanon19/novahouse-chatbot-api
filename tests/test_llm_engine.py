"""Tests for the unified LLM engine providers."""

import importlib.util
import sys
import types

from src.services.llm.engine import (
    DEV_ASSISTANT_SYSTEM_PROMPT,
    run_llm,
)


def test_dummy_provider_returns_configured_response(monkeypatch):
    """Dummy provider should short-circuit and return the configured text."""

    monkeypatch.setenv("LLM_PROVIDER", "dummy")
    monkeypatch.setenv("DUMMY_LLM_RESPONSE", "dummy-response")

    response = run_llm([{"role": "user", "content": "hi"}])

    assert response == "dummy-response"


def test_groq_without_key_is_disabled(monkeypatch, capsys):
    """Groq provider should gracefully disable when no API key is present."""

    # Stub groq module to avoid optional dependency import errors in CI
    monkeypatch.setitem(
        sys.modules,
        "groq",
        types.SimpleNamespace(Groq=lambda **_: None, __spec__=types.SimpleNamespace()),
    )

    monkeypatch.setenv("LLM_PROVIDER", "groq")
    monkeypatch.delenv("GROQ_API_KEY", raising=False)

    response = run_llm([{"role": "user", "content": "hi"}])

    captured = capsys.readouterr()

    assert response is None
    assert "GROQ_API_KEY" in captured.out


def test_groq_package_missing_disables_provider(monkeypatch, capsys):
    """Groq provider should disable cleanly when dependency is absent."""

    monkeypatch.setattr(importlib.util, "find_spec", lambda _: None)
    monkeypatch.setenv("LLM_PROVIDER", "groq")

    response = run_llm([{"role": "user", "content": "hi"}])

    captured = capsys.readouterr()

    assert response is None
    assert "groq package not installed" in captured.out


def test_dev_assistant_prompt_injected_when_enabled(monkeypatch):
    """DEV_ASSISTANT_MODE should prepend the engineering system prompt."""

    captured = {}

    def create_stub_response(*, model, messages, temperature, max_tokens):
        captured["messages"] = messages

        class StubMessage:
            def __init__(self, content):
                self.content = content

        class StubChoice:
            def __init__(self, content):
                self.message = StubMessage(content)

        class StubResponse:
            def __init__(self, content):
                self.choices = [StubChoice(content)]

        return StubResponse("ack")

    stub_client = types.SimpleNamespace(
        chat=types.SimpleNamespace(
            completions=types.SimpleNamespace(create=create_stub_response)
        )
    )

    monkeypatch.setenv("DEV_ASSISTANT_MODE", "true")
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_MODEL", "stub-model")
    monkeypatch.setenv("OPENAI_API_KEY", "stub-key")

    monkeypatch.setattr(
        "src.services.llm.engine.load_provider",
        lambda: {"name": "openai", "client": stub_client, "model": "stub-model"},
    )

    response = run_llm([{"role": "user", "content": "Hello"}])

    assert response == "ack"
    assert captured["messages"][0]["role"] == "system"
    assert DEV_ASSISTANT_SYSTEM_PROMPT in captured["messages"][0]["content"]
    assert all(m["role"] != "system" for m in captured["messages"][1:])
