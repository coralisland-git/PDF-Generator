import cStringIO

from document_specific_styles import *
from common.signatures import *
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT


def generate_municipal_court_caseload_report():
    cr = MCCRReport()
    buff = cStringIO.StringIO()
    return cr.create_report(buff)


class MCCRReport:
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
                "Page "+str(doc.page)+"of 1",
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
                                        "OBTAIN FINGER PRINTS", 
                                        styles["rc-doc-header"]
                                    )
                                ],
                                [
                                    Paragraph(
                                        """
                                        STATE OF GEORGIA <br />
                                        DEKALB COUNTY
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
                                    Paragraph("<b>REPORT TO:</b> ", extend_style(styles['rc-aawp-main-content'])),
                                    Paragraph(
                                        """
                                        BROOKHAVEN POLICE DEPARTMENT <br />
                                        2665 BUFORD HWY <br />
                                        BROOKHAVEN, GA 30324 <br />
                                        404-637-0600
                                        """,
                                        extend_style(styles['rc-aawp-main-content'])
                                    )
                                ]
                            ],
                            style=extend_table_style(styles["rc-main-table"], [
                                ("VALIGN", (0, 0), (-1, -1), "TOP")
                            ]),
                            colWidths=(28*mm, 77*mm)
                        ),
                        Table(
                            [   
                                [
                                    Paragraph("<b>HOURS:</b>", styles['rc-aawp-main-content']),
                                    Paragraph(
                                        """
                                        TUESDAY & THURSDAY  <br />
                                        8:00 AM - 12:00 PM  <br />
                                        6:00 PM - 8:00 PM
                                        """, styles['rc-aawp-main-content']),
                                ]
                            ],
                            style=extend_table_style(styles["rc-main-table"], [
                                ("VALIGN", (0, 0), (-1, -1), "TOP")
                            ]),
                            colWidths=(20*mm, 55*mm)
                        ),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
                colWidths=(105*mm, 75*mm)
            ),
            Spacer(0, 4.2*mm),
            Paragraph("""
                UPON COMPLETION OF FORM, RETURN TO BROOKHAVEN MUNICIPAL COURT FOR [CCH] PROCESSING OF FINGER PRINTS. <br />
                BROOKHAVEN MUNICIPAL COURT WILL PROVIDE A COPY OF THIS FORM TO THE PROBATION OFFICE.
                """, 
                extend_style(styles['rc-aawp-main-content'], alignment=TA_CENTER, fontSize=8)
            ),
            Spacer(0, 4.2*mm),
            Table(
                [   
                    [
                        Paragraph("<b>FULL NAME:</b> JUAN URIEL MELENDEZ HERRERA", styles['rc-aawp-main-content']),
                        None, None, None
                    ],
                    [
                        Paragraph("<b>GENDER:</b> Male", styles['rc-aawp-main-content']),
                        Paragraph("<b>RACE:</b> White", styles['rc-aawp-main-content']),
                        Paragraph("""<b>HEIGHT:</b> 5' 5" """, styles['rc-aawp-main-content']),
                        Paragraph("<b>WEIGHT:</b> 150", styles['rc-aawp-main-content']),
                    ],
                    [
                        Paragraph("<b>EYE COLOR:</b> Brown", styles['rc-aawp-main-content']),
                        None,
                        Paragraph("<b>HAIR COLOR:</b> Brown", styles['rc-aawp-main-content']),
                        None
                    ],
                    [
                        Paragraph("<b>PLACE OF BIRTH:</b> {}".format(TEST_DATA), styles['rc-aawp-main-content']),
                        None,
                        Paragraph("<b>DATE OF BIRTH:</b> 09/24/1987", styles['rc-aawp-main-content']),
                        None
                    ],
                    [   
                        Paragraph("<b>RESIDENCE OF PERSON:</b> ", styles['rc-aawp-main-content']),
                        Paragraph(
                            """                            
                            3649 BUFORD HWY NE APT E6 <br />
                            BROOKHAVEN, GA 30329-1137
                            """, 
                            styles['rc-aawp-main-content']
                        ),
                        None, None
                    ],
                    [
                        Paragraph("<b>DATE OF ARREST:</b> 10/17/2016", styles['rc-aawp-main-content']),
                        None,
                        Paragraph("<b>WARRANT ISSUED:</b> {}".format(TEST_DATA), styles['rc-aawp-main-content']),
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("TOPPADDING", (0, 0), (-1, -1), 1.2 * mm),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 1.2 * mm),
                    ("SPAN", (0, 0), (3, 0)),
                    ("SPAN", (0, 2), (1, 2)),
                    ("SPAN", (2, 2), (3, 2)),
                    ("SPAN", (0, 3), (1, 3)),
                    ("SPAN", (2, 3), (3, 3)),
                    ("SPAN", (1, 4), (3, 4)),
                    ("SPAN", (0, 5), (1, 5)),
                    ("SPAN", (2, 5), (3, 5)),
                ]),                
                colWidths=(45*mm, 45*mm, 45*mm, 45*mm)
            ),
            Spacer(0, 4.2*mm),
        ]
        violation_table = [
            [
                Paragraph("<b>Ticket #</b>", styles['rc-aawp-main-content']),
                Paragraph("<b>Statute</b>", styles['rc-aawp-main-content']),
                Paragraph("<b>Charge Description</b>", styles['rc-aawp-main-content']),
                Paragraph("<b>Bond Amount</b>", styles['rc-aawp-main-content']),
                Paragraph("<b>Disposition</b>", styles['rc-aawp-main-content']),
            ]
        ]
        violation_arr = [
            {
                "Ticket #" : "E31415",
                "Statute" : "40-6-48 ",
                "Charge Description" : "FAILURE TO MAINTAIN LANE-1ST",
                "Bond Amount" : "",
                "Disposition" : "Pled Guilty"
            },{
                "Ticket #" : "E31416",
                "Statute" : "40-5-20",
                "Charge Description" : "DRIVING WITHOUT A VALID LICENSE-1ST",
                "Bond Amount" : "",
                "Disposition" : "Pled Guilty"
            },{
                "Ticket #" : "E31417",
                "Statute" : "10-6-391a'",
                "Charge Description" : "DUI-ALCOHOL-LESS SAFE-1ST",
                "Bond Amount" : "",
                "Disposition" : "Pled Guilty"
            },{
                "Ticket #" : "E62869",
                "Statute" : "18-11",
                "Charge Description" : "PUBLIC INTOXICATION AND PUBLIC CONSUMF",
                "Bond Amount" : "",
                "Disposition" : "Pled Guilty"
            },{
                "Ticket #" : "E62870",
                "Statute" : "40-6-92",
                "Charge Description" : "CROSSING ROADWAY ELSEWHERE THAN AT",
                "Bond Amount" : "",
                "Disposition" : "Pled Guilty"
            },{
                "Ticket #" : "E62869",
                "Statute" : "9-7",
                "Charge Description" : "FAILURE TO APPEAR",
                "Bond Amount" : "",
                "Disposition" : "Pled Guilty"
            }
        ]
        for idx, violation in enumerate(violation_arr):
            violation_table.append(
                [
                    Paragraph(violation["Ticket #"], styles['rc-aawp-main-content']),
                    Paragraph(violation["Statute"], styles['rc-aawp-main-content']),
                    Paragraph(violation["Charge Description"], styles['rc-aawp-main-content']),
                    Paragraph(violation["Bond Amount"], styles['rc-aawp-main-content']),
                    Paragraph(violation["Disposition"], styles['rc-aawp-main-content']),
                ]
            )  
        elems +=[
            Table(
                violation_table,
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("GRID", (0, 0), (-1, -1),  .1, "black"),
                    ("TOPPADDING", (0, 0), (-1, -1), 1.8 * mm),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 1.8 * mm),
                    ("LEFTPADDING", (0, 0), (-1, -1), 1.8 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 1.8 * mm),
                ]),
                colWidths=(25*mm, 25*mm, 85*mm, 30*mm, 30*mm)
            ),
            Spacer(0, 5*mm),
            Table(
                [   
                    [
                        Paragraph("<b>PROBATION:</b> {}".format(TEST_DATA), styles['rc-aawp-main-content']),
                        Paragraph("<b>END DATE:</b> {}".format(TEST_DATA), styles['rc-aawp-main-content']),
                    ],
                    [
                        Paragraph("<b>WITH:</b> {}".format(TEST_DATA), styles['rc-aawp-main-content']),
                        Paragraph("<b>OFFICIAL TAKING PRINTS:</b> {}".format(TEST_DATA), styles['rc-aawp-main-content']),
                    ],
                    [
                        Paragraph("<b>OTN:</b> {}".format(TEST_DATA), styles['rc-aawp-main-content']),
                        Paragraph("<b>DATE:</b> {}".format(TEST_DATA), styles['rc-aawp-main-content'])
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("TOPPADDING", (0, 0), (-1, -1), 1.2 * mm),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 1.2 * mm),
                ]),
                colWidths=(90*mm, 90*mm)
            ),
            Spacer(0, 4.2*mm),
            Paragraph("<b>***Finger Prints WILL NOT be taken without valid Photo ID***</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_CENTER)),
            Spacer(0, 4.2*mm),
            Table(
                [   
                    [
                        Paragraph("Clerk Name", extend_style(styles['rc-aawp-main-content'], fontSize=12)),
                        Paragraph("Clerk Signature", extend_style(styles['rc-aawp-main-content'], fontSize=12)),
                    ],
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]),
                colWidths=(140*mm, 50*mm)
            ),
        ]
        
        return elems