"""
app.py — Flask application factory and entry point.
"""

from flask import Flask
from config import Config
from models.db import init_db
from routes.auth import auth_bp
from routes.student import student_bp
from routes.admin import admin_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialise database tables
    init_db()

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(admin_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
