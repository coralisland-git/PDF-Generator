from common.reportlab_styles import *

styles["rc-mdr-main-content"] = ParagraphStyle(
    "rc-mdr-main-content",
    parent=styles["rc-aawp-main"],
    fontName="Arial",
    fontSize=9.5,
    leading=15,
)

styles["rc-mdr-header"] = ParagraphStyle(
    "rc-mdr-header",
    parent=styles["rc-header"],
    fontName="Times-Roman",
    fontSize=15,
    leading=15,
)

styles["footer"] = ParagraphStyle(
    "footer",
    parent=styles["detail-slimfit"],
)

styles["signature"] = ParagraphStyle(
    "signature",
    parent=styles["body"],
    fontSize=9.5,
)