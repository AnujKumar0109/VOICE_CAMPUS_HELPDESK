"""
intent_service.py
Detects the campus query intent using keyword rules.
Categories: fees, exam, timetable, hostel, library,
            admission, faculty, department, scholarship, general
"""

INTENT_KEYWORDS = {
    "fees": [
        "fee", "fees", "tuition", "payment", "challan", "due date",
        "semester fee", "pay", "amount", "cost", "charge",
    ],
    "exam": [
        "exam", "examination", "test", "schedule", "date sheet",
        "result", "marks", "grade", "paper", "hall ticket", "admit card",
    ],
    "timetable": [
        "timetable", "time table", "schedule", "class", "lecture",
        "period", "slot", "timing", "routine",
    ],
    "hostel": [
        "hostel", "dormitory", "room", "mess", "warden", "accommodation",
        "resident", "curfew", "entry", "hostel rules",
    ],
    "library": [
        "library", "book", "issue", "return", "reading room", "catalogue",
        "borrow", "librarian", "fine", "renew", "journal",
    ],
    "admission": [
        "admission", "apply", "application", "eligibility", "merit",
        "counselling", "enrollment", "registration", "form", "document",
    ],
    "faculty": [
        "faculty", "professor", "teacher", "lecturer", "staff",
        "hod", "head of department", "contact", "cabin", "sir", "madam",
    ],
    "department": [
        "department", "office", "admin", "principal", "dean",
        "section", "branch", "mca", "bca", "btech",
    ],
    "scholarship": [
        "scholarship", "stipend", "financial aid", "grant", "merit",
        "income", "certificate", "scholarship form",
    ],
    "notice": [
        "notice", "circular", "announcement", "update", "news",
        "event", "holiday", "notification",
    ],
}


def detect_intent(text: str) -> str:
    """Return the most likely intent category for the given text."""
    text_lower = text.lower()
    scores = {intent: 0 for intent in INTENT_KEYWORDS}
    for intent, keywords in INTENT_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                scores[intent] += 1
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "general"
