import common
from common.reportlab_styles import *
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily, stringWidth

# document specific styles go here

FONT_DIR = os.path.join(os.path.dirname(common.__file__), "fonts")

pdfmetrics.registerFont(
    TTFont("Arial-Italic", os.path.join(FONT_DIR, "arialit.ttf"))
)

styles["rc-doc-header"] = ParagraphStyle(
    "rc-doc-header",
    parent=styles["rc-doc-header"],
    fontName="Arial-Bold",    
    leading=18,
    fontSize=13
)

styles["rc-header"] = ParagraphStyle(
    "rc-header",
    parent=styles["rc-header"],
    fontName="Arial",
    spaceBefore=12,
    fontSize=13  
)

styles["rc-aawp-main-content"] = ParagraphStyle(
    "rc-aawp-main-content",
    parent=styles["rc-aawp-main"],
    leading=14,
    fontSize=10,
    fontName="Arial"
)

styles["rc-aawp-main-date"] = ParagraphStyle(
    "rc-aawp-main-date",
    parent=styles["rc-aawp-main-content"],    
    fontName="Arial-Italic"
)