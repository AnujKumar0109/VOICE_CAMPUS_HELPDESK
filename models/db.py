import sqlite3
from config import Config


def get_db():
    """Return a new SQLite connection."""
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create all tables if they do not exist."""
    conn = get_db()
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT    NOT NULL,
            email    TEXT    NOT NULL UNIQUE,
            password TEXT    NOT NULL,
            role     TEXT    NOT NULL DEFAULT 'student'
        );

        CREATE TABLE IF NOT EXISTS faqs (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT    NOT NULL,
            answer   TEXT    NOT NULL,
            category TEXT    NOT NULL DEFAULT 'general'
        );

        CREATE TABLE IF NOT EXISTS queries (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER NOT NULL REFERENCES users(id),
            question   TEXT    NOT NULL,
            response   TEXT,
            status     TEXT    NOT NULL DEFAULT 'answered',
            created_at TEXT    NOT NULL DEFAULT (datetime('now','localtime'))
        );

        CREATE TABLE IF NOT EXISTS feedback (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id  INTEGER NOT NULL REFERENCES users(id),
            query_id INTEGER REFERENCES queries(id),
            rating   INTEGER NOT NULL DEFAULT 5,
            comment  TEXT
        );

        CREATE TABLE IF NOT EXISTS analytics (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            category    TEXT    NOT NULL UNIQUE,
            query_count INTEGER NOT NULL DEFAULT 0
        );
    """)
    conn.commit()
    conn.close()
