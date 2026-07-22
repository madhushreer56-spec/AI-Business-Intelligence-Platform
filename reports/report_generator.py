from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_report(

    question,

    sql,

    result,

    insight,

    filename="Business_Report.pdf"

):

    styles = getSampleStyleSheet()

    pdf = SimpleDocTemplate(filename)

    story = []

    story.append(
        Paragraph("<b>AI Business Intelligence Report</b>", styles["Title"])
    )

    story.append(Spacer(1,12))

    story.append(
        Paragraph(f"<b>Business Question:</b><br/>{question}",styles["BodyText"])
    )

    story.append(Spacer(1,12))

    story.append(
        Paragraph("<b>Generated SQL</b>",styles["Heading2"])
    )

    story.append(
        Paragraph(sql.replace("\n","<br/>"),styles["Code"])
    )

    story.append(Spacer(1,12))

    story.append(
        Paragraph("<b>Query Result</b>",styles["Heading2"])
    )

    story.append(
        Paragraph(result.to_html(index=False),styles["BodyText"])
    )

    story.append(Spacer(1,12))

    story.append(
        Paragraph("<b>AI Business Insight</b>",styles["Heading2"])
    )

    story.append(
        Paragraph(insight.replace("\n","<br/>"),styles["BodyText"])
    )

    pdf.build(story)

    return filename