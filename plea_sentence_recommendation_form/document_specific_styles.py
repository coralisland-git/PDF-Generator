from common.reportlab_styles import *

# document specific styles go here

styles["rc-doc-header"] = ParagraphStyle(
    "rc-doc-header",
    parent=styles["rc-doc-header"],    
    fontSize=14,
	leading=21
)

styles["rc-doc-header-s"] = ParagraphStyle(
    "rc-doc-header",
    parent=styles["rc-doc-header"],
    fontName="Times-Roman",
    fontSize=12
)

styles["rc-aawp-main-content"] = ParagraphStyle(
    "rc-aawp-main-content",
    parent=styles["rc-aawp-main"],    
    leading=12,
    fontSize=11,    
)

styles["rc-aawp-main-content-tb"] = ParagraphStyle(
    "rc-aawp-main-content-tb",
    parent=styles["rc-aawp-main-content"],    
    leading=11
)

styles["rc-aawp-main-content-s"] = ParagraphStyle(
    "rc-aawp-main-content-s",
    parent=styles["rc-aawp-main-content"],    
    fontSize=10,
    leading=10
)