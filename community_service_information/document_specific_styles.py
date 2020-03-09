from common.reportlab_styles import *
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT

# document specific styles go here

styles["rc-tdwp-main"] = ParagraphStyle(
    "rc-tdwp-main",
    parent=styles["rc-main"],
    fontSize=10,
    leading=14,
)

styles["rc-tdwp-main-list"] = ParagraphStyle(
    "rc-tdwp-main",
    parent=styles["rc-main"],
    fontSize=9,
    leading=12,
)

styles["rc-tdwp-main-tb"] = ParagraphStyle(
    "rc-tdwp-main-tb",
    parent=styles["rc-tdwp-main"],
    fontSize=10,
    leading=12
)

styles["rc-tdwp-main-header"] = ParagraphStyle(
    "rc-tdwp-main-header",
    parent=styles["rc-tdwp-main"],
    fontSize=24,
    leading=32,
    spaceBefore=18,
    alignment=TA_CENTER
)

styles["rc-tdwp-main-header-box"] = ParagraphStyle(
    "rc-tdwp-main-header-box",
    parent=styles["rc-tdwp-main"],
    fontSize=13,
    alignment=TA_CENTER,
    leading=14
)