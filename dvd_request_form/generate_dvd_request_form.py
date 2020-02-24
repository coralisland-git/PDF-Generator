import cStringIO

from document_specific_styles import *
from common.signatures import *


def generate_dvd_request_form():
    cr = DRFReport()
    buff = cStringIO.StringIO()
    return cr.create_report(buff)


class DRFReport:
    def __init__(self, title=None, author=None):
        self.page_size = letter
        self.page_margin = (24.4 * mm, 18.4 * mm)
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
        line_styles = []
        for idx in range(0, 11):
            line_styles += [
                ("LINEBELOW", (1, idx), (1, idx), 0.1, "black")
            ]
        elems += [
            Spacer(0, 9.8 * mm),
            Paragraph(
                "<u>BROOKHAVEN MUNICIPAL COURT</u>",
                styles["rc-doc-header"]
            ),
            Paragraph(
                """
                    2665 BUFORD HIGHWAY <br />
                    BROOKHAVEN, GEORGIA 30324 <br />
                    404-637-0660 
                """,
                styles["rc-doc-header-sub"]
            ),
            Paragraph(
                "<u>COURT PBROOKHAVENGA.GOV</u>",
                extend_style(styles["rc-doc-header-sub"], spaceBefore=2)
            ),
            Paragraph(
                "<u>GSP VIDEO/DVD REQUEST FORM</u>",
                extend_style(styles["rc-doc-header"], spaceBefore=30)
            ),
            Spacer(0, 2.4 * mm),
            Table(
                [
                    [
                        Paragraph("Defendant:", styles["rc-aawp-main-content"]),
                        Paragraph("Test Data", styles["rc-aawp-main-content"]),
                        None
                    ],
                    [
                        Paragraph("Citation Number(s):", styles["rc-aawp-main-content"]),
                        Paragraph("Test Data", styles["rc-aawp-main-content"]),
                    ],
                    [
                        Paragraph("Arresting Officer:", styles["rc-aawp-main-content"]),
                        Paragraph("Test Data", styles["rc-aawp-main-content"]),
                        None
                    ],
                    [
                        Paragraph("Date/Time of Arrest:", styles["rc-aawp-main-content"]),
                        Paragraph("Test Data", styles["rc-aawp-main-content"]),
                        None
                    ],
                    [
                        Paragraph("Location of Arrest:", styles["rc-aawp-main-content"]),
                        Paragraph("Test Data", styles["rc-aawp-main-content"]),
                        None
                    ],
                    [
                        Paragraph("Color/Model of Vehicle:", styles["rc-aawp-main-content"]),
                        Paragraph("Test Data", styles["rc-aawp-main-content"]),
                        None
                    ],
                    [
                        Paragraph("Person Requesting Video:", styles["rc-aawp-main-content"]),
                        Paragraph("Test Data", styles["rc-aawp-main-content"]),
                        None
                    ],
                    [    
                        Paragraph("Address:", extend_style(styles["rc-aawp-main-content"], leftIndent=13.2*mm)),
                        Paragraph("1 Test Dr. Apt. 123, Testcity, XX 12345", styles["rc-aawp-main-content"]),
                        None
                    ],
                    [
                        Paragraph("", styles["rc-aawp-main-content"]),
                        Paragraph("1 Test Dr. Apt. 123, Testcity, XX 12345", styles["rc-aawp-main-content"]),
                        None
                    ],
                    [
                        Paragraph("", styles["rc-aawp-main-content"]),
                        Paragraph("1 Test Dr. Apt. 123, Testcity, XX 12345", styles["rc-aawp-main-content"]),
                        None
                    ],
                    [
                        Paragraph("Phone Number:", extend_style(styles["rc-aawp-main-content"], leftIndent=13.2*mm)),
                        Paragraph("Test Data", styles["rc-aawp-main-content"]),
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], line_styles),
                colWidths=(53*mm, 105*mm, 9*mm),
                rowHeights=7.8*mm
            ),
            Spacer(0, 10.4 * mm),
            Table(
                [
                    [
                        Paragraph("Date of Request:", styles["rc-aawp-main-content"]),
                        Paragraph("Test Data", styles["rc-aawp-main-content"]),
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (1, 0), (1, 0), 0.1, "black"),
                ]),
                colWidths=(38*mm, 120*mm, 9*mm)
            ),
            Spacer(0, 8.4 * mm),
            Table(
                [
                    [
                        Paragraph(
                            """
                            Please be advised that GSP charges $33.50 (VHS) and $11.14 (DVD). Please call GSP prior to 
                            sending payment to determine format and cost of the arrest video. Mail form and check to : 
                            GSP, ATTN: Open Records, P.O. Box 1456, Atlanta, GA 30371. Phone number is 404-624-7591
                            """, 
                            styles["rc-aawp-main-content"])
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (0, 0), (0, 0), 1.4, "black"),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), .75 * mm)
                ]),                
            ),
            Paragraph("Approved by:", extend_style(styles["rc-aawp-main-content"], spaceBefore=16)),
            Spacer(0, 10.4 * mm),
            Table(
                [
                    [
                        Paragraph("Solicitor, Brookhaven Municipal Court", styles["rc-aawp-main-content"]),
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEABOVE", (0, 0), (0, 0), 0.1, "black"),
                    ("TOPPADDING", (0, 0), (-1, -1), .75 * mm)
                ]),
                colWidths=(65*mm, 102*mm,)
            ),
        ]
        
        return elems
