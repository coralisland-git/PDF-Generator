# -*- coding: utf-8 -*-
import cStringIO
import datetime
from reportlab.platypus.flowables import HRFlowable, PageBreak
from document_specific_styles import *


def directive_to_pull_and_clear_warrant(title=None, author=None):
    cr = DPCWReport(title, author)
    buff = cStringIO.StringIO()
    return cr.create_report(buff)


class DPCWReport:
    def __init__(self, title=None, author=None):
        self.page_size = letter
        self.page_margin = (30.5 * mm, 2.8 * mm)
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
            Spacer(0, 9.8 * mm),
            Paragraph(
                "BROOKHAVEN MUNICIPAL COURT", 
                styles["rc-doc-header"]
            ),
            Paragraph(
                "DIRECTIVE TO PULL AND CLEAR WARRANT", 
                styles["rc-header-dc"]
            ),
            Spacer(0, 6 * mm),
            Paragraph(
                "To:"+"&nbsp;"*6+"Brookhaven Police Department", 
                styles["rc-aawp-main-content"]
            ),
            Paragraph("From:"+"&nbsp;"*2+"Brookhaven Municipal Court", extend_style(styles["rc-aawp-main-content"])),
            Paragraph("Please clear the following active warrants, attach the documents to this request and return to the Court Clerk's office.", extend_style(styles["rc-aawp-main-content"])),
            Paragraph("Date of Request:"+"&nbsp;"*8+"3/30/2017", extend_style(styles["rc-aawp-main-content"])),
            Paragraph("Re: "+"_"*5, extend_style(styles["rc-aawp-main-content"], fontSize=14)),
            Paragraph("&nbsp;"*10+"Defendant", extend_style(styles["rc-aawp-main"], fontSize=14)),
            Paragraph("Race: "+"_"*5+"&nbsp;"*3+" Sex: "+"_"*4+"&nbsp;"*31+" DOB: "+"_"*5, extend_style(styles["rc-aawp-main-content"])),
            Paragraph("Citation/Case Number/ Warrant Number(s): "+"_"*5, extend_style(styles["rc-aawp-main-content"])),
            Spacer(0, 11.4 * mm),
            Table(
                    [
                        [
                            Paragraph("Offense(s):", styles["rc-aawp-main-content"]),
                            Paragraph("_"*5, styles["rc-aawp-main-content"]),
                        ],
                        [
                            None,
                            Paragraph("_"*5, styles["rc-aawp-main-content"]),
                        ],
                        [
                            None,
                            Paragraph("_"*5, styles["rc-aawp-main-content"]),
                        ]
                    ],
                    style=styles["rc-main-table"],
                    colWidths=(25 * mm, 130 * mm),
                    rowHeights=10.4 * mm              
                ),
            Spacer(0, 4 * mm),
            Paragraph("Requested by: "+"_"*49, extend_style(styles["rc-aawp-main-content"], leading=14)),
            Paragraph("&nbsp;"*36+"Court Administrator/Deputy Court Clerk", styles["rc-aawp-main"]),
            Spacer(0, 26 * mm),
            Table(
                [
                    [
                        Paragraph("Please complete the following and return to the Court:", styles["rc-aawp-main-content"]),
                    ],
                    [
                        Paragraph("Date Cleared: "+"_"*58, styles["rc-aawp-main-content"]),
                    ],
                    [
                        Paragraph("Date Cleared: "+"_"*58, styles["rc-aawp-main-content"]),
                    ],
                    [
                        Paragraph("PSR: "+"_"*65, styles["rc-aawp-main-content"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                        ("OUTLINE", (0, 0), (-1, -1), 0.7, "black"),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 1.8 * mm)
                ]),
                colWidths=159*mm,
                rowHeights=10.4 * mm
            ),
            Spacer(0, 22.4 * mm),
            Paragraph("AUG 2015", extend_style(styles["rc-aawp-main-content"], fontSize=8))
        ]
        
        return elems