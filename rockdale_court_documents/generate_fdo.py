from reportlab_styles import styles, extend_style, extend_table_style, SignatureDocTemplate, SignatureRect
import cStringIO
import io
import datetime
import textwrap
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import PageTemplate, Frame, Flowable, Paragraph, Table, Spacer


def generate_fdo(pdf_dict, title=None, author=None):
    cr = FDOReport(title, author)
    buff = cStringIO.StringIO()
    return cr.create_report(pdf_dict, buff)


class XBox(Flowable):
    def __init__(self, size, checked=None, x=0, y=0):
        Flowable.__init__(self)
        self.width = size
        self.height = size
        self.size = size
        self.checked = checked
        self.offset = (x, y)

    def draw(self):
        self.canv.saveState()
        self.canv.setLineWidth(0.11 * self.size)
        self.canv.rect(self.offset[0], self.offset[1], self.width, self.height)
        if self.checked is True:
            self.check()
        self.canv.restoreState()

    def check(self):
        self.canv.setFont('Times-Bold', self.size * 0.95)
        to = self.canv.beginText(self.width * 0.13 + self.offset[0], self.height * 0.155 + self.offset[1])
        to.textLine("X")
        self.canv.drawText(to)


class XBoxParagraph(Paragraph):
    def __init__(self, text, style, size, checked, **kwargs):
        Paragraph.__init__(self, text, style, **kwargs)
        if self.style.firstLineIndent < size:
            self.style.firstLineIndent = size * 1.5
        self.xbox = XBox(size, checked)

    def draw(self):
        Paragraph.draw(self)
        self.xbox.offset = (self.style.leftIndent, self.height - self.xbox.size * 1.5)
        self.xbox.canv = self.canv
        self.xbox.draw()


class FDOReport:
    def __init__(self, title=None, author=None):
        self.page_size = letter
        self.page_margin = (15.8 * mm, 12.5 * mm)
        self.sections = ["header", "section_1", "section_2", "section_3", "section_4", "section_5", "section_6",
                         "section_7", "section_8", "section_9"]
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

        page_t = PageTemplate(
            'normal', [
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
            ],
            onPage=self._page_footer
        )
        doc_t = SignatureDocTemplate(
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
        metadata = doc_t.build(story)
        buff.seek(0)
        return {
            "metadata": metadata,
            "document": buff
        }

    @staticmethod
    def _page_footer(canv, doc):
        dt = datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p")
        p = Paragraph(dt, style=extend_style(
            styles["rc-fdo-main"],
            alignment=TA_RIGHT,
        ))
        p_height = p.wrapOn(canv, doc.width, doc.height)[1]
        p.drawOn(canv, doc.leftMargin, doc.bottomMargin - p_height)

    def _section_header(self):
        elems = list()
        elems.append(
            Paragraph(
                "IN THE MAGISTRATE COURT OF ROCKDALE COUNTY<br />STATE OF GEORGIA",
                style=styles["rc-fdo-doc-header"],
            )
        )
        ps = extend_style(styles["rc-fdo-main"], fontSize=9)
        if len(self.data["citations"]):
            cit_str = ', '.join([c["citation_number"] for c in self.data["citations"]])
            text_width = stringWidth(cit_str, ps.fontName, ps.fontSize)
            cit_lines = textwrap.wrap(cit_str, int(len(cit_str) / (text_width / int((95 * mm) + 1))))
            if len(cit_lines) < 2:
                cit_lines.append("")
        else:
            cit_lines = ["", ""]
        elems.append(
            Table(
                [
                    [
                        Table(
                            [
                                [
                                    None,
                                    Paragraph("<b>ROCKDALE COUNTY, GEORGIA</b>", ps),
                                    None
                                ],
                                [
                                    None,
                                    Paragraph("<b>vs.</b>", ps),
                                ],
                                [
                                    None,
                                    Paragraph("%s" % self.data["defendant_name"], styles["rc-fdo-main"]),
                                    Paragraph("<b>,</b>", ps),
                                ],
                                [
                                    None,
                                    Paragraph("<b>DEFENDANT.</b>", ps),
                                ],
                            ],
                            style=extend_table_style(styles["rc-main-table"], [
                                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                ("VALIGN", (2, 2), (2, 2), "BOTTOM"),
                                ("LINEBELOW", (1, 2), (1, 2), 0.6, "black"),
                            ]),
                            colWidths=(2 * mm, 62.5 * mm, 6 * mm),
                            rowHeights=(10.5 * mm, 5.5 * mm, 5.5 * mm, 5.5 * mm),
                        ),
                        Table(
                            [
                                [
                                    None,
                                    Paragraph("<b>Ordinance Case No.</b>", ps),
                                    Paragraph("%s" % self.data["case_number"], styles["rc-fdo-main"]),
                                    None,
                                    None,
                                ],
                                [
                                    None,
                                    Paragraph("<b>Citation No(s). and Violation(s):</b>", ps),
                                ],
                                [
                                    None,
                                    Paragraph("%s" % cit_lines[0], styles["rc-fdo-main"]),
                                ],
                                [
                                    None,
                                    Paragraph("%s" % cit_lines[1], styles["rc-fdo-main"]),
                                ],
                                [
                                    None,
                                    None,
                                    None,
                                    Paragraph(
                                        "%s" % self.data["term"],
                                        extend_style(styles["rc-fdo-main"], alignment=TA_CENTER)
                                    ),
                                    Paragraph("Term", ps),
                                ]
                            ],
                            style=extend_table_style(styles["rc-main-table"], [
                                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                                ("SPAN", (1, 1), (2, 1)),
                                ("LINEBELOW", (2, 0), (4, 0), 0.6, "black"),
                                ("SPAN", (1, 2), (4, 2)),
                                ("SPAN", (1, 3), (4, 3)),
                                ("LINEBELOW", (1, 2), (4, 2), 0.6, "black"),
                                ("LINEBELOW", (1, 3), (4, 3), 0.6, "black"),
                                ("VALIGN", (4, 4), (4, 4), "BOTTOM"),
                                ("LINEBELOW", (3, 4), (3, 4), 0.4, "black"),
                            ]),
                            colWidths=(2 * mm, 28 * mm, 36 * mm, 33.5 * mm, 7.5 * mm),
                            rowHeights=(3.3 * mm, 6.5 * mm, 4.5 * mm, 5.3 * mm, 5.5 * mm),
                        ),

                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEAFTER", (0, 0), (0, -1), 0.5, "black"),
                ]),
                colWidths=(70.2 * mm, None),
                rowHeights=32 * mm,
                spaceBefore=4.5 * mm,
                spaceAfter=4.5 * mm,
            )
        )
        return elems

    def _section_section_1(self):
        elems = list()
        elems.append(
            Paragraph(
                "<u>FINAL DISPOSITION</u>",
                extend_style(styles["rc-header"], rightIndent=10 * mm)
            )
        )
        elems.append(Spacer(0, 1.3 * mm))
        ps = extend_style(styles["rc-header"], alignment=TA_LEFT)
        elems.append(
            Table(
                [
                    [
                        None,
                        XBox(6.8, True if self.data["original_sentence"] else False),
                        Paragraph("Original Sentence", ps),
                        XBox(6.8, True if self.data["modified_sentence"] else False),
                        Paragraph("Modified Sentence", ps),
                        XBox(6.8, True if self.data["revocation_sentence"] else False),
                        Paragraph("Revocation Sentence", ps),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LINEBELOW", (0, 0), (-1, -1), 1.4, "black", "butt"),
                ]),
                colWidths=(17 * mm, 4 * mm, 44 * mm, 4 * mm, 47 * mm, 4 * mm, 55 * mm),
                rowHeights=5.75 * mm,
                hAlign="LEFT"
            )
        )
        elems.append(Spacer(0, 2.2 * mm))
        elems.append(
            Table(
                [
                    [
                        None,
                        Table(
                            [
                                [
                                    XBox(6.7, True if self.data["plea"] else False),
                                    Paragraph("<b>PLEA</b>:", styles["rc-fdo-main"]),
                                    XBox(6.7, True if self.data["in_person"] else False),
                                    Paragraph("In Person", styles["rc-fdo-main"]),
                                    XBox(6.7, True if self.data["by_mail"] else False),
                                    Paragraph("By Mail", styles["rc-fdo-main"]),
                                ]
                            ],
                            style=extend_table_style(styles["rc-main-table"], [
                                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                            ]),
                            colWidths=(3 * mm, 12 * mm, 3 * mm, 14 * mm, 3 * mm, 14 * mm,)
                        ),
                        None,
                        XBox(6.7, True if self.data["trial_verdict"] else False),
                        Paragraph("<b>TRIAL VERDICT</b>", styles["rc-fdo-main"]),
                        None,
                        XBox(6.7, True if self.data["other_disposition"] else False),
                        Paragraph("<b>OTHER DISPOSITION:</b>", styles["rc-fdo-main"]),
                    ],
                    [
                        None,
                        XBox(6.7, True if self.data["negotiated"] else False),
                        Paragraph("Negotiated", styles["rc-fdo-main"]),
                        XBox(6.7, True if self.data["guilty_on_citations"] else False),
                        Paragraph("Guilty on Citation No(s).:", styles["rc-fdo-main"]),
                        None,
                        XBox(6.7, True if self.data["nolle_prosequi_order_on_citations"] else False),
                        Paragraph("Nolle Prosequi Order on Citation", styles["rc-fdo-main"]),
                    ],
                    [
                        None,
                        XBox(6.7, True if self.data["non_negotiated"] else False),
                        Paragraph("Non-Negotiated", styles["rc-fdo-main"]),
                        Paragraph(
                            "%s" % ', '.join(self.data["guilty_on_citation_numbers"]),
                            extend_style(styles["rc-fdo-main"], fontSize=styles["rc-fdo-main"].fontSize - 1)
                        ),
                        None,
                        None,
                        Table(
                            [
                                [
                                    Paragraph("No(s).:", styles["rc-fdo-main"]),
                                    Paragraph(
                                        "%s" % ', '.join(self.data["nolle_prosequi_order_on_citations"]),
                                        extend_style(styles["rc-fdo-main"], fontSize=styles["rc-fdo-main"].fontSize - 1)
                                    ),
                                ]
                            ],
                            style=extend_table_style(styles["rc-main-table"], [
                                ("LINEBELOW", (1, 0), (1, 0), 0.5, "black"),
                            ]),
                            colWidths=(10 * mm, 42 * mm)
                        ),
                        None,
                    ],
                    [
                        None,
                        XBox(6.7, True if self.data["guilty"] else False),
                        Paragraph("Guilty", styles["rc-fdo-main"]),
                        XBox(6.7, True if self.data["non_guilty_on_citations"] else False),
                        Paragraph("Not Guilty on Citation No(s).:", styles["rc-fdo-main"]),
                        None,
                        Paragraph("See County's Motion and Order", styles["rc-fdo-main"]),
                    ],
                    [
                        None,
                        XBox(6.7, True if self.data["non_contest"] else False),
                        Paragraph("No Contest", styles["rc-fdo-main"]),
                        Paragraph(
                            "%s" % ', '.join(self.data["non_guilty_on_citation_numbers"]),
                            extend_style(styles["rc-fdo-main"], fontSize=styles["rc-fdo-main"].fontSize - 1)
                        ),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("SPAN", (3, 2), (4, 2)),
                    ("LINEBELOW", (3, 2), (4, 2), 0.5, "black"),
                    ("SPAN", (6, 3), (7, 3)),
                    ("SPAN", (3, 4), (4, 4)),
                    ("LINEBELOW", (3, 4), (4, 4), 0.5, "black"),
                ]),
                colWidths=(8.8 * mm, 4 * mm, 47 * mm, 4 * mm, 43 * mm, 16.5 * mm, 4 * mm, 48 * mm),
                hAlign="LEFT",
            )
        )
        elems.append(Spacer(0, 5 * mm))
        elems.append(
            Table(
                [
                    [
                        None,
                        None,
                        None,
                        None,
                        None,
                    ],
                    [
                        None,
                        XBox(6.7, True if self.data["defendant_filed_bond_forfeiture_form"] else False),
                        Paragraph("<b>Defendant filed Bond Forfeiture Form</b>", styles["rc-fdo-main"]),
                        XBox(
                            6.7,
                            True if self.data["defendant_filed_acknowledgment_of_waiver_of_rights_form"] else False
                        ),
                        Paragraph(
                            "<b>Defendant filed Acknowledgment of Waiver of Rights Form</b>",
                            styles["rc-fdo-main"]
                        ),
                    ],
                    [
                        None
                    ],
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LINEBELOW", (1, 0), (4, 0), 0.6, "black"),
                    ("LINEBELOW", (1, 2), (4, 2), 0.6, "black"),
                ]),
                colWidths=(9.7 * mm, 3.2 * mm, 61 * mm, 3.2 * mm, 96.5 * mm),
                rowHeights=(3.8 * mm, 6.2 * mm, 3.8 * mm),
                hAlign="LEFT"
            )
        )
        elems.append(Spacer(0, 1 * mm))
        return elems

    def _section_section_2(self):
        elems = list()
        elems.append(
            Paragraph(
                "<b>THE FOLLOWING JUDGMENT IS HEREBY ORDERED IN THIS ACTION</b>:",
                styles["rc-main"]
            )
        )
        elems.append(Spacer(0, 5 * mm))
        ps_title = extend_style(styles["rc-fdo-main"], alignment=TA_CENTER)
        data = [
            [
                Paragraph("<b>Ordinance Citation/Count No.</b>", ps_title),
                Paragraph("<b>Disposition</b><br />Guilty, No Contest, Nolle Pros., Bond Forfeiture", ps_title),
                Paragraph("<b>Length of Sentence</b><br />Days or Months", ps_title),
                Table(
                    [
                        [
                            Paragraph("<b>Computation of Sentence</b>", ps_title)
                        ],
                        [
                            Paragraph(
                                "Probation, Suspended, Commuted to Time Served, Concurrent, Consecutive",
                                extend_style(ps_title, fontSize=ps_title.fontSize - 1,
                                             leading=ps_title.leading - 1))
                        ]
                    ],
                    style=styles["rc-main-table"]
                ),
                Paragraph("<b>Fine & Fine Surcharges</b>", ps_title),
                Paragraph("<b>Community Service Hrs.</b>", ps_title),
                Paragraph("<b>Restitution</b>", ps_title),
            ]
        ]
        ps = extend_style(styles["rc-fdo-main"], fontSize=9)
        for citation in self.data["citation_table"]:
            data.append([
                Paragraph("<font size=10><seq>.</font> <b>%s</b>" % citation["citation_number"], ps),
                Paragraph("%s" % citation["disposition"], ps),
                Paragraph("%s" % citation["length_of_sentence"], ps),
                Paragraph("%s" % citation["computation_of_sentence"], ps),
                Paragraph("$ %s" % citation["fine"], ps),
                Paragraph("%s" % citation["community_service_hours"], ps),
                Paragraph("%s" % citation["restitution"], ps),
                Spacer(0, 8.2 * mm)
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
                colWidths=(35 * mm, 22.3 * mm, 23.9 * mm, 33.3 * mm, 22.2 * mm, 22.2 * mm, 20.6 * mm, 1),
                hAlign="LEFT"
            )
        )
        return elems

    def _section_section_3(self):
        ps = styles["rc-fdo-main"]
        elems = [Spacer(0, 1.1 * mm)]
        elems.append(
            Paragraph("<b>IT IS FURTHER ORDERED that (Check only the section that applies)</b>:", ps)
        )
        line_data = list()
        line_data.append(
            Table(
                [

                    [
                        XBoxParagraph(
                            "<seq id=\"s3_l0\">. The Defendant is to receive a sentence of <b>TIME SERVED</b> for pretrial confinement served in the custody of the Rockdale County Jail or such other institution as the Sheriff of Rockdale County or the Court may direct, to be computed as provided by law; <b>OR</b>",
                            extend_style(ps, alignment=TA_JUSTIFY),
                            6.5,
                            True if self.data["1"] else False,
                        )
                    ],

                ],
                style=styles["rc-main-table"],
                spaceAfter=1.9 * mm
            )
        )
        line_data.append(
            Table(
                [
                    [
                        XBoxParagraph(
                            "<seq id=\"s3_l0\">. The Defendant is to serve 10 (ten) days of this sentence in confinement, which is suspended in its entirety and not subject to a suspension revocation, provided the Defendant makes full payment to the Court of all restitution,",
                            extend_style(ps, alignment=TA_JUSTIFY, justifyLastLine=1),
                            6.5,
                            True if self.data["2"] else False,
                        )
                    ],
                    [
                        Table(
                            [
                                [
                                    Paragraph("fines and fine surcharges ordered no later than", ps),
                                    Paragraph("%s" % self.data["2_order_date"], extend_style(ps, alignment=TA_CENTER)),
                                    Paragraph("by 4:00 p.m.; <b>OR</b>", ps),
                                ],
                            ],
                            style=extend_table_style(styles["rc-main-table"], [
                                ("LINEBELOW", (1, 0), (1, 0), 0.5, "black"),
                                ("LEFTPADDING", (2, 0), (2, 0), 1 * mm),
                            ]),
                            colWidths=(66.4 * mm, 35.1 * mm, None)
                        )
                    ]
                ],
                style=styles["rc-main-table"],
                spaceAfter=1.9 * mm,
            )
        )
        line_data.append(
            Table(
                [
                    [
                        Table(
                            [
                                [
                                    XBoxParagraph(
                                        "<seq id=\"s3_l0\">. The Defendant is to serve",
                                        extend_style(ps, alignment=TA_JUSTIFY, justifyLastLine=1),
                                        6.5,
                                        True if self.data["3"] else False
                                    ),
                                    Paragraph("%s" % self.data["3_month"], extend_style(ps, alignment=TA_CENTER)),
                                    Paragraph(
                                        "months on probation, provided that the Defendant remains in",
                                        extend_style(ps, alignment=TA_JUSTIFY, justifyLastLine=1),
                                    ),
                                ],

                            ],
                            style=extend_table_style(styles["rc-main-table"], [
                                ("LINEBELOW", (1, 0), (1, 0), 0.5, "black"),
                                ("RIGHTPADDING", (0, 0), (0, 0), 2 * mm),
                                ("LEFTPADDING", (2, 0), (2, 0), 2 * mm),
                            ]),
                            colWidths=(50.5 * mm, 19.2 * mm, None)
                        )
                    ],
                    [
                        Paragraph(
                            "compliance with the below General and Special Conditions of Probation/Suspension, including but not limited to the payment of all restitution, fines, fine surcharges, probation supervision fees, community service hours and other General and Special Conditions of Probation/Suspension ordered herein; <b>OR</b>",
                            extend_style(ps, alignment=TA_JUSTIFY),
                        )
                    ]
                ],
                style=styles["rc-main-table"],
                spaceAfter=1.9 * mm,
            )
        )
        line_data.append(
            Table(
                [
                    [
                        Table(
                            [
                                [
                                    XBoxParagraph(
                                        "<seq id=\"s3_l0\">. The Defendant is to serve",
                                        extend_style(ps, alignment=TA_JUSTIFY, justifyLastLine=1),
                                        6.5,
                                        True if self.data["4"] else False
                                    ),
                                    Paragraph("%s" % self.data["4_month"], extend_style(ps, alignment=TA_CENTER)),
                                    Paragraph(
                                        "months on probation, which will be:",
                                        extend_style(ps, alignment=TA_JUSTIFY, justifyLastLine=1),
                                    ),
                                    XBox(6.5, True if self.data["4_suspended"] else False),
                                    Paragraph("suspended <b>or</b>", ps),
                                    XBox(6.5, True if self.data["4_terminated"] else False),
                                    Paragraph("terminated", ps),
                                ],
                            ],
                            style=extend_table_style(styles["rc-main-table"], [
                                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                                ("LINEBELOW", (1, 0), (1, 0), 0.5, "black"),
                                ("RIGHTPADDING", (0, 0), (0, 0), 1.5 * mm),
                                ("LEFTPADDING", (2, 0), (2, 0), 1 * mm),
                                ("RIGHTPADDING", (2, 0), (2, 0), 1.5 * mm),
                            ]),
                            colWidths=(46.5 * mm, 19.4 * mm, 55 * mm, 4.5 * mm, 20.5 * mm, 4.5 * mm, None)
                        )
                    ],
                    [
                        Paragraph(
                            "upon the Defendant's payment of all restitution, fines, fine surcharges, probation supervision fees and completion of community service hours ordered herein; <b>OR</b>",
                            extend_style(ps, alignment=TA_JUSTIFY),
                        )
                    ]
                ],
                style=styles["rc-main-table"],
                spaceAfter=1.9 * mm,
            )
        )
        line_data.append(
            Table(
                [
                    [
                        Table(
                            [
                                [
                                    XBoxParagraph(
                                        "<seq id=\"s3_l0\">. The Defendant is to serve the first",
                                        extend_style(ps, alignment=TA_JUSTIFY, justifyLastLine=1),
                                        6.5,
                                        True if self.data["5"] else False
                                    ),
                                    Paragraph("%s" % self.data["5_day"], extend_style(ps, alignment=TA_CENTER)),
                                    Paragraph(
                                        "days of this sentence in confinement and the remainder",
                                        extend_style(ps, alignment=TA_JUSTIFY, justifyLastLine=1),
                                    ),
                                    XBox(6.5, True if self.data["5_probation"] else False),
                                    Paragraph("on", ps),
                                ],
                            ],
                            style=extend_table_style(styles["rc-main-table"], [
                                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                                ("LINEBELOW", (1, 0), (1, 0), 0.5, "black"),
                                ("RIGHTPADDING", (0, 0), (0, 0), 1.5 * mm),
                                ("LEFTPADDING", (2, 0), (2, 0), 1 * mm),
                            ]),
                            hAlign="LEFT",
                            colWidths=(57.5 * mm, 19.3 * mm, 81 * mm, 4.5 * mm, None)
                        ),
                    ],
                    [
                        Table(
                            [
                                [
                                    Paragraph("probation <b>or</b>", ps),
                                    XBox(6.5, True if self.data["5_suspended"] else False),
                                    Paragraph("suspended <b>or</b>", ps),
                                    XBox(6.5, True if self.data["5_terminated"] else False),
                                    Paragraph(
                                        "terminated, provided that the Defendant remains in compliance with the below",
                                        ps
                                    ),
                                ],
                                [
                                    Paragraph(
                                        "General and Special Conditions of Probation/Suspension, including but not limited to the payment of all restitution, fines, fine surcharges, probation supervision fees, community service hours and the other General and Special conditions of Probation/Suspension ordered herein.",
                                        extend_style(ps, alignment=TA_JUSTIFY),
                                    ),
                                ],
                                [
                                    None
                                ]
                            ],
                            style=extend_table_style(styles["rc-main-table"], [
                                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                                ("SPAN", (0, 1), (-1, 1)),
                                ("LINEBELOW", (0, 2), (-1, 2), 0.5, "black"),
                            ]),
                            colWidths=(18 * mm, 4 * mm, 19 * mm, 4 * mm, None)
                        )
                    ],
                ],
                style=styles["rc-main-table"],
                spaceAfter=1.9 * mm,
            )
        )
        elems.append(
            Table(
                [
                    [
                        None,
                        line_data
                    ]
                ],
                style=styles["rc-main-table"],
                colWidths=(9.5 * mm, 165.5 * mm),
                hAlign="LEFT"
            )
        )
        elems.append(Spacer(0, 1 * mm))
        return elems

    def _section_section_4(self):
        ps = extend_style(styles["rc-fdo-main"], alignment=TA_JUSTIFY)
        data = list()
        data.append(
            Paragraph(
                "<b>FINES SURCHARGES OR ADD-ONS</b>:&nbsp;&nbsp;The Court assesses all fines surcharges or add-ons as required by the laws of the State of Georgia and as applicable to the Citation/Case No(s). for which the Defendant has been convicted.",
                ps
            )
        )
        t1 = Table(
            [
                data
            ],
            style=styles["rc-main-table"],
            colWidths=174 * mm,
            hAlign="LEFT",
            spaceAfter=1.9 * mm
        )
        return [t1]

    def _section_section_5(self):
        def create_victim_table(victim, num, ps):
            address_parts = victim["victim_address"].split(",")
            vt = Table(
                [
                    [
                        Paragraph("(%s) Victim Name:" % unichr(num), ps),
                        Paragraph("%s" % victim["victim_name"], ps),
                        None,
                        None,
                    ],
                    [
                        Paragraph("Victim Mailing Address:", ps),
                        None,
                        None,
                        Paragraph("%s" % address_parts[0], ps),
                    ],
                    [
                        Paragraph("%s" % ", ".join(address_parts[1:]), ps),
                    ],
                    [
                        Paragraph("Ordered Restitution:&nbsp;&nbsp;$", ps),
                        None,
                        Paragraph("%s" % victim["amount"], ps),
                        None,
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("SPAN", (1, 0), (-1, 0)),
                    ("LINEBELOW", (1, 0), (-1, 0), 0.5, "black"),
                    ("SPAN", (0, 1), (2, 1)),
                    ("LINEBELOW", (3, 1), (-1, 1), 0.5, "black"),
                    ("SPAN", (0, 2), (-1, 2)),
                    ("LINEBELOW", (0, 2), (-1, 2), 0.5, "black"),
                    ("SPAN", (0, 3), (1, 3)),
                    ("SPAN", (2, 3), (-1, 3)),
                    ("LINEBELOW", (2, 3), (-1, 3), 0.5, "black"),
                ]),
                colWidths=(25.1 * mm, 8.5 * mm, 3.8 * mm, None),
                rowHeights=5.5 * mm,
            )
            return vt

        ps = extend_style(styles["rc-fdo-main"], alignment=TA_JUSTIFY)
        elems = list()
        data = list()
        data.append(
            Paragraph(
                "<b>RESTITUTION</b>:&nbsp;&nbsp;The Defendant must pay the ordered restitution as specified by the Court herein or within a period of the first three months of the probated portion of the sentence if no other period of time is specified.&nbsp;&nbsp;The Defendant must provide the restitution payment as follows:",
                ps
            )
        )
        victim_data = list()
        victim_nums = len(self.data["victims"])
        num = 0x61
        for i in range(0, victim_nums, 2):
            try:
                victim_data.append([
                    create_victim_table(self.data["victims"][i], num, ps),
                    None,
                    create_victim_table(self.data["victims"][i + 1], num + 1, ps),
                ])
                num += 2
            except IndexError:
                victim_data.append(
                    [create_victim_table(self.data["victims"][i], num, ps), None, None]
                )
                num += 1
        elems.append(
            Table(
                [
                    [
                        Paragraph(
                            "<b>RESTITUTION</b>:&nbsp;&nbsp;The Defendant must pay the ordered restitution as specified by the Court herein or within a period of the first three months of the probated portion of the sentence if no other period of time is specified.&nbsp;&nbsp;The Defendant must provide the restitution payment as follows:",
                            ps
                        )
                    ],
                    [
                        Table(
                            [
                                [
                                    None,
                                    Table(
                                        [
                                            [
                                                XBox(6.5, True if self.data["pay_to_court"] else False),
                                                Paragraph("Pay to Court <b>OR</b>", style=styles["rc-fdo-main"]),
                                                XBox(6.5, True if self.data["pay_to_probation"] else False),
                                                Paragraph("Pay to Probation <b>OR</b>", style=styles["rc-fdo-main"]),
                                                XBox(6.5, True if self.data["pay_to_victim"] else False),
                                                Paragraph(
                                                    "Pay directly to victim(s).&nbsp;&nbsp;The victim(s) are identified as:",
                                                    style=styles["rc-fdo-main"]),
                                            ]
                                        ],
                                        style=extend_table_style(styles["rc-main-table"], [
                                            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                                        ]),
                                        colWidths=(3.2 * mm, 26.5 * mm, 3.2 * mm, 32.2 * mm, 3.2 * mm, None),
                                    )
                                ],
                                [
                                    None,
                                    Table(
                                        victim_data,
                                        style=styles["rc-main-table"],
                                        colWidths=(71 * mm, 17.8 * mm, 71 * mm)
                                    )
                                ]
                            ],
                            style=styles["rc-main-table"],
                            colWidths=(9.5 * mm, None),
                        )
                    ]
                ],
                style=styles["rc-main-table"],
                colWidths=174 * mm,
                hAlign="LEFT",
                spaceAfter=1.2 * mm
            )
        )
        return elems

    def _section_section_6(self):
        data = list()
        data.append(
            Paragraph(
                "<b>COMMUNITY SERVICE HOURS</b>:&nbsp;&nbsp;The Defendant must complete all community service hours imposed by the Court as specified herein or within a period of the first three months of the probated portion of thesentence if no other period of time is specified.&nbsp;&nbsp;All community service locations and work to be performed must be pre-approved by the Probation Officer/Supervisor.",
                styles["rc-fdo-main"]
            )
        )
        t1 = Table(
            [
                data
            ],
            style=styles["rc-main-table"],
            colWidths=174 * mm,
            hAlign="LEFT",
            spaceAfter=1.5 * mm
        )
        return [t1]

    def _section_section_7(self):
        data = list()
        data.append(
            Paragraph(
                "<b>GENERAL CONDITIONS OF PROBATION/SUSPENSION</b>:&nbsp;&nbsp;The Defendant is subject to arrest and revocation for any violation of the probated or suspended sentence. The Defendant must comply with the following General Conditions: 1) Do not violate the criminal laws of any governmental unit; 2) Avoid injurious and vicious habits-especially alcoholic intoxication, narcotics and other dangerous drugs unless prescribed lawfully; 3) Avoid persons or places of disreputable or harmful character; 4) Report to the Probation Officer/Supervisor as directed and permit him/her to visit you at home or elsewhere; 5) Work faithfully at suitable employment insofar as possible; 6) Do not change your residence, move outside the jurisdiction of the Court or leave the State for any period of time without prior permission of the Probation Officer/Supervisor; 7) Pay restitution, fines, fine surcharges and monthly probation supervision fees; and 8) Agree to the conversion of fines and surcharges to community service hours as defined by law and the Probation Officer/Supervisor may direct.",
                extend_style(styles["rc-fdo-main"], alignment=TA_JUSTIFY)
            )
        )
        t1 = Table(
            [
                data
            ],
            style=styles["rc-main-table"],
            colWidths=174 * mm,
            hAlign="LEFT",
            spaceAfter=1.5 * mm
        )
        return [t1]

    def _section_section_8(self):
        ps = styles["rc-fdo-main"]
        elems = list()
        elems.append(
            Table(
                [
                    [
                        Paragraph(
                            "<b>SPECIAL CONDITIONS OF PROBATION/SUSPENSION</b>:&nbsp;&nbsp;The Defendant is subject to arrest and revocation for any violation of the probated or suspended sentence.&nbsp;&nbsp;The Defendant must comply with the following Special Conditions:",
                            extend_style(ps, alignment=TA_JUSTIFY)
                        ),
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                    ],
                    [
                        None,
                        XBox(6, True if self.data["stay_away"] else False),
                        Paragraph("Stay away from the Victim(s):", ps),
                        None,
                        None,
                        Paragraph("%s" % ", ".join(self.data["stay_away_victims"]), ps),

                    ],
                    [
                        None,
                        XBox(6, True if self.data["not_return"] else False),
                        Paragraph("Not return to the following address:", ps),
                        None,
                        None,
                        None,
                        Paragraph("%s" % self.data["not_return_address"], ps),
                    ],
                    [
                        None,
                        XBox(6, True if self.data["not_commit"] else False),
                        Paragraph(
                            "Not commit the same type of offense(s) for which the Defendant has been convicted herein.",
                            ps
                        ),
                    ],
                    [
                        None,
                        XBox(6, True if self.data["pay_fine"] else False),
                        Paragraph(
                            "Pay restitution, fines, fine surcharges and monthly probation supervision fees.",
                            ps
                        ),
                    ],
                    [
                        None,
                        XBox(6, True if self.data["complete_service"] else False),
                        Paragraph("Complete community service hours.", ps),
                    ],
                    [
                        None,
                        XBox(6, True if self.data["other"] else False),
                        Paragraph("Other: ", ps),
                        Paragraph("%s" % self.data["other_text"], ps),
                    ],
                    [
                        None,
                        XBox(6, True if self.data["shall_appear"] else False),
                        Paragraph(
                            "Defendant shall appear before the Court for a post-sentence compliance hearing at 8:30 a.m. on date:",
                            ps
                        ),
                    ],
                    [
                        None,
                        Paragraph("%s" % self.data["shall_appear_date"], ps),
                        None,
                        None,
                        Paragraph(
                            ", only if the Defendant has failed to pay the restitution and/or fine and surcharges in FULL or has other",
                            ps
                        ),
                    ],
                    [
                        None,
                        Paragraph("special conditions that require a status update.", ps),
                    ],
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0.25 * mm),
                    ("SPAN", (0, 0), (-1, 0)),
                    ("SPAN", (2, 1), (4, 1)),
                    ("SPAN", (5, 1), (-1, 1)),
                    ("LINEBELOW", (5, 1), (6, 1), 0.5, "black"),
                    ("SPAN", (2, 2), (5, 2)),
                    ("LINEBELOW", (6, 2), (6, 2), 0.5, "black"),
                    ("SPAN", (2, 3), (-1, 3)),
                    ("SPAN", (2, 4), (-1, 4)),
                    ("SPAN", (2, 5), (-1, 5)),
                    ("SPAN", (3, 6), (7, 6)),
                    ("LINEBELOW", (3, 6), (7, 6), 0.5, "black"),
                    ("SPAN", (2, 7), (-1, 7)),
                    ("SPAN", (1, 8), (3, 8)),
                    ("LINEBELOW", (1, 8), (3, 8), 0.5, "black"),
                    ("SPAN", (4, 8), (-1, 8)),
                    ("SPAN", (1, 9), (-1, 9)),
                ]),
                colWidths=(9.5 * mm, 3 * mm, 10 * mm, 5 * mm, 30 * mm, 7.5 * mm, 70 * mm, 39 * mm),
                hAlign="LEFT",
                spaceAfter=1.5 * mm
            )
        )
        signature_label = "Defendant's Attorney" if self.data["defendant_represented_by_attorney"] else "Defendant"
        elems.append(
            Table(
                [
                    [
                        Paragraph("The Defendant represented by:", ps),
                        XBox(6.7, True if self.data["defendant_represented_by_self"] else False),
                        Paragraph("Self <b>OR </b>", ps),
                        XBox(6.7, True if self.data["defendant_represented_by_attorney"] else False),
                        Paragraph("Attorney at Law: ", ps),
                        SignatureRect(75 * mm, 3.8 * mm, label=signature_label)
                    ],
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LINEBELOW", (5, 0), (5, 0), 0.5, "black"),
                ]),
                colWidths=(44.5 * mm, 3 * mm, 13 * mm, 3 * mm, 25 * mm, 76 * mm),
                hAlign="LEFT"
            )
        )
        date_parts = self.data["order_date"].split("/")
        date_parts[0] = int(date_parts[0])
        date_suff = ["th", "st", "nd", "rd"]
        try:
            date_parts[0] = "%s%s" % (date_parts[0], date_suff[date_parts[0]])
        except IndexError:
            date_parts[0] = "%s%s" % (date_parts[0], date_suff[0])
        date_parts[1] = datetime.date(1900, int(date_parts[1]), 1).strftime('%B')
        elems.append(
            Table(
                [
                    [
                        None,
                        Paragraph("<b>SO ORDERED</b> this", ps),
                        Paragraph("%s" % date_parts[0], extend_style(ps, alignment=TA_CENTER)),
                        Paragraph("of", extend_style(ps, alignment=TA_CENTER)),
                        Paragraph("%s" % date_parts[1], extend_style(ps, alignment=TA_CENTER)),
                        Paragraph(", %s." % date_parts[2], ps),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (2, 0), (2, 0), 0.5, "black"),
                    ("LINEBELOW", (4, 0), (4, 0), 0.5, "black"),
                ]),
                colWidths=(22.5 * mm, 30 * mm, 12.5 * mm, 4.5 * mm, 30 * mm, 12 * mm),
                hAlign="LEFT"
            )
        )
        elems.append(Spacer(0, 1 * mm))
        elems.append(SignatureRect(88 * mm, 7 * mm, label="Magistrate Judge", leftIndent=86 * mm))
        elems.append(
            Table(
                [
                    [
                        None,
                        XBox(6.7, True if self.data["judge_is_phinia_aten"] else False),
                        Paragraph("Chief Magistrate Judge Phinia Aten", ps),
                        None,
                    ],
                    [
                        None,
                        XBox(6.7, True if self.data["judge_other"] else False),
                        Paragraph("Magistrate Judge:", ps),
                        Paragraph("%s" % self.data["judge_other_name"], ps),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEABOVE", (1, 0), (3, 0), 0.9, "black"),
                    ("LINEBELOW", (3, 1), (3, 1), 0.5, "black"),
                    ("LEFTPADDING", (2, 0), (2, -1), 1.5 * mm),
                    ("LEFTPADDING", (3, 1), (3, 1), 0.5 * mm),
                    ("RIGHTPADDING", (1, 0), (1, -1), 2 * mm),
                    ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                    ("VALIGN", (1, 0), (1, -1), "MIDDLE"),
                    ("SPAN", (2, 0), (3, 0)),
                ]),
                colWidths=(86 * mm, 11 * mm, 27 * mm, 50 * mm),
                hAlign="LEFT"
            )
        )
        return elems

    def _section_section_9(self):
        elems = [Spacer(0, 7.8 * mm)]
        elems.append(
            Table(
                [
                    [
                        Paragraph(
                            "<b>DEFENDANT'S ACKNOWLEDGMENT</b>:&nbsp;&nbsp;I have read the terms of this sentence or had them explained to me.&nbsp;&nbsp;If all or any part of this sentence is terminated, probated or suspended, I certify that I understand the meaning of this termination, probation or suspension and the conditions of same.&nbsp;&nbsp;I understand that violation of the general or special conditions of my probation/suspension could result in revocation of some, or even all, of the remaining time of my probated or suspended sentence.",
                            styles["rc-fdo-main"]
                        )
                    ],
                    [
                        Table(
                            [
                                [
                                    None,
                                    SignatureRect(65 * mm, 4.3 * mm, label="Defendant"),
                                    None,
                                    SignatureRect(82 * mm, 4.3 * mm, label="Probation Officer/Supervisor")
                                ],
                                [
                                    None,
                                    Paragraph("DEFENDANT'S SIGNATURE", styles["rc-fdo-main"]),
                                    None,
                                    Paragraph("PROBATION OFFICER/SUPERVISOR'S SIGNATURE", styles["rc-fdo-main"]),
                                ],
                            ],
                            style=extend_table_style(styles["rc-main-table"], [
                                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                ("LINEBELOW", (1, 0), (1, 0), 0.5, "black"),
                                ("LINEBELOW", (3, 0), (3, 0), 0.5, "black"),
                            ]),
                            colWidths=(10 * mm, 65 * mm, 11 * mm, 82 * mm),
                            rowHeights=4.3 * mm
                        )
                    ]
                ],
                style=styles["rc-main-table"],
                colWidths=176 * mm,
                hAlign="LEFT"
            )
        )
        return elems
