from common.reportlab_styles import *

# document specific styles go here

styles['rc-doc-header-fda'] = ParagraphStyle(
	"rc-doc-header-fda",
	parent=styles["rc-doc-header"],
	fontName='Arial-Bold',
	fontSize=14
)

styles["rc-aawp-main-content"] = ParagraphStyle(
    "rc-aawp-main-content",
    parent=styles["rc-aawp-main"],
    fontName="Arial",
    fontSize=14,
    leading=15,
    spaceBefore=14
)