import common
from common.reportlab_styles import extend_style, extend_table_style
from reportlab.lib.enums import TA_LEFT, TA_CENTER
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

styles = dict()
styles["oas-main"] = ParagraphStyle(
    "oas-main",
    fontSize=7,
    leading=8,
    spaceBefore=0,
    spaceAfter=0,
    leftIndent=0,
    rightIndent=0,
    wordWrap=None,
    alignment=TA_LEFT,
    fontName="LiberationSans",
)
styles["oas-doc-header"] = ParagraphStyle(
    "oas-doc-header",
    parent=styles["oas-main"],
    fontSize=9.5,
    leading=12,
    trailing=0,
    alignment=TA_CENTER,
)
styles["oas-section-header"] = ParagraphStyle(
    "oas-section-header",
    parent=styles["oas-main"],
    fontSize=8,
    leading=12.5,
    trailing=0,
    alignment=TA_CENTER,
)
styles["oas-main-table"] = TableStyle([
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ("TOPPADDING", (0, 0), (-1, -1), 0),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ("VALIGN", (0, 0), (-1, -1), "TOP")
])
