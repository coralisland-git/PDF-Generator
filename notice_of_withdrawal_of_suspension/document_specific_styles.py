import common
from common.reportlab_styles import extend_style, extend_table_style
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import registerFont, registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import TableStyle
import os

FONT_DIR = os.path.dirname(common.__file__)
registerFont(
    TTFont("LiberationSans", os.path.join(FONT_DIR, "fonts", "LiberationSans-Regular.ttf"))
)
registerFont(
    TTFont("LiberationSans-Bold", os.path.join(FONT_DIR, "fonts", "LiberationSans-Bold.ttf"))
)
registerFont(
    TTFont("LiberationSans-Italic", os.path.join(FONT_DIR, "fonts", "LiberationSans-Italic.ttf"))
)
registerFont(
    TTFont("LiberationSans-BoldItalic", os.path.join(FONT_DIR, "fonts", "LiberationSans-BoldItalic.ttf"))
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
    fontSize=9,
    leading=10.5,
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
    fontSize=10.8,
    leading=13,
    leftIndent=81 * mm,
)
styles["doc-footer"] = ParagraphStyle(
    "doc-footer",
    parent=styles["main"],
    fontSize=10,
    leading=12,
)
styles["field-label"] = ParagraphStyle(
    "field-label",
    parent=styles["main"],
    underlineProportion=0.08,
)
styles["field-value"] = ParagraphStyle(
    "field-value",
    parent=styles["main"],
    fontSize=12,
    leftIndent=0.2 * mm,
    spaceBefore=2.2 * mm
)
styles["main-table"] = TableStyle([
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ("TOPPADDING", (0, 0), (-1, -1), 0),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
])
styles["wrapper-table"] = TableStyle([
    ("OUTLINE", (0, 0), (-1, -1), 0.5 * mm, "black"),
    ("LEFTPADDING", (0, 0), (-1, -1), 2 * mm),
    ("RIGHTPADDING", (0, 0), (-1, -1), 2 * mm),
    ("TOPPADDING", (0, 0), (-1, -1), 1 * mm),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 1 * mm),
])
