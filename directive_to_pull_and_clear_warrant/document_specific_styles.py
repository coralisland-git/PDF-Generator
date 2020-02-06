from common.reportlab_styles import *

# document specific styles go here

styles["rc-header-dc"] = ParagraphStyle(
    "rc-header-dc",
    parent=styles["rc-header"],
    fontName="Times-Roman",
    spaceBefore=12
)

styles["rc-aawp-main-content"] = ParagraphStyle(
    "rc-aawp-main-content",
    parent=styles["rc-aawp-main"],
    leading=16,
    spaceBefore=13
)