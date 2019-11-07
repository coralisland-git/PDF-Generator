# -*- coding: utf-8 -*-
import cStringIO
import datetime

from reportlab_styles import *


def generate_remittance_report(pdf_dict, title=None, author=None):
    cr = AAWPReport(title, author)
    buff = cStringIO.StringIO()
    return cr.create_report(pdf_dict, buff)


class AAWPReport:
    def __init__(self, title=None, author=None):
        self.page_size = letter
        self.page_margin = (23.5 * mm, 12.4 * mm)
        self.sections = ["header", "section_1", "section_2"]
        self.title = title
        self.author = author
        self.data = None

    def create_report(self, data_dict, buff=None):
        def get_method(section):
            try:
                method = getattr(self, "_section_" + section)
            except AttributeError:
                raise Exception("Section method not found: " + section)
            return method

        self.data = data_dict
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
        elems = list()
        elems.append(
            Paragraph(
                "REMITTANCE REPORT",
                style=styles["rc-doc-header"]
            )
        )
        elems.append(Spacer(0, 9.8 * mm))

        return elems

    def _section_section_2(self):
        elems = []
        elems.append(Spacer(0, 3 * mm))
        elems += [
            Paragraph(
                "To the best of my knowledge and belief this is a correct amount for the period stated above which is due the Peace Officers' Annuity and Benefit Fund of Georgia as provided by GA. Laws, 1950. p.50, as amended.",
                extend_style(styles["rc-main"], leftIndent=1.9 * mm, rightIndent=1.9 * mm)
            ),
        ]
        elems.append(Spacer(0, 8 * mm))
        elems.append(
            Table(
                [
                    [
                        Paragraph("Date", style=styles["rc-main"]),
                        None,
                        None,
                        None,
                    ],
                    [
                        Paragraph("Check #", style=styles["rc-main"]),
                        None,
                        None,
                        None,
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEBELOW", (1, 0), (1, 0), 0.5, "black"),
                    ("LINEBELOW", (1, 1), (1, 1), 0.5, "black"),
                    ("LINEBELOW", (3, 0), (3, 0), 0.5, "black"),
                    ("LINEBELOW", (3, 1), (3, 1), 0.5, "black"),
                ]),
                colWidths=(20 * mm, 54 * mm, 25 * mm, 62 * mm),
                rowHeights=6 * mm
            )
        )
        elems.append(Spacer(0, 8 * mm))

        elems += [
            Paragraph(
                "Each remitting agent is required to keep accurate records of all cases handled so that they may be inspected or audited at any time. For your information, please refer to 47-17-60 section of Georgia Laws on making remittances. Please note that there is a time limitation for making such remittances as set forth in the Section of Georgia Law referred to.",
                extend_style(styles["rc-main"], leftIndent=1.9 * mm, rightIndent=1.9 * mm)
            ),
        ]
        elems.append(Spacer(0, 8 * mm))

        return elems

    def _section_section_1(self):
        elems = list()
        elems.append(
            Paragraph(
                "Report of Fines and/or Forfeitures for cases during the month(s).",
                styles["rc-fdo-main"]
            )
        )
        elems.append(Spacer(0, 5 * mm))
        elems.append(
            Paragraph(
                "August 01, 2019 To August 31, 2019",
                styles["rc-fdo-main"]
            )
        )
        elems.append(Spacer(0, 8 * mm))
        ps_title = extend_style(styles["rc-fdo-main"], alignment=TA_CENTER)
        data = [
            [
                Paragraph("Amount of Fine and/or<br/> Bond forteiture", ps_title),
                Paragraph("Number of Cases", ps_title),
                Paragraph("Amount due on each case", ps_title),
                Paragraph("Total", ps_title),
            ]
        ]
        ps = extend_style(styles["rc-fdo-main"], fontSize=9)
        for citation in self.data["citation_table"] + self.data["citation_table"] + self.data["citation_table"]:
            data.append([
                Paragraph("%s" % citation["computation_of_sentence"], ps),
                Paragraph("$ %s" % citation["fine"], ps),
                Paragraph("%s" % citation["community_service_hours"], ps),
                Paragraph("%s" % citation["restitution"], ps),
                Spacer(0, 8.2*mm)
            ])
        elems.append(
            Table(
                data,
                style=extend_table_style(styles["rc-main-table"], [
                    ("GRID", (0, 0), (-2, -1), 0.5, "black"),
                    ("LEFTPADDING", (0, 0), (-2, -1), 1.5 * mm),
                    ("RIGHTPADDING", (0, 0), (-2, -1), 1.5 * mm),
                    ("BOTTOMPADDING", (0, 0), (-2, 0), 0.25 * mm),
                    ("ALIGN", (0, 0), (-2, 0), "CENTER"),
                    ("VALIGN", (0, 0), (-2, -1), "TOP"),
                ]),
                colWidths=(50 * mm, 40 * mm, 40 * mm, 40 * mm, 1),
                hAlign="LEFT"
            )
        )
        return elems
