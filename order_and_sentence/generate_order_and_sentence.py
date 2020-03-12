# coding=utf-8
from document_specific_styles import styles, extend_style, extend_table_style
from common.signatures import SignatureDocTemplate, SignatureRect
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.platypus import PageTemplate, Frame, Flowable, Paragraph, Table, Spacer
import datetime
from copy import copy
import cStringIO
import io


def generate_order_and_sentence(pdf_dict, title=None, author=None):
    cr = OrderSentenceReport(title, author)
    buff = cStringIO.StringIO()
    return cr.create_report(pdf_dict, buff)


class XBoxParagraph(Paragraph):
    def __init__(self, text, style, size, checked, **kwargs):
        new_style = copy(style)
        Paragraph.__init__(self, text, new_style, **kwargs)
        if self.style.firstLineIndent < size:
            self.style.firstLineIndent = size * 1.5
        self.xbox = XBox(size, checked)

    def draw(self):
        Paragraph.draw(self)
        self.xbox.offset = (self.style.leftIndent, self.height - self.xbox.width * 1.5)
        self.xbox.canv = self.canv
        self.xbox.draw()


class XBox(Flowable):
    def __init__(self, size, checked=None):
        Flowable.__init__(self)
        self.width = size
        self.height = size
        self.size = size
        self.checked = checked

    def draw(self):
        self.canv.saveState()
        self.canv.setLineWidth(0.11 * self.size)
        self.canv.rect(0, 0, self.width * 0.89, self.height * 0.89)
        if self.checked is True:
            self.check()
        self.canv.restoreState()

    def check(self):
        self.canv.setFont('Times-Bold', self.size * 0.85)
        to = self.canv.beginText(self.width * 0.13, self.height * 0.155)
        to.textLine("X")
        self.canv.drawText(to)


class OrderSentenceReport:
    def __init__(self, title=None, author=None):
        self.page_size = letter
        self.page_margin = (12.2 * mm, 7.9 * mm)
        self.sections = ["header", "section_1", "section_2", "section_3", "section_4"]
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
        dt = datetime.datetime.now().strftime("%m/%d/%Y at %I:%M %p")
        p = Paragraph(dt, style=extend_style(
            styles["oas-main"],
            alignment=TA_CENTER,
        ))
        p_height = p.wrapOn(canv, doc.width, doc.height)[1]
        p.drawOn(canv, doc.leftMargin, doc.bottomMargin - p_height)

    def _section_header(self):
        ps = styles["oas-doc-header"]
        elems = [
            Table(
                [
                    [
                        [
                            Spacer(0, 4.5 * mm),
                            Paragraph("CITY OF BROOKHAVEN<br />vs.<br />%s" % self.data["defendant_name"], ps)
                        ],
                        Paragraph("<b>BROOKHAVEN MUNICIPAL COURT<br />COUNTY OF DEKALB<br />STATE OF GEORGIA</b>",
                                  extend_style(ps, fontSize=(ps.fontSize * 1.1))),
                        None
                    ]
                ],
                style=styles["oas-main-table"],
                colWidths=[58 * mm, 95 * mm, None],
            ),
            Paragraph("<b>ORDER AND SENTENCE</b>",
                      extend_style(ps, fontSize=(ps.fontSize * 1.5), firstLineIndent=20 * mm))
        ]
        return elems

    def _section_section_1(self):
        elems = list()
        elems.append(Spacer(0, 4.6 * mm))
        ps = extend_style(styles["oas-main"], fontSize=8)
        ps_center = extend_style(ps, alignment=TA_CENTER)
        ps_right = extend_style(ps, alignment=TA_RIGHT)
        data = [
            [
                Paragraph("<b><u>CITATION</u></b>", ps),
                Paragraph("<b><u>OFFENSE</u></b>", ps),
                None,
                Paragraph("<b><u>DISPOSITION</u></b>", ps_center),
                None,
                Paragraph("<b><u>CASE BALANCE</u></b>", ps),
                None,
            ]
        ]
        for citation in self.data["citation_table"]:
            data.append([
                Paragraph("%s" % citation["citation_number"], ps),
                Paragraph("%s" % citation["offense_number"], ps),
                Paragraph("%s" % citation["offense_description"], ps),
                Paragraph("%s" % citation["disposition"], ps_center),
                None,
                Paragraph("$ %s" % citation["balance"], ps),
                None
            ])
        elems.append(
            Table(
                data,
                style=extend_table_style(styles["oas-main-table"], [
                    ("LEFTPADDING", (5, 1), (5, -1), 1.8 * mm),
                ]),
                colWidths=[21.8 * mm, 17.1 * mm, 100.5 * mm, 22.3 * mm, 1.9 * mm, 22.5 * mm, None],
                rowHeights=4.22 * mm,
                spaceAfter=1 * mm
            )
        )
        elems.append(
            Table(
                [
                    [
                        Paragraph("TOTAL AMOUNT OF FINE(S) / FEE(S)", ps_right),
                        None,
                        Paragraph("$ %s" % self.data["total_amount"], ps),
                        None
                    ],
                    [
                        Paragraph("CASH BONDS RECEIVED", ps_right),
                        None,
                        Paragraph("$ %s" % self.data["bonds_received"], ps),
                    ]
                ],
                style=extend_table_style(styles["oas-main-table"], [
                    ("LEFTPADDING", (2, 0), (2, -1), 1.8 * mm),
                ]),
                colWidths=[161.8 * mm, 1.9 * mm, 22.5 * mm, None],
                spaceAfter=1 * mm,
            )
        )
        ps = styles["oas-main"]
        ps_center = extend_style(ps, alignment=TA_CENTER)
        elems.append(
            Paragraph(
                "Upon accepting the defendant's above indicated plea or judgment by this court and after reviewing the defendant's criminal history record, it now appears to this Court that acceptance of the defendant's plea would be in the best interest of justice.",
                ps
            )
        )
        elems.extend([
            Spacer(0, 0.75 * mm),
            Table(
                [[
                    Paragraph(
                        "Whereas, the above disposition has been made against the above named defendant, the defendant is hereby sentenced to confinement for a period of",
                        ps
                    ),
                    Paragraph("%s" % self.data["sentence_length"], ps_center),
                    None,
                ]],
                style=extend_table_style(styles["oas-main-table"], [
                    ("LINEBELOW", (1, 0), (1, 0), 0.5, "black"),
                ]),
                colWidths=[170 * mm, 10 * mm, None],
                rowHeights=3.5 * mm
            ),
            Table(
                [[
                    XBoxParagraph(
                        "months", ps, 8.2,
                        True if self.data["sentence_period"] == "months" else False,
                    ),
                    XBoxParagraph(
                        "days", ps, 8.2,
                        True if self.data["sentence_period"] == "days" else False,
                    ),
                    Paragraph(
                        "and ordered to pay a fine in the total amount stated above, of which includes all surcharges pursuant to the Official Code of Georgia Annotated.",
                        ps),
                ]],
                style=styles["oas-main-table"],
                colWidths=[17.5 * mm, 13.5 * mm, None],
                rowHeights=3.25 * mm
            ),
            Table(
                [
                    [
                        Paragraph("Upon service of", ps),
                        Paragraph("%s" % self.data["house_eligable_length"], ps_center),
                        XBoxParagraph(
                            "months", ps, 8.2,
                            True if self.data["house_eligable_period"] == "months" else False,
                        ),
                        XBoxParagraph(
                            "days", ps, 8.2,
                            True if self.data["house_eligable_period"] == "days" else False,
                        ),
                        Paragraph("of the above sentence confined in jail, defendant will serve", ps),
                        Paragraph("%s" % self.data["house_length"], ps_center),
                        XBoxParagraph(
                            "months", ps, 8.2,
                            True if self.data["house_period"] == "months" else False,
                        ),
                        XBoxParagraph(
                            "days", ps, 8.2,
                            True if self.data["house_period"] == "days" else False,
                        ),
                        XBoxParagraph(
                            "hours", ps, 8.2,
                            True if self.data["house_period"] == "hours" else False,
                        ),
                        None,
                    ],
                    [
                        Paragraph(
                            "in house confinement. Defendant shall receive no reduction of total sentence time based upon any credit for good time served if incarcerated. ",
                            ps),
                    ]
                ],
                style=extend_table_style(styles["oas-main-table"], [
                    ("LINEBELOW", (1, 0), (1, 0), 0.5, "black"),
                    ("SPAN", (0, 1), (-1, 1)),
                    ("LEFTPADDING", (2, 0), (2, 0), 3 * mm),
                    ("LINEBELOW", (5, 0), (5, 0), 0.5, "black"),
                    ("LEFTPADDING", (6, 0), (6, 0), 3 * mm),
                ]),
                colWidths=[19.5 * mm, 10.5 * mm, 19.7 * mm, 12.5 * mm, 67 * mm, 10.5 * mm, 20 * mm, 14.7 * mm,
                           12.5 * mm, None],
                rowHeights=3.2 * mm
            ),
            Table(
                [
                    [
                        Paragraph("The defendant is to report to the jail", ps),
                        XBoxParagraph("immediately or", ps, 8.2, self.data["jail_immediate"]),
                        XBoxParagraph("on", ps, 8.2, True if self.data["jail_date"] else False),
                        Paragraph("%s" % self.data["jail_date"], ps_center),
                        Paragraph("at", ps),
                        Paragraph("%s" % self.data["jail_time"], ps_center),
                        Paragraph("to begin service.", ps),
                    ],
                    [
                        Paragraph(
                            "HOWEVER, It is further ordered by the court that the defendant serve the remainder of the sentence on probation; provided that the said defendant complies with the following general and special conditions herein imposed by the court as part of this sentence.",
                            styles["oas-main"]),
                    ]
                ],
                style=extend_table_style(styles["oas-main-table"], [
                    ("SPAN", (0, 1), (-1, 1)),
                    ("LINEBELOW", (3, 0), (3, 0), 0.5, "black"),
                    ("LINEBELOW", (5, 0), (5, 0), 0.5, "black"),
                    ("LEFTPADDING", (4, 0), (4, 0), 2.2 * mm),
                    ("LEFTPADDING", (6, 0), (6, 0), 2.2 * mm),
                ]),
                colWidths=[46 * mm, 23 * mm, 8 * mm, 25 * mm, 8.6 * mm, 25.2 * mm, None],
            ),
        ])

        elems.append(Spacer(0, 1 * mm))
        return elems

    def _section_section_2(self):
        elems = [
            Spacer(0, 3 * mm),
            Paragraph("<b>GENERAL CONDITIONS OF PROBATION / SUSPENDED SENTENCE</b>", styles["oas-section-header"]),
            Paragraph(
                "The defendant is hereby granted the privilege of serving all or part of the above stated sentence on probation, subject to the following general conditions:",
                styles["oas-main"]
            ),
            Spacer(0, 1.5 * mm),
        ]
        ps = extend_style(styles["oas-main"], leading=9)
        list_text = [
            "Do not violate the criminal laws of any governmental unit. Must report any arrest and / or citation to probation officer within 48 hours.",
            "Avoid persons or places of disreputable or harmful character.",
            "Report to a probation supervisor as directed and permit such supervisor to visit your home or elsewhere.",
            "Work faithfully at suitable employment insofar as may be possible.",
            "Do not change your present place of residence, move outside the jurisdiction of the Court, or leave the state for any period of time without prior permission of the probation supervisor.",
            "Support your legal dependents to the best of your ability.",
            "Pay a probation supervisor fee of $35.00 a month for probation services provided for the City by an independent corporation pursuant to the Official Code of Georgia  Annotated.",
            "Pay a monthly Crime Victims Compensation Program Fee of $9.00 and pay a $10.00 probation case initiation fee.",
            "Avoid injurious and vicious habits, especially alcoholic intoxication, narcotics, and other dangerous drugs unless prescribed lawfully.",
            "Behave in a truthful and respectful manner towards the probation supervisor.",
        ]
        table_data = list()
        for text in list_text:
            table_data.append([Paragraph("<seq id=\"s2s3_l0\">.", ps), Paragraph(text, ps)])
        elems.append(
            Table(
                table_data,
                style=extend_table_style(styles["oas-main-table"], [
                    ("LEFTPADDING", (0, 0), (0, -1), 7 * mm),
                ]),
                colWidths=[13.5 * mm, None],
            )
        )
        return elems

    def _section_section_3(self):
        elems = [
            Spacer(0, 1.5 * mm),
            Paragraph(
                "<b>SPECIAL CONDITIONS OF PROBATION<br />(conditions are only applicable if checked and will be completed at the defendant's expense)</b>",
                styles["oas-section-header"]
            ),
            Spacer(0, 2.5 * mm),
        ]
        ps = styles["oas-main"]
        ps_center = extend_style(ps, alignment=TA_CENTER)
        list_items = list()
        list_items.append(
            Table(
                [[
                    Paragraph("Pay restitution in the amount of", ps),
                    Paragraph("$ %s" % self.data["11_amount"], ps),
                    Paragraph("to", ps),
                    Paragraph("%s" % self.data["11_party"], ps),
                ]],
                style=extend_table_style(styles["oas-main-table"], [
                    ("LINEBELOW", (1, 0), (1, 0), 0.5, "black"),
                    ("LEFTPADDING", (2, 0), (2, 0), 1 * mm),
                    ("LINEBELOW", (3, 0), (3, 0), 0.5, "black"),
                ]),
                colWidths=[38.4 * mm, 14.5 * mm, 6.5 * mm, None]
            )
        )
        list_items.append(
            Paragraph(
                "Abstain from the use of alcohol and drugs, and be subjected to random alcohol / drug testing of defendant's blood, breath, urine and hair as requested by court, probation, or law enforcement.",
                ps
            ),
        )
        list_items.append(
            Paragraph(
                "Obtain an alcohol and drug use evaluation or anger management evaluation as directed, and follow all further directives for treatment or counseling.",
                ps
            ),
        )
        list_items.append(
            Paragraph(
                "Complete a Risk Reduction course conducted by an agency licensed by the State of Georgia and submit proof to the Georgia Department of Driver Services within 120 days of this plea.",
                ps
            ),
        )
        list_items.append(
            Paragraph(
                "Complete the Interlock Ignition device requirements pursuant to the Official Code of Georgia Annotated.",
                ps
            ),
        )
        list_items.append(
            Table(
                [[
                    Paragraph("Attend", ps),
                    Paragraph("%s" % self.data["16_meetings"], ps_center),
                    Paragraph("Alcoholics / Narcotics Anonymous meetings; and", ps),
                    Paragraph("%s" % self.data["16_sessions"], ps_center),
                    Paragraph("counseling sessions per week.", ps),
                ]],
                style=extend_table_style(styles["oas-main-table"], [
                    ("LINEBELOW", (1, 0), (1, 0), 0.5, "black"),
                    ("LEFTPADDING", (2, 0), (2, 0), 2.5 * mm),
                    ("LINEBELOW", (3, 0), (3, 0), 0.5, "black"),
                    ("LEFTPADDING", (4, 0), (4, 0), 2.5 * mm),
                ]),
                colWidths=[8.7 * mm, 10 * mm, 61.7 * mm, 9.8 * mm, None]
            )
        )
        list_items.append(
            Table(
                [[
                    Paragraph("Successfully complete", ps),
                    Paragraph("%s" % self.data["17_length"], ps_center),
                    XBoxParagraph(
                        "hours", styles["oas-main"], 8.2,
                        True if self.data["17_period"] == "hours" else False
                    ),
                    XBoxParagraph(
                        "days", styles["oas-main"], 8.2,
                        True if self.data["17_period"] == "days" else False
                    ),
                    Paragraph("of community service as directed by the probation supervisor or the City.", ps),
                ]],
                style=extend_table_style(styles["oas-main-table"], [
                    ("LINEBELOW", (1, 0), (1, 0), 0.5, "black"),
                    ("LEFTPADDING", (2, 0), (2, 0), 2.7 * mm),
                ]),
                colWidths=[27.7 * mm, 10 * mm, 17.5 * mm, 14.5 * mm, None]
            )
        )
        list_items.append(
            Table(
                [[
                    Paragraph("%s" % self.data["18_hours"], ps_center),
                    Paragraph(
                        "hours of community service may be completed in lieu of fine at a rate of $10.00 per hour",
                        ps
                    ),
                ]],
                style=extend_table_style(styles["oas-main-table"], [
                    ("LINEBELOW", (0, 0), (0, 0), 0.5, "black"),
                ]),
                colWidths=[10 * mm, None]
            )
        )
        list_items.append(
            Table(
                [[
                    Paragraph(
                        "Defendant shall complete defensive driving school and submit proof of completion to the clerk of Court within",
                        ps
                    ),
                    Paragraph("%s" % self.data["19_days"], ps_center),
                    Paragraph("days of plea", ps),
                ]],
                style=extend_table_style(styles["oas-main-table"], [
                    ("LINEBELOW", (1, 0), (1, 0), 0.5, "black"),
                    ("LEFTPADDING", (2, 0), (2, 0), 2.5 * mm),
                ]),
                colWidths=[124.5 * mm, 10 * mm, None]
            )
        )
        list_items.append(
            Table(
                [
                    [
                        Paragraph("Probation supervisor fee to be suspended after", ps),
                        Paragraph("%s" % self.data["20_months"], ps_center),
                        Paragraph(
                            "months if defendant has paid all of the fine and completed all special conditions of probation,",
                            ps
                        ),
                    ],
                    [Paragraph("with general conditions of probation to remain in effect throughout the term.", ps)]
                ],
                style=extend_table_style(styles["oas-main-table"], [
                    ("LINEBELOW", (1, 0), (1, 0), 0.5, "black"),
                    ("SPAN", (0, 1), (-1, 1)),
                    ("LEFTPADDING", (2, 0), (2, 0), 2.5 * mm),
                ]),
                colWidths=[55.3 * mm, 9.8 * mm, None],
                rowHeights=2.95 * mm
            )
        )
        list_items.append(
            Table(
                [[
                    Paragraph("Probation can be terminated after", ps),
                    Paragraph("%s" % self.data["21_months"], ps_center),
                    Paragraph(
                        "months if defendant has paid all of the fine and completed all special conditions of probation.",
                        ps),
                ]],
                style=extend_table_style(styles["oas-main-table"], [
                    ("LINEBELOW", (1, 0), (1, 0), 0.5, "black"),
                    ("LEFTPADDING", (2, 0), (2, 0), 2.8 * mm),
                ]),
                colWidths=[40.4 * mm, 9.8 * mm, None]
            )
        )
        list_items.append(
            Table(
                [[
                    Paragraph("Pay all fines and surcharges within", ps),
                    Paragraph("%s" % self.data["22_months"], ps_center),
                    Paragraph("months at a rate of ", ps),
                    Paragraph("$ %s" % self.data["16_sessions"], ps),
                    Paragraph("per month. (to be filled out by probation offcer after disposition.)", ps),
                ]],
                style=extend_table_style(styles["oas-main-table"], [
                    ("LINEBELOW", (1, 0), (1, 0), 0.5, "black"),
                    ("LEFTPADDING", (2, 0), (2, 0), 2.8 * mm),
                    ("LINEBELOW", (3, 0), (3, 0), 0.5, "black"),
                    ("LEFTPADDING", (4, 0), (4, 0), 2.2 * mm),
                ]),
                colWidths=[40.4 * mm, 9.8 * mm, 26 * mm, 14.5 * mm, None]
            )
        )
        list_items.append(
            Table(
                [[
                    Paragraph("Complete all special conditions within", ps),
                    Paragraph("%s" % self.data["23_months"], ps_center),
                    Paragraph("months.", ps),
                ]],
                style=extend_table_style(styles["oas-main-table"], [
                    ("LINEBELOW", (1, 0), (1, 0), 0.5, "black"),
                    ("LEFTPADDING", (2, 0), (2, 0), 2.7 * mm),
                ]),
                colWidths=[44.5 * mm, 10 * mm, None]
            )
        )
        list_items.append(
            Paragraph(
                "Defendant shall attend all classes and work successfully toward obtaining a high school diploma or GED during period of probation.",
                ps),
        )
        list_items.append(
            Table(
                [[
                    Paragraph("Other:", ps),
                    Paragraph("%s" % self.data["25_description"], ps),
                ]],
                style=extend_table_style(styles["oas-main-table"], [
                    ("LINEBELOW", (1, 0), (1, 0), 0.5, "black"),
                    ("LEFTPADDING", (1, 0), (1, 0), 0.5 * mm),
                ]),
                colWidths=[8.5 * mm, None]
            )
        )

        table_data = list()
        i = 11
        for item in list_items:
            table_data.append([
                XBox(9.5, self.data[str(i)]), Paragraph("<seq id=\"s2s3_l0\">.", ps_center), item
            ])
            i += 1
        elems.append(
            Table(
                table_data,
                style=extend_table_style(styles["oas-main-table"], [
                    ("ALIGN", (0, 0), (0, -1), "CENTER"),
                    ("BOTTOMPADDING", (1, 0), (-1, -1), 0.45 * mm),
                ]),
                colWidths=[4.3 * mm, 9.3 * mm, None],
            )
        )
        elems.append(Spacer(0, 1.9 * mm))
        elems.append(
            Paragraph(
                "IT IS THE FURTHER ORDER of the Court, and the defendant is hereby advised that the Court may, at any time, upon violation of any of the general or special conditions of probation, revoke any conditions of the probation / suspension herein granted. If such probation / suspension is revoked, the Court may order the execution of the sentence which was originally imposed or any portion thereof in the manner provided by law, after deducting the amount of time the defendant has on probation or suspension.",
                ps),
        )

        return elems

    def _section_section_4(self):
        ps = styles["oas-main"]
        ps_center = extend_style(ps, alignment=TA_CENTER)
        elems = [
            Spacer(0, 7.6 * mm),
            Paragraph("SO ORDERED this the 16th of July, 2019.", extend_style(ps_center, rightIndent=2.5 * mm)),
            Spacer(0, 0.8 * mm),
            Table(
                [
                    [
                        SignatureRect(51 * mm, 16.5 * mm, label="defendent"),
                        None,
                        SignatureRect(50 * mm, 16.5 * mm, label="attorney"),
                        None,
                        SignatureRect(65 * mm, 10 * mm, label="judge"),
                        None,
                    ],
                    [
                        None, None, None, None,
                        Paragraph("Judge, MUNICIPAL COURT OF BROOKHAVEN", ps_center),
                    ],
                    [
                        Paragraph("Defendant", ps_center),
                        None,
                        Paragraph("Defendant's Attorney", ps_center),
                    ]
                ],
                style=extend_table_style(styles["oas-main-table"], [
                    ("SPAN", (0, 0), (0, 1)),
                    ("SPAN", (2, 0), (2, 1)),
                    ("LINEBELOW", (4, 0), (4, 0), 0.6 * mm, "black"),
                    ("LINEBELOW", (0, 1), (0, 1), 0.6 * mm, "black"),
                    ("LINEBELOW", (2, 1), (2, 1), 0.6 * mm, "black"),
                    ("LEFTPADDING", (1, 0), (1, 0), 0.5 * mm),
                    ("TOPPADDING", (4, 1), (4, 1), 0.4 * mm),
                    ("TOPPADDING", (0, 2), (2, 2), 0.4 * mm),
                ]),
                colWidths=[52 * mm, 8 * mm, 51 * mm, 12.4 * mm, 66 * mm, None],
                rowHeights=[11 * mm, 6.5 * mm, 4 * mm]
            )
        ]
        return elems
