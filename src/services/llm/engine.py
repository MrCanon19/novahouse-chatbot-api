"""Unified LLM engine with pluggable providers."""

import os
from typing import Dict, List, Optional

ProviderConfig = Dict[str, Optional[str]]


def load_provider() -> Dict:
    """Load configured LLM provider and client.

    Returns
    -------
    dict
        Contains provider name, client instance (or None when disabled), and default model.
    """

    provider_name = os.getenv("LLM_PROVIDER", "openai").lower()
    model_default = os.getenv("LLM_MODEL", "gpt-4o-mini")

    if provider_name == "groq":
        from groq import Groq

        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or api_key.lower().startswith("test_"):
            return {
                "name": "groq",
                "client": None,
                "model": os.getenv("GROQ_MODEL", "llama3-8b-8192"),
                "disabled_reason": "GROQ_API_KEY missing or placeholder",
            }

        client = Groq(api_key=api_key)
        return {
            "name": "groq",
            "client": client,
            "model": os.getenv("GROQ_MODEL", "llama3-8b-8192"),
        }

    from openai import OpenAI

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key.lower().startswith("test_"):
        return {
            "name": "openai",
            "client": None,
            "model": os.getenv("OPENAI_MODEL", model_default),
            "disabled_reason": "OPENAI_API_KEY missing or placeholder",
        }

    client = OpenAI(api_key=api_key)
    return {
        "name": provider_name,
        "client": client,
        "model": os.getenv("OPENAI_MODEL", model_default),
    }


def unify_response(raw_response) -> Optional[str]:
    """Normalize provider responses to text content."""

    if raw_response is None:
        return None

    choices = getattr(raw_response, "choices", None)
    if not choices:
        return None

    first_choice = choices[0]
    message = getattr(first_choice, "message", None)
    if message and getattr(message, "content", None):
        return message.content

    text = getattr(first_choice, "text", None)
    if text:
        return text

    return None


def run_llm(
    messages: List[Dict[str, str]],
    *,
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 500,
) -> Optional[str]:
    """Execute a chat completion against the configured provider."""

    provider = load_provider()
    client = provider.get("client")
    if client is None:
        reason = provider.get("disabled_reason", "provider client not available")
        print(f"⚠️  LLM client unavailable: {reason}")
        return None

    model_name = model or provider.get("model")
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return unify_response(response)
