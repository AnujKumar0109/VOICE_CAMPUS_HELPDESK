"""
routes/auth.py — Registration, login, logout.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.user import create_user, get_user_by_email
from utils.helpers import check_password

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/", methods=["GET"])
def index():
    if "user_id" in session:
        if session.get("role") == "admin":
            return redirect(url_for("admin.panel"))
        return redirect(url_for("student.dashboard"))
    return redirect(url_for("auth.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("auth.index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = get_user_by_email(email)
        if user and check_password(password, user["password"]):
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["role"] = user["role"]
            if user["role"] == "admin":
                return redirect(url_for("admin.panel"))
            return redirect(url_for("student.dashboard"))
        flash("Invalid email or password.", "danger")

    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not name or not email or not password:
            flash("All fields are required.", "warning")
            return render_template("login.html", show_register=True)
        if create_user(name, email, password):
            flash("Account created! Please log in.", "success")
            return redirect(url_for("auth.login"))
        flash("Email already registered.", "danger")
        return render_template("login.html", show_register=True)
    return render_template("login.html", show_register=True)


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("auth.login"))
