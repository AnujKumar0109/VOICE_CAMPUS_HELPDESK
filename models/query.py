from models.db import get_db


def save_query(user_id, question, response, status="answered"):
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO queries (user_id, question, response, status) VALUES (?, ?, ?, ?)",
        (user_id, question, response, status),
    )
    query_id = cur.lastrowid
    conn.commit()
    conn.close()
    return query_id


def get_queries_by_user(user_id):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM queries WHERE user_id=? ORDER BY id DESC", (user_id,)
    ).fetchall()
    conn.close()
    return rows


def get_all_queries():
    conn = get_db()
    rows = conn.execute(
        """SELECT q.*, u.name as user_name
           FROM queries q
           JOIN users u ON q.user_id = u.id
           ORDER BY q.id DESC"""
    ).fetchall()
    conn.close()
    return rows


def get_unanswered_queries():
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM queries WHERE status='unanswered' ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return rows


def get_query_by_id(query_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM queries WHERE id=?", (query_id,)).fetchone()
    conn.close()
    return row


def get_total_queries():
    conn = get_db()
    count = conn.execute("SELECT COUNT(*) as c FROM queries").fetchone()["c"]
    conn.close()
    return count


def get_unanswered_count():
    conn = get_db()
    count = conn.execute(
        "SELECT COUNT(*) as c FROM queries WHERE status='unanswered'"
    ).fetchone()["c"]
    conn.close()
    return count
