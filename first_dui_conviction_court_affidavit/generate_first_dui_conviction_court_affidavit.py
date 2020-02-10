import cStringIO

from document_specific_styles import *
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Flowable, Paragraph, Table, Spacer


def generate_first_dui_conviction_court_affidavit():
    cr = FDCCAReport()
    buff = cStringIO.StringIO()
    return cr.create_report(buff)


class FDCCAReport:
    def __init__(self, title=None, author=None):
        self.page_size = letter
        self.page_margin = (13.4 * mm, 4.4 * mm)
        self.sections = ["content"]
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
                rightPadding=0,
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

    def _section_content(self):
        elems = list()
        elems += [
            Spacer(0, 9.8 * mm),
            Paragraph(
                "FIRST DUI CONVICTION COURT AFFIDAVIT",
                styles["rc-doc-header-fda"]
            ),
            Paragraph(
                "PLEASE PRINT OR TYPE",
                styles["rc-header-dc"]
            ),
            Spacer(0, 4.4 * mm),
            Table(
                [
                    [
                        Paragraph("Name", styles["rc-aawp-main-content"]),
                        Paragraph("TAMICA SHEREE JOHNSON", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("Date of Birth", styles["rc-aawp-main-content"]),
                        Paragraph("07/06/1969", styles["rc-aawp-main-content"])
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (1, 0), (1, 0), 0.1, "black"),
                    ("LINEBELOW", (4, 0), (4, 0), 0.1, "black"),
                ]),
                colWidths=(12 * mm, 94 * mm, 8 * mm , 22 * mm, 53 * mm)
            ),
            Spacer(0, 2.4 * mm),
            Table(
                [
                    [
                        Paragraph("Address", styles["rc-aawp-main-content"]),
                        Paragraph("2086 GRAMERCY CIR", styles["rc-aawp-main-content"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (1, 0), (1, 0), 0.1, "black"),
                ]),
                colWidths=(15 * mm, 174 * mm),
                rowHeights=6.4 * mm
            ),
            Spacer(0, 2.4 * mm),
            Table(
                [
                    [
                        Paragraph("ATLANTA", styles["rc-aawp-main-content"]),
                        Paragraph("GA", styles["rc-aawp-main-content"]),
                        Paragraph("30341", styles["rc-aawp-main-content"]),
                    ],
                    [
                        Paragraph("City", styles["rc-aawp-main-content"]),
                        Paragraph("State", styles["rc-aawp-main-content"]),
                        Paragraph("Zip", styles["rc-aawp-main-content"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (0, 0), (2, 0), 0.1, "black"),
                ]),
                colWidths=(111* mm, 54 * mm, 24 * mm ),
                rowHeights=6.4 * mm
            ),
            Spacer(0, 2.4 * mm),
            Table(
                [
                    [
                        Paragraph("07/10/2019", styles["rc-aawp-main-content"]), None, 
                        None, None
                    ],
                    [
                        Paragraph("Date of Violation", styles["rc-aawp-main-content"]), None, 
                        Paragraph("Date of Conviction", styles["rc-aawp-main-content"]), None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (0, 0), (0, 0), 0.1, "black"),
                    ("LINEBELOW", (2, 0), (2, 0), 0.1, "black"),
                ]),
                colWidths=(82 * mm, 14 * mm , 82 * mm, 11 * mm),
                rowHeights=6.4 * mm
            ),
            Spacer(0, 2.4 * mm),
            Table(
                [
                    [
                        Paragraph("GA 060274748", styles["rc-aawp-main-content"]), None,
                        Paragraph("C", styles["rc-aawp-main-content"]), None,
                        None, None, 
                        None
                    ],
                    [
                        Paragraph("Driver's License Number", styles["rc-aawp-main-content"]), None,
                        Paragraph("Class", styles["rc-aawp-main-content"]), None,
                        Paragraph("Expiration Date", styles["rc-aawp-main-content"]), None,
                        Paragraph("Restrictions", styles["rc-aawp-main-content"])
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (0, 0), (0, 0), 0.1, "black"),
                    ("LINEBELOW", (2, 0), (2, 0), 0.1, "black"),
                    ("LINEBELOW", (4, 0), (4, 0), 0.1, "black"),
                    ("LINEBELOW", (6, 0), (6, 0), 0.1, "black"),
                ]),
                colWidths=(61 * mm, 6 * mm, 19 * mm, 6 * mm,  
                            26 * mm, 6 * mm, 65 * mm),
                rowHeights=6.4 * mm
            ),
            Spacer(0, 4.2 * mm),
            Table(
                [
                    [
                        Table(
                            [
                                [
                                    Paragraph("License Surrendered to court?", styles["rc-aawp-main-content"]),
                                    XBox(11, True), Paragraph("YES", styles["rc-aawp-main-chk"]),
                                    XBox(11), Paragraph("NO", styles["rc-aawp-main-chk"]),
                                ],
                                [
                                    Paragraph("If no, Lost License Affidavit?", styles["rc-aawp-main-content"]),
                                    XBox(11, True), Paragraph("YES", styles["rc-aawp-main-chk"]),
                                    XBox(11), Paragraph("NO", styles["rc-aawp-main-chk"]),
                                ],
                                [
                                    Paragraph("License previously surrendered?", styles["rc-aawp-main-content"]),
                                    XBox(11, True), Paragraph("YES", styles["rc-aawp-main-chk"]),
                                    XBox(11), Paragraph("NO", styles["rc-aawp-main-chk"]),
                                ]
                            ],
                            style=extend_table_style(styles["rc-main-table"], [
                                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ]),
                            colWidths=(54 * mm, 6 * mm, 12 * mm, 6 * mm, 12 * mm),
                            rowHeights=8.4 * mm
                        ),
                        Table(
                            [
                                [
                                    Table(
                                        [
                                            [
                                                None, None, None
                                            ],
                                            [
                                                Paragraph("Date License Surrendered", styles["rc-aawp-main-content-sub"]), None,
                                                Paragraph("Issue Date of License <br /> Surrendered", styles["rc-aawp-main-content-sub"]),
                                            ],
                                            [
                                                Paragraph("07/16/2019", styles["rc-aawp-main-content-sub"]), None, None
                                            ],
                                            [
                                                Paragraph("Date Affidavit Signed", styles["rc-aawp-main-content-sub"]), None, None
                                            ]
                                        ],
                                        style=extend_table_style(styles["rc-main-table"], [
                                            ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                                            ("LINEABOVE", (0, 1), (0, 1), 0.1, "black"),
                                            ("LINEABOVE", (2, 1), (2, 1), 0.1, "black"),
                                            ("LINEABOVE", (0, 3), (0, 3), 0.1, "black"),
                                        ]),
                                        colWidths=(42 * mm, 6 * mm, 42 * mm),
                                    )
                                ],  
                                [
                                    Paragraph("SEE REVERSE FOR IMPORTANT INFORMATION", styles["rc-aawp-main-content"]), None, None
                                ]
                            ],
                            style=extend_table_style(styles["rc-main-table"], [  
                                ("TOPPADDING", (0, 1), (0, 1), 1.8 * mm)
                            ]),
                        )
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("OUTLINE", (0, 0), (-1, -1), 1, "black"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 2.2 * mm),
                    ("TOPPADDING", (0, 0), (-1, -1), 2.2 * mm),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 1.4 * mm)

                ]),
                colWidths=(92*mm, 97 * mm)                
            ),
            Spacer(0, 17.5 * mm),
            Table(
                [                        
                    [
                        Paragraph("Signature of Authorized Official", styles["rc-aawp-main-content"]), None, 
                        Paragraph("<b>DS-1126 (02/06)</b>", styles["rc-aawp-main-content"])
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEABOVE", (0, 0), (0, 0), 0.1, "black"),                        
                ]),
                colWidths=(72 * mm, 90 * mm, 27 * mm),
                rowHeights=6.4 * mm
            ),
            Paragraph("SEAL", extend_style(styles["rc-aawp-main-content"], spaceBefore=4))
        ]
        
        return elems


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