import common
from common.reportlab_styles import extend_style, extend_table_style
import os
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import registerFont, registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import TableStyle

font_dir = os.path.dirname(common.__file__)
registerFont(
    TTFont("LiberationSans", os.path.join(font_dir, "fonts", "LiberationSans-Regular.ttf"))
)
registerFont(
    TTFont("LiberationSans-Bold", os.path.join(font_dir, "fonts", "LiberationSans-Bold.ttf"))
)
registerFont(
    TTFont("LiberationSans-Italic", os.path.join(font_dir, "fonts", "LiberationSans-Italic.ttf"))
)
registerFont(
    TTFont("LiberationSans-BoldItalic", os.path.join(font_dir, "fonts", "LiberationSans-BoldItalic.ttf"))
)
registerFontFamily(
    "LiberationSans",
    normal="LiberationSans",
    bold="LiberationSans-Bold",
    italic="LiberationSans-Italic",
    boldItalic="LiberationSans-BoldItalic",
)

styles = dict()
styles["main"] = ParagraphStyle(
    "main",
    fontSize=9.75,
    leading=11.5,
    trailing=0,
    spaceBefore=0,
    spaceAfter=0,
    leftIndent=0,
    rightIndent=0,
    wordWrap=None,
    alignment=TA_LEFT,
    fontName="LiberationSans",
)
styles["doc-header"] = ParagraphStyle(
    "doc-header",
    parent=styles["main"],
    fontSize=11.75,
    leading=14,
    alignment=TA_CENTER,
)
styles["field-label"] = ParagraphStyle(
    "field-label",
    parent=styles["main"],
    fontName="LiberationSans-Bold",
)
styles["field-value"] = ParagraphStyle(
    "field-value",
    parent=styles["main"],
)
styles["main-table"] = TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ("TOPPADDING", (0, 0), (-1, -1), 0),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
])
styles["section-table"] = TableStyle([
    ("LEFTPADDING", (0, 0), (-1, -1), 1 * mm),
    ("RIGHTPADDING", (0, 0), (-1, -1), 1 * mm),
    ("TOPPADDING", (0, 0), (-1, -1), 0.5 * mm),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 0.5 * mm),
])
