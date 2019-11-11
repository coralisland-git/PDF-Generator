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
        elems.append(Spacer(0, 4 * mm))
        elems.append(
            Paragraph(
                "REMITTANCE REPORT",
                style=styles["rc-doc-header-rmt"]
            )
        )
        elems.append(
            Table(
                [
                    [
                        Paragraph("To:", style=extend_style(styles["rc-main-rmt"], alignment=TA_RIGHT)),
                        Paragraph("Peace Officers'<br/>Annuity and Benefit Fund<br/>P.O. Box 56<br/>Griffin, GA 30224", style=styles["rc-main-rmt"]),
                        Paragraph("From:<br/>Magistrate Court<br/>Rockdale County<br/>Court No. 122033J", style=styles["rc-main-rmt"])
                    ]
                ],
                colWidths=(10 * mm, 60 * mm, 90 * mm),
                style=(
                    ('VALIGN', (0, 0), (0, 0), 'TOP'),
                )
            )
        )
        elems.append(Spacer(0, 2 * mm))

        return elems

    def _section_section_1(self):
        elems = list()
        elems.append(
            Paragraph(
                "Report of Fines and/or Forfeitures for cases during the month(s).",
                styles["rc-rmt-main"]
            )
        )
        elems.append(Spacer(0, 2.5 * mm))
        date1 = datetime.datetime.strptime(self.data['date_range_from'], '%m/%d/%Y')
        date2 = datetime.datetime.strptime(self.data['date_range_to'], '%m/%d/%Y')

        elems.append(
            Paragraph(
                "{} To {}".format(date1.strftime('%B %d, %Y'), date2.strftime('%B %d, %Y')),
                styles["rc-rmt-main"]
            )
        )
        elems.append(Spacer(0, 6 * mm))
        ps_title = extend_style(styles["rc-rmt-main"], alignment=TA_CENTER)
        data = [
            [
                Paragraph("Amount of Fine and/or<br/> Bond forteiture", ps_title),
                Paragraph("Number of Cases", ps_title),
                Paragraph("Amount due on each<br/> case", ps_title),
                Paragraph("Total", ps_title),
            ]
        ]
        ps = extend_style(styles["rc-rmt-main"], fontSize=9, alignment=TA_CENTER)

        title_map = {
            '4_to_25': '$4.01 through $25.00', 
            '25_to_50': '$25.01 through $50.00', 
            '50_to_100': '$50.01 through $100.00', 
            'over_100': '$100.01 and over', 
            'partial_payment': 'Partial Payment', 
            'grand_total': 'GRAND TOTAL'
        }

        for ii in ['4_to_25', '25_to_50', '50_to_100', 'over_100', 'partial_payment', 'grand_total']:
            val = self.data[ii]
            if ii == 'over_100':
                amt = val['amount_due_per_case']
            elif ii == 'partial_payment':
                amt = '--------'
            elif ii == 'grand_total':
                amt = ''
            else:
                amt = "$%s" % val["amount_due_per_case"]

            data.append([
                Paragraph("%s" % title_map[ii], ps),
                Paragraph("%s" % val["number_of_cases"], ps),
                Paragraph(amt, ps),
                Paragraph("$%s" % val["total_amount"], ps),
            ])

        elems.append(
            Table(
                data,
                style=extend_table_style(styles["rc-main-table"], [
                    ("GRID", (0, 0), (-1, -1), 0.5, "black"),
                    ("BACKGROUND", (2, -1), (2, -1), 'gray'),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4 * mm),
                    ("TOPPADDING", (0, 1), (-1, -1), 4 * mm),
                    ("TOPPADDING", (0, 0), (-1, 0), 6 * mm),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]),
                colWidths=(52 * mm, 39 * mm, 39 * mm, 39 * mm),
            )
        )
        return elems

    def _section_section_2(self):
        elems = []
        elems.append(Spacer(0, 9 * mm))
        elems += [
            Paragraph(
                "To the best of my knowledge and belief this is a correct amount for the period stated above which is due the Peace Officers' Annuity and Benefit Fund of Georgia as provided by GA. Laws, 1950. p.50, as amended.",
                extend_style(styles["rc-main-rmt"], leftIndent=0 * mm, rightIndent=1.9 * mm, fontSize=8)
            ),
        ]
        elems.append(Spacer(0, 6 * mm))
        elems.append(
            Table(
                [
                    [
                        Paragraph("Date", style=extend_style(styles["rc-main-1"], alignment=TA_RIGHT)),
                        Paragraph(self.data['order_date'], style=extend_style(styles["rc-main-1"], alignment=TA_CENTER)),
                        None,
                        None,
                    ],
                    [
                        None,
                        None,
                        None,
                        Paragraph("Signature", style=extend_style(styles["rc-main-1"], alignment=TA_CENTER)),
                    ],
                    [
                        Paragraph("Check #", style=extend_style(styles["rc-main-1"], alignment=TA_RIGHT)),
                        None,
                        None,
                        None,
                    ],
                    [
                        None,
                        None,
                        None,
                        Paragraph("Title", style=extend_style(styles["rc-main-1"], alignment=TA_CENTER)),
                    ]
                ],
                style=[
                    ("VALIGN", (3, 1), (3, 1), "TOP"),
                    ("VALIGN", (3, 3), (3, 3), "TOP"),
                    ("VALIGN", (0, 0), (0, 2), "MIDDLE"),
                    # ("VALIGN", (0, 2), (3, 2), "BOTTOM"),
                    ("VALIGN", (1, 0), (1, 0), 0.5, "TOP"),
                    ("LINEBELOW", (1, 0), (1, 0), 0.5, "black"),
                    ("LINEBELOW", (3, 0), (3, 0), 0.5, "black"),
                    ("LINEBELOW", (1, 2), (1, 2), 0.5, "black"),
                    ("LINEBELOW", (3, 2), (3, 2), 0.5, "black"),
                ],
                colWidths=(15 * mm, 50 * mm, 30 * mm, 68 * mm),
                rowHeights=(7.2 * mm, 5.2 * mm, 5.2 * mm, 5.2 * mm)
            )
        )
        elems.append(Spacer(0, 6 * mm))

        elems += [
            Paragraph(
                "Each remitting agent is required to keep accurate records of all cases handled so that they may be inspected or audited at any time. For your information, please refer to 47-17-60 section of Georgia Laws on making remittances. Please note that there is a time limitation for making such remittances as set forth in the Section of Georgia Law referred to.",
                extend_style(styles["rc-main-rmt"], leftIndent=5.3 * mm, rightIndent=5.4 * mm, fontSize=8)
            ),
        ]
        elems.append(Spacer(0, 8 * mm))

        elems += [
            Table(
                [
                    [
                        Paragraph("This report should be mailed with your remittance to:", style=styles['rc-main-rmt']),
                        Paragraph("Peace Officers' A & B Fund of Ga.<br/>P.O. Box 56<br/>Griffin, GA 30224", style=styles['rc-main-rmt'])
                    ],
                    [
                        Paragraph("Form No. 701. - Revised July 1, 2004", style=styles['rc-main-rmt']), ""
                    ]
                ],
                rowHeights=15 * mm,
                colWidths=(74 * mm, 64 * mm),
                style=(("VALIGN", (0, 0), (-1, -1), "TOP"),)
            )
        ]
        elems.append(Spacer(0, 8 * mm))

        timestamp = datetime.datetime.now().strftime('%m/%d/%Y %I:%m %p')
        elems += [
            Table(
                [
                    [
                        Paragraph("Printed on {}".format(timestamp), style=styles['rc-main-rmt'])
                    ]
                ],
                rowHeights=5 * mm,
                colWidths=180 * mm,
                style=(
                    ("BOX", (0, 0), (0, 0), 0.5, "gray"),
                )
            )
        ]

        return elems

