# -*- coding: utf-8 -*-
import cStringIO
from common.signatures import *
from reportlab.platypus.flowables import HRFlowable, PageBreak
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from document_specific_styles import *


def generate_fpc_receipt(title=None, author=None):
    cr = FPCR(title, author)
    buff = cStringIO.StringIO()
    return cr.create_report(buff)


class FPCR:
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
                Paragraph("ITEM (TAG) #", styles["rc-aawp-main-content"]),
                Paragraph("SERIAL #", styles["rc-aawp-main-content"]),
                Paragraph("BRAND", styles["rc-aawp-main-content"]),
                Paragraph("MODEL", styles["rc-aawp-main-content"]),
                Paragraph("DESCRIPTION", styles["rc-aawp-main-content"])
            ],
        ]
        for idx in range(7):
            table.append([
                Paragraph("", styles["rc-aawp-main-content"]),
                Paragraph("", styles["rc-aawp-main-content"]),
                Paragraph("", styles["rc-aawp-main-content"]),
                Paragraph("", styles["rc-aawp-main-content"]),
                Paragraph("", styles["rc-aawp-main-content"])
            ])
        elems = [
            Spacer(0, -3.4 * mm),
            Paragraph("PROPERTY RELEASE RECEIPT", extend_style(styles["rc-header"], spaceBefore=0, spaceAfter=20)),
            Paragraph("Case Number: {}".format(''), styles["rc-aawp-main-content"]),
            Paragraph("Location: {}".format(''), styles["rc-aawp-main-content"]),
            Paragraph("Classification(s): {}".format(''), styles["rc-aawp-main-content"]),
            Spacer(0, 4.4 * mm),
            Table(
                table,
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (0, 0), (-1, 0), 0.1, "black"),
                    ("OUTLINE", (0, 0), (-1, -1), 0.1, "black"),
                    ("LINEAFTER", (0, 0), (-1, -1), 0.1, "black"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 1.4 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 1.4 * mm),
                ]),
                colWidths=(26*mm, 25*mm, 35*mm, 35*mm, 70*mm),
                rowHeights=5.4*mm
            ),
            Spacer(0, 4.4 * mm),

            Paragraph("OWNER INFORMATION",extend_style(styles["rc-header"])),
            Spacer(0, 2.2 * mm),
            Table(
                [
                    [
                        Paragraph("Owner Name: {}".format(''), styles["rc-aawp-main-content"]),
                    ],[
                        Paragraph("Address: {}".format(''), styles["rc-aawp-main-content"])
                    ],[
                        Paragraph("Home Phone: {}".format(''), styles["rc-aawp-main-content"])
                    ],[
                        Paragraph("Work Phone: {}".format(''), styles["rc-aawp-main-content"])
                    ],[
                        Paragraph("Cell Phone: {}".format(''), styles["rc-aawp-main-content"])
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                ]),
                colWidths=(190*mm),
            ),

            Paragraph("RELEASED TO",extend_style(styles["rc-header"])),
            Spacer(0, -2.8 * mm),
            Table(
                [
                    [
                        Paragraph("Name: {}".format(''), styles["rc-aawp-main-content"]),
                        Paragraph("Date / Time: {}".format(''), styles["rc-aawp-main-content"]),
                    ],[
                        Paragraph("Destroyed by (if applicable): {}".format(''), styles["rc-aawp-main-content"]),
                        Paragraph("Date / Time: {}".format(''), styles["rc-aawp-main-content"]),
                    ],[
                        Paragraph("Signature: {}".format(''), styles["rc-aawp-main-content"]),
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                ]),
                colWidths=(113*mm, 77*mm),
                rowHeights=10.4*mm
            ),

            Paragraph("RELEASED BY",extend_style(styles["rc-header"])),
            Spacer(0, -2.8 * mm),
            Table(
                [
                    [
                        Paragraph("Name / Badge: {}".format(''), styles["rc-aawp-main-content"]),
                        Paragraph("Date / Time: {}".format(''), styles["rc-aawp-main-content"]),
                    ],[
                        Paragraph("Signature: {}".format(''), styles["rc-aawp-main-content"]),
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                ]),
                colWidths=(125*mm, 65*mm),
                rowHeights=10.4*mm
            ),
            Paragraph("ADDITIONAL INFORMATION",extend_style(styles["rc-header"])),
            Spacer(0, 3.4 * mm),
            Table(
                [
                    [
                        Paragraph("Notes: {}".format(''), styles["rc-aawp-main-content"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                ]),
                colWidths=(190*mm),
            ),
        ]
        return elems