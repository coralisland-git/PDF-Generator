import cStringIO

from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Flowable, Paragraph, Table, Spacer

from document_specific_styles import *

class XBox(Flowable):
    def __init__(self, size, checked=None):
        Flowable.__init__(self)
        self.width = size
        self.height = size
        self.size = size
        self.checked = checked

    def draw(self):
        self.canv.saveState()
        self.canv.setLineWidth(0.11 * self.size)
        self.canv.rect(0, 0, self.width, self.height)
        if self.checked is True:
            self.check()
        self.canv.restoreState()

    def check(self):
        self.canv.setFont('Times-Bold', self.size * 0.95)
        to = self.canv.beginText(self.width * 0.13, self.height * 0.155)
        to.textLine("X")
        self.canv.drawText(to)


def generate_detention_order():
    buff = cStringIO.StringIO()
    doc = BaseDocTemplate(buff, pagesize=letter)
    f = Frame(gutters[0] * 1.5, gutters[2], usable_width-gutters[0], usable_height, showBoundary=0)

    story = []
    story.append(Image('brookhaven.jpg', 48 * mm, 16 * mm))
    story.append(Spacer(0, 4 * mm))
    story += [
        Paragraph(
            "IN THE MUNICIPAL COURT OF BROOKHAVEN <br />STATE OF GEORGIA",
            styles["ddo-heading"]
        ),
        Spacer(0, 4.2 * mm),
        Paragraph(
            "DETENTION ORDER",
            styles["ddo-heading"]
        ),
    ]
    story.append(
        Table(
            [
                [
                    Table(
                        [
                            [Paragraph("STATE OF GEORGIA", styles["ddo-main"])],
                            [Paragraph("VS", styles["ddo-main"])],
                            [None],
                        ],
                        style=extend_table_style(styles["rc-main-table"], [
                            ("LINEBELOW", (0, 2), (0, 2), 0.7, "black"),
                            ("LEFTPADDING", (0, 1), (0, 1), 12 * mm),
                        ]),
                        colWidths=70 * mm,
                        rowHeights=9 * mm
                    ),
                    Table(
                        [
                            [
                                Paragraph("DATE:", styles["ddo-main"]),
                                None
                            ],
                            [
                                Paragraph("CASE #:", styles["ddo-main"]),
                                None,
                            ],
                            [
                                Paragraph("CHARGE", styles["ddo-main"]),
                                None,
                            ],
                        ],
                        style=extend_table_style(styles["rc-main-table"], [
                            ("LINEBELOW", (1, 0), (1, -1), 0.5, "black"),
                            ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
                        ]),
                        colWidths=(18 * mm, 60 * mm),
                        rowHeights=9 * mm
                    ),
                ]
            ],
            style=extend_table_style(styles["rc-main-table"], [
                ("LEFTPADDING", (1, 0), (1, -1), 18 * mm),
            ]),
            colWidths=(77 * mm, 115 * mm),
            rowHeights=28 * mm
        )
    )
    story.append(Spacer(0, 9.2 * mm))
    story.append(Paragraph("To:  Officer in Charge", styles["ddo-main"]))
    story.append(Paragraph("Dekalb County Detention Center", extend_style(styles["ddo-main"], leftIndent=5 * mm)))
    story.append(Spacer(0, 3.2 * mm))
    story.append(Paragraph("In the disposition of the above styled case, and in accordance with the order of this court, the above named defendant is remanded to the custody of the Dekalb County Detention Center, Decatur, Georgia.", styles["ddo-main"]))
    story.append(Spacer(0, 3.2 * mm))
    story.append(Paragraph("The defendant is hereby ordered to serve a period of confinement of not less than:", styles["ddo-main"]))

    story.append(Spacer(0, 2 * mm))
    story.append(
        Table(
            [
                [
                    None,
                    XBox(12),
                    Paragraph("Days", styles["ddo-main"]),
                    XBox(12),
                    Paragraph("Hours", styles["ddo-main"]),
                    None
                ]
            ],
            style=extend_table_style(styles["rc-main-table"], [
                ("LINEBELOW", (0, 0), (0, 0), 0.5, "black"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]),
            colWidths=(16 * mm, 10 * mm, 12 * mm, 10 * mm, 12 * mm, 132 * mm),
            rowHeights=5.4 * mm
        )
    )
    story.append(Spacer(0, 5 * mm))

    table_data = []
    num_citations = 5
    for i in range(0, num_citations):
        table_data.append([
            Paragraph("Start Date:", style=extend_style(styles["ddo-main"], leftIndent=2 * mm)),
            None,
            Paragraph("@", style=styles["ddo-heading"]),
            None,
            XBox(9),
            Paragraph("AM", style=styles["ddo-heading"]),
            XBox(9),
            Paragraph("PM", style=styles["ddo-heading"])
        ])
        table_data.append([
            Paragraph("End Date:", style=extend_style(styles["ddo-main"], leftIndent=2 * mm)),
            None,
            Paragraph("@", style=styles["ddo-heading"]),
            None,
            XBox(9),
            Paragraph("AM", style=styles["ddo-heading"]),
            XBox(9),
            Paragraph("PM", style=styles["ddo-heading"])
        ])

    story.append(
        Table(
            table_data,
            style=extend_table_style(styles["rc-main-table"], [
                ("GRID", (0, 0), (-1, -1), 0.5, "black"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]),
            colWidths=(20 * mm, 62 * mm, 8 * mm, 18 * mm, 8 * mm, 10 * mm, 8 * mm, 10 * mm),
            rowHeights=7 * mm
        )
    )

    story.append(Spacer(0, 10 * mm))
    story.append(
        Table(
            [
                [
                    Paragraph("Judge", styles["ddo-main"]),
                    None,
                    None
                ],
                [
                    None,
                    None,
                    Paragraph("By Clerk", extend_style(styles["ddo-main"], alignment=TA_RIGHT)),
                ]
            ],
            style=extend_table_style(styles["rc-main-table"], [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 1.5 * mm),
                ("LINEABOVE", (0, 0), (0, 0), 0.5, "black"),
                ("LINEABOVE", (2, 1), (2, 1), 0.5, "black"),
            ]),
            colWidths=(82 * mm, 28 * mm, 82 * mm),
            rowHeights=4.3 * mm
        )
    )
    story.append(Spacer(0, 5.6 * mm))
    story.append(Paragraph("*" * 155, styles["ddo-main"]))
    story.append(Paragraph("To be completed by booking/releasing Officer", styles["ddo-heading"]))
    story.append(Paragraph("Defendant DID/DID NOT serve the above confinement in the DeKalb County Detention Center as ordered by the court.", styles["ddo-heading"]))
    story.append(Spacer(0, 8.5 * mm))
    story.append(
        Table(
            [
                [
                    Paragraph("Officer's Name", styles["ddo-main"]),
                    None,
                    Paragraph("Signature", styles["ddo-main"]),
                    None,
                    Paragraph("Date", styles["ddo-main"]),
                ]
            ],
            style=extend_table_style(styles["rc-main-table"], [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 1.5 * mm),
                ("LINEABOVE", (0, 0), (0, 0), 0.5, "black"),
                ("LINEABOVE", (2, 0), (2, 0), 0.5, "black"),
                ("LINEABOVE", (4, 0), (4, 0), 0.5, "black"),
            ]),
            colWidths=(68 * mm, 20 * mm, 67 * mm, 8 * mm, 30 * mm),
            rowHeights=4.3 * mm
        )
    )
    story.append(Spacer(0, 7.5 * mm))
    story.append(Paragraph("<font color='grey'>REVISED FEB. 2016</font>", extend_style(styles["ddo-main"], fontSize=5)))

    main_template = PageTemplate(id="main_template", frames=[f])
    doc.addPageTemplates([main_template])
    doc.build(story)
    del doc

    buff.seek(0)
    return buff

