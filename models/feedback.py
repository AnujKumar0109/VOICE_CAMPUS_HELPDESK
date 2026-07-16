from models.db import get_db


def save_feedback(user_id, query_id, rating, comment):
    conn = get_db()
    conn.execute(
        "INSERT INTO feedback (user_id, query_id, rating, comment) VALUES (?, ?, ?, ?)",
        (user_id, query_id, rating, comment),
    )
    conn.commit()
    conn.close()


def get_all_feedback():
    conn = get_db()
    rows = conn.execute(
        """SELECT f.*, u.name as user_name
           FROM feedback f
           JOIN users u ON f.user_id = u.id
           ORDER BY f.id DESC"""
    ).fetchall()
    conn.close()
    return rows


def get_feedback_by_user(user_id):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM feedback WHERE user_id=? ORDER BY id DESC", (user_id,)
    ).fetchall()
    conn.close()
    return rows


def get_avg_rating():
    conn = get_db()
    result = conn.execute("SELECT AVG(rating) as avg FROM feedback").fetchone()
    conn.close()
    avg = result["avg"]
    return round(avg, 1) if avg else 0.0
