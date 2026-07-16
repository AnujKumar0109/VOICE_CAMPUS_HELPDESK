import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "voice_helpdesk_secret_2026")
    DATABASE = os.path.join(os.path.dirname(__file__), "database.db")
    DEBUG = True
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
