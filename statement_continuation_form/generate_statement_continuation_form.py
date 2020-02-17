import cStringIO

from document_specific_styles import *
from common.signatures import *
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT


def generate_statement_continuation_form():
    cr = ORFReport()
    buff = cStringIO.StringIO()
    return cr.create_report(buff)


class ORFReport:
    def __init__(self, title=None, author=None):
        self.page_size = letter
        self.page_margin = (12.4 * mm, 12.4 * mm)
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
            Table(
                [
                    [
                        Image('brookhaven.jpg', 42 * mm, 15 * mm),
                        Table(
                            [
                                [
                                    Paragraph(
                                        "BROOKHAVEN POLICE DEPARTMENT",
                                        styles["rc-doc-header-scf"],
                                    ),
                                ],
                                [
                                    Paragraph(
                                        "STATEMENT CONTINUATION FORM",
                                        extend_style(styles["rc-doc-header-scf"], fontSize=13.5, leading=14),
                                    )
                                ]
                            ],
                            style=styles["rc-main-table"]
                        )
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("ALIGN", (0, 0), (0, 0), "RIGHT"),
                    ("RIGHTPADDING", (0, 0), ( 0, 0), 7 * mm )
                ]),                
                colWidths=(48*mm, 132*mm)
            ),
            Spacer(0, .8 * mm),
            Paragraph(
                "PAGE &nbsp;"+"_"*6+" &nbsp;&nbsp; OF &nbsp;&nbsp; "+"_"*6,
                extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER, spaceBefore=20, leftIndent=22),
            )
        ]
        for idx in range(0, 22):
            elems.append(
                Paragraph("_"*103, styles["rc-aawp-main-content"]),
            )
        elems +=[
            Spacer(0, 12.8 * mm),
            Table(
                [
                    [
                        Paragraph(
                            "PERSON MAKING STATEMENT SIGNATURE",
                            styles["rc-aawp-main-content-tb"],
                        ),
                        None,
                        Paragraph(
                            "TODAY'S DATE & TIME",
                            styles["rc-aawp-main-content-tb"],
                        ),
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEABOVE", (0, 0), (0, 0), 0.1, "black"),
                    ("LINEABOVE", (2, 0), (2, 0), 0.1, "black"),
                    ("LEFTPADDING", (0, 0), ( -1, -1), 1.6 * mm )
                ]),
                colWidths=(76*mm, 10*mm, 68*mm, 36*mm)
            ),
            Spacer(0, 6.4 * mm),
            Table(
                [
                    [
                        Paragraph(
                            "OFFICER'S SIGNATURE",
                            styles["rc-aawp-main-content-tb"],
                        ), None,
                        Paragraph(
                            "BADGE #",
                            styles["rc-aawp-main-content-tb"],
                        ), None,
                        Paragraph(
                            "CASE NUMBER",
                            styles["rc-aawp-main-content-tb"],
                        ), None                 
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEABOVE", (0, 0), (0 , 0), 0.1, "black"),
                    ("LINEABOVE", (2, 0), (2, 0), 0.1, "black"),
                    ("LINEABOVE", (4, 0), (4, 0), 0.1, "black"),
                    ("LEFTPADDING", (0, 0), ( -1, -1), 1.6 * mm )
                ]),
                colWidths=(55*mm, 5*mm, 48*mm, 5*mm, 60*mm, 17*mm)
            )
        ]
        
        return elems
