from common.reportlab_styles import *
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT

# document specific styles go here

styles['rc-doc-header'] = ParagraphStyle(
	"rc-doc-header",
	parent=styles["rc-doc-header"],
	fontName='Arial-Bold',
	fontSize=10,
	leading=19.5,
	alignment=TA_LEFT
)

styles["rc-aawp-main-content"] = ParagraphStyle(
    "rc-aawp-main-content",
    parent=styles["rc-aawp-main"],
    fontName="Arial",
    fontSize=10
)

styles["rc-aawp-main-content-centre"] = ParagraphStyle(
    "rc-aawp-main-content-centre",
    parent=styles["rc-aawp-main-content"],
    alignment=TA_CENTER
)

styles["rc-aawp-main-content-right"] = ParagraphStyle(
    "rc-aawp-main-content-right",
    parent=styles["rc-aawp-main-content"],
    alignment=TA_RIGHT
)

styles["rc-aawp-main-content-page"] = ParagraphStyle(
    "rc-aawp-main-content-page",
    parent=styles["rc-aawp-main"],
    fontName="Arial-Bold",
    fontSize=8.5
)