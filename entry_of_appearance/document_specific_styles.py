from common.reportlab_styles import *

# document specific styles go here

styles['rc-doc-header'] = ParagraphStyle(
	"rc-doc-header",
	parent=styles["rc-doc-header"],
    fontName="Times-Roman",
	spaceBefore=24,
	fontSize=10.5,
	leading=12
)

styles["rc-aawp-main-content"] = ParagraphStyle(
    "rc-aawp-main-content",
    parent=styles["rc-aawp-main"],
    fontSize=11,
    leading=14.5
)