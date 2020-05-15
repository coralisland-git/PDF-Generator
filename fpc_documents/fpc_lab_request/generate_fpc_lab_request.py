# -*- coding: utf-8 -*-
import cStringIO
from common.signatures import *
from reportlab.platypus.flowables import HRFlowable, PageBreak
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from document_specific_styles import *


def generate_fpc_lab_request(title=None, author=None):
    cr = FPCLR(title, author)
    buff = cStringIO.StringIO()
    return cr.create_report(buff)


class FPCLR:
    def __init__(self, title=None, author=None):
        self.page_size = letter
        self.page_margin = (14.4 * mm, 18.4 * mm)
        self.sections = ["header", "content"]
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

    def _section_header(self):
        elems = [
            Table(
                [
                    [
                        Image('logo.jpg', 19.5 * mm, 24* mm),
                        Paragraph(
                            """
                            FOREST PRESERVES OF COOK COUNTY <br />
                            POLICE DEPARTMENT
                            """,
                            styles["rc-doc-header"]
                        ),
                        Paragraph("(date)", extend_style(styles["rc-aawp-main-date"], alignment=TA_RIGHT)),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
                colWidths=(25*mm, 138*mm, 25*mm)
            ),
        ]        
        return elems

    def _section_content(self):        
        table = [
            [
                Paragraph("FROM", styles["rc-aawp-main-content-tb"]),
                Paragraph("TO", styles["rc-aawp-main-content-tb"]),
                Paragraph("DATE", styles["rc-aawp-main-content-tb"]),
                Paragraph("TIME", styles["rc-aawp-main-content-tb"])
            ],
        ]
        for idx in range(10):
            table.append([
                Paragraph("", styles["rc-aawp-main-content-tb"]),
                Paragraph("", styles["rc-aawp-main-content-tb"]),
                Paragraph("", styles["rc-aawp-main-content-tb"]),
                Paragraph("", styles["rc-aawp-main-content-tb"])
            ])
        elems = [
            Spacer(0, -3.4 * mm),
            Paragraph("REQUEST FOR LABORATORY REPORT", extend_style(styles["rc-header"], spaceBefore=0)),
            Table(
                [
                    [
                        Paragraph("Tag Number: {}".format(''), styles["rc-aawp-main-content"]), None
                    ],[
                        Paragraph("Case Number: {}".format(''), styles["rc-aawp-main-content"]), None
                    ],[
                        Paragraph("Recovering: {}".format(''), styles["rc-aawp-main-content"]),
                        Paragraph("&nbsp;"*13+"Area / {}".format(''), styles["rc-aawp-main-content"])
                    ],[
                        Paragraph("&nbsp;&nbsp;&nbsp;Officer/Badge: {}".format(''), styles["rc-aawp-main-content"]),
                        Paragraph("Unit Assigned: {}".format(''), styles["rc-aawp-main-content"])
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                ]),
                colWidths=(105*mm, 85*mm),
            ),

            Paragraph("ARREST INFORMATION",extend_style(styles["rc-header"],)),
            Table(
                [
                    [
                        Paragraph("Location of Arrest: {}".format(''), styles["rc-aawp-main-content"]),
                        Paragraph("Date / Time: {}".format(''), styles["rc-aawp-main-content"]),
                    ],[
                        Paragraph("Offense: {}".format(''), styles["rc-aawp-main-content"]),
                        None
                    ],[
                        Paragraph("Offender's Name: {}".format(''), styles["rc-aawp-main-content"]),
                        Table(
                            [
                                [
                                    Paragraph("DOB: {}".format(''), extend_style(styles["rc-aawp-main-content"], leftIndent=11*mm)),
                                    Paragraph("Race: {}".format(''), extend_style(styles["rc-aawp-main-content"], leftIndent=11*mm)),
                                    Paragraph("Sex: {}".format(''), extend_style(styles["rc-aawp-main-content"], leftIndent=11*mm)),
                                ]
                            ],
                            style=extend_table_style(styles["rc-main-table"], [
                            ]),
                        ),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                ]),
                colWidths=(110*mm, 80*mm),
            ),

            Paragraph("COURT INFORMATION",extend_style(styles["rc-header"])),
            Table(
                [
                    [
                        Paragraph("Court Date/Time: {}".format(''), styles["rc-aawp-main-content"]),
                        Paragraph("Court District & Room Number: {}".format(''), styles["rc-aawp-main-content"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                ]),
                colWidths=(80*mm, 110*mm),
            ),
            Spacer(0, 12.4 * mm),
            Table(
                [
                    [
                        Paragraph("Description of Evidence: {}".format(''), styles["rc-aawp-main-content"]),                        
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                ]),
                colWidths=(190*mm),
            ),            
            Spacer(0, 8.4 * mm),

            Paragraph("CHAIN OF POSSESSION OF EVIDENCE",extend_style(styles["rc-header"], spaceAfter=6)),
            Table(
                table,
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (0, 0), (-1, 0), 0.1, "black"),
                    ("OUTLINE", (0, 0), (-1, -1), 0.1, "black"),
                    ("LINEAFTER", (0, 0), (-1, -1), 0.1, "black"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 1.4 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 1.4 * mm),
                ]),
                colWidths=(65*mm, 65*mm, 25*mm, 35*mm),
                rowHeights=5.4*mm
            ),
            Spacer(0, 4.4 * mm),
        ]
        return elems