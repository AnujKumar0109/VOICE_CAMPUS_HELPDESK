"""
response_service.py
Matches a user query against stored FAQs using TF-IDF + Cosine Similarity.
Falls back to "unanswered" if similarity is below threshold.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from models.faq import get_all_faqs
from services.nlp_service import clean_text

SIMILARITY_THRESHOLD = 0.20  # minimum score to count as a match


def get_best_answer(user_question: str):
    """
    Returns (answer, category, score) tuple.
    If no FAQ matches above threshold, returns (None, 'general', 0.0).
    """
    faqs = get_all_faqs()
    if not faqs:
        return None, "general", 0.0

    faq_questions = [clean_text(f["question"]) for f in faqs]
    cleaned_query = clean_text(user_question)

    corpus = faq_questions + [cleaned_query]

    vectorizer = TfidfVectorizer()
    try:
        tfidf_matrix = vectorizer.fit_transform(corpus)
    except ValueError:
        return None, "general", 0.0

    query_vec = tfidf_matrix[-1]
    faq_vecs = tfidf_matrix[:-1]
    scores = cosine_similarity(query_vec, faq_vecs).flatten()

    best_idx = int(scores.argmax())
    best_score = float(scores[best_idx])

    if best_score >= SIMILARITY_THRESHOLD:
        best_faq = faqs[best_idx]
        return best_faq["answer"], best_faq["category"], best_score

    return None, "general", best_score


def get_suggestions(user_question: str, top_n: int = 3):
    """Return top N similar FAQ questions as suggestions."""
    faqs = get_all_faqs()
    if not faqs:
        return []

    faq_questions = [clean_text(f["question"]) for f in faqs]
    cleaned_query = clean_text(user_question)
    corpus = faq_questions + [cleaned_query]

    vectorizer = TfidfVectorizer()
    try:
        tfidf_matrix = vectorizer.fit_transform(corpus)
    except ValueError:
        return []

    query_vec = tfidf_matrix[-1]
    faq_vecs = tfidf_matrix[:-1]
    scores = cosine_similarity(query_vec, faq_vecs).flatten()

    top_indices = scores.argsort()[::-1][:top_n]
    suggestions = [faqs[i]["question"] for i in top_indices if scores[i] > 0.05]
    return suggestions
