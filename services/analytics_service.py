"""
analytics_service.py
Generates summary stats and category breakdown for the analytics dashboard.
"""

from models.analytics import get_analytics
from models.query import get_total_queries, get_unanswered_count
from models.feedback import get_avg_rating


def get_dashboard_stats():
    """Return a dict of high-level stats for the admin analytics page."""
    analytics = get_analytics()
    total = get_total_queries()
    unanswered = get_unanswered_count()
    avg_rating = get_avg_rating()
    answered = total - unanswered

    labels = [row["category"] for row in analytics]
    counts = [row["query_count"] for row in analytics]

    return {
        "total_queries": total,
        "answered": answered,
        "unanswered": unanswered,
        "avg_rating": avg_rating,
        "chart_labels": labels,
        "chart_counts": counts,
    }
