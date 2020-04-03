import cStringIO

from common.signatures import *
from document_specific_styles import *
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT


def generate_bkh_bench_warrant():
    cr = BBWReport()
    buff = cStringIO.StringIO()
    return cr.create_report(buff)


class BBWReport:
    def __init__(self, title=None, author=None):
        self.page_size = letter
        self.page_margin = (9.4 * mm, 7.8 * mm)
        self.sections = ["content", "content_2"]
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
                "Page "+str(doc.page)+" of 2",
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
                                        """
                                        BENCH WARRANT <br />
                                        """,
                                        styles["rc-doc-header"]
                                    )
                                ],
                                [
                                    Paragraph(
                                        """
                                        <b>
                                        STATE OF GEORGIA <br />
                                        DEKALB COUNTY
                                        </b>
                                        """,
                                        styles["rc-aawp-main-header"]
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
                colWidths=(42*mm, 112*mm, 43*mm),
            ),
            Spacer(0, 6.4*mm),
            Paragraph("<b>AFFIDAVIT</b>", 
                extend_style(styles['rc-aawp-main-header'], fontSize=10)
            ),
            Paragraph(
                """
                <b>Case Number:</b> E50082 &nbsp;&nbsp;&nbsp;&nbsp;
                <b>Warrant Number:</b> E50082
                """, 
                extend_style(styles['rc-aawp-main-content'],  alignment=TA_CENTER)
            ),
            Spacer(0, 3.2*mm),
            Paragraph(
                """
                Personally appeared the undersigned affiant who, being sworn on oath says COOPER, CHARLIE CLEVELAND
                """, 
                extend_style(styles['rc-aawp-main-content'], leftIndent=10, rightIndent=10)
            ),
            Table(
                [   
                    [
                        Paragraph("<b>SSN: </b> {}".format(TEST_DATA), extend_style(styles['rc-aawp-main-content'])),
                        Paragraph("<b>DOB: </b> 09/26/1962", extend_style(styles['rc-aawp-main-content'])),
                        Paragraph("<b>Sex: </b> Male", extend_style(styles['rc-aawp-main-content'])),
                        Paragraph("""<b>Height: </b> 5' 8" """, extend_style(styles['rc-aawp-main-content'])),
                    ],
                    [
                        Paragraph("<b>DL#: </b> GA 051513953", extend_style(styles['rc-aawp-main-content'])),
                        Paragraph("<b>Age: </b> 56", extend_style(styles['rc-aawp-main-content'])),
                        Paragraph("<b>Race: </b> Black", extend_style(styles['rc-aawp-main-content'])),
                        Paragraph("<b>Weight: </b> 170", extend_style(styles['rc-aawp-main-content'])),
                    ],
                    [
                        Paragraph("<b>Hair: </b> Black", extend_style(styles['rc-aawp-main-content'])),
                        Paragraph("<b>Eyes: </b> Brown", extend_style(styles['rc-aawp-main-content'])),
                        None, None
                    ],
                    [
                        Paragraph(
                            """
                            <b>Address: </b> 201 WASHINGTON ST SW
                            ATLANTA, GA 30303-3546
                            """, extend_style(styles['rc-aawp-main-content'])),
                        None, None, None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("SPAN", (0, 3), (3, 3))
                ]),
                colWidths=(47.5*mm, 47.5*mm, 47.5*mm, 47.5*mm),
                rowHeights=5.2*mm
            ),
            Paragraph(
                """
                accused herein, did commit the offense of FAILURE TO APPEAR in said jurisdiction on or about , as prohibited by City Ordinance 9-7.
                """, 
                extend_style(styles['rc-aawp-main-content'], leftIndent=10, rightIndent=10)
            ),
            Spacer(0, 3.2*mm),
            Paragraph(
                """
                <b>ORIGINATING VIOLATION:</b>
                """, 
                extend_style(styles['rc-aawp-main-content'], leftIndent=10, rightIndent=10)
            ),
            Spacer(0, 1.6*mm),
        ]
        item_table = []
        item_arr = [
            {
                "value": TEST_DATA,
            },
        ]
        for idx, item in enumerate(item_arr):
            item_table.append(
                [
                    Paragraph(item["value"], styles['rc-aawp-main-content']),
                ]
            )
        elems +=[
            Table(
                item_table,
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("GRID", (0, 0), (-1, -1),  .1, "black"),
                    ("TOPPADDING", (0, 0), (-1, -1), 1.4 * mm),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 1.4 * mm),
                    ("LEFTPADDING", (0, 0), (-1, -1), 1.4 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 1.4 * mm)                    
                ]),
                colWidths=(190*mm)
            ),
            Spacer(0, 9.6*mm),  
            Table(
                [
                    [
                        Paragraph("Affiant Signature", extend_style(styles['rc-aawp-main-content'])),
                        None
                    ]                
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEABOVE", (0, 0), (0, 0), 0.1, "black"),                    
                    ("TOPPADDING", (0, 0), (-1, -1), .4 * mm),
                ]),
                colWidths=(80*mm, 110*mm)
            ),
            Paragraph("""Sworn and subscribed before me this the 18th of July, 2019""", 
                extend_style(styles['rc-aawp-main-content'], leftIndent=10, rightIndent=10)
            ),
            Spacer(0, 12.8*mm),
            Table(
                [
                    [
                        Paragraph("Judge, BROOKHAVEN MUNICIPAL COURT", extend_style(styles['rc-aawp-main-content'])),
                        None
                    ]                
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEABOVE", (0, 0), (0, 0), 0.1, "black"),
                    ("TOPPADDING", (0, 0), (-1, -1), .4 * mm),
                ]),
                colWidths=(80*mm, 110*mm)
            ),
            Spacer(0, 3.2*mm),
            Paragraph("<b>BENCH WARRANT</b>", 
                extend_style(styles['rc-aawp-main-header'], fontSize=10)
            ),
            Spacer(0, 3.2*mm),
            Paragraph(
                """
                CITY OF BROOKHAVEN, DEKALB COUNTY: GEORGIA <br />
                To any duly authorized officer of DEKALB COUNTY, and to any Sheriff or his deputy, Coroner, 
                Constable, or Marshall of said State, GREETING: <br />
                Affiant, makes oath before me on the 18th of July, 2019 in the CITY and County aforesaid, 
                that the above named accused did commit the offense of FAILURE TO APPEAR as prohibited by City 
                Ordinance 9-7, the place of occurance being BROOKHAVEN, DEKALB COUNTY, for sufficient cause 
                made known to me in the above affidavit, incorporated by reference, and other sworn testimony 
                establishing probable cause for the arrest of the accused. You are therefore hereby commanded 
                to arrest the body of the said accused, based on probable cause provided by the affiant and bring 
                him / her before me or some other Judicial officer of this CITY to be dealt with as the law directs.
                <br /><br />
                Herein fail not. <br />
                This the 18th of July, 2019. <br />
                Release upon cash payment of bond in the amount of <b>$100.00</b>
                """, 
                extend_style(styles['rc-aawp-main-content'], leftIndent=10, rightIndent=10)
            ),
            Spacer(0, 12.8*mm),
            Table(
                [
                    [
                        Paragraph("Judge, BROOKHAVEN MUNICIPAL COURT", extend_style(styles['rc-aawp-main-content'])),
                        None
                    ]                
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEABOVE", (0, 0), (0, 0), 0.1, "black"),                    
                    ("TOPPADDING", (0, 0), (-1, -1), .4 * mm),
                ]),
                colWidths=(80*mm, 110*mm)
            ),
            PageBreak()
        ]
        
        return elems

    def _section_content_2(self):
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
                                        """
                                        BENCH WARRANT <br />
                                        """,
                                        styles["rc-doc-header"]
                                    )
                                ],
                                [
                                    Paragraph(
                                        """
                                        <b>
                                        STATE OF GEORGIA <br />
                                        DEKALB COUNTY
                                        </b>
                                        """,
                                        styles["rc-aawp-main-header"]
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
            Paragraph("<b>AFFIDAVIT</b>", 
                extend_style(styles['rc-aawp-main-header'], fontSize=10)
            ),
            Paragraph(
                """
                <b>Case Number:</b> E50082 &nbsp;&nbsp;&nbsp;&nbsp;
                <b>Warrant Number:</b> E50082
                """, 
                extend_style(styles['rc-aawp-main-content'],  alignment=TA_CENTER)
            ),
            Spacer(0, 3.2*mm),
            Paragraph(
                """
                Personally appeared the undersigned affiant who, being sworn on oath says COOPER, CHARLIE CLEVELAND
                """, 
                extend_style(styles['rc-aawp-main-content'], leftIndent=10, rightIndent=10)
            ),
            Table(
                [   
                    [
                        Paragraph("<b>SSN: </b> {}".format(TEST_DATA), extend_style(styles['rc-aawp-main-content'])),
                        Paragraph("<b>DOB: </b> 09/26/1962", extend_style(styles['rc-aawp-main-content'])),
                        Paragraph("<b>Sex: </b> Male", extend_style(styles['rc-aawp-main-content'])),
                        Paragraph("""<b>Height: </b> 5' 8" """, extend_style(styles['rc-aawp-main-content'])),
                    ],
                    [
                        Paragraph("<b>DL#: </b> GA 051513953", extend_style(styles['rc-aawp-main-content'])),
                        Paragraph("<b>Age: </b> 56", extend_style(styles['rc-aawp-main-content'])),
                        Paragraph("<b>Race: </b> Black", extend_style(styles['rc-aawp-main-content'])),
                        Paragraph("<b>Weight: </b> 170", extend_style(styles['rc-aawp-main-content'])),
                    ],
                    [
                        Paragraph("<b>Hair: </b> Black", extend_style(styles['rc-aawp-main-content'])),
                        Paragraph("<b>Eyes: </b> Brown", extend_style(styles['rc-aawp-main-content'])),
                        None, None
                    ],
                    [
                        Paragraph(
                            """
                            <b>Address: </b> 201 WASHINGTON ST SW
                            ATLANTA, GA 30303-3546
                            """, extend_style(styles['rc-aawp-main-content'])),
                        None, None, None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("SPAN", (0, 3), (3, 3))
                ]),
                colWidths=(47.5*mm, 47.5*mm, 47.5*mm, 47.5*mm),
                rowHeights=5.2*mm
            ),
            Paragraph(
                """
                accused herein, did commit the offense of FAILURE TO APPEAR in said jurisdiction on or about 09/13/2018, as prohibited by City Ordinance 9-7.
                """, 
                extend_style(styles['rc-aawp-main-content'], leftIndent=10, rightIndent=10)
            ),
            Spacer(0, 3.2*mm),
            Paragraph(
                """
                <b>ORIGINATING VIOLATION:</b>
                """, 
                extend_style(styles['rc-aawp-main-content'], leftIndent=10, rightIndent=10)
            ),
               Spacer(0, 1.6*mm),
        ]
        item_table = []
        item_arr = [
            {
                "value": "Ticket: E50082, 08/09/2018, 18-4: SHOPLIFTING LESS THAN $500-1ST",
            },
        ]
        for idx, item in enumerate(item_arr):
            item_table.append(
                [
                    Paragraph(item["value"], styles['rc-aawp-main-content']),
                ]
            )
        elems +=[
            Table(
                item_table,
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("GRID", (0, 0), (-1, -1),  .1, "black"),
                    ("TOPPADDING", (0, 0), (-1, -1), 1.4 * mm),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 1.4 * mm),
                    ("LEFTPADDING", (0, 0), (-1, -1), 1.4 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 1.4 * mm)                    
                ]),
                colWidths=(190*mm)
            ),
            Spacer(0, 9.6*mm),
            Table(
                [
                    [
                        Paragraph("Affiant Signature", extend_style(styles['rc-aawp-main-content'])),
                        None
                    ]                
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEABOVE", (0, 0), (0, 0), 0.1, "black"),                    
                    ("TOPPADDING", (0, 0), (-1, -1), .4 * mm),
                ]),
                colWidths=(80*mm, 110*mm)
            ),
            Paragraph("""Sworn and subscribed before me this the 26th of July, 2018""", 
                extend_style(styles['rc-aawp-main-content'], leftIndent=10, rightIndent=10)
            ),
            Spacer(0, 12.8*mm),
            Table(
                [
                    [
                        Paragraph("Judge, BROOKHAVEN MUNICIPAL COURT", extend_style(styles['rc-aawp-main-content'])),
                        None
                    ]                
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEABOVE", (0, 0), (0, 0), 0.1, "black"),
                    ("TOPPADDING", (0, 0), (-1, -1), .4 * mm),
                ]),
                colWidths=(80*mm, 110*mm)
            ),
            Spacer(0, 3.2*mm),
            Paragraph("<b>BENCH WARRANT</b>", 
                extend_style(styles['rc-aawp-main-header'], fontSize=10)
            ),
            Spacer(0, 3.2*mm),
            Paragraph(
                """
                CITY OF BROOKHAVEN, DEKALB COUNTY: GEORGIA <br />
                To any duly authorized officer of DEKALB COUNTY, and to any Sheriff or his deputy, Coroner, 
                Constable, or Marshall of said State, GREETING: <br />
                Affiant, makes oath before me on the 26th of July, 2018 in the CITY and County aforesaid, 
                that the above named accused did commit the offense of FAILURE TO APPEAR as prohibited by City 
                Ordinance 9-7, the place of occurance being BROOKHAVEN, DEKALB COUNTY, for sufficient cause 
                made known to me in the above affidavit, incorporated by reference, and other sworn testimony 
                establishing probable cause for the arrest of the accused. You are therefore hereby commanded 
                to arrest the body of the said accused, based on probable cause provided by the affiant and bring 
                him / her before me or some other Judicial officer of this CITY to be dealt with as the law directs.
                <br /><br />
                Herein fail not. <br />
                This the 26th of July, 2018. <br />
                Release upon cash payment of bond in the amount of <b>$450.00</b>
                """, 
                extend_style(styles['rc-aawp-main-content'], leftIndent=10, rightIndent=10)
            ),
            Spacer(0, 12.8*mm),
            Table(
                [
                    [
                        Paragraph("Judge, BROOKHAVEN MUNICIPAL COURT", extend_style(styles['rc-aawp-main-content'])),
                        None
                    ]                
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEABOVE", (0, 0), (0, 0), 0.1, "black"),                    
                    ("TOPPADDING", (0, 0), (-1, -1), .4 * mm),
                ]),
                colWidths=(80*mm, 110*mm)
            ),
            PageBreak()
        ]
        
        return elems
