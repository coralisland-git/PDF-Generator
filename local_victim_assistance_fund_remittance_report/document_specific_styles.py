from common.reportlab_styles import *

styles["check_body"] = ParagraphStyle(
    "check_body",
    parent=styles["body"],
    alignment=TA_LEFT,
    leftIndent=inch/1.5,
    rightIndent=inch/1.5,
)
