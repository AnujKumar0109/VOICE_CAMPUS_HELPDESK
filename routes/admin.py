"""
routes/admin.py — Admin panel routes.
"""

from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, jsonify,
)
from utils.helpers import admin_required
from models.faq import (
    get_all_faqs, get_faq_by_id,
    add_faq, update_faq, delete_faq, get_categories,
)
from models.query import get_all_queries, get_unanswered_queries
from models.feedback import get_all_feedback
from models.user import get_all_users
from services.analytics_service import get_dashboard_stats

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# ─── Admin Panel Dashboard ───────────────────────────────────────────────────
@admin_bp.route("/")
@admin_required
def panel():
    stats = get_dashboard_stats()
    return render_template("admin_panel.html", stats=stats)


# ─── FAQ Management ──────────────────────────────────────────────────────────
@admin_bp.route("/faqs")
@admin_required
def faqs():
    all_faqs = get_all_faqs()
    categories = get_categories()
    return render_template("faq_management.html", faqs=all_faqs, categories=categories)


@admin_bp.route("/faqs/add", methods=["POST"])
@admin_required
def add_faq_route():
    question = request.form.get("question", "").strip()
    answer = request.form.get("answer", "").strip()
    category = request.form.get("category", "general").strip()
    if question and answer:
        add_faq(question, answer, category)
        flash("FAQ added successfully.", "success")
    else:
        flash("Question and answer cannot be empty.", "warning")
    return redirect(url_for("admin.faqs"))


@admin_bp.route("/faqs/edit/<int:faq_id>", methods=["GET", "POST"])
@admin_required
def edit_faq(faq_id):
    faq = get_faq_by_id(faq_id)
    if not faq:
        flash("FAQ not found.", "danger")
        return redirect(url_for("admin.faqs"))
    if request.method == "POST":
        question = request.form.get("question", "").strip()
        answer = request.form.get("answer", "").strip()
        category = request.form.get("category", "general").strip()
        update_faq(faq_id, question, answer, category)
        flash("FAQ updated.", "success")
        return redirect(url_for("admin.faqs"))
    categories = get_categories()
    return render_template("faq_management.html",
                           faqs=get_all_faqs(),
                           categories=categories,
                           edit_faq=faq)


@admin_bp.route("/faqs/delete/<int:faq_id>", methods=["POST"])
@admin_required
def delete_faq_route(faq_id):
    delete_faq(faq_id)
    flash("FAQ deleted.", "info")
    return redirect(url_for("admin.faqs"))


# ─── Analytics ───────────────────────────────────────────────────────────────
@admin_bp.route("/analytics")
@admin_required
def analytics():
    stats = get_dashboard_stats()
    return render_template("analytics.html", stats=stats)


# ─── All Queries ─────────────────────────────────────────────────────────────
@admin_bp.route("/queries")
@admin_required
def queries():
    all_q = get_all_queries()
    unanswered = get_unanswered_queries()
    return render_template("admin_queries.html", queries=all_q, unanswered=unanswered)


# ─── Feedback List ────────────────────────────────────────────────────────────
@admin_bp.route("/feedback")
@admin_required
def feedback():
    fb = get_all_feedback()
    return render_template("admin_feedback.html", feedback=fb)


# ─── Users ───────────────────────────────────────────────────────────────────
@admin_bp.route("/users")
@admin_required
def users():
    all_users = get_all_users()
    return render_template("admin_users.html", users=all_users)
