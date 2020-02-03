# -*- coding: utf-8 -*-
import cStringIO
import datetime

from document_specific_styles import *


def bench_trial_demand_english(title=None, author=None):
    cr =TDReport(title, author)
    buff = cStringIO.StringIO()
    return cr.create_report(buff)


class TDReport:
    def __init__(self, title=None, author=None):
        self.page_size = letter
        self.page_margin = (12.4 * mm, 12.4 * mm)
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
        elems = list()
        elems += [
            Paragraph(
                "In the Municipal Court of Brookhaven <br />State of Georgia",                
                extend_style(styles["rc-doc-header"], fontSize=14, leading=14.5)
            ),
            Spacer(0, 9.8 * mm),
            Table(
                [
                    [
                        Paragraph("City of Brookhaven", styles["rc-tdwp-main-tb"]),
                        None,
                        Paragraph("Case/ Citation No: "+'_'*20, styles["rc-tdwp-main-tb"])
                    ],
                    [
                        None,
                        None,
                        None
                    ],
                    [
                        Paragraph("V.", styles["rc-tdwp-main-tb"]),
                        None,
                        Paragraph("Charge(s): "+'_'*27, styles["rc-tdwp-main-tb"])
                    ],
                    [
                        None,
                        None,
                        None
                    ],
                    [
                        None,
                        None,
                        None
                    ],
                    [
                        Paragraph("Defendant", styles["rc-tdwp-main-tb"]),
                        None,
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 5), (-1, -1), "TOP"),
                    ("TOPPADDING", (0, 5), (-1, -1), 0.2 * mm),
                    ("LINEBELOW", (0, 4), (0, 4), 0.1, "black"),
                ]),
                colWidths=(73 * mm, 14, 113 * mm),
                rowHeights=4.2 * mm
            ),
            Paragraph(
                "<u>BENCH TRIAL DEMAND <br />WAIVER OF RIGHT TO BIND OVER</u>",
                extend_style(styles["rc-header"], fontSize=11 ,spaceBefore=10)
            ),
            Spacer(0, 1.5 * mm)
        ]
            
        return elems

    def _section_content(self):
        pre_dash = "_"*4
        elems = [
            Paragraph(
                "The above named defendant having this "+'_'*5+" day of "+'_'*11+", 20 "+'_'*4+" appeared before the Court for arraignment and entered a plea of not guilty.",
                extend_style(styles["rc-tdwp-main"], fontSize=11)
            ),
        ]        
        elems += [
            Paragraph(
                "*" * 102,
                extend_style(styles["rc-tdwp-main"], leading=9)
            ),
            Table(
                [
                    [
                        Paragraph(pre_dash, extend_style(styles["rc-tdwp-main"])),
                        Paragraph(
                            "I understand that I have a Constitutional right to have this case bound over to the State Court of DeKalb County and to have a jury trial or bench trial there.",
                            extend_style(styles["rc-tdwp-main"], spaceBefore=0)
                        )
                    ],        
                    [
                        Paragraph(pre_dash, extend_style(styles["rc-tdwp-main"])),
                        Paragraph(
                            "I understand that by requesting a bench trial in the City of Brookhaven Municipal Court, I am waiving my right to bind this case over to State Court and waiving my right to a jury trial.",
                            styles["rc-tdwp-main"]
                        )
                    ],
                    [
                        Paragraph(pre_dash, extend_style(styles["rc-tdwp-main"])),
                        Paragraph(
                            "I understand that I have the right to seek legal counsel or apply for a court appointed attorney to represent me at trial but I must retain an attorney before the trial date if I choose to be represented by an attorney.",
                            styles["rc-tdwp-main"]
                        )
                    ],
                    [
                        Paragraph(pre_dash, extend_style(styles["rc-tdwp-main"])),
                        Paragraph(
                            "I understand the charges against me and the maximum and minimum punishment for each of the charges against me.",
                            styles["rc-tdwp-main"]
                        )
                    ],
                    [
                        Paragraph(pre_dash, extend_style(styles["rc-tdwp-main"])),
                        Paragraph(
                            "I understand that the rules of evidence will apply to me although I am not an attorney.",
                            styles["rc-tdwp-main"]
                        )
                    ],
                    [
                        Paragraph(pre_dash, extend_style(styles["rc-tdwp-main"])),
                        Paragraph(
                            "I understand I <u>do not</u> have to testify and I have the right to remain silent. I further understand that if I do not wish to testify, this cannot be used against me.",
                            styles["rc-tdwp-main"]
                        )
                    ],
                    [
                        Paragraph(pre_dash, extend_style(styles["rc-tdwp-main"])),
                        Paragraph(
                            "I understand that I am entitled to the subpoena powers of this court in order to subpoena any witnesses to appear for trial.",
                            styles["rc-tdwp-main"]
                        )
                    ],
                    [
                        Paragraph(pre_dash, extend_style(styles["rc-tdwp-main"])),
                        Paragraph(
                            "I understand that I am required to bring <u>any and all</u> evidence with me on my trial date.",
                            styles["rc-tdwp-main"]
                        )
                    ]
                ],
                colWidths=(8.5 * mm, 182 * mm),                
                style=(
                    ('VALIGN', (0, 0), (1, 7), 'TOP'),
                    ("LEFTPADDING", (0, 0), (1, 7), 0.0 * mm),
                    ("RIGHTPADDING", (0, 0), (1, 7), 0.0 * mm),
                    ("BOTTOMPADDING", (0, 0), (1, 7), 2.5 * mm)
                )
            ),
            Paragraph(
                "*" * 102,
                extend_style(styles["rc-tdwp-main"], leading=9, spaceBefore=6)
            ),
            Table(
                [
                    [
                        Paragraph(pre_dash, extend_style(styles["rc-tdwp-main"])),
                        Paragraph(
                            "At this time, I wish to go forward with a non-jury trial before this court.",
                            extend_style(styles["rc-tdwp-main"], spaceBefore=0)
                        )
                    ],
                    [
                        Paragraph(pre_dash, extend_style(styles["rc-tdwp-main"])),
                        Paragraph(
                            "By signing this demand, I acknowledge I have received a copy.",
                            styles["rc-tdwp-main"]
                        )
                    ],
                    [
                        Paragraph(pre_dash, extend_style(styles["rc-tdwp-main"])),
                        Paragraph(
                            "By signing this demand, I acknowledge that I must appear in court on the date scheduled and I waive my right to pay in advance of the court date.",
                            styles["rc-tdwp-main"]
                        )
                    ],
                ],
                colWidths=(8.5 * mm, 182 * mm),
                style=(
                    ('VALIGN', (0, 0), (1, 2), 'TOP'),
                    ("LEFTPADDING", (0, 0), (1, 2), 0.0 * mm),
                    ("RIGHTPADDING", (0, 0), (1, 2), 0.0 * mm),
                    ("BOTTOMPADDING", (0, 0), (1, 2), 2.5 * mm)
                )
            ),
            Paragraph(
                "<b>I ACKNOWLEDGE my non-jury trial date is "+'_'*5+" day "+'_'*15+" of 20 "+'_'*4+" at <u>8:30 AM</u></b>",
                extend_style(styles["rc-tdwp-main"], spaceBefore=4)
            ),
            Paragraph(
                "I SWEAR under penalties of perjury that these statements are true and correct.",
                styles["rc-tdwp-main"]
            ),
            Paragraph(
                "I ATTEST that by signing this demand, that no promise or threat has been made to me to waive my right to an attorney or waive my right to a jury trial. I further attest that I have read this document in it entirety and understand its content.",
                styles["rc-tdwp-main"]
            ),
            Spacer(0, 7 * mm),
            Table(
                [
                    [
                        None,
                        None,
                        Paragraph("Date", styles["rc-tdwp-main-tb"]),
                        None,
                        None,
                        Paragraph("Phone #:", styles["rc-tdwp-main-tb"]),
                        None,
                        None
                    ],
                    [
                        Paragraph("Defendant's/Defense Attorney's Signature", styles["rc-tdwp-main-tb"]),
                        None,
                        None,
                        Paragraph("", styles["rc-tdwp-main-tb"]),
                        None,
                        None,
                        Paragraph("", styles["rc-tdwp-main-tb"]),
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 1), (-1, -1), "TOP"),
                    ("TOPPADDING", (0, 1), (-1, -1), 0.2 * mm),
                    ("LINEABOVE", (0, 1), (0, 1), 0.1, "black"),
                    ("LINEABOVE", (3, 1), (3, 1), 0.1, "black"),
                    ("LINEABOVE", (6, 1), (6, 1), 0.1, "black"),
                ]),
                colWidths=(66 * mm, 10 * mm, 9 * mm, 24 * mm, 8 * mm , 15 * mm, 34 * mm, 25 * mm),
                rowHeights=2.2 * mm
            ),
            Spacer(0, 5 * mm),
            Paragraph(
                "REVISED 02/2019",
                extend_style(styles["rc-tdwp-main"], fontSize=6)
            )
        ]

        return elems
