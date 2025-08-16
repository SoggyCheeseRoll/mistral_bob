"""
Helpers for performing a simple emotion analysis using whatever LLM backend is
configured in ``llm_client``.  This module was originally written to call
OpenAI directly but has been updated to use ``llm_client.complete`` so that
models like Mistral running locally via Ollama can be swapped in without
changing the rest of the codebase.

The analyzer constructs a short system prompt describing Bob's identity and
instructing the model to return a small JSON object summarising the
emotions, tone and intensity of the user message.  The returned value is
parsed into a Python object when possible; otherwise the raw string is
returned so that callers can still display it.
"""

import json
from utils.bob_identity import BOB_IDENTITY
from llm_client import complete

def get_identity_context() -> str:
    """Return a short blurb describing Bob's identity and emotional truths."""
    core = ', '.join(BOB_IDENTITY["core_traits"])
    truths = ', '.join([k.replace('_', ' ') for k, v in BOB_IDENTITY["truths"].items() if v])
    return (
        f"You are analyzing emotions for Bob, a 23-year-old mechanic in Everwood. "
        f"Core traits: {core}. Emotional truths: {truths}."
    )

def analyze_emotion_with_gpt(message_text: str, role: str = "user") -> dict | str:
    """
    Analyse an utterance and return a structured emotion/tone summary.

    ``message_text``: The text the model should analyse.
    ``role``: Who spoke the message (e.g. "user" or "assistant").

    The model is asked to emit a JSON object with ``emotion`` (list of
    strings), ``tone`` (list of strings), ``intensity`` (float), and
    ``summary`` (short sentence).  If the response cannot be parsed as
    JSON the raw text is returned instead.
    """
    # Build a system prompt describing Bob and instructing the model to return JSON.
    system_prompt = (
        f"{get_identity_context()}\n"
        "You are an emotional reflection engine. Analyze the following message and return ONLY raw JSON:\n"
        "{\n"
        "  \"emotion\": [\"emotion1\", \"emotion2\"],\n"
        "  \"tone\": [\"tone1\", \"tone2\"],\n"
        "  \"intensity\": 0.0,\n"
        "  \"summary\": \"short sentence\"\n"
        "}\n"
        "IMPORTANT: Do not include any explanation or extra text—just the JSON."
    )

    user_prompt = f"Message: \"{message_text}\"\nSpeaker: {role}"

    response_text = complete(system_prompt, user_prompt, temperature=0.2, max_tokens=150)
    response_text = response_text.strip() if isinstance(response_text, str) else str(response_text)

    # Attempt to parse JSON; fall back to raw text on failure.
    try:
        return json.loads(response_text)
    except Exception:
        return response_text
