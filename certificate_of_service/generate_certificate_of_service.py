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
    Image('brookhaven.jpg', 48 * mm, 20 * mm),

    story = [
        Table(
            [
                [
                    Image('brookhaven.jpg', 20 * mm, 14 * mm),
                    Table(
                        [
                            [None],
                            [
                                Paragraph(
                                    """
                                    <b>CERTIFICATE OF SERVICE</b> <br/>
                                    """,
                                    styles['rc-doc-header-fda']
                                )
                            ],
                            [None],
                            [
                                Paragraph(
                                    """
                                    STATE OF GEORGIA, DEKALB COUNTY <br />
                                    """,
                                    extend_style(styles['rc-doc-sub-header'])
                                )
                            ],
                            [None],
                            [
                                Paragraph(
                                    """
                                    Case Number: E31417 <br/>
                                    BROOKHAVEN MUNICIPAL COURT <br />
                                    2665 BUFORD HWY, BROOKHAVEN, GA 30324 <br />
                                    Phone: 404-637-660, Fax: (404) 671-3410
                                    """,
                                    extend_style(styles["rc-aawp-main-content"])
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
                ("TOPPADDING", (2, 0), (0, 0), 1.2 * mm),
            ]),
            colWidths=(30 * mm, 112 * mm, 43 * mm)
        ),
    ]

    main_template = PageTemplate(id="main_template", frames=[f])
    doc.addPageTemplates([main_template])
    doc.build(story, canvasmaker=PageNumCanvas)
    del doc

    buff.seek(0)
    return buff
