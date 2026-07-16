from models.db import get_db


def increment_category(category: str):
    """Increment query count for a category, insert row if missing."""
    conn = get_db()
    existing = conn.execute(
        "SELECT id FROM analytics WHERE category=?", (category,)
    ).fetchone()
    if existing:
        conn.execute(
            "UPDATE analytics SET query_count = query_count + 1 WHERE category=?",
            (category,),
        )
    else:
        conn.execute(
            "INSERT INTO analytics (category, query_count) VALUES (?, 1)", (category,)
        )
    conn.commit()
    conn.close()


def get_analytics():
    conn = get_db()
    rows = conn.execute("SELECT * FROM analytics ORDER BY query_count DESC").fetchall()
    conn.close()
    return rows


def get_top_category():
    conn = get_db()
    row = conn.execute(
        "SELECT category FROM analytics ORDER BY query_count DESC LIMIT 1"
    ).fetchone()
    conn.close()
    return row["category"] if row else "N/A"
