
# Recursive Self — Mistral/Ollama Ready

This patch lets you switch the project from OpenAI GPT to **Mistral via Ollama** (or back) without rewriting your logic.

## New pieces
- `llm_client.py` — thin adapter with two backends:
  - `BACKEND=ollama` (default) → uses `ollama run $MODEL_OLLAMA` (default: `bob_mistral`)
  - `BACKEND=openai` → uses `OPENAI_API_KEY` and `MODEL_OPENAI` (default: `gpt-4o-mini`)
- `main_ollama.py` — an orchestrator that calls `llm_client.complete()` instead of the OpenAI client directly.
- Patched `memory/gpt_emotion_analyzer.py` to use `llm_client.complete()` (backup saved as `.bak`).

## Env vars
Create a `.env` or export in your shell:

```
# choose backend
BACKEND=ollama
# ollama model name
MODEL_OLLAMA=bob_mistral

# OR (if using OpenAI)
# BACKEND=openai
# OPENAI_API_KEY=sk-...
# MODEL_OPENAI=gpt-4o-mini
```

## Run
```
# ensure your ollama model exists
# ollama create bob_mistral -f Modelfile
python -m "Recursive Self.main_ollama"
```

Artifacts will be saved in `Recursive Self/out/`:
- `last_reflection.txt`
- `last_summary.json`

## Notes
- If your `build_prompt()` already includes world state & recent messages, great; otherwise extend it.
- You can switch backends at any time by changing `BACKEND` without code changes.
- For stricter Bob vs. Helper voices, add the `[BOB]...[/BOB]` or `[OOC]...[/OOC]` markers in `system_prompt` or inject them inside `user_prompt`.
