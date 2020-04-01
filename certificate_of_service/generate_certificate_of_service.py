import cStringIO

from common.signatures import *
from document_specific_styles import *
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    Table,
    Spacer,
    TableStyle,
    BaseDocTemplate,
    PageTemplate,
    Frame,
)


def generate_certificate_of_service():
    buff = cStringIO.StringIO()
    doc = SignatureDocTemplate(buff, pagesize=letter)
    f = Frame(gutters[0], gutters[2], usable_width, usable_height, showBoundary=0)
    story = [
        Table(
            [
                [
                    Image("brookhaven.jpg", 24 * mm, 14 * mm),
                    Table(
                        [
                            [None],
                            [
                                Paragraph(
                                    """
                                    <b>CERTIFICATE OF SERVICE</b> <br/>
                                    """,
                                    styles["rc-doc-header-fda"],
                                )
                            ],
                            [None],
                            [
                                Paragraph(
                                    """
                                    STATE OF GEORGIA, DEKALB COUNTY <br />
                                    """,
                                    extend_style(styles["rc-doc-sub-header"]),
                                )
                            ],
                            [None],
                            [
                                Paragraph(
                                    """
                                    BROOKHAVEN MUNICIPAL COURT <br />
                                    2665 BUFORD HWY, BROOKHAVEN, GA 30324 <br />
                                    Phone: 404-637-660, Fax: (404) 671-3410
                                    """,
                                    extend_style(styles["rc-doc-header-info"]),
                                )
                            ],
                        ],
                        style=extend_table_style(
                            styles["rc-main-table"],
                            [("VALIGN", (0, 0), (-1, -1), "TOP")],
                        ),
                    ),
                    Paragraph(
                        """
                        """,
                        extend_style(
                            styles["rc-doc-sub-header"], alignment=TA_RIGHT, fontSize=9
                        ),
                    ),
                ]
            ],
            style=extend_table_style(
                styles["rc-main-table"],
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("TOPPADDING", (0, 0), (0, 0), 12 * mm),
                    ("TOPPADDING", (2, 0), (0, 0), 1.2 * mm),
                ],
            ),
            colWidths=(45 * mm, 108 * mm, 40 * mm),
        ),
        Table(
            [
                [None],
                [None],
                [
                    Paragraph(
                        """
                        <b>
                        CITY OF BROOKHAVEN <br/>
                        VS. <br/>
                        JUAN URIEL MELENDEZ HERRERA</b>
                        """,
                        styles["rc-aawp-main-header"],
                    ),
                    None,
                    Paragraph(
                        """
                        <br/>
                        Case Number: E31417
                        """,
                        styles["rc-aawp-main-header"],
                    ),
                ],
                [None],
                [None],
                [None],
                [None],
            ],
            style=extend_table_style(
                styles["rc-main-table"], [("VALIGN", (0, 0), (-1, -1), "TOP")]
            ),
            colWidths=(60 * mm, 50 * mm, 60 * mm),
        ),
        Paragraph(
            """
            CERTIFICATE OF SERVICE <br/>
            OF CLERK'S OFFICE TRANSMITTAL TO THE COURT APPOINTED ATTORNEY <br/>
            """,
            style=styles["rc-doc-content-header-fda"],
        ),
        Spacer(0, 6 * mm),
        Paragraph(
            "This is to certify that I have this day served by the attorney appointed by the court in the above-styled "
            "case with a true and correct copy of the document(s) checked below: __ by depositing same in the U.S. "
            "Mail, properly addressed and with sufficient postage affixed to insure delivery"
            " or __ by email provided by the appointed attorney.",
            style=styles["rc-aawp-main-content"],
        ),
        Spacer(0, 10 * mm),
        Paragraph("__ a. Copy of Citation(s)", style=styles["rc-aawp-main-content"]),
        Spacer(0, 6 * mm),
        Paragraph(
            "__ b. List of Witnesses - [AS CONTAINED IN ATTACHED (PORTION OF) INCIDENT AND/OR ACCIDENT REPORT "
            "& Scientific Reports)",
            style=styles["rc-aawp-main-content"],
        ),
        Spacer(0, 6 * mm),
        Paragraph(
            "__ c. Defendant's Oral Statements - [AS CONTAINED IN ATTACHED (PORTION OF) INCIDENT AND/OR "
            "ACCIDENT REPORT",
            style=styles["rc-aawp-main-content"],
        ),
        Spacer(0, 6 * mm),
        Paragraph(
            "__ d. Defendant's Written Statements - [ATTACHED][N/A]",
            style=styles["rc-aawp-main-content"],
        ),
        Spacer(0, 6 * mm),
        Paragraph(
            "__ e. Written Scientific Reports - Intox or Division of Forensic Science Report",
            style=styles["rc-aawp-main-content"],
        ),
        Spacer(0, 6 * mm),
        Paragraph(
            "__ f. Form for request of video if applicable",
            style=styles["rc-aawp-main-content"],
        ),
        Spacer(0, 15 * mm),
        Paragraph("The day of 07/16/2019", style=styles["rc-aawp-main-content"]),
        Spacer(0, 20 * mm),
        Paragraph("________________________", style=styles["rc-doc-signature"]),
        Spacer(0, 3 * mm),
        Paragraph("Clerk / Deputy Court Clerk", style=styles["rc-doc-signature"]),
    ]

    main_template = PageTemplate(id="main_template", frames=[f])
    doc.addPageTemplates([main_template])
    doc.build(story, canvasmaker=PageNumCanvas)
    del doc

    buff.seek(0)
    return buff
