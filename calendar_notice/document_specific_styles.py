from common.reportlab_styles import *

# document specific styles go here
styles["note"] = ParagraphStyle(
    "note",
    parent=styles["body"],
    fontSize=9,
    leading=10,
    leftIndent=0,
    rightIndent=0,
    vAlign='TOP',
    alignment=TA_CENTER
)
styles["rc-main-rmt-addr"] = ParagraphStyle(
    "rc-main-rmt-addr",
    parent=styles['rc-main-rmt'],
    fontName="Times-Roman",
    fontSize=12,
    leading=15,
)
styles["rc-aawp-main-content"] = ParagraphStyle(
    "rc-aawp-main-content",
    parent=styles["rc-aawp-main"],
    leading=20,
    leftIndent=1.9 * mm, 
    rightIndent=1.9 * mm
)
styles['rc-footer'] = ParagraphStyle(
    'body',
    parent=styles["body"],
    fontSize=10, 
    spaceAfter=0,
    leading=18, 
    leftIndent=14 * mm, 
    rightIndent=14 * mm
)