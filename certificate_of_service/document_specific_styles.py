from common.reportlab_styles import *

styles["rc-header"] = ParagraphStyle(
    "rc-header", parent=styles["rc-header"], fontSize=11
)

styles["rc-doc-header-fda"] = ParagraphStyle(
    "rc-doc-header-fda",
    parent=styles["rc-doc-header"],
    fontName="Arial-Bold",
    fontSize=15,
)

styles["rc-doc-sub-header"] = ParagraphStyle(
    "rc-doc-sub-header", parent=styles["rc-header"], fontSize=12
)

styles["rc-doc-header-info"] = ParagraphStyle(
    "rc-doc-sub-header-info", alignment=TA_CENTER, fontSize=10
)

styles["rc-aawp-main-content"] = ParagraphStyle(
    "rc-aawp-main-content",
    parent=styles["rc-aawp-main"],
    fontName="Arial",
    fontSize=12,
)

styles["rc-aawp-main-header"] = ParagraphStyle(
    "rc-aawp-main-header",
    parent=styles["rc-aawp-main"],
    fontSize=10,
    alignment=TA_CENTER,
)

styles["rc-doc-content-header-fda"] = ParagraphStyle(
    "rc-doc-content-header-fda",
    parent=styles["rc-doc-header"],
    fontName="Arial-Bold",
    fontSize=13,
)

styles["rc-doc-signature"] = ParagraphStyle(
    "rc-doc-signature", fontSize=12, alignment=TA_RIGHT,
)
