from common.reportlab_styles import extend_style, extend_table_style
import os
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import TableStyle

pdfmetrics.registerFont(TTFont("Calibri", os.path.join(os.getcwd(), "fonts", "Calibri Regular.ttf")))
pdfmetrics.registerFont(TTFont("Calibri-Bold", os.path.join(os.getcwd(), "fonts", "Calibri Bold.ttf")))
pdfmetrics.registerFont(TTFont("Calibri-Italic", os.path.join(os.getcwd(), "fonts", "Calibri Italic.ttf")))
pdfmetrics.registerFont(TTFont("Calibri-BoldItalic", os.path.join(os.getcwd(), "fonts", "Calibri Bold Italic.ttf")))
pdfmetrics.registerFontFamily(
    "Calibri",
    normal="Calibri",
    bold="Calibri-Bold",
    italic="Calibri-Italic",
    boldItalic="Calibri-BoldItalic"
)

styles = dict()
styles["main"] = ParagraphStyle(
    "main",
    fontSize=11,
    leading=13,
    trailing=0,
    spaceBefore=0,
    spaceAfter=0,
    leftIndent=0,
    rightIndent=0,
    wordWrap=None,
    alignment=TA_LEFT,
    fontName="Calibri",
)
styles["doc-header"] = ParagraphStyle(
    "doc-header",
    parent=styles["main"],
    fontSize=14,
    leading=17,
    alignment=TA_CENTER,
)
styles["sect-header"] = ParagraphStyle(
    "sect-header",
    parent=styles["main"],
    fontSize=8,
    leading=8.5,
    alignment=TA_CENTER,
)
styles["field-label"] = ParagraphStyle(
    "field-label",
    parent=styles["main"],
    fontSize=11,
    leading=13,
)
styles["field-value"] = ParagraphStyle(
    "field-value",
    parent=styles["main"],
    fontSize=10.4,
    leading=14,
    fontName="Helvetica",
)
styles["invoice-field-value"] = ParagraphStyle(
    "invoice-field-value",
    parent=styles["field-value"],
    fontSize=10,
    leading=12,
)
styles["approval-field-value"] = ParagraphStyle(
    "approval-field-value",
    parent=styles["invoice-field-value"],
    leading=12.5,
)
styles["main-table"] = TableStyle([
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ("TOPPADDING", (0, 0), (-1, -1), 0),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
])
styles["section-table"] = TableStyle([
    ("OUTLINE", (0, 0), (-1, -1), 0.45, "black"),
    ("TOPPADDING", (0, 0), (-1, -1), 0.3 * mm),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 1.1 * mm),
    ("LEFTPADDING", (0, 0), (-1, -1), 2 * mm),
    ("RIGHTPADDING", (0, 0), (-1, -1), 2 * mm),
])
