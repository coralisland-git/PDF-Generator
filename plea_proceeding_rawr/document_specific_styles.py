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
    fontSize=10.5,
    leading=12,
    spaceBefore=10
)