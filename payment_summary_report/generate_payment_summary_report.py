import cStringIO

from document_specific_styles import *
from common.signatures import *
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT


def generate_payment_summary_report():
    cr = PSRReport()
    buff = cStringIO.StringIO()
    return cr.create_report(buff)


class PSRReport:
    def __init__(self, title=None, author=None):
        self.page_size = letter
        self.page_margin = (19.4 * mm, 9.8 * mm)
        self.sections = ["page_1", "page_2"]
        self.title = title
        self.author = author
        self.data = None

    def create_report(self, buff=None):
        def get_method(section):
            try:
                method = getattr(self, "_section_" + section)
            except AttributeError:
                raise Exception("Section method not found: " + section)
            return method     

        if not buff:
            buff = io.BytesIO()

        story = []
        for section in self.sections:
            elems = get_method(section)()
            for elem in elems:
                story.append(elem)

        page_t = PageTemplate('normal', [
            Frame(
                self.page_margin[0],
                self.page_margin[1],
                self.page_size[0] - self.page_margin[0] * 2,
                self.page_size[1] - self.page_margin[1] * 2,
                leftPadding=0,
                bottomPadding=0,
                rightPadding=62*mm,
                topPadding=0,
            )
        ])
        doc_t = BaseDocTemplate(
            buff,
            pagesize=letter,
            title=self.title,
            author=self.author,
            leftMargin=self.page_margin[0],
            rightMargin=self.page_margin[0],
            topMargin=self.page_margin[1],
            bottomMargin=self.page_margin[1],
        )
        doc_t.addPageTemplates(page_t)
        doc_t.build(story)
        buff.seek(0)
        return buff

    def _section_page_1(self):
        elems = list()
        elems += [
            Spacer(0, 4 * mm),
            Paragraph(
                "BROOKHAVEN MUNICIPAL COURT",
                styles["rc-doc-header"]
            ),
            Paragraph(
                """
                    Payment Summary Report <br />
                    07/17/2019 To 07/17/2019 
                """,
                styles["rc-doc-header"]
            ),
            Table(
                [
                    [
                        Paragraph("<b>Description</b>", styles["rc-aawp-main-content"]),
                        Paragraph("<b>Account</b>", styles["rc-aawp-main-content"]),
                        Paragraph("<b>Amount</b>", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        Paragraph("ATTY FEE", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("0.00", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        Paragraph("Base Fine", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("555.27", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        Paragraph("Base Fine 2", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("0.00", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        Paragraph("CONTEMPT CHRG", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("0.00", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        Paragraph("INDIGENT APP FEE", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("0.00", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        Paragraph("Jail", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("0.00", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        Paragraph("LATE FEE", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("0.00", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        Paragraph("MISC CHRG", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("0.00", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        Paragraph("NSF", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("0.00", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        Paragraph("Over Payment", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("0.00", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        Paragraph("PRE TRIAL FEE", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("0.00", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        Paragraph("PRE TRIAL POABF", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("0.00", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        Paragraph("Processing Fee", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("240.00", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        Paragraph("RESTITUTION", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("0.00", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        Paragraph("WARRANT FEE", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("0.00", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        None,
                        None,
                        Paragraph("795.27", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        Paragraph("Poilce Off Annuity", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("40.35", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        None,
                        None,
                        Paragraph("40.35", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        Paragraph("Brain Spinal Inj Fd", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("0.00", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        Paragraph("Crime Lab Fee", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("0.00", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        Paragraph("Crime Vic Emg", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("0.00", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        Paragraph("Dr Edu Train(1.5%)", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("7.22", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        Paragraph("Dr Edu Train(5%)", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("0.00", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        Paragraph("POPIDF-A", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("48.07", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        Paragraph("POPIDF-B", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("48.07", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        None,
                        None,
                        Paragraph("103.36", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        Paragraph("Drug Abuse Trt Edu", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("0.00", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        None,
                        None,
                        Paragraph("0.00", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        Paragraph("Bond Forfeiture", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("0.00", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        Paragraph("Local Vic Asst Prg", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("24.02", styles["rc-aawp-main-content-right"]),
                    ],                    
                    [
                        None,
                        None,
                        Paragraph("24.02", styles["rc-aawp-main-content-right"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (0, 0), (2, 0), 0.1, "black"),
                    ("LINEBELOW", (2, 15), (2, 15), 0.1, "black"),
                    ("LINEBELOW", (2, 17), (2, 17), 0.1, "black"),
                    ("LINEBELOW", (2, 25), (2, 25), 0.1, "black"),
                    ("LINEBELOW", (2, 27), (2, 27), 0.1, "black"),
                    ("LINEBELOW", (2, 30), (2, 30), 0.1, "black"),
                ]),
                colWidths=(52*mm, 38*mm, 25*mm),
                rowHeights=5.7*mm
            ),
            Spacer(0, 47.4 * mm),
            Table(
                [
                    [
                        Paragraph("07/18/2019 at 08:20 AM", styles["rc-aawp-main-content-page"]),
                        Paragraph("Page 1 of 2", extend_style(styles["rc-aawp-main-content-page"], alignment=TA_RIGHT)),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [                    
                ]),
                colWidths=(90*mm, 25*mm)
            )
        ]
        return elems

    def _section_page_2(self):
        elems = list()
        elems += [
            Spacer(0, 4 * mm),
            Paragraph(
                "BROOKHAVEN MUNICIPAL COURT",
                styles["rc-doc-header"]
            ),
            Paragraph(
                """
                    Payment Summary Report <br />
                    07/17/2019 To 07/17/2019 
                """,
                styles["rc-doc-header"]
            ),
            Table(
                [
                    [
                        Paragraph("<b>Description</b>", styles["rc-aawp-main-content"]),
                        Paragraph("<b>Account</b>", styles["rc-aawp-main-content"]),
                        Paragraph("<b>Amount</b>", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        Paragraph("Case Processing Fee", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("0.00", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        None,
                        None,
                        Paragraph("0.00", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        None,
                        None,
                        Paragraph("963.00", styles["rc-aawp-main-content-right"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (0, 0), (2, 0), 0.1, "black"),
                    ("LINEBELOW", (2, 1), (2, 1), 0.1, "black"),
                    ("LINEBELOW", (0, 2), (2, 2), 0.1, "black"),
                    ("BOTTOMPADDING", (0, 2), (2, 2), 1 * mm),
                    ("LINEBELOW", (0, 2), (2, 2), 0.1, "black"),
                    ("LINEBELOW", (0, 3), (2, 3), 0.1, "black"),
                ]),
                colWidths=(52*mm, 38*mm, 25*mm),
                rowHeights=5.8*mm
            ),
            Table(
                [                    
                    [
                        Paragraph("<b>Cash Tendered</b>", styles["rc-aawp-main-content"]),
                        Paragraph("30.00", styles["rc-aawp-main-content-right"]), None,
                        Paragraph("<b>Total</b>", styles["rc-aawp-main-content"]),
                        Paragraph("963.00", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        Paragraph("<b>Check Tendered</b>", styles["rc-aawp-main-content"]),
                        Paragraph("0.00", styles["rc-aawp-main-content-right"]), None,
                        Paragraph("<b>(CB Applied)</b>", styles["rc-aawp-main-content"]),
                        Paragraph("50.00", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        Paragraph("<b>MO Tendered</b>", styles["rc-aawp-main-content"]),
                        Paragraph("0.00", styles["rc-aawp-main-content-right"]), None,
                        None, None
                    ],
                    [
                        Paragraph("<b>CC Tendered</b>", styles["rc-aawp-main-content"]),
                        Paragraph("883.00", styles["rc-aawp-main-content-right"]), None,
                        None, None
                    ],
                    [
                        Paragraph("<b>ECA Tendered</b>", styles["rc-aawp-main-content"]),
                        Paragraph("0.00", styles["rc-aawp-main-content-right"]), None,
                        Paragraph("<b>NC Fefunds</b>", styles["rc-aawp-main-content"]),
                        Paragraph("0.00", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        Paragraph("<b>CB Cash</b>", styles["rc-aawp-main-content"]),
                        Paragraph("0.00", styles["rc-aawp-main-content-right"]), None,
                        Paragraph("<b>CB Cash</b>", styles["rc-aawp-main-content"]),
                        Paragraph("0.00", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        Paragraph("<b>CB CC</b>", styles["rc-aawp-main-content"]),
                        Paragraph("0.00", styles["rc-aawp-main-content-right"]), None,
                        Paragraph("<b>CB CC</b>", styles["rc-aawp-main-content"]),
                        Paragraph("0.00", styles["rc-aawp-main-content-right"]),
                    ],
                    [
                        Paragraph("<b>Net</b>", styles["rc-aawp-main-content"]),
                        Paragraph("913.00", styles["rc-aawp-main-content-right"]), None,
                        Paragraph("<b>Net</b>", styles["rc-aawp-main-content"]),
                        Paragraph("913.00", styles["rc-aawp-main-content-right"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [                    
                ]),
                colWidths=(35*mm, 15*mm, 15*mm, 35*mm, 15*mm),
                rowHeights=5.8*mm
            ),            
            Spacer(0, 160 * mm),
            Table(
                [
                    [
                        Paragraph("07/18/2019 at 08:20 AM", styles["rc-aawp-main-content-page"]),
                        Paragraph("Page 2 of 2", extend_style(styles["rc-aawp-main-content-page"], alignment=TA_RIGHT)),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [                    
                ]),
                colWidths=(90*mm, 25*mm)
            ),
        ]
        return elems
