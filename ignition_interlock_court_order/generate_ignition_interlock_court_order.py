import cStringIO

from common.signatures import *
from document_specific_styles import *


def generate_ignition_interlock_court_order():
    buff = cStringIO.StringIO()
    doc = SignatureDocTemplate(buff, pagesize=letter)
    f = Frame(gutters[0], gutters[2], usable_width, usable_height, showBoundary=0)

    story = []
    story += header()
    story += body()

    main_template = PageTemplate(id="main_template", frames=[f])
    doc.addPageTemplates([main_template])
    doc.build(story, canvasmaker=PageNumCanvas)
    del doc

    buff.seek(0)
    return buff

def header():
    story = []
    story.append(
        Table(
            [
                [
                    Image('brookhaven.jpg', 24 * mm, 14 * mm),
                    Table(
                        [
                            [
                                Paragraph(
                                    """                                        
                                    <b>BROOKHAVEN MUNICIPAL COURT</b> <br />
                                    2665 BUFORD HWY BROOKHAVEN, GA 30324 <br />
                                    PHONE: 404-637-0660 <br />
                                    FAX: (404) 671-3410
                                    """,
                                    extend_style(styles['rc-aawp-main-header'])
                                )
                            ],
                            [
                                None
                            ],
                            [
                                Paragraph(
                                    "IGNITION INTERLOCK COURT ORDER",
                                    styles["rc-doc-header"]
                                )
                            ],
                            [
                                Paragraph(
                                    """
                                    STATE OF GEORGIA <br />
                                    DEKALB COUNTY   <br />
                                    CITY OF BROOKHAVEN
                                    """,
                                    extend_style(styles["rc-doc-header"], fontSize=12)
                                )
                            ]
                        ],
                        style=extend_table_style(styles["rc-main-table"], [
                            ("VALIGN", (0, 0), (-1, -1), "TOP")
                        ]),
                    ),
                    Paragraph(
                        """
                        """,
                        extend_style(styles['rc-aawp-main-header'], alignment=TA_RIGHT, fontSize=9)
                    )
                ]
            ],
            style=extend_table_style(styles["rc-main-table"], [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (0, 0), 12 * mm),
                ("TOPPADDING", (2, 0), (2, 0), 1.2 * mm),
            ]),
            colWidths=(42 * mm, 112 * mm, 43 * mm)
        ),
    )
    return story

def body():
    story = []
    TEST_DATA = "Test Data"
    story += [
        Table(
            [
                [
                    Table(
                        [
                            [
                                Paragraph(
                                    """
                                    <b>
                                    STATE OF GEORGIA <br />
                                    VS <br />
                                    TAMICA SHREE JOHNSON <br />
                                    Charge: DRIVING WHILE LIC. SUSPENDED OR REVOKED (MANDATORY)
                                    </b>
                                    """,
                                    extend_style(styles['rc-aawp-main-content'])
                                )
                            ]
                        ],
                        style=extend_table_style(styles["rc-main-table"], [
                            ("VALIGN", (0, 0), (-1, -1), "TOP")
                        ]),
                    ),
                    Table(
                        [
                            [
                                Paragraph("<b>Agency Code:</b> 044201J", styles['rc-aawp-main-content']),
                                Paragraph("<b>Ticket No:</b> E31417", styles['rc-aawp-main-content']),
                            ],
                            [
                                Paragraph("<b>DL#:</b> NL", styles['rc-aawp-main-content']),
                                Paragraph("<b>SSN:</b> {}".format(TEST_DATA), styles['rc-aawp-main-content'])
                            ],
                            [
                                Paragraph("<b>Sex:</b> MALE", styles['rc-aawp-main-content']),
                                Paragraph("<b>Race:</b> WHITE", styles['rc-aawp-main-content']),
                            ],
                            [
                                Paragraph("<b>DOB:</b> 09/24/1987 ", styles['rc-aawp-main-content']),
                                Paragraph("<b>Age:</b> 31", styles['rc-aawp-main-content']),
                            ]
                        ],
                        style=extend_table_style(styles["rc-main-table"], [
                            ("VALIGN", (0, 0), (-1, -1), "TOP")
                        ]),
                        rowHeights=6.2 * mm
                    ),
                ]
            ],
            style=extend_table_style(styles["rc-main-table"], [
                ("VALIGN", (0, 0), (-1, -1), "TOP")
            ]),
            colWidths=(90 * mm, 90 * mm)
        ),
    ]
    return story
