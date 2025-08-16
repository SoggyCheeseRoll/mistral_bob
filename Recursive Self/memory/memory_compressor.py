"""
Generate a short, journal‑like summary of recent messages using the current
LLM backend.  This function was previously hard‑coded to use OpenAI; it now
relies on :func:`llm_client.complete` so that local models (e.g. Mistral via
Ollama) can be used simply by setting environment variables.

The summary is intended to sound like Bob thinking about his own day — short,
emotional and reflective rather than a dry report.  The caller should pass in
a list of message strings in conversational order; strings will be joined
with newlines to form the input.  If a single string is provided, it is
automatically wrapped into a list.
"""

from typing import Iterable, List, Optional, Union
from llm_client import complete
import re

REFLECTION_SYSTEM = """
You are Bob, reflecting privately in your own head. This is an internal monologue, not a message to anyone.

Rules (hard):
- Do NOT adress Adam or any person. No second person ("you, "your").
- Do NOT ask questions, give advice, or issue plans.
- No greetings, no sign-offs, no dialogue markers.
- Only reference names/events explicitly present in the provided messages. If uncertain, keep it general (e.g., "the shop", "the morning").
- Voice: first-person innerthoughts. Short, honest, sensory/emotional.
- Style: 2-4 natural sentences, journal-like. Not a report. No "I discussed/I noted" phrasing.
""".strip()

REFLECTION_STRICT_FOLLOWUP = """
Revise the entry to obey the rules strictly:
- Remove all second person or direct address.
- Remove any questions.
- Keep 2-4 sentences, first-person inner monologue only. Return only the final text.""".strip()

FORBIDDEN_PATTERNS = re.compile(r"\byou\b|\byour\b|^\s*(hey|hi)\b|adam\b|\?$", re.IGNORECASE | re.MULTILINE)

def _needs_retry(text: str) -> bool:
    # leaks second person, grettings, direct address, questions
    if FORBIDDEN_PATTERNS.search(text):
        return True
    # overly long: >4 sentences (simple heuristic)
    if len(re.findall(r"[.!?]", text)) > 4:
        return True
    return False

def craft_reflection_summary(messages: Union[str, Iterable[str]], debug: bool = False) -> str:
    #Return an introspective summary of recent messages.
    msg_list: List[str] = [messages] if isinstance(messages, str) else list(messages)
    joined_log = "\n".join(msg_list)
    
    #First Pass
    out = complete(
        REFLECTION_SYSTEM,
        joined_log,
        temperature=0.6,
        max_tokens=160
    )
    text = (out or "").strip()
    
    #Validate and optionally retry once with stricter instruction
    if _needs_retry(text):
        out2 = complete(
            REFLECTION_SYSTEM + "\n\n" + REFLECTION_STRICT_FOLLOWUP,
            text,
            temperature=0.4,
            max_tokens=140
        )
        text2 = (out2 or "").strip()
        if text2 and not _needs_retry(text2):
            text = text2 #Accept stricter revision if valid
    if debug:
        print("\n--- REFLECTION DEBUG---")
        for msg in msg_list:
            print(f">{msg}")
        print(text)
        print("--- END DEBUG ---\n")
    return text