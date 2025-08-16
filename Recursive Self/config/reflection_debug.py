# reflection_debug.py

# Global flag to toggle debug output for reflection summaries
DEBUG_REFLECTION = True

def reflection_debug_toggle():
    """
    Toggles the global DEBUG_REFLECTION flag.
    This allows developers to enable or disable printouts during reflection summary generation
    without editing main compressor logic.
    """
    global DEBUG_REFLECTION
    DEBUG_REFLECTION = not DEBUG_REFLECTION
    print(f"[DEBUG] Reflection Debug Mode is now: {'ON' if DEBUG_REFLECTION else 'OFF'}")
