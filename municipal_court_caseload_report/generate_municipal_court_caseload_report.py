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
                                        """
                                        BROOKHAVEN MUNICIPAL COURT <br />
                                        Municipal Court Caseload Report
                                        """, 
                                        styles["rc-doc-header"]
                                    )
                                ],
                                [
                                    Paragraph(
                                        """
                                        CASE COUNTS FOR: 06/01/2019 - 06/30/2019
                                        """,
                                        extend_style(styles["rc-aawp-main-content"], fontSize=12, alignment=TA_CENTER)
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
            Paragraph("""
                Notes: <br />
                (1) Cases Open: A count of cases that, at the start of the reporting period, are awaiting disposition <br />
                (2) Cases Filed: A count of cases that have been filed with the court for the first time during the reporting period. <br />
                (3) Cases Disposed: A count of cases for which an original entry of judgment has been entered during the reporting period. <br />
                """, 
                extend_style(styles['rc-aawp-main-content'], leftIndent=20)
            ),
            Spacer(0, 4.2*mm),
        ]
        violation_table = [
            [
                Paragraph("", styles['rc-aawp-main-content']),
                Paragraph("<b>Cases Open</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_CENTER)),
                Paragraph("<b>Cases Filed</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_CENTER)),
                Paragraph("<b>Cases Disposed</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_CENTER)),
                Paragraph("<b>Bindover</b>", extend_style(styles['rc-aawp-main-content'], alignment=TA_CENTER)),
            ]
        ]
        violation_arr = [
            {
                "Ticket" : "SERIOUS TRAFFIC - DUI",
                "Cases Open" : "55",
                "Cases Filed" : "13",
                "Cases Disposed" : "11",
                "Bindover" : "7"
            },
            {
                "Ticket" : "SERIOUS TRAFFIC - OTHER",
                "Cases Open" : "312",
                "Cases Filed" : "82",
                "Cases Disposed" : "67",
                "Bindover" : "15"
            },{
                "Ticket" : "MISDEMEANOR - TRAFFIC",
                "Cases Open" : "1215",
                "Cases Filed" : "430",
                "Cases Disposed" : "379",
                "Bindover" : "18"
            },{
                "Ticket" : "MISDEMEANOR - DRUG",
                "Cases Open" : "15",
                "Cases Filed" : "0",
                "Cases Disposed" : "0",
                "Bindover" : "0"
            },{
                "Ticket" : "MISDEMEANOR - OTHER",
                "Cases Open" : "511",
                "Cases Filed" : "83",
                "Cases Disposed" : "46",
                "Bindover" : "3"
            },{
                "Ticket" : "PARKING VIOLATION",
                "Cases Open" : "304",
                "Cases Filed" : "7",
                "Cases Disposed" : "10",
                "Bindover" : "0"
            },{
                "Ticket" : "ORDINANCE",
                "Cases Open" : "1050",
                "Cases Filed" : "26",
                "Cases Disposed" : "20",
                "Bindover" : "1"
            },{
                "Ticket" : "TOTAL",
                "Cases Open" : "3642",
                "Cases Filed" : "641",
                "Cases Disposed" : "533",
                "Bindover" : "44"
            }
        ]
        for idx, violation in enumerate(violation_arr):
            violation_table.append(
                [
                    Paragraph(violation["Ticket"], styles['rc-aawp-main-content']),
                    Paragraph(violation["Cases Open"], extend_style(styles['rc-aawp-main-content'], alignment=TA_CENTER)),
                    Paragraph(violation["Cases Filed"], extend_style(styles['rc-aawp-main-content'], alignment=TA_CENTER)),
                    Paragraph(violation["Cases Disposed"], extend_style(styles['rc-aawp-main-content'], alignment=TA_CENTER)),
                    Paragraph(violation["Bindover"], extend_style(styles['rc-aawp-main-content'], alignment=TA_CENTER)),
                ]
            )  
        elems +=[
            Table(
                violation_table,
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("GRID", (0, 0), (-1, -1),  .1, "black"),
                    ("TOPPADDING", (0, 0), (-1, -1), 1.4 * mm),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 1.4 * mm),
                    ("LEFTPADDING", (0, 0), (-1, -1), 1.4 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 1.4 * mm),
                ]),
                colWidths=(70*mm, 30*mm, 30*mm, 30*mm, 30*mm)
            )
        ]
        
        return elems