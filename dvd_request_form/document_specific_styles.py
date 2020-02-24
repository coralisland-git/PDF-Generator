from common.reportlab_styles import *

# document specific styles go here

styles['rc-doc-header'] = ParagraphStyle(
	"rc-doc-header",
	parent=styles["rc-doc-header"],
	fontName='Arial-Bold',
	fontSize=10,
	leading=14
)

styles['rc-doc-header-sub'] = ParagraphStyle(
	"rc-doc-header-sub",
	parent=styles["rc-doc-header"],
	fontName='Arial'	
)

styles["rc-aawp-main-content"] = ParagraphStyle(
    "rc-aawp-main-content",
    parent=styles["rc-aawp-main"],
    fontName="Arial",
    fontSize=11,    
)