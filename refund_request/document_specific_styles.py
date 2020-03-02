import common
from common.reportlab_styles import extend_style, extend_table_style
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.fonts import ps2tt
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase.pdfmetrics import registerFont, registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import TableStyle
import os

FONT_DIR = os.path.join(os.path.dirname(common.__file__), "fonts")

try:
    ps2tt("LiberationSans")
except ValueError:
    registerFont(TTFont("LiberationSans", os.path.join(FONT_DIR, "LiberationSans-Regular.ttf")))
    registerFont(TTFont("LiberationSans-Bold", os.path.join(FONT_DIR, "LiberationSans-Bold.ttf")))
    registerFont(TTFont("LiberationSans-Italic", os.path.join(FONT_DIR, "LiberationSans-Italic.ttf")))
    registerFont(TTFont("LiberationSans-BoldItalic", os.path.join(FONT_DIR, "LiberationSans-BoldItalic.ttf")))
    registerFontFamily(
        "LiberationSans",
        normal="LiberationSans",
        bold="LiberationSans-Bold",
        italic="LiberationSans-Italic",
        boldItalic="LiberationSans-BoldItalic",
    )

try:
    ps2tt("LiberationSansNarrow")
except ValueError:
    registerFont(TTFont("LiberationSansNarrow", os.path.join(FONT_DIR, "LiberationSansNarrow-Regular.ttf")))
    registerFont(TTFont("LiberationSansNarrow-Bold", os.path.join(FONT_DIR, "LiberationSansNarrow-Bold.ttf")))
    registerFont(TTFont("LiberationSansNarrow-Italic", os.path.join(FONT_DIR, "LiberationSansNarrow-Italic.ttf")))
    registerFont(
        TTFont("LiberationSansNarrow-BoldItalic", os.path.join(FONT_DIR, "LiberationSansNarrow-BoldItalic.ttf")))
    registerFontFamily(
        "LiberationSansNarrow",
        normal="LiberationSansNarrow",
        bold="LiberationSansNarrow-Bold",
        italic="LiberationSansNarrow-Italic",
        boldItalic="LiberationSansNarrow-BoldItalic",
    )

styles = dict()
styles["main"] = ParagraphStyle(
    "main",
    fontSize=9.5,
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
styles["main-right"] = ParagraphStyle(
    "main-right",
    parent=styles["main"],
    alignment=TA_RIGHT,
)
styles["main-narrow"] = ParagraphStyle(
    "main-narrow",
    parent=styles["main"],
    fontSize=10.8,
    leading=10.8,
    fontName="LiberationSansNarrow",
)
styles["main-narrow-right"] = ParagraphStyle(
    "main-narrow-right",
    parent=styles["main-narrow"],
    alignment=TA_RIGHT,
)
styles["doc-header"] = ParagraphStyle(
    "doc-header",
    parent=styles["main"],
    fontSize=12,
    leading=16,
    alignment=TA_CENTER,
    fontName="LiberationSansNarrow",
)
styles["doc-footer"] = ParagraphStyle(
    "doc-footer",
    parent=styles["main"],
    fontSize=8.25,
    leading=10.5,
    alignment=TA_CENTER,
    fontName="LiberationSansNarrow",
)
styles["section-header"] = ParagraphStyle(
    "section-header",
    parent=styles["main-narrow"],
    alignment=TA_CENTER,
)
styles["section-main"] = ParagraphStyle(
    "section-main",
    parent=styles["main"],
    fontSize=9.8,
    leading=12,
)
styles["field-label"] = ParagraphStyle(
    "field-label",
    parent=styles["main"],
)
styles["field-value"] = ParagraphStyle(
    "field-value",
    parent=styles["main"],
)
styles["main-table"] = TableStyle([
    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ("TOPPADDING", (0, 0), (-1, -1), 0),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
])
