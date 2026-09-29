from io import BytesIO
from datetime import datetime
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


BRAND_NAME = "Research Intelligence"


def clean_markdown_text(text):
    """Remove Markdown formatting that is not needed in PDF paragraphs."""
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"`(.*?)`", r"\1", text)
    text = re.sub(r"~~(.*?)~~", r"\1", text)

    # Remove HTML tags accidentally returned by the model
    text = re.sub(r"<[^>]+>", "", text)

    return text.strip()


def split_markdown_table(lines):
    """Convert a Markdown table into ReportLab table data."""
    rows = []

    for line in lines:
        if "|" not in line:
            continue

        cells = [
            clean_markdown_text(cell.strip())
            for cell in line.strip().strip("|").split("|")
        ]

        # Ignore separator row: |---|---|
        if all(re.fullmatch(r":?-{2,}:?", cell) for cell in cells):
            continue

        rows.append(cells)

    return rows


def add_page_footer(canvas, doc):
    """Footer displayed on every PDF page."""
    canvas.saveState()

    width, height = A4

    canvas.setStrokeColor(colors.HexColor("#D9E2EC"))
    canvas.setLineWidth(0.5)

    canvas.line(
        18 * mm,
        13 * mm,
        width - 18 * mm,
        13 * mm,
    )

    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#64748B"))

    canvas.drawString(
        18 * mm,
        8 * mm,
        f"{BRAND_NAME} · Multi-Agent Research System",
    )

    canvas.drawRightString(
        width - 18 * mm,
        8 * mm,
        f"Page {doc.page}",
    )

    canvas.restoreState()


def create_pdf(report_markdown, question):
    """
    Generate a professionally formatted PDF from the final Markdown report.

    Returns:
        BytesIO: PDF file in memory.
    """

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
        title=BRAND_NAME,
        author=BRAND_NAME,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=30,
        alignment=TA_CENTER,
        spaceAfter=10,
        textColor=colors.HexColor("#0F172A"),
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=15,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#64748B"),
        spaceAfter=5,
    )

    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=21,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=14,
        spaceAfter=8,
    )

    subheading_style = ParagraphStyle(
        "SubHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#1E3A5F"),
        spaceBefore=10,
        spaceAfter=5,
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#334155"),
        spaceAfter=7,
    )

    bullet_style = ParagraphStyle(
        "Bullet",
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-7,
        spaceAfter=4,
    )

    small_style = ParagraphStyle(
        "Small",
        parent=body_style,
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#64748B"),
    )

    story = []

    # ---------------------------------------------------------
    # Cover / Header
    # ---------------------------------------------------------

    story.append(Spacer(1, 25 * mm))

    story.append(
        Paragraph(
            BRAND_NAME,
            title_style,
        )
    )

    story.append(
        Paragraph(
            "Multi-Agent Research Report",
            subtitle_style,
        )
    )

    story.append(Spacer(1, 8 * mm))

    question_data = [
        [
            Paragraph(
                "<b>Research Question</b>",
                body_style,
            ),
            Paragraph(
                clean_markdown_text(question),
                body_style,
            ),
        ],
        [
            Paragraph(
                "<b>Generated</b>",
                body_style,
            ),
            Paragraph(
                datetime.now().strftime("%d %B %Y, %H:%M"),
                body_style,
            ),
        ],
        [
            Paragraph(
                "<b>Research System</b>",
                body_style,
            ),
            Paragraph(
                "7-Agent Collaborative Research Intelligence System",
                body_style,
            ),
        ],
    ]

    question_table = Table(
        question_data,
        colWidths=[38 * mm, 132 * mm],
        hAlign="CENTER",
    )

    question_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#F1F5F9"),
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#CBD5E1"),
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.3,
                    colors.HexColor("#E2E8F0"),
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    story.append(question_table)
    story.append(Spacer(1, 15 * mm))

    story.append(
        Paragraph(
            "Generated by seven specialized research agents working "
            "collaboratively across web, academic, industry, evidence "
            "analysis, fact checking, and synthesis.",
            small_style,
        )
    )

    story.append(PageBreak())

    # ---------------------------------------------------------
    # Parse Markdown report
    # ---------------------------------------------------------

    lines = report_markdown.splitlines()

    i = 0

    while i < len(lines):

        line = lines[i].strip()

        if not line:
            i += 1
            continue

        # Markdown heading
        if line.startswith("# "):
            heading = clean_markdown_text(line[2:])
            story.append(Paragraph(heading, heading_style))
            i += 1
            continue

        if line.startswith("## "):
            heading = clean_markdown_text(line[3:])
            story.append(Paragraph(heading, subheading_style))
            i += 1
            continue

        # Markdown table
        if "|" in line and i + 1 < len(lines) and "|" in lines[i + 1]:

            table_lines = []

            while i < len(lines) and "|" in lines[i]:
                table_lines.append(lines[i])
                i += 1

            table_data = split_markdown_table(table_lines)

            if table_data:

                processed = []

                for row_index, row in enumerate(table_data):

                    processed_row = []

                    for cell in row:
                        processed_row.append(
                            Paragraph(
                                clean_markdown_text(cell),
                                small_style,
                            )
                        )

                    processed.append(processed_row)

                col_count = max(len(row) for row in processed)

                # Normalize row lengths
                for row in processed:
                    while len(row) < col_count:
                        row.append(Paragraph("", small_style))

                col_width = 174 * mm / col_count

                table = Table(
                    processed,
                    colWidths=[col_width] * col_count,
                    repeatRows=1,
                    hAlign="LEFT",
                )

                table.setStyle(
                    TableStyle(
                        [
                            (
                                "BACKGROUND",
                                (0, 0),
                                (-1, 0),
                                colors.HexColor("#E2E8F0"),
                            ),
                            (
                                "TEXTCOLOR",
                                (0, 0),
                                (-1, 0),
                                colors.HexColor("#0F172A"),
                            ),
                            (
                                "FONTNAME",
                                (0, 0),
                                (-1, 0),
                                "Helvetica-Bold",
                            ),
                            (
                                "GRID",
                                (0, 0),
                                (-1, -1),
                                0.4,
                                colors.HexColor("#CBD5E1"),
                            ),
                            (
                                "VALIGN",
                                (0, 0),
                                (-1, -1),
                                "TOP",
                            ),
                            (
                                "LEFTPADDING",
                                (0, 0),
                                (-1, -1),
                                5,
                            ),
                            (
                                "RIGHTPADDING",
                                (0, 0),
                                (-1, -1),
                                5,
                            ),
                            (
                                "TOPPADDING",
                                (0, 0),
                                (-1, -1),
                                5,
                            ),
                            (
                                "BOTTOMPADDING",
                                (0, 0),
                                (-1, -1),
                                5,
                            ),
                        ]
                    )
                )

                story.append(Spacer(1, 3 * mm))
                story.append(table)
                story.append(Spacer(1, 5 * mm))

            continue

        # Bullet
        if line.startswith("- ") or line.startswith("* "):
            bullet = clean_markdown_text(line[2:])
            story.append(
                Paragraph(
                    f"• {bullet}",
                    bullet_style,
                )
            )
            i += 1
            continue

        # Numbered list
        numbered = re.match(r"^\d+\.\s+(.*)", line)

        if numbered:
            item = clean_markdown_text(numbered.group(1))
            story.append(
                Paragraph(
                    f"• {item}",
                    bullet_style,
                )
            )
            i += 1
            continue

        # Normal paragraph
        paragraph = clean_markdown_text(line)

        if paragraph:
            story.append(
                Paragraph(
                    paragraph,
                    body_style,
                )
            )

        i += 1

    # ---------------------------------------------------------
    # Build PDF
    # ---------------------------------------------------------

    doc.build(
        story,
        onFirstPage=add_page_footer,
        onLaterPages=add_page_footer,
    )

    buffer.seek(0)

    return buffer
