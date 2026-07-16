"""
pdf_service.py
Generates a PDF report of a user's chat history using ReportLab.
"""

import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)


def generate_chat_pdf(user_name: str, queries: list) -> bytes:
    """
    Build a PDF from a list of query rows and return bytes.
    Each query row must have: question, response, status, created_at.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontSize=18,
        textColor=colors.HexColor("#1a3c5e"),
        spaceAfter=6,
    )
    sub_style = ParagraphStyle(
        "Sub",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.grey,
        spaceAfter=12,
    )
    q_style = ParagraphStyle(
        "Q",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#1a3c5e"),
        fontName="Helvetica-Bold",
        spaceAfter=2,
    )
    a_style = ParagraphStyle(
        "A",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#2d2d2d"),
        spaceAfter=10,
        leftIndent=12,
    )

    story = [
        Paragraph("Voice-Based Campus Helpdesk", title_style),
        Paragraph(f"Chat History Report — {user_name}", sub_style),
        HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1a3c5e")),
        Spacer(1, 12),
    ]

    if not queries:
        story.append(Paragraph("No queries found.", styles["Normal"]))
    else:
        for i, q in enumerate(queries, 1):
            status_color = "#28a745" if q["status"] == "answered" else "#dc3545"
            story.append(
                Paragraph(
                    f"<b>Q{i}:</b> {q['question']}  "
                    f"<font color='{status_color}'>[{q['status'].upper()}]</font>",
                    q_style,
                )
            )
            answer_text = q["response"] if q["response"] else "No answer available."
            story.append(Paragraph(f"A: {answer_text}", a_style))
            story.append(
                Paragraph(
                    f"<font color='grey' size='8'>{q['created_at']}</font>",
                    styles["Normal"],
                )
            )
            story.append(Spacer(1, 6))

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
