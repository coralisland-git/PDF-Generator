from common.reportlab_styles import *

# document specific styles go here

styles["rc-tdwp-main"] = ParagraphStyle(
    "rc-tdwp-main",
    parent=styles["rc-main"],
    fontSize=10.5,
    leading=13.7,
    leftIndent=0.5 * mm, 
    rightIndent=0.5 * mm,
    spaceBefore=10
)

styles["rc-tdwp-main-tb"] = ParagraphStyle(
    "rc-tdwp-main-tb",
    parent=styles["rc-tdwp-main"],
    fontSize=11,
)