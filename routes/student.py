"""
routes/student.py — Student-facing pages.
"""

from flask import (
    Blueprint, render_template, request, redirect,
    url_for, session, flash, jsonify, make_response,
)
from utils.helpers import login_required
from models.query import save_query, get_queries_by_user, get_query_by_id
from models.feedback import save_feedback, get_feedback_by_user
from models.analytics import increment_category
from services.response_service import get_best_answer, get_suggestions
from services.intent_service import detect_intent
from services.speech_service import speak_text, tts_available
from services.pdf_service import generate_chat_pdf

student_bp = Blueprint("student", __name__)


# ─── Dashboard ──────────────────────────────────────────────────────────────
@student_bp.route("/dashboard")
@login_required
def dashboard():
    history = get_queries_by_user(session["user_id"])
    recent = list(history)[:5]
    return render_template(
        "dashboard.html",
        recent_queries=recent,
        total_queries=len(list(history)),
    )


# ─── Voice / Text Query page ────────────────────────────────────────────────
@student_bp.route("/query", methods=["GET"])
@login_required
def query_page():
    return render_template("voice_query.html")


# ─── AJAX: process a query ───────────────────────────────────────────────────
@student_bp.route("/ask", methods=["POST"])
@login_required
def ask():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip()
    speak = data.get("speak", False)
    voice_rate = int(data.get("rate", 150))

    if not question:
        return jsonify({"error": "Empty question"}), 400

    intent = detect_intent(question)
    answer, category, score = get_best_answer(question)
    suggestions = []

    if answer:
        status = "answered"
        if speak:
            speak_text(answer, rate=voice_rate)
    else:
        status = "unanswered"
        answer = (
            "Sorry, I could not find a specific answer for your query. "
            "Please contact the campus office or try rephrasing your question."
        )
        suggestions = get_suggestions(question)

    query_id = save_query(session["user_id"], question, answer, status)
    increment_category(category)

    return jsonify({
        "answer": answer,
        "intent": intent,
        "category": category,
        "score": round(score, 3),
        "status": status,
        "query_id": query_id,
        "suggestions": suggestions,
        "tts_available": tts_available(),
    })


# ─── Chat history page ───────────────────────────────────────────────────────
@student_bp.route("/chat")
@login_required
def chat():
    history = get_queries_by_user(session["user_id"])
    return render_template("chat.html", history=history)


# ─── Feedback page ───────────────────────────────────────────────────────────
@student_bp.route("/feedback", methods=["GET", "POST"])
@login_required
def feedback():
    queries = get_queries_by_user(session["user_id"])
    if request.method == "POST":
        query_id = request.form.get("query_id")
        rating = int(request.form.get("rating", 5))
        comment = request.form.get("comment", "").strip()
        save_feedback(session["user_id"], query_id or None, rating, comment)
        flash("Thank you for your feedback!", "success")
        return redirect(url_for("student.feedback"))
    my_feedback = get_feedback_by_user(session["user_id"])
    return render_template("feedback.html", queries=queries, my_feedback=my_feedback)


# ─── Report / PDF download ───────────────────────────────────────────────────
@student_bp.route("/report")
@login_required
def report():
    history = get_queries_by_user(session["user_id"])
    return render_template("report.html", history=history)


@student_bp.route("/report/download")
@login_required
def download_report():
    history = get_queries_by_user(session["user_id"])
    pdf_bytes = generate_chat_pdf(session["user_name"], [dict(q) for q in history])
    response = make_response(pdf_bytes)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = (
        f'attachment; filename="chat_report_{session["user_id"]}.pdf"'
    )
    return response
