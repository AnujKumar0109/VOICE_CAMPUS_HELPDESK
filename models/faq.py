from models.db import get_db


def get_all_faqs():
    conn = get_db()
    faqs = conn.execute("SELECT * FROM faqs ORDER BY category, id").fetchall()
    conn.close()
    return faqs


def get_faq_by_id(faq_id):
    conn = get_db()
    faq = conn.execute("SELECT * FROM faqs WHERE id = ?", (faq_id,)).fetchone()
    conn.close()
    return faq


def add_faq(question, answer, category):
    conn = get_db()
    conn.execute(
        "INSERT INTO faqs (question, answer, category) VALUES (?, ?, ?)",
        (question, answer, category),
    )
    conn.commit()
    conn.close()


def update_faq(faq_id, question, answer, category):
    conn = get_db()
    conn.execute(
        "UPDATE faqs SET question=?, answer=?, category=? WHERE id=?",
        (question, answer, category, faq_id),
    )
    conn.commit()
    conn.close()


def delete_faq(faq_id):
    conn = get_db()
    conn.execute("DELETE FROM faqs WHERE id = ?", (faq_id,))
    conn.commit()
    conn.close()


def get_faqs_by_category(category):
    conn = get_db()
    faqs = conn.execute("SELECT * FROM faqs WHERE category = ?", (category,)).fetchall()
    conn.close()
    return faqs


def get_categories():
    conn = get_db()
    rows = conn.execute("SELECT DISTINCT category FROM faqs ORDER BY category").fetchall()
    conn.close()
    return [r["category"] for r in rows]
