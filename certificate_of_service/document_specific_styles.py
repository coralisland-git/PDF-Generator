from common.reportlab_styles import *

styles['rc-header'] = ParagraphStyle(
	"rc-header",
	parent=styles["rc-header"],
	fontSize=11
)

styles['rc-doc-header-fda'] = ParagraphStyle(
	"rc-doc-header-fda",
	parent=styles["rc-doc-header"],
	fontName='Arial-Bold',
	fontSize=14
)

styles['rc-doc-sub-header'] = ParagraphStyle(
	"rc-doc-sub-header",
	parent=styles["rc-header"],
	fontSize=12
)

styles["rc-aawp-main-content"] = ParagraphStyle(
    "rc-aawp-main-content",
    parent=styles["rc-aawp-main"],
    fontName="Arial",
    fontSize=10,
    alignment=TA_CENTER
)

styles["rc-aawp-main-header"] = ParagraphStyle(
    "rc-aawp-main-header",
    parent=styles["rc-aawp-main"],
    fontSize=12,
    leading=18,
    alignment=TA_CENTER
)
