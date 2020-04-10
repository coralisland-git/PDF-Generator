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
    leading=13
)

styles["judge-signature"] = ParagraphStyle(
    "judge-signature",
    parent=styles["rc-aawp-main"],
    fontSize=10,
    leading=13,
    alignment=1
)

styles["rc-aawp-main-box"] = ParagraphStyle(
    "rc-aawp-main-box",
    parent=styles["rc-aawp-main"],
    fontSize=10,
    leading=11,
    alignment=TA_RIGHT
)

styles["rc-tdwp-main"] = ParagraphStyle(
    "rc-tdwp-main",
    parent=styles["rc-main"],
    fontSize=12,
    spaceBefore=14
)

styles["rc-tdwp-main-tb"] = ParagraphStyle(
    "rc-tdwp-main-tb",
    parent=styles["rc-tdwp-main"],
    fontSize=13,
    leading=13,
    spaceBefore=0
)

styles["rc-main-rmt-addr"] = ParagraphStyle(
    "rc-main-rmt-addr",
    parent=styles['rc-main-rmt'],
    fontName="Times-Roman",
    fontSize=12,
    leading=15,
    alignment=TA_LEFT
)

styles["rc-header"] = ParagraphStyle(
    "rc-main",
    parent=styles["rc-main"],
    fontSize=13,
    leading=13.5,
    trailing=0,
    fontName="Times-Bold",
    alignment=TA_CENTER,
)