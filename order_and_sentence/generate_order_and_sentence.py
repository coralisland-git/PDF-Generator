# coding=utf-8
from document_specific_styles import styles, extend_style, extend_table_style
from common.signatures import SignatureDocTemplate, SignatureRect
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import Paragraph, Table, Spacer, BaseDocTemplate, PageTemplate, Frame
from reportlab.platypus.flowables import HRFlowable, Flowable
from copy import copy
import datetime
import io
import textwrap

try:
    import cStringIO
except ModuleNotFoundError:
    pass


def generate_order_and_sentence(pdf_dict, title=None, author=None):
    report = OrderSentence(title=title, author=author)
    try:
        buff = cStringIO.StringIO()
    except NameError:
        buff = None
    return report.create_report(pdf_dict, buff)


class CustomXBox(Flowable):
    def __init__(self, size=6.0, value=None, x=0, y=0):
        Flowable.__init__(self)
        self.width = self.height = size
        self.value = value
        self.offset = (x, y)

    def __repr__(self):
        return "CustomXBox(w=%s, h=%s, v=%s)" % (self.width, self.height, self.value)

    def draw(self):
        self.canv.saveState()
        self.canv.setLineWidth(self.width * 0.11)
        self.canv.rect(self.offset[0], self.offset[1], self.width, self.height)
        if self.value:
            self.canv.setFont(styles["main"].fontName, self.height * 0.9)
            self.canv.drawCentredString(0.5 * self.width + self.offset[0], 0.2 * self.height + self.offset[1], "X")
        self.canv.restoreState()


class XBoxParagraph(Paragraph):
    def __init__(self, text, style, size, checked, **kwargs):
        new_style = copy(style)
        Paragraph.__init__(self, text, new_style, **kwargs)
        if self.style.firstLineIndent < size:
            self.style.firstLineIndent = size * 1.5
        self.xbox = CustomXBox(size, checked)

    def draw(self):
        Paragraph.draw(self)
        self.xbox.offset = (self.style.leftIndent, self.height - self.xbox.width * 1.5)
        self.xbox.canv = self.canv
        self.xbox.draw()


class PDFReport:
    def __init__(self, page_size=None, page_margin=None, page_padding=None, doc_template_type=None, sections=None,
                 title=None, author=None, subject=None, creator=None):
        self.page_size = page_size if page_size else letter
        # left, top, right, bottom
        self.page_margin = [12.7 * mm, 12.7 * mm, 12.7 * mm, 12.7 * mm]
        self.page_padding = [0, 0, 0, 0]
        if page_margin:
            if isinstance(page_margin, (list, set)) and len(page_margin) == 4:
                self.page_margin = page_margin
            else:
                self.page_margin = [page_margin, page_margin, page_margin, page_margin]
        if page_padding:
            if isinstance(page_padding, (list, set)) and len(page_padding) == 4:
                self.page_padding = page_padding
            else:
                self.page_padding = [page_padding, page_padding, page_padding, page_padding]
        self.doc_template_type = doc_template_type if doc_template_type else BaseDocTemplate
        self.sections = sections
        self.title = title
        self.author = author
        self.subject = subject
        self.creator = creator
        self.data = None

    def create_report(self, data_dict, buff=None):
        self.data = data_dict
        if not buff:
            buff = io.BytesIO()
        story = []
        for section in self._content_methods():
            elems = getattr(self, section)()
            story.extend(elems)
        doc_t = self._create_document(buff)
        metadata = doc_t.build(story)
        buff.seek(0)
        return {"metadata": metadata, "document": buff}

    def _content_methods(self):
        if self.sections:
            return self.sections
        return sorted([x for x in dir(self) if x.startswith("_section_")])

    def _create_document(self, buff, page=None, doc=None):
        if not page:
            page = PageTemplate(
                "normal",
                [
                    Frame(
                        self.page_margin[0],
                        self.page_margin[1],
                        self.page_size[0] - self.page_margin[0] - self.page_margin[2],
                        self.page_size[1] - self.page_margin[1] - self.page_margin[3],
                        leftPadding=self.page_padding[0],
                        bottomPadding=self.page_padding[3],
                        rightPadding=self.page_padding[2],
                        topPadding=self.page_padding[1],
                    )
                ],
            )
        if not doc:
            doc = self.doc_template_type(
                buff,
                pagesize=letter,
                title=self.title,
                author=self.author,
                subject=self.subject,
                creator=self.creator,
                leftMargin=self.page_margin[0],
                rightMargin=self.page_margin[2],
                topMargin=self.page_margin[1],
                bottomMargin=self.page_margin[3],
            )
        doc.addPageTemplates(page)
        return doc


class OrderSentence(PDFReport):
    def __init__(self, *args, **kwargs):
        PDFReport.__init__(
            self,
            *args,
            page_size=letter,
            doc_template_type=SignatureDocTemplate,
            **kwargs
        )

    def _content_methods(self):
        methods = PDFReport._content_methods(self)
        methods.insert(0, methods.pop(methods.index("_section_doc_header")))
        return methods

    def _create_document(self, *args, **kwargs):
        page = PageTemplate(
            "normal",
            [
                Frame(
                    self.page_margin[0],
                    self.page_margin[1],
                    self.page_size[0] - self.page_margin[0] - self.page_margin[2],
                    self.page_size[1] - self.page_margin[1] - self.page_margin[3],
                    leftPadding=self.page_padding[0],
                    bottomPadding=self.page_padding[3],
                    rightPadding=self.page_padding[2],
                    topPadding=self.page_padding[1],
                )
            ],
            onPage=self._page_footer
        )
        kwargs["page"] = page
        doc = PDFReport._create_document(self, *args, **kwargs)
        return doc

    @staticmethod
    def underline_pad(width, text, style):
        text = str(text)
        padded_text = "<u>"
        space_width = stringWidth(" ", style.fontName, style.fontSize)
        text_width = stringWidth(text, style.fontName, style.fontSize)
        num_spaces = (width - text_width) / space_width
        for i in range(1, int(num_spaces / 2)):
            padded_text += "&nbsp;"
        padded_text += text
        for i in range(1, int((num_spaces / 2) + 0.5) - 2):
            padded_text += "&nbsp;"
        padded_text += "</u>"
        padded_text += "&nbsp;" * 2
        return padded_text

    @staticmethod
    def _page_footer(canv, doc):
        dt = datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p")
        p = Paragraph(dt, style=extend_style(styles["main"], alignment=TA_RIGHT))
        p_height = p.wrapOn(canv, doc.width, doc.height)[1]
        p.drawOn(canv, doc.leftMargin, doc.bottomMargin - p_height)

    def _section_doc_header(self):
        elems = [
            Paragraph("<b>IN THE MUNICIPAL COURT OF DEKALB COUNTY<br />STATE OF GEORGIA</b>",
                      styles["doc-header"])
        ]
        ps = extend_style(styles["main"], fontSize=9)
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
                                [Paragraph("<b>CITY OF BROOKHAVEN</b>", ps), None],
                                [None, None],
                                [Paragraph("<b>vs.</b>", ps), None],
                                [Paragraph("%s" % self.data["defendant_name"], ps), Paragraph("<b>,</b>", ps)],
                                [Paragraph("<b>DEFENDANT.</b>", ps), ]
                            ],
                            style=extend_table_style(styles["main-table"], [
                                ("LINEBELOW", (0, 3), (0, 3), 0.5, "black"),
                                ("VALIGN", (0, 2), (-1, 2), "BOTTOM"),
                            ]),
                            colWidths=[None, 2 * mm],
                            rowHeights=5 * mm,
                        ),
                        Table(
                            [
                                [Paragraph("<b>Citation No(s). and Violation(s):</b>", ps)],
                                [Paragraph("%s" % cit_lines[0], ps)],
                                [Paragraph("%s" % cit_lines[1], ps)],
                            ],
                            style=extend_table_style(styles["main-table"], [
                                ("LINEBELOW", (0, 1), (-1, -1), 0.6, "black"),
                            ]),
                            rowHeights=6 * mm,
                        )
                    ],
                    [
                        Spacer(0, 5 * mm)
                    ]
                ],
                style=extend_table_style(styles["main-table"], [
                    ("LINEAFTER", (0, 0), (0, -1), 0.5, "black"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 5 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 5 * mm,),
                ]),
                colWidths=(75 * mm, None),
                spaceBefore=5 * mm,
                spaceAfter=2 * mm,
            )
        )
        elems.extend([
            Paragraph("<b><u>ORDER AND SENTENCE</u></b>", extend_style(styles["doc-header"], fontSize=12)),
        ])
        return elems

    def _section_1(self):
        elems = list()
        ps = extend_style(styles["section-main"], alignment=TA_LEFT, fontSize=styles["section-main"].fontSize * 0.9,
                          leading=styles["section-main"].fontSize * 0.9)
        ps_right = extend_style(styles["section-main"], alignment=TA_RIGHT)
        ps_title = extend_style(styles["section-main"], alignment=TA_CENTER,
                                leading=styles["section-main"].fontSize * 1.35)
        data = [
            [
                Paragraph("<b>Citation</b>", ps_title),
                Paragraph("<b>Offense</b>", ps_title),
                Paragraph("<b>Disposition</b>", ps_title),
                Paragraph("<b>Case Balance</b>", ps_title),
                None
            ]
        ]
        for citation in self.data["citations"]:
            data.append([
                Paragraph("<font size=10><seq>.</font> <b>%s</b>" % citation["citation_number"], ps),
                Table(
                    [[
                        Paragraph("%s" % citation["offense_number"], ps),
                        Paragraph("%s" % citation["offense_description"], ps),
                    ]],
                    style=extend_table_style(styles["main-table"], [
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ]),
                    colWidths=[20 * mm, None],
                ),
                Paragraph("%s" % citation["disposition"], ps),
                Paragraph("$ %s" % citation["balance"], ps),
                Spacer(0, 6 * mm),
            ])
        elems.append(
            Table(
                data,
                style=extend_table_style(styles["main-table"], [
                    ("GRID", (0, 0), (-2, -1), 0.5, "black"),
                    ("LEFTPADDING", (0, 0), (-2, -1), 1.5 * mm),
                    ("RIGHTPADDING", (0, 0), (-2, -1), 1.5 * mm),
                    ("TOPPADDING", (0, 0), (-2, -1), 0.25 * mm),
                    ("BOTTOMPADDING", (0, 0), (-2, -1), 1 * mm),
                    ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]),
                colWidths=[30 * mm, None, 25 * mm, 25 * mm, 0],
            )
        )
        elems.append(
            Table(
                [
                    [
                        Paragraph("TOTAL AMOUNT OF FINE(S) / FEE(S)", ps_right),
                        Paragraph("$ %s" % self.data["total_amount"], ps),
                        None
                    ],
                    [
                        Paragraph("CASH BONDS RECEIVED", ps_right),
                        Paragraph("$ %s" % self.data["bonds_received"], ps),
                    ]
                ],
                style=extend_table_style(styles["main-table"], [
                    ("LEFTPADDING", (0, 0), (-1, -1), 1.5 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 1.5 * mm),
                ]),
                colWidths=[None, 25 * mm, 5],
            )
        )
        elems.append(Spacer(0, 2 * mm))
        return elems

    def _section_2(self):
        ps = extend_style(styles["section-main"], alignment=TA_JUSTIFY, underlineProportion=0.07)
        ps_center = extend_style(ps, alignment=TA_CENTER)
        elems = [
            Paragraph(
                "Upon accepting the defendant's above indicated plea or judgment by this court and after reviewing the defendant's criminal history record, it now appears to this Court that acceptance of the defendant's plea would be in the best interest of justice.",
                ps
            ),
            Spacer(0, 0.5 * mm),
        ]
        period_text = self.underline_pad(
            22 * mm,
            "%s %s" % (self.data["sentence_length"], self.data["sentence_period"]),
            ps
        )
        elems.append(
            Paragraph(
                "Whereas, the above disposition has been made against the above named defendant, the defendant is hereby sentenced to confinement for a period of %s and ordered to pay a fine in the total amount stated above, of which includes all surcharges pursuant to the Official Code of Georgia Annotated." % period_text,
                ps
            ),
        )
        period_text = (
            self.underline_pad(
                22 * mm,
                "%s %s" % (self.data["house_eligible_length"], self.data["house_eligible_period"]),
                ps
            ),
            self.underline_pad(
                22 * mm,
                "%s %s" % (self.data["house_length"], self.data["house_period"]),
                ps
            ),
        )
        elems.append(
            Paragraph(
                "Upon service of %s of the above sentence confined in jail, defendant will serve %s in confinement. Defendant shall receive no reduction of total sentence time based upon any credit for good time served if incarcerated." % period_text,
                ps
            ),
        )
        elems.extend([
            Table(
                [[
                    Paragraph("The defendant is to report to the jail", ps),
                    CustomXBox(8.2, self.data["jail_immediate"]),
                    Paragraph("immediately <b>or</b>", ps),
                    CustomXBox(8.2, True if self.data["jail_date"] else False),
                    Paragraph("on", ps),
                    Paragraph("%s" % self.data["jail_date"], ps_center),
                    Paragraph("at", ps_center),
                    Paragraph("%s" % self.data["jail_time"], ps_center),
                    Paragraph("to begin service.", ps),
                ]],
                style=extend_table_style(styles["main-table"], [
                    ("LEFTPADDING", (8, 0), (8, 0), 1 * mm),
                    ("LINEBELOW", (5, 0), (5, 0), 0.6, "black"),
                    ("LINEBELOW", (7, 0), (7, 0), 0.6, "black"),
                ]),
                colWidths=[55 * mm, 5 * mm, 25 * mm, 5 * mm, 5 * mm, None, 5 * mm, None]
            ),
            Spacer(0, 2 * mm)
        ])
        return elems

    def _section_3(self):
        ps = styles["section-main"]
        elems = [
            Paragraph(
                "<b>GENERAL CONDITIONS OF PROBATION / SUSPENDED SENTENCE</b>: The defendant is hereby granted the privilege of serving all or part of the above stated sentence on probation, subject to the following general conditions:",
                ps
            ),
        ]
        ps = extend_style(ps, alignment=TA_JUSTIFY)
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
            table_data.append([Paragraph("<seq id=\"s3s4_l0\">.&nbsp;&nbsp;%s" % text, ps)])
        elems.append(
            Table(
                table_data,
                style=extend_table_style(styles["main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (0, -1), 14 * mm),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 1 * mm),
                ]),
            )
        )
        elems.append(Spacer(0, 1 * mm))
        return elems

    def _section_4(self):
        ps = styles["section-main"]
        elems = [
            Paragraph(
                "<b>SPECIAL CONDITIONS OF PROBATION (conditions are only applicable if checked and will be completed at the defendant's expense):</b>",
                ps
            ),
        ]
        field_values = [
            (
                self.underline_pad(22 * mm, self.data["11_amount"], ps),
                self.underline_pad(50 * mm, self.data["11_party"], ps)
            ),
            (
                self.underline_pad(15 * mm, self.data["16_meetings"], ps),
                self.underline_pad(15 * mm, self.data["16_sessions"], ps),
            ),
            self.underline_pad(22 * mm, "%s %s" % (self.data["17_length"], self.data["17_period"]), ps),
            self.underline_pad(15 * mm, self.data["18_hours"], ps),
            self.underline_pad(15 * mm, self.data["19_days"], ps),
            self.underline_pad(15 * mm, self.data["20_months"], ps),
            self.underline_pad(15 * mm, self.data["21_months"], ps),
            (
                self.underline_pad(15 * mm, self.data["22_months"], ps),
                self.underline_pad(20 * mm, self.data["22_amount"], ps)
            ),
            self.underline_pad(15 * mm, self.data["23_months"], ps),
        ]
        line_data = [
            [
                XBoxParagraph("<seq id=\"s3s4_l0\">. Pay restitution in the amount of $ %s to %s" % field_values[0],
                              ps, 6.5, True if self.data["11"] else False)
            ],
            [
                XBoxParagraph(
                    "<seq id=\"s3s4_l0\">. Abstain from the use of alcohol and drugs, and be subjected to random alcohol / drug testing of defendant's blood, breath, urine and hair as requested by court, probation, or law enforcement.",
                    ps, 6.5, True if self.data["12"] else False)
            ],
            [
                XBoxParagraph(
                    "<seq id=\"s3s4_l0\">. Obtain an alcohol and drug use evaluation or anger management evaluation as directed, and follow all further directives for treatment or counseling.",
                    ps, 6.5, True if self.data["13"] else False)
            ],
            [
                XBoxParagraph(
                    "<seq id=\"s3s4_l0\">. Complete a Risk Reduction course conducted by an agency licensed by the State of Georgia and submit proof to the Georgia Department of Driver Services within 120 days of this plea.",
                    ps, 6.5, True if self.data["14"] else False)
            ],
            [
                XBoxParagraph(
                    "<seq id=\"s3s4_l0\">. Complete the Interlock Ignition device requirements pursuant to the Official Code of Georgia Annotated.",
                    ps, 6.5, True if self.data["15"] else False)
            ],
            [
                XBoxParagraph(
                    "<seq id=\"s3s4_l0\">. Attend %s Alcoholics / Narcotics Anonymous meetings; and %s counseling sessions per week." %
                    field_values[1],
                    ps, 6.5, True if self.data["16"] else False
                )
            ],
            [
                XBoxParagraph(
                    "<seq id=\"s3s4_l0\">. Successfully complete %s of community service as directed by the probation supervisor or the City." %
                    field_values[2],
                    ps, 6.5, True if self.data["17"] else False
                )
            ],
            [
                XBoxParagraph(
                    "<seq id=\"s3s4_l0\">. %s hours of community service may be completed in lieu of fine at a rate of $10.00 per hour" %
                    field_values[3],
                    ps, 6.5, True if self.data["18"] else False)

            ],
            [
                XBoxParagraph(
                    "<seq id=\"s3s4_l0\">. Defendant shall complete defensive driving school and submit proof of completion to the clerk of Court within %s days of plea" %
                    field_values[4],
                    ps, 6.5, True if self.data["19"] else False,
                )
            ],
            [
                XBoxParagraph(
                    "<seq id=\"s3s4_l0\">. Probation supervisor fee to be suspended after %s months if defendant has paid all of the fine and completed all special conditions of probation, with general conditions of probation to remain in effect throughout the term." %
                    field_values[5],
                    ps, 6.5, True if self.data["20"] else False,
                )
            ],
            [
                XBoxParagraph(
                    "<seq id=\"s3s4_l0\">. Probation can be terminated after %s months if defendant has paid all of the fine and completed all special conditions of probation." %
                    field_values[6],
                    ps, 6.5, True if self.data["21"] else False,
                )
            ],
            [
                XBoxParagraph(
                    "<seq id=\"s3s4_l0\">. Pay all fines and surcharges within %s months at a rate of $ %s per month. (to be filled out by probation offcer after disposition.)" %
                    field_values[7],
                    ps, 6.5, True if self.data["22"] else False,
                )
            ],
            [
                XBoxParagraph(
                    "<seq id=\"s3s4_l0\">. Complete all special conditions within %s months." % field_values[8], ps,
                    6.5, True if self.data["23"] else False, )
            ],
            [
                XBoxParagraph(
                    "<seq id=\"s3s4_l0\">. Defendant shall attend all classes and work successfully toward obtaining a high school diploma or GED during period of probation.",
                    ps, 6.5, True if self.data["24"] else False, )
            ],
            [
                XBoxParagraph("<seq id=\"s3s4_l0\">. Other: %s" % self.data["25_description"], ps,
                              6.5, True if self.data["25"] else False)
            ],
            [HRFlowable(color="black", width="90%")],
        ]
        elems.append(
            Table(
                line_data,
                style=extend_table_style(styles["main-table"], [
                    ("LEFTPADDING", (0, 0), (-1, -1), 10.5 * mm),
                    ("ALIGN", (0, -1), (-1, -1), "RIGHT"),
                    ("BOTTOMPADDING", (0, 0), (-1, -3), 1 * mm),
                ]),
            )
        )
        elems.append(Spacer(0, 2 * mm))
        return elems

    def _section_5(self):
        ps = styles["section-main"]
        elems = [
            Paragraph(
                "IT IS THE FURTHER ORDER of the Court, and the defendant is hereby advised that the Court may, at any time, upon violation of any of the general or special conditions of probation, revoke any conditions of the probation / suspension herein granted. If such probation / suspension is revoked, the Court may order the execution of the sentence which was originally imposed or any portion thereof in the manner provided by law, after deducting the amount of time the defendant has on probation or suspension.",
                ps,
            )
        ]
        elems.append(Spacer(0, 1 * mm))
        date_parts = self.data["order_date"].split("/")
        date_parts[1] = int(date_parts[0])
        date_suff = ["th", "st", "nd", "rd"]
        try:
            date_parts[1] = "%s%s" % (date_parts[1], date_suff[date_parts[1]])
        except IndexError:
            date_parts[1] = "%s%s" % (date_parts[1], date_suff[0])
        date_parts[0] = datetime.date(1900, int(date_parts[0]), 1).strftime('%B')
        elems.append(
            Table(
                [
                    [
                        None,
                        Paragraph("<b>SO ORDERED</b> this", ps),
                        Paragraph("%s" % date_parts[1], extend_style(ps, alignment=TA_CENTER)),
                        Paragraph("of", extend_style(ps, alignment=TA_CENTER)),
                        Paragraph("%s" % date_parts[0], extend_style(ps, alignment=TA_CENTER)),
                        Paragraph(", %s." % date_parts[2], ps),
                    ]
                ],
                style=extend_table_style(styles["main-table"], [
                    ("LINEBELOW", (2, 0), (2, 0), 0.5, "black"),
                    ("LINEBELOW", (4, 0), (4, 0), 0.5, "black"),
                ]),
                colWidths=(25 * mm, 30 * mm, 12.5 * mm, 4.5 * mm, 30 * mm, 12 * mm),
                hAlign="LEFT"
            )
        )
        elems.extend([
            Spacer(0, 1 * mm),
            Table(
                [
                    [None, SignatureRect(88 * mm, 7 * mm, label="Judge", leftIndent=4 * mm)],
                    [None, Paragraph("Judge, MUNICIPAL COURT OF BROOKHAVEN", ps)],
                ],
                style=extend_table_style(styles["main-table"], [
                    ("LINEABOVE", (1, 1), (1, 1), 0.9, "black"),
                ]),
            )
        ])
        elems.extend([
            Spacer(0, 10 * mm),
            Table(
                [
                    [
                        None,
                        SignatureRect(65 * mm, 7 * mm, label="Defendant"),
                        None,
                        SignatureRect(82 * mm, 7 * mm, label="Defendants Attorney"),
                        None
                    ],
                    [
                        None,
                        Paragraph("Defendant", ps),
                        None,
                        Paragraph("Defendant's Attorney", ps),
                    ],
                ],
                style=extend_table_style(styles["main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEBELOW", (1, 0), (1, 0), 0.9, "black"),
                    ("LINEBELOW", (3, 0), (3, 0), 0.9, "black"),
                ]),
                colWidths=(10 * mm, None, 10 * mm, None, 10 * mm),
            )
        ])

        return elems
