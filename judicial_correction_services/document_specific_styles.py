from common.reportlab_styles import *
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT

# document specific styles go here

styles['rc-doc-header'] = ParagraphStyle(
	"rc-doc-header",
	parent=styles["rc-doc-header"],
	fontName='Arial-Bold',
	fontSize=15,	
	alignment=TA_LEFT	
)

styles["rc-aawp-main-content"] = ParagraphStyle(
    "rc-aawp-main-content",
    parent=styles["rc-aawp-main"],
    fontName="Arial",
    fontSize=9.5,
    leading=13
)

styles["rc-main-table_inner"] = TableStyle(
    [
        ("LEFTPADDING", (0, 0), (-1, -1), .8*mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), .8*mm),
        ("TOPPADDING", (0, 0), (-1, -1), .5*mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0*mm),        
    ]
)
