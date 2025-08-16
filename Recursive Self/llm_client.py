
import os
import subprocess
from typing import Optional

BACKEND = (os.getenv("BACKEND") or "ollama").lower()
MODEL_OLLAMA = os.getenv("MISTRAL")  # could be None or ""
MODEL_OPENAI = os.getenv("MODEL_OPENAI") or "gpt-4o-mini"

def _model_ollama():
    # Fallback to your actual local model name
    return (MODEL_OLLAMA or "mistral_bob").strip()

def _complete_ollama(system, user, temperature=0.7, top_p=0.9, max_tokens=None) -> str:
    parts = []
    if system:
        parts.append(f"<|system|>{system}")
    parts.append(f"<|user|>{user}")
    prompt = "\n".join(parts) + "\n<|assistant|>"

    model = _model_ollama()
    args = ["ollama", "run", model]
    try:
        proc = subprocess.run(
            args,
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if proc.returncode != 0:
            # Show the actual ollama error output
            return f"ERROR: Ollama returned {proc.returncode}: {proc.stderr.decode('utf-8', 'ignore').strip()}"
        return proc.stdout.decode("utf-8", "ignore").strip()
    except Exception as e:
        return f"ERROR: Ollama call failed: {e}"


def complete(system: Optional[str], user: str, temperature: float=0.7, top_p: float=0.9, max_tokens: Optional[int]=None) -> str:
    if BACKEND == "ollama":
        return _complete_ollama(system, user, temperature, top_p, max_tokens)
