import common
from common.reportlab_styles import extend_style, extend_table_style
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.fonts import ps2tt
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase.pdfmetrics import registerFont, registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import TableStyle
import os

FONT_DIR = os.path.join(os.path.dirname(common.__file__), "fonts")

try:
    ps2tt("LiberationSerif")
except ValueError:
    registerFont(TTFont("LiberationSerif", os.path.join(FONT_DIR, "LiberationSerif-Regular.ttf")))
    registerFont(TTFont("LiberationSerif-Bold", os.path.join(FONT_DIR, "LiberationSerif-Bold.ttf")))
    registerFont(TTFont("LiberationSerif-Italic", os.path.join(FONT_DIR, "LiberationSerif-Italic.ttf")))
    registerFont(TTFont("LiberationSerif-BoldItalic", os.path.join(FONT_DIR, "LiberationSerif-BoldItalic.ttf")))
    registerFontFamily(
        "LiberationSerif",
        normal="LiberationSerif",
        bold="LiberationSerif-Bold",
        italic="LiberationSerif-Italic",
        boldItalic="LiberationSerif-BoldItalic",
    )

styles = dict()
styles["main"] = ParagraphStyle(
    "main",
    fontSize=10,
    leading=11.5,
    trailing=0,
    spaceBefore=0,
    spaceAfter=0,
    leftIndent=0,
    rightIndent=0,
    wordWrap=None,
    alignment=TA_LEFT,
    fontName="LiberationSerif",
)
styles["doc-header"] = ParagraphStyle(
    "doc-header",
    parent=styles["main"],
    spaceBefore=10,
    spaceAfter=10,
    alignment=TA_CENTER,
)
styles["section-main"] = ParagraphStyle(
    "section-main",
    parent=styles["main"],
    fontSize=10,
    leading=11.5,
    alignment=TA_JUSTIFY,
)
styles["main-table"] = TableStyle([
    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ("TOPPADDING", (0, 0), (-1, -1), 0),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
])
