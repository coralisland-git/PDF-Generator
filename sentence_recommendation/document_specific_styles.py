from common.reportlab_styles import *

styles['rc-doc-header-scf'] = ParagraphStyle(
	"rc-doc-header-scf",
	parent=styles["rc-doc-header"],	
	fontSize=20.5,
    leading=25,
    fontName="Times-Roman"
)

styles["rc-aawp-main-content"] = ParagraphStyle(
    "rc-aawp-main-content",
    parent=styles["rc-aawp-main"],
    fontSize=12,
    leading=22
)

styles["rc-aawp-main-content-tb"] = ParagraphStyle(
    "rc-aawp-main-content-tb",
    parent=styles["rc-aawp-main"],
    fontSize=12    
)