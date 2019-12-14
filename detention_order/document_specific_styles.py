from common.reportlab_styles import *

styles["ddo-heading"] = ParagraphStyle(
    "rc-main-rmt",
    fontSize=9,
    leading=15,
    alignment=TA_CENTER,
    fontName="Arial",
)

styles["ddo-main"] = ParagraphStyle(
    "rc-main-rmt",
    parent=styles['ddo-heading'],
    alignment=TA_LEFT
)
