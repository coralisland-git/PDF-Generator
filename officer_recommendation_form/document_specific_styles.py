from common.reportlab_styles import *

# document specific styles go here

styles['rc-doc-header-orf'] = ParagraphStyle(
	"rc-doc-header-orf",
	parent=styles["rc-doc-header"],
	fontName='Arial-Bold',
	fontSize=9
)

styles["rc-aawp-main-content"] = ParagraphStyle(
    "rc-aawp-main-content",
    parent=styles["rc-aawp-main"],
    fontName="Arial",
    fontSize=9,
    leading=15,
    spaceBefore=10
)