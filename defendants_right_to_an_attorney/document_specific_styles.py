from common.reportlab_styles import *

# document specific styles go here

styles['rc-header'] = ParagraphStyle(
	"rc-header",
	parent=styles["rc-header"],
	fontSize=11
)

styles["rc-aawp-main-header"] = ParagraphStyle(
    "rc-aawp-main-header",
    parent=styles["rc-aawp-main"],
    fontSize=11,
    leading=13,
    spaceBefore=8
)

styles["rc-aawp-main-content"] = ParagraphStyle(
    "rc-aawp-main-content",
    parent=styles["rc-aawp-main"],
    fontSize=10,
    leading=12,
    spaceBefore=8
)