from common.reportlab_styles import *

styles["rc-doc-header"] = ParagraphStyle(
    "rc-doc-header",
    parent=styles["rc-doc-header"],
    fontName="Arial",
    leading=14,
    fontSize=9
)

styles["rc-aawp-main-content"] = ParagraphStyle(
    "rc-aawp-main-content",
    parent=styles["rc-aawp-main"],    
    leading=11,
    fontSize=9,
    fontName="Arial"
)
