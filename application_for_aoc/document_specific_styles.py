from common.reportlab_styles import *

# document specific styles go here

styles['rc-header'] = ParagraphStyle(
	"rc-header",
	parent=styles["rc-header"],
	fontSize=12
)

styles["rc-aawp-main-content"] = ParagraphStyle(
    "rc-aawp-main-content",
    parent=styles["rc-aawp-main"],
    fontSize=11,
    leading=14,
    spaceBefore=10
)

styles["rc-aawp-main-content-tb"] = ParagraphStyle(
    "rc-aawp-main-content-tb",
    parent=styles["rc-aawp-main-content"],
    leading=18.5
)