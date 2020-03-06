from common.reportlab_styles import *

# document specific styles go here

styles["rc-tdwp-main"] = ParagraphStyle(
    "rc-tdwp-main",
    parent=styles["rc-main"],
    fontSize=12,
    spaceBefore=14
)

styles["rc-tdwp-main-tb"] = ParagraphStyle(
    "rc-tdwp-main-tb",
    parent=styles["rc-tdwp-main"],
    fontSize=12,
    leading=13,
    spaceBefore=0
)
