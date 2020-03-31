import cStringIO

from common.signatures import *
from document_specific_styles import *
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT


def generate_license_suspension_notice():
    cr = LSNReport()
    buff = cStringIO.StringIO()
    return cr.create_report(buff)


class LSNReport:
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
                                        LICENSE SUSPENSION NOTICE <br />
                                        """,
                                        styles["rc-doc-header"]
                                    )
                                ],
                                [
                                    Paragraph(
                                        """
                                        <b>
                                        STATE OF GEORGIA <br />
                                        CITY OF BROOKHAVEN </b>
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
             Table(
                [   
                    [
                        Paragraph("""
                            <b>TO:</b>
                            """, 
                            extend_style(styles['rc-aawp-main-content'])
                        ),
                        Paragraph("""
                            MICKEY MOUSE <br />
                            1234 DISNEY WAY <br />
                            BROOKHAVEN, GA 30319
                            """, 
                            extend_style(styles['rc-aawp-main-content'])
                        ),
                        Paragraph(
                            """
                            Court Clerk <br />
                            BROOKHAVEN MUNICIPAL COURT  <br />
                            BROOKHAVEN, GA 30324 <br />
                            404-637-0660
                            """, extend_style(styles['rc-aawp-main-content'])
                        ),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
                colWidths=(10*mm, 90*mm, 80*mm)
            ),
            Spacer(0, 6.4*mm),
            Paragraph(
                """
                You are hereby notified that you have one or more citations overdue in this court. Failure to pay this fine 
                (by cash or money-order) WILL RESULT IN YOUR LICENSE BEING SUSPENDED. <br />
                Please respond within 30 days from the NOTICE DATE above to avoid suspension of your license. <br />
                Sincerely,
                """, 
                extend_style(styles['rc-aawp-main-content'], leftIndent=30, rightIndent=30)
            ),
            Spacer(0, 6.4*mm),
        ]
        item_table = [
            [
                Paragraph("<b>Ticket Date</b>", styles['rc-aawp-main-content']),
                Paragraph("<b>Ticket #</b>", styles['rc-aawp-main-content']),
                Paragraph("<b>Statute</b>", styles['rc-aawp-main-content']),
                Paragraph("<b>Violation(s)</b>", styles['rc-aawp-main-content']),
                Paragraph("<b>Court Date</b>", styles['rc-aawp-main-content']),
                Paragraph("<b>Balance</b>", styles['rc-aawp-main-content']),
            ]
        ]
        item_arr = [
            {
                "Ticket Date": "06/20/2018",
                "Ticket #": "1234TEST",
                "Statute": "40-8-51",
                "Violation(s)": "DEFECTIVE BRAKES (40-8-51)-1ST",
                "Court Date": "07/21/2018",
                "Balance": "$923.00",
            }
        ]
        for idx, item in enumerate(item_arr):
            item_table.append(
                [
                    Paragraph(item["Ticket Date"], styles['rc-aawp-main-content']),
                    Paragraph(item["Ticket #"], styles['rc-aawp-main-content']),
                    Paragraph(item["Statute"], styles['rc-aawp-main-content']),
                    Paragraph(item["Violation(s)"], styles['rc-aawp-main-content']),
                    Paragraph(item["Court Date"], styles['rc-aawp-main-content']),
                    Paragraph(item["Balance"], styles['rc-aawp-main-content']),                    
                ]
            )
        item_table.append(
            [None, None, None, None, None, None]
        )
        item_table.append(
            [
                Paragraph("<b>Total</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_RIGHT, rightIndent=20)), None, None, None, None,
                Paragraph("$923.00", styles['rc-aawp-main-content'])                
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
                    ("RIGHTPADDING", (0, 0), (-1, -1), 1.4 * mm),
                    ("SPAN", (0, -2), (5, -2)),
                    ("SPAN", (0, -1), (4, -1)),
                ]),
                colWidths=(25*mm, 25*mm, 25*mm, 65*mm, 25*mm, 25*mm)
            )
        ]
        
        return elems