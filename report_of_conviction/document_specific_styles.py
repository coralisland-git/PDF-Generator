from common.reportlab_styles import *

from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT

# document specific styles go here

styles["rc-tdwp-main"] = ParagraphStyle(
    "rc-tdwp-main",
    parent=styles["rc-main"],
    fontSize=8.5,
    leading=13,
    leftIndent=0.5 * mm, 
    rightIndent=0.5 * mm,
    spaceBefore=6,
    fontName="Arial"
)

styles["rc-tdwp-main-chk"] = ParagraphStyle(
    "rc-tdwp-main-chk",
    parent=styles["rc-tdwp-main"],    
    leading=10.5
)

styles["rc-tdwp-main-tt"] = ParagraphStyle(
    "rc-tdwp-main-tt",
    parent=styles["rc-tdwp-main"],    
    alignment=TA_CENTER
)

styles["rc-doc-header-roc"] = ParagraphStyle(
    "rc-doc-header-roc",
    parent=styles["rc-doc-header"],
    fontName="Arial-Bold",
    fontSize=13, 
    leading=14.5
)