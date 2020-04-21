import cStringIO

from common.signatures import *
from document_specific_styles import *
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT


def generate_general_notice():
    cr = GCReport()
    buff = cStringIO.StringIO()
    return cr.create_report(buff)


class GCReport:
    def __init__(self, title=None, author=None):
        self.page_size = letter
        self.page_margin = (9.4 * mm, 7.8 * mm)
        self.sections = ["content",]
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
                "Page "+str(doc.page)+" of 1",
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
                                        GENERAL NOTICE <br />
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
            Paragraph(
                """
                <b>Case Number:</b> E31415                
                """, 
                extend_style(styles['rc-aawp-main-content'],  alignment=TA_CENTER)
            ),
            Spacer(0, 6.4*mm),
            Paragraph(
                """
                <b>
                STATE OF GEORGIA <br />
                CITY OF BROOKHAVEN
                </b> <br />
                VS. <br />
                <b>
                JUAN URIEL MELENDEZ HERRERA
                </b>
                """,
                extend_style(styles["rc-aawp-main-header"], alignment=TA_LEFT, leftIndent=10, rightIndent=10)
            ),
            Paragraph(
                """
                <b>Court Date:</b> <u>&nbsp;&nbsp;{}&nbsp;&nbsp;</u> at <u>&nbsp;&nbsp;{}&nbsp;&nbsp;</u> <br />
                <b>Charge:</b> FAILURE TO MAINTAIN LANE-1ST
                """.format(TEST_DATA, TEST_DATA), 
                extend_style(styles['rc-aawp-main-content'], leftIndent=30, rightIndent=10)
            ),
            Spacer(0, 14.4*mm),
            Table(
                [
                    [
                        None,
                        Paragraph("<b>SARCHER</b>", extend_style(styles['rc-aawp-main-content']))
                    ]  ,
                    [
                        None,
                        Paragraph("Court Clerk / Deputy Court Clerk", extend_style(styles['rc-aawp-main-content']))
                    ]                
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEABOVE", (1, 1), (1, 1), 0.1, "black"),                    
                    ("TOPPADDING", (0, 0), (-1, -1), .4 * mm),
                ]),
                colWidths=(100*mm, 90*mm)
            ),
            Spacer(0, 14.4*mm),
            Paragraph(
                """ <b>
                Case #: E31415 <br />
                JUAN URIEL MELENDEZ HERRERA <br />
                3649 BUFORD HWY NE <br />
                BROOKHAVEN, GA 30329-1134
                </b>
                """, 
                extend_style(styles['rc-aawp-main-content'], leftIndent=10, rightIndent=10)
            ),
            PageBreak()
        ]
        
        return elems
