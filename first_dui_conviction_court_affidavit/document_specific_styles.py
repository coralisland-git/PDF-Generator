from common.reportlab_styles import *
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT

# document specific styles go here

styles['rc-doc-header-fda'] = ParagraphStyle(
	"rc-doc-header-fda",
	parent=styles["rc-doc-header"],
	fontName='Arial-Bold',
	fontSize=14
)

styles["rc-header-dc"] = ParagraphStyle(
    "rc-header-dc",
    parent=styles["rc-header"],
    fontName="Arial-Italic",
    spaceBefore=14,    
    alignment=TA_LEFT,
)

styles["rc-aawp-main-content"] = ParagraphStyle(
    "rc-aawp-main-content",
    parent=styles["rc-aawp-main"],
    fontName="Arial",
    fontSize=10,
    leading=15
)

styles["rc-aawp-main-content-sub"] = ParagraphStyle(
	"rc-aawp-main-content-sub",
	alignment=TA_CENTER
)

styles["rc-aawp-main-chk"] = ParagraphStyle(
    "rc-aawp-main-chk",
    parent=styles["rc-aawp-main-content"],    
    leading=12,
    fontSize=10
)