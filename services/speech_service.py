"""
speech_service.py
Speech-to-Text  : uses browser Web Speech API (handled in JS).
Text-to-Speech  : pyttsx3 for server-side TTS (returns audio via endpoint).

Note: Microphone capture from a browser cannot use server-side SpeechRecognition
      directly because the browser controls the mic. Instead, the JS voice.js sends
      the transcript as text to the server.  pyttsx3 is used to optionally read the
      answer aloud when the user is running locally.
"""

import threading

try:
    import pyttsx3
    _ENGINE = pyttsx3.init()
    _TTS_AVAILABLE = True
except Exception:
    _ENGINE = None
    _TTS_AVAILABLE = False


def speak_text(text: str, rate: int = 150):
    """Speak the given text using pyttsx3 in a daemon thread so Flask does not block."""
    if not _TTS_AVAILABLE or not _ENGINE:
        return
    def _run():
        try:
            _ENGINE.setProperty("rate", rate)
            _ENGINE.say(text)
            _ENGINE.runAndWait()
        except Exception:
            pass
    t = threading.Thread(target=_run, daemon=True)
    t.start()


def tts_available() -> bool:
    return _TTS_AVAILABLE
