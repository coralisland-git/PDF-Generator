import cStringIO

from document_specific_styles import *
from common.signatures import *
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Flowable, Paragraph, Table, Spacer
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT


def generate_abstract_of_court_record():
    cr = FDCCAReport()
    buff = cStringIO.StringIO()
    return cr.create_report(buff)


class FDCCAReport:
    def __init__(self, title=None, author=None):
        self.page_size = letter
        self.page_margin = (9.4 * mm, 7.8 * mm)
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

        def page_number(canv, doc):
            page_num = Paragraph(
                str(doc.page),
                extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER, fontSize=8),
            )
            page_num.wrapOn(canv, self.page_size[0], 0)
            page_num.drawOn(canv, 0, 4.8*mm)

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
        ], onPage=page_number)
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
        TEST_DATA = "Test Data"
        elems += [            
            Table(
                [
                    [
                        Image('brookhaven.jpg', 16 * mm, 14* mm),
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
                                        "ABSTRACT OF COURT RECORD", 
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
                            03/18/2020
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
                colWidths=(42*mm, 112*mm, 43*mm)
            ),
            Spacer(0, 6.4*mm),
            Table(
                [   
                    [
                        Table(
                            [   
                                [
                                    Paragraph(
                                        """
                                        <b>  
                                        E31417 <br />
                                        JUAN URIEL MELENDEZ HERRERA <br />
                                        3649 BUFORD HWY NE <br />
                                        BROOKHAVEN, GA 30329-1134
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
                            rowHeights=6.2*mm
                        ),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
                colWidths=(90*mm, 90*mm)
            ),
            Spacer(0, 4.2*mm),
            Table(
                [   
                    [
                        Paragraph("VEHICLE INFORMATION", styles['rc-aawp-main-content']),
                        Table(
                            [   
                                [
                                    Paragraph("<b>TAG #:</b> QBC4838", styles['rc-aawp-main-content']),
                                    Paragraph("<b>STATE:</b> GA", styles['rc-aawp-main-content']),
                                    Paragraph("<b>YEAR:</b> {}".format(TEST_DATA), styles['rc-aawp-main-content']),
                                ],
                                [   
                                    Paragraph("<b>DESCRIPTION:</b> BLU 2001 VOLKSWAGON GOLF GLS", styles['rc-aawp-main-content']),
                                    None, None
                                ]
                            ],
                            style=extend_table_style(styles["rc-main-table"], [
                                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                ("SPAN", (0, 1), (2, 1)),
                            ]),
                            rowHeights=6.2*mm
                        ),
                    ],            
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
                colWidths=(55*mm, 125*mm)
            ),

            Spacer(0, 4.2*mm),
        ]
        violation_table = []
        violation_styles = [
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("OUTLINE", (0, 0), (-1, -1), .1, "black"), 
            ("TOPPADDING", (0, 0), (-1, -1), 1.8 * mm),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1.8 * mm),
            ("LEFTPADDING", (0, 0), (-1, -1), 1.8 * mm),
            ("RIGHTPADDING", (0, 0), (-1, -1), 1.8 * mm),
        ]
        violation_arr = [
            {
                "Initial Charge" : "DUI-ALCOHOL-LESS SAFE-1ST",
                "Convicted Charge" : "DUI-ALCOHOL-LESS SAFE-1ST",
                "BAC %": TEST_DATA,
                "Speed" : TEST_DATA,
                "Zone" : TEST_DATA,
                "Date of Violation" : "10/17/2016",
                "Officer" : "S MILLER",
                "Badge No" : "1683",
                "Complainant" : TEST_DATA,
                "Date of Judgment" : "01/12/2017",
                "Judge" : "JONATHAN R. GRANADE",
                "Judgment of Court" : "Warrant-Bench",
                "Represented by (if any)" : TEST_DATA,
                "Appointed (if any)" : TEST_DATA,
                "Remarks" : TEST_DATA
            },
            {
                "Initial Charge" : "DUI-ALCOHOL-LESS SAFE-1ST",
                "Convicted Charge" : "DUI-ALCOHOL-LESS SAFE-1ST",
                "BAC %": TEST_DATA,
                "Speed" : TEST_DATA,
                "Zone" : TEST_DATA,
                "Date of Violation" : "10/17/2016",
                "Officer" : "S MILLER",
                "Badge No" : "1683",
                "Complainant" : TEST_DATA,
                "Date of Judgment" : "01/12/2017",
                "Judge" : "JONATHAN R. GRANADE",
                "Judgment of Court" : "Warrant-Bench",
                "Represented by (if any)" : TEST_DATA,
                "Appointed (if any)" : TEST_DATA,
                "Remarks" : TEST_DATA
            },
        ]
        for idx, violation in enumerate(violation_arr):
            violation_table.append(
                [Table(
                    [
                        [
                            Paragraph("<b>Initial Charge:</b> {}".format(violation['Initial Charge']), styles['rc-aawp-main-content']),
                            Paragraph("<b>Convicted Charge:</b> {}".format(violation['Convicted Charge']), styles['rc-aawp-main-content']),
                            Paragraph("<b>BAC %: </b> {}".format(violation['BAC %']), styles['rc-aawp-main-content']),
                        ],
                        [
                            Paragraph("<b>Speed:</b> {}".format(violation['Speed']), styles['rc-aawp-main-content']),
                            Paragraph("<b>Zone:</b> {}".format(violation['Zone']), styles['rc-aawp-main-content']),
                            Paragraph("<b>Date of Violation:</b> {}".format(violation['Speed']), styles['rc-aawp-main-content']),
                        ],
                        [
                            Paragraph("<b>Officer:</b> {}".format(violation['Officer']), styles['rc-aawp-main-content']),
                            Paragraph("<b>Badge No:</b> {}".format(violation['Badge No']), styles['rc-aawp-main-content']),
                            Paragraph("<b>Complainant:</b> {}".format(violation['Complainant']), styles['rc-aawp-main-content']),
                        ],
                        [
                            Paragraph("<b>Date of Judgment:</b> {}".format(violation['Date of Judgment']), styles['rc-aawp-main-content']),
                            Paragraph("<b>Judge:</b> {}".format(violation['Judge']), styles['rc-aawp-main-content']),
                            Paragraph("<b>Judgment of Court:</b> {}".format(violation['Judgment of Court']), styles['rc-aawp-main-content']),
                        ],
                        [
                            Paragraph("<b>Represented by (if any):</b> {}".format(violation['Represented by (if any)']), styles['rc-aawp-main-content']),
                            Paragraph("<b>Appointed (if any):</b> {}".format(violation['Appointed (if any)']), styles['rc-aawp-main-content']),
                            Paragraph("<b>Remarks:</b> {}".format(violation['Remarks']), styles['rc-aawp-main-content']),
                        ]
                    ],
                    style=extend_table_style(styles["rc-main-table"], [
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ]),
                )]
            )  
            violation_styles.append(
                ("LINEBELOW", (0, idx), (0, idx), 0.1, "black")
            )      
        elems +=[
            Table(                
                violation_table,
                style=extend_table_style(styles["rc-main-table"], violation_styles),
            ),
            Spacer(0, 5*mm),
            Table(
                [   
                    [
                        Paragraph("<b>PROBATION:</b> {}".format(TEST_DATA), styles['rc-aawp-main-content']),
                        Paragraph("<b>END DATE:</b> {}".format(TEST_DATA), styles['rc-aawp-main-content']),
                        Paragraph("<b>WITH:</b> {}".format(TEST_DATA), styles['rc-aawp-main-content'])
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
                colWidths=(60*mm, 60*mm, 60*mm)
            ),
            Spacer(0, 1.8*mm),
            Table(
                [   
                    [
                        Table(
                            [   
                                [
                                    Paragraph("<b>DEFENDANT WAS FINED:</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                                    None
                                ],
                                [
                                    Paragraph("<b>FINE AMOUNT $:</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                                    Paragraph("437.55", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                                ],
                                [   
                                    Paragraph("<b>PLUS ASSESSMENTS OF $:</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                                    Paragraph("512.45", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                                ],
                                [   
                                    Paragraph("<b>FOR A TOTAL OF $:</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                                    Paragraph("950.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                                ],
                                [   
                                    Paragraph("<b>- PAYMENTS $:</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                                    Paragraph("950.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                                ],
                                [   
                                    Paragraph("<b>TOTAL $:</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                                    Paragraph("0.00", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                                ]
                            ],
                            style=extend_table_style(styles["rc-main-table"], [
                                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                ("LEFTPADDING", (0, 0), (0, 5), 1.8 * mm),
                                ("LINEABOVE", (1, 3), (1, 3), 0.1, "black"),
                                ("LINEABOVE", (1, 5), (1, 5), 0.1, "black"),
                            ]),
                            colWidths=(60*mm, 18*mm)
                        ),
                        Table(
                            [   
                                [
                                    Paragraph("<b>BAIL FORFEITED:</b>", styles['rc-aawp-main-box']),
                                    XBox(8, True)
                                ],
                                [
                                    Paragraph("<b>FINE PAID:</b>", styles['rc-aawp-main-box']),
                                    XBox(8, True)
                                ],
                                [
                                    Paragraph("<b>APPEALED:</b>", styles['rc-aawp-main-box']),
                                    XBox(8, True)
                                ],
                                [
                                    None,
                                    XBox(8, True)
                                ],
                                [
                                    Paragraph(
                                        "<b>SENTENCED TO:</b> <br />", 
                                        styles['rc-aawp-main-content']
                                    ),
                                    None
                                ],
                                [
                                    Paragraph(
                                        """                                        
                                        Years in Jail, <br />
                                        Months in Jail, <br />
                                        Days in Jail.
                                        """, 
                                        extend_style(styles['rc-aawp-main-content'], leftIndent=12*mm, leading=10)
                                    ),
                                    None
                                ],
                            ],
                            style=extend_table_style(styles["rc-main-table"], [
                                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                ("LEFTPADDING", (1, 0), (1, 3), 2.4 * mm),
                                ("TOPPADDING", (1, 0), (1, 3), .9 * mm),
                                ("BOTTOMPADDING", (0, 3), (0, 3), 1.2 * mm),
                                ("LINEBELOW", (0, 3), (0, 3), 0.1, "black"),
                            ]),
                        ),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),                
            ),
            Spacer(0, 3.2*mm),
            Paragraph("I certify that this is a true and correct copy of my court record.", extend_style(styles['rc-aawp-main-content'], leftIndent=9*mm)),
            Spacer(0, 1.8*mm),
            Table(
                [   
                    [
                        Paragraph("<b>DOCKET:</b> E31417", extend_style(styles['rc-aawp-main-content'], leftIndent=22*mm)),
                        Paragraph("<b>SIGNED</b>", styles['rc-aawp-main-content']),
                        Paragraph("", styles['rc-aawp-main-content']),                        
                    ],
                    [
                        None,
                        None,
                        Paragraph("Court Clerk / Deputy Court Clerk ", styles['rc-aawp-main-content']),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEBELOW", (2, 0), (2, 0), 0.1, "black"),
                ]),
                colWidths=(100*mm, 16*mm, 81*mm)
            ),
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