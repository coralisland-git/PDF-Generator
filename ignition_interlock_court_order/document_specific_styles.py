from common.reportlab_styles import *
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT

# document specific styles go here

styles['rc-doc-header'] = ParagraphStyle(
	"rc-doc-header",
	parent=styles["rc-doc-header"],
	fontSize=16,
	leading=24
)

styles["rc-aawp-main-header"] = ParagraphStyle(
    "rc-aawp-main-header",
    parent=styles["rc-aawp-main"],
    fontSize=12,
    leading=18,
    alignment=TA_CENTER
)

styles["rc-aawp-main-content"] = ParagraphStyle(
    "rc-aawp-main-content",
    parent=styles["rc-aawp-main"],
    fontSize=10,
    leading=13
)

styles["rc-aawp-main-box"] = ParagraphStyle(
    "rc-aawp-main-box",
    parent=styles["rc-aawp-main"],
    fontSize=10,
    leading=11,
    alignment=TA_RIGHT
)

styles["ddo-heading"] = ParagraphStyle(
    "rc-main-rmt",
    fontSize=9,
    leading=15,
    alignment=TA_CENTER,
    fontName="Arial",
)

styles["ddo-main"] = ParagraphStyle(
    "rc-main-rmt",
    parent=styles['ddo-heading'],
    alignment=TA_LEFT,
    fontSize=12,
)

