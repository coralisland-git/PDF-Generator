# -*- coding: utf-8 -*-
import cStringIO
import datetime

from reportlab_styles import *


def generate_ordinance_revocation_hearing(pdf_dict, title=None, author=None):
    cr = AAWPReport(title, author)
    buff = cStringIO.StringIO()
    return cr.create_report(pdf_dict, buff)


class AAWPReport:
    def __init__(self, title=None, author=None):
        self.page_size = letter
        self.page_margin = (23.5 * mm, 12.4 * mm)
        self.sections = ["header", "section_1"]
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
                "IN THE MAGISTRATE COURT OF ROCKDALE COUNTY<br />STATE OF GEORGIA",
                style=styles["rc-doc-header"]
            )
        )
        elems.append(Spacer(0, 9.8 * mm))
        elems += [
            Paragraph(
                "ROCKDALE COUNTY,",
                extend_style(styles["rc-aawp-main"], leftIndent=1.9 * mm, rightIndent=1.9 * mm)
            ),
            Spacer(0, 3 * mm),
            Paragraph(
                "vs.",
                extend_style(styles["rc-aawp-main"], leftIndent=1.9 * mm, rightIndent=1.9 * mm)
            ),
            Spacer(0, 3 * mm)
        ]
        elems.append(
            Table(
                [
                    [
                        Paragraph(self.data["defendant_name"], style=extend_style(styles["rc-aawp-main"], alignment=TA_CENTER)),
                        None,
                        Paragraph("CASE NO", style=extend_style(styles["rc-aawp-main"], alignment=TA_CENTER)),
                        Paragraph(self.data['case_number'], style=extend_style(styles["rc-aawp-main"], alignment=TA_CENTER)),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (0, 0), (0, 0), 0.7, "black"),
                    ("LINEBELOW", (3, 0), (3, 0), 0.7, "black"),
                    # ("TOPPADDING", (0, 0), (0, 0), 0.5 * mm),
                    # ("LEFTPADDING", (0, 0), (0,0), 2 * mm),
                    # ("TOPPADDING", (0, 0), (0, 0), 1 * mm)
                ]),
                colWidths=(40 * mm, 50 * mm, 30 * mm, 40 * mm)
            )
        )
        elems.append(Spacer(0, 3 * mm))
        elems.append(Paragraph("Defendant.", extend_style(styles["rc-aawp-main"], leftIndent=16 * mm, rightIndent=1.9 * mm)))
        elems.append(Spacer(0, 7 * mm))
        elems = elems + [
            Paragraph(
                "<u>REVOCATION OF PROBATED AND SUSPENDED SENTENCE HEARING:<br />WAIVER OF ATTORNEY (if not represented)<br />WAIVER OF NOTICE<br />ADMISSION OF GUILT</u>",
                styles["rc-header"]
            ),
            Spacer(0, 9 * mm),
        ]
        return elems

    def _section_section_1(self):
        elems = [
            Paragraph(
                "I, the above-named Defendant, hereby acknowledge that I have the right to be represented by an attorney at all stages of these proceedings. I understand that if I am indigent (financially unable to afford an attorney) as defined by law, a public defender will be appointed to represent me. I am electing to go forward with my probation or suspended sentence revocation proceedings and I understand the allegations against me.",
                extend_style(styles["rc-aawp-main"], leftIndent=1.9 * mm, rightIndent=1.9 * mm)
            ),
        ]
        elems.append(Spacer(0, 3 * mm))
        elems += [
            Paragraph(
                "I have been advised of my right to counsel and if counsel does not currently represent me, I freely and voluntarily waive any benefit of counsel. I have received in advance of today’s proceedings a copy of the revocation petition against me.",
                extend_style(styles["rc-aawp-main"], leftIndent=1.9 * mm, rightIndent=1.9 * mm)
            ),
        ]
        elems.append(Spacer(0, 3 * mm))
        elems += [
            Paragraph(
                "I also understand that I am entitled to seventy-two hours’ notice before my hearing to prepare for the allegations against me. I understand that if I elect to invoke my right to the seventy-two hours’ notice that the Court would continue my case to allow me at least seventy-two hours to prepare for my hearing. However, I am electing to waive the seventy-two hours’ notice of the hearing and go forward with my hearing today.",
                extend_style(styles["rc-aawp-main"], leftIndent=1.9 * mm, rightIndent=1.9 * mm)
            ),
        ]
        elems.append(Spacer(0, 3 * mm))
        elems += [
            Paragraph(
                "After being advised of my rights above, I freely and voluntarily admit responsibility and guilt to the sentence violation(s) as alleged in the Petition, waive the benefit of counsel (if not represented by counsel), and waive my right to seventy-two hours’ notice of the hearing.",
                extend_style(styles["rc-aawp-main"], leftIndent=1.9 * mm, rightIndent=1.9 * mm)
            ),
        ]
        elems.append(Spacer(0, 8 * mm))

        date_parts = self.data["order_date"].split("/")
        date_parts[1] = int(date_parts[1])
        if date_parts[1] == 1:
            date_parts[1] = "1st"
        elif date_parts[1] == 2:
            date_parts[1] = "2nd"
        elif date_parts[1] == 3:
            date_parts[1] = "3rd"
        else:
            date_parts[1] = "%sth" % date_parts[1]
        date_parts[0] = datetime.date(1900, int(date_parts[0]), 1).strftime('%B')
        # date_parts[2] = date_parts[2][2:]
        elems.append(
            Table(
                [
                    [
                        Paragraph("this", styles["rc-aawp-main"]),
                        Paragraph("%s" % date_parts[1], extend_style(styles["rc-aawp-main"], alignment=TA_CENTER)),
                        Paragraph("day of", extend_style(styles["rc-aawp-main"], alignment=TA_CENTER)),
                        Paragraph("%s" % date_parts[0], extend_style(styles["rc-aawp-main"], alignment=TA_CENTER)),
                        # Paragraph("20", extend_style(styles["rc-aawp-main"], alignment=TA_RIGHT)),
                        Paragraph("%s" % date_parts[2], styles["rc-aawp-main"]),
                        Paragraph(".", styles["rc-aawp-main"]),
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LEFTPADDING", (0, 0), (0, -1), 1.9 * mm),
                    ("LINEBELOW", (1, 0), (1, 0), 0.5, "black"),
                    ("LINEBELOW", (3, 0), (3, 0), 0.5, "black"),
                    ("LINEBELOW", (4, 0), (4, 0), 0.5, "black"),
                ]),
                colWidths=(9 * mm, 16.5 * mm, 12.8 * mm, 28 * mm, 13.3 * mm, 2 * mm, None)
            )
        )
        elems.append(Spacer(0, 5 * mm))
        elems.append(
            Table(
                [
                    [
                        Paragraph("Defendant's Signature", style=styles["rc-aawp-main"]),
                        None,  # TODO signature field
                        Paragraph("Date", style=extend_style(styles["rc-aawp-main"], alignment=TA_CENTER)),
                        None,  # TODO signature date field
                    ],
                    [
                        Paragraph("Defendant's Attorney Signature", style=styles["rc-aawp-main"]),
                        None,  # TODO signature field
                        Paragraph("Date", style=extend_style(styles["rc-aawp-main"], alignment=TA_CENTER)),
                        None,  # TODO signature date field
                    ],
                    [
                        Paragraph("County’s Prosecutor Signature", style=styles["rc-aawp-main"]),
                        None,  # TODO signature field
                        Paragraph("Date", style=extend_style(styles["rc-aawp-main"], alignment=TA_CENTER)),
                        None,  # TODO signature date field
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEBELOW", (1, 0), (1, 0), 0.5, "black"),
                    ("LINEBELOW", (1, 1), (1, 1), 0.5, "black"),
                    ("LINEBELOW", (1, 2), (1, 2), 0.5, "black"),
                    ("LINEBELOW", (3, 0), (3, 0), 0.5, "black"),
                    ("LINEBELOW", (3, 1), (3, 1), 0.5, "black"),
                    ("LINEBELOW", (3, 2), (3, 2), 0.5, "black"),
                ]),
                colWidths=(58 * mm, 54 * mm, 10.5 * mm, 42 * mm),
                rowHeights=6 * mm
            )
        )

        return elems
