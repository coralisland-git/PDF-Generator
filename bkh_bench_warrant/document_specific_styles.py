from common.reportlab_styles import *

styles['rc-doc-header'] = ParagraphStyle(
	"rc-doc-header",
	parent=styles["rc-doc-header"],	
	fontSize=16,
	leading=24
)

styles["rc-aawp-main-header"] = ParagraphStyle(
    "rc-aawp-main-header",
    parent=styles["rc-aawp-main"],
    fontSize=12,
    leading=18,
    alignment=TA_CENTER
)

styles["rc-aawp-main-content"] = ParagraphStyle(
    "rc-aawp-main-content",
    parent=styles["rc-aawp-main"],
    fontSize=10,
    leading=14
)
