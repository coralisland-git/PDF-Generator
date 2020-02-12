from common.reportlab_styles import *

# document specific styles go here

styles["rc-doc-header-nor"] = ParagraphStyle(
    "rc-doc-header-nor",
    parent=styles["rc-doc-header"],
    fontName="Arial-Bold",
    leading=13.5,
    fontSize=12
)

styles["rc-doc-header-nor-s"] = ParagraphStyle(
    "rc-doc-header-nor-s",
    parent=styles["rc-doc-header"],
    fontName="Arial"
)

styles["rc-aawp-main-content"] = ParagraphStyle(
    "rc-aawp-main-content",
    parent=styles["rc-aawp-main"],
    fontName="Arial",
    leading=12,
    fontSize=10,
    spaceBefore=12.5
)

styles["rc-aawp-main-content-tb"] = ParagraphStyle(
    "rc-aawp-main-content-tb",
    parent=styles["rc-aawp-main-content"],    
    leading=14
)

styles["rc-aawp-main-chk"] = ParagraphStyle(
    "rc-aawp-main-chk",
    parent=styles["rc-aawp-main-content"],    
    leading=12,
    fontSize=10
)