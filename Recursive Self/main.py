"""
Interactive console for chatting with Bob using the configured LLM backend.

This module originally used the OpenAI client directly; it has been adapted to
call into :func:`llm_client.complete` so that a local Mistral model can be
used instead.  The rest of the conversation loop remains largely the same:
we analyse the user's emotions, load the world state and any subjective
memory fragments, build a prompt using :func:`build_prompt`, send it to the
language model, and then write out a reflection summary.
"""

from memory.gpt_emotion_analyzer import analyze_emotion_with_gpt
from memory.prompt_builder import build_prompt
from memory.memory_compressor import craft_reflection_summary
from core.integration_hook import inject_subjective_memory
from memory.subjective_log import log_subjective_entry
from config.reflection_debug import DEBUG_REFLECTION
from memory.world_state_loader import get_current_world_state
# load_recent_dialogue_from_reflections is no longer used here; the reflection
# summary is now based solely on the current exchange.
from memory.reflection_writer import write_reflection_entry
from llm_client import complete
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

def main_loop() -> None:
    """Run the interactive chat loop with Bob until the user types exit/quit."""
    print("==== Bob's Interactive Console (LLM backend) ====")
    # The name used in prompt building.  Previously this was hard‑coded to
    # "GPTBob" but since we are no longer using GPT specifically the shorter
    # "Bob" feels more natural.  Change this if you prefer another alias.
    user_name = "Bob"

    while True:
        try:
            user_input = input("You: ")
        except EOFError:
            # Gracefully handle Ctrl+D or other EOF conditions
            print("\nSession ended.")
            break
        if user_input.strip().lower() in {"exit", "quit"}:
            print("Session ended.")
            break

        # Step 1: Emotion Analysis
        emotion_result = analyze_emotion_with_gpt(user_input)
        print(f"[Emotion Parse] → {emotion_result}")

        # Step 2: Load World State
        world_state = get_current_world_state() or {}

        # Step 3: Inject Subjective Fragment (if any)
        inner_fragment = inject_subjective_memory(world_state) or ""

        # Step 4: Build Prompt including world state, recent messages and identity
        prompt = build_prompt(user_name)
        if inner_fragment:
            prompt += f"\n[INNER MEMORY]: {inner_fragment}"
        prompt += f"\nUser said: \"{user_input}\""

        # Step 5: Generate Bob's reply using the configured LLM backend
        bot_reply = complete(None, prompt, temperature=0.6, max_tokens=300)
        bot_reply_str = bot_reply.strip() if isinstance(bot_reply, str) else str(bot_reply)
        print(f"\nBob: {bot_reply_str}")

        # Step 6: Reflection Summary on the latest exchange
        # Summarise just this turn so that Bob reflects on the current interaction
        reflection = craft_reflection_summary([
            f"You: {user_input}",
            f"Bob: {bot_reply_str}"
        ], debug=DEBUG_REFLECTION)

        print(f"\n[Reflection Summary] → {reflection}")

        # Persist the reflection entry
        write_reflection_entry(
            dialogue=f"You: {user_input}\nBob: {bot_reply_str}",
            summary=reflection,
            source="main_loop"
        )

        # Step 7: Optional Subjective Log Trigger
        lower_ref = reflection.lower() if isinstance(reflection, str) else str(reflection).lower()
        if any(token in lower_ref for token in ("realized", "felt like", "thought about", "believe", "identity shift", "self-reflection")):
            log_subjective_entry(
                content=reflection,
                tags=["reflection", "dialogue"],
                source="main_loop_auto"
            )

if __name__ == "__main__":
    main_loop()
