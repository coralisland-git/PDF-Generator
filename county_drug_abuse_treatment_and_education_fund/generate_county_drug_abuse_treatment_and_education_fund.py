import cStringIO

from document_specific_styles import *
from common.signatures import *
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT


def generate_county_drug_abuse_treatment_and_education_fund():
    cr = CDATEFReport()
    buff = cStringIO.StringIO()
    return cr.create_report(buff)


class CDATEFReport:
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
                                        """
                                        COUNTY DRUG ABUSE TREATMENT AND EDUCATION FUND 
                                        REMITTANCE REPORT
                                        """,
                                        styles["rc-doc-header"]
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
                        Paragraph("""
                            <b>PLEASE MAIL ALL REPORTS TO:</b> <br />
                            DeKalb County Finance Dept <br />
                            Attn: Hyacinth Robinson <br />
                            1300 Commerce Drive <br />
                            Decatur, GA 30030
                            """, 
                            extend_style(styles['rc-aawp-main-content'])
                        ),
                        Paragraph("""
                            <b>CITY REPORTING:</b> BROOKHAVEN <br />
                            <b>COUNTY:</b> DEKALB <br />
                            <b>TIME PERIOD FOR REPORT:</b> June 2019
                            """, 
                            extend_style(styles['rc-aawp-main-content'])
                        )
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
                colWidths=(100*mm, 80*mm)
            ),
            Spacer(0, 6.4*mm),
            Table(
                [
                    [
                        Paragraph("Number of cases with complete payments", extend_style(styles['rc-aawp-main-content'])),
                        Paragraph("3", extend_style(styles['rc-aawp-main-content'], alignment=TA_CENTER)),
                    ],[
                        Paragraph("Amount of fines assessed", extend_style(styles['rc-aawp-main-content'])),
                        Paragraph("1,176.48", extend_style(styles['rc-aawp-main-content'], alignment=TA_CENTER)),
                    ],[
                        Paragraph("Additional Penalty per Code Section 15-21-101", extend_style(styles['rc-aawp-main-content'])),
                        Paragraph("50% OF BASE-FINE", extend_style(styles['rc-aawp-main-content'], alignment=TA_CENTER)),
                    ],[
                        Paragraph("Amount of funds collected", extend_style(styles['rc-aawp-main-content'])),
                        Paragraph("588.24", extend_style(styles['rc-aawp-main-content'], alignment=TA_CENTER)),
                    ],[
                        Paragraph("", extend_style(styles['rc-aawp-main-content'])),
                        Paragraph("", extend_style(styles['rc-aawp-main-content'], alignment=TA_CENTER)),
                    ],[
                        Paragraph("Partial-Payments: number of cases", extend_style(styles['rc-aawp-main-content'])),
                        Paragraph("3", extend_style(styles['rc-aawp-main-content'], alignment=TA_CENTER)),
                    ],[
                        Paragraph("Partial-Payments: amount of funds collected", extend_style(styles['rc-aawp-main-content'])),
                        Paragraph("299.20", extend_style(styles['rc-aawp-main-content'], alignment=TA_CENTER)),
                    ],[
                        Paragraph("Amount Collected and Remitted for this Fund", extend_style(styles['rc-aawp-main-content'])),
                        Paragraph("887.44", extend_style(styles['rc-aawp-main-content'], alignment=TA_CENTER)),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("GRID", (0, 0), (-1, -1),  .1, "black"),
                    ("TOPPADDING", (0, 0), (-1, -1), 1.4 * mm),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 1.4 * mm),
                    ("LEFTPADDING", (0, 0), (-1, -1), 1.4 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 1.4 * mm),
                ]),
                colWidths=(130*mm, 60*mm)
            ),
            Spacer(0, 6.4*mm),
            Table(
                [
                    [
                        Paragraph("<b>Report Prepared by:</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("Test Data", extend_style(styles['rc-aawp-main-content'])),
                    ],[
                        Paragraph("<b>Date Prepared:</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("07/18/2019", extend_style(styles['rc-aawp-main-content'])),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEBELOW", (1, 0), (1, 0), 0.1, "black"),
                    ("LINEBELOW", (1, 1), (1, 1), 0.1, "black"),
                    ("TOPPADDING", (0, 0), (-1, -1), 2.8 * mm),
                    ("LEFTPADDING", (0, 0), (-1, -1), 1.4 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 1.4 * mm),
                ]),
                colWidths=(50*mm, 130*mm)
            ),
            Spacer(0, 6.4*mm),
            Paragraph("I certify that the above report is correct and complete to the best of my knowledge.", extend_style(styles['rc-aawp-main-content'], leftIndent=8*mm)),
            Spacer(0, 9.8*mm),
            Table(
                [
                    [
                        Paragraph("Court Clerk's Signature", extend_style(styles['rc-aawp-main-content']))
                    ]                
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEABOVE", (0, 0), (0, 0), 0.1, "black"),                    
                    ("TOPPADDING", (0, 0), (-1, -1), .8 * mm),
                ]),
                colWidths=(180*mm)
            ),
            Spacer(0, 6.4*mm),
            Table(
                [
                    [
                        Paragraph("<b>Check Number:</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("Test Data", extend_style(styles['rc-aawp-main-content'])),
                        None
                    ],[
                        Paragraph("<b>Date Prepared:</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT)),
                        Paragraph("887.44", extend_style(styles['rc-aawp-main-content'])),
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEBELOW", (1, 0), (1, 0), 0.1, "black"),
                    ("LINEBELOW", (1, 1), (1, 1), 0.1, "black"),
                    ("TOPPADDING", (0, 0), (-1, -1), 2.8 * mm),
                    ("LEFTPADDING", (0, 0), (-1, -1), 1.4 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 1.4 * mm),
                ]),
                colWidths=(30*mm, 25*mm, 125*mm)
            ),
            Spacer(0, 6.4*mm),
            Paragraph("""
                Note: In every case in which any court shall impose a fine, which shall be construed to include costs, 
                for any offense prohibited by Code Section 16-13-30, 16-13-30.1, or 16-13-31, which offenses relate to certain 
                activities regarding marijuana, controlled substances, and non-controlled substances, there shall be imposed as 
                an additional penalty a sum equal to 50 percent of the original fine. This report is based on all payments 
                (partial or full) made to the court during the reporting period that applies to the DATE fund.
                """, 
                extend_style(styles['rc-aawp-main-content'], leftIndent=8*mm, rightIndent=8*mm)
            )
        ]
        
        return elems