"""
nlp_service.py
Text preprocessing: lowercase, punctuation removal, stopword filtering, stemming.
Uses NLTK (no spaCy model download required at runtime).
"""

import re
import string
import nltk

# Download required NLTK data silently on first run
try:
    nltk.download("stopwords", quiet=True)
    nltk.download("punkt", quiet=True)
    nltk.download("punkt_tab", quiet=True)
except Exception:
    pass

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

_STOP_WORDS = set(stopwords.words("english"))
_STEMMER = PorterStemmer()

# Simple Hindi → English keyword map for basic multilingual support
_HINDI_MAP = {
    "fees": "fees",
    "शुल्क": "fees",
    "परीक्षा": "exam",
    "exam": "exam",
    "hostel": "hostel",
    "छात्रावास": "hostel",
    "library": "library",
    "पुस्तकालय": "library",
    "admission": "admission",
    "प्रवेश": "admission",
    "scholarship": "scholarship",
    "छात्रवृत्ति": "scholarship",
    "timetable": "timetable",
    "समय": "timetable",
    "faculty": "faculty",
    "शिक्षक": "faculty",
}


def translate_hindi_keywords(text: str) -> str:
    """Replace known Hindi keywords with their English equivalents."""
    for hindi, english in _HINDI_MAP.items():
        text = text.replace(hindi, english)
    return text


def clean_text(text: str) -> str:
    """Full preprocessing pipeline: translate → lowercase → strip punctuation → remove stopwords → stem."""
    text = translate_hindi_keywords(text)
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)  # remove punctuation
    text = re.sub(r"\s+", " ", text).strip()
    tokens = text.split()
    tokens = [_STEMMER.stem(t) for t in tokens if t not in _STOP_WORDS and len(t) > 1]
    return " ".join(tokens)


def tokenize(text: str) -> list:
    return text.split()
