from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
import io


def summary_to_pdf(summary_text):

    buffer = io.BytesIO()
    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("PDF NLP Summarizer - Summary", styles["Title"]))
    story.append(Spacer(1, 20))

    story.append(Paragraph(summary_text, styles["BodyText"]))

    doc = SimpleDocTemplate(buffer, pagesize=A4)
    doc.build(story)

    buffer.seek(0)

    return buffer