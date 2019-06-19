from .reportlab_styles import styles, extend_style, extend_table_style
from reportlab.graphics.barcode import code39
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Flowable, Paragraph, Table, Spacer
from reportlab.platypus.flowables import HRFlowable
import ast
import io


def generate_il_state_pdf(citation_info, copy_type="VIOLATOR", violation_text="", overweight_text="", extra_title="",
                          title=None, author=None):
    copy_type_info = dict()
    if citation_info["is_traffic"]:
        copy_type_info[
            "instructions_violator"] = "INSERT APPROPRIATE TEXT FROM THE PRINTING INSTRUCTIONS, INSTRUCTIONS TO THE VIOLATOR SECTION"
        copy_type_info[
            "instructions_complaint"] = "INSERT APPROPRIATE TEXT FROM THE PRINTING INSTRUCTIONS, INSTRUCTIONS TO THE VIOLATOR SECTION"
        copy_type_info[
            "instructions_release"] = "INSERT APPROPRIATE TEXT FROM THE PRINTING INSTRUCTIONS, RELEASE SECTION"
        cr = TrafficCitationReport(
            citation_info,
            "ILLINOIS CITATION AND COMPLAINT",
            copy_type,
            copy_type_info,
            violation_text=violation_text
        )
    elif citation_info["is_overweight"]:
        copy_type_info["instructions_consequences"] = "INSERT APPROPRIATE TEXT HERE"
        if not extra_title:
            extra_title = "ILLINOIS STATE POLICE"
        cr = OverweightCitationReport(
            citation_info,
            "ILLINOIS OVERWEIGHT CITATION AND COMPLAINT<br />" + extra_title,
            copy_type,
            copy_type_info,
            overweight_text=overweight_text
        )
    else:
        cr = NonTrafficCitationReport(
            citation_info,
            "NON-TRAFFIC COMPLAINT AND NOTICE TO APPEAR<br />" + extra_title,
            copy_type,
            copy_type_info,
        )
    if title:
        cr.title = title
    if author:
        cr.author = author

    cr.create_report()

    # cr.save("docs/output.pdf")
    if cr.content:
        cr.content.seek(0)
        return cr.content, cr.page_size


def field_string_from_flags(info_dict, sen_list):
    field = ""
    for key, val in info_dict.items():
        if val:
            for sen in sen_list:
                if key.startswith(sen):
                    name = key[len(sen):].replace("_", " ")
                    field += name + ","
                    break
    if field:
        field = field[:-1]
    return field


class XBox(Flowable):
    def __init__(self, size, checked=None):
        Flowable.__init__(self)
        self.width = size
        self.height = size
        self.size = size
        self.checked = checked

    def draw(self):
        self.canv.saveState()
        self.canv.setLineWidth(0.15 * self.size)
        self.canv.rect(0, 0, self.width, self.height)
        if self.checked > 0:
            self.check()
        self.canv.restoreState()

    def check(self):
        self.canv.setFont('Times-Bold', self.size * 0.725)
        to = self.canv.beginText(self.width * 0.23, self.height * 0.23)
        to.textLine("X")
        self.canv.drawText(to)


class SectionField(Paragraph):
    def __init__(self, text1, style1, text2, style2, offset=None):
        Paragraph.__init__(self, text1, style1)
        self.data_text = text2
        self.data_style = style2
        if offset:
            self.offset = offset
        else:
            # self.offset = (stringWidth(self.text, self.style.fontName, self.style.fontSize), -1 * mm)
            self.offset = (2, -2.5 * mm)

    def draw(self):
        Paragraph.draw(self)
        self.canv.setFont(self.data_style.fontName, self.data_style.fontSize)
        to = self.canv.beginText(self.offset[0], self.offset[1])
        to.textLine(self.data_text)
        self.canv.drawText(to)


class RotatedParagraph(Paragraph):
    def draw(self):
        self.canv.saveState()
        self.width = self.style.width
        self.canv.translate(11, 0)
        self.canv.rotate(90)
        self.wrap(self.width, self.height)
        Paragraph.draw(self)
        self.canv.restoreState()


class CitationReport:
    def __init__(self, ticket, sections, header, copy_type, copy_type_info, violation_text, title, author):
        self.citation_info = ticket
        self.sections = sections
        self.header = header
        self.content = None
        self.content_width = 0
        self.title_width = 0
        self.page_size = None
        self.page_margin = 0
        self.title = title
        self.author = author
        self.content_height = 0
        self.copy_type = copy_type.upper()
        if copy_type_info:
            self.copy_type_info = copy_type_info
        else:
            self.copy_type_info = dict()
        self.violation_text = violation_text

    def create_report(self):
        def get_method(section):
            try:
                method = getattr(self, "_section_" + section)
            except AttributeError:
                raise Exception("Section method not found " + section)
            return method

        story = []
        for section in self.sections:
            if isinstance(section, list):
                wrapper_elems = []
                for s in section:
                    wrapper_elems.append(get_method(s)()[0])
                elems = self._section_wrapper(wrapper_elems)
            else:
                elems = get_method(section)()

            for elem in elems:
                story.append(elem)
                self.content_height += elem.wrap(self.page_size[0], 0)[1]
        buff = io.BytesIO()
        page_t = PageTemplate('normal', [
            Frame(
                self.page_margin,
                self.page_margin,
                self.page_size[0] - self.page_margin * 2,
                self.content_height,
                leftPadding=0,
                bottomPadding=0,
                rightPadding=0,
                topPadding=0,
            )
        ])
        self.page_size = (self.page_size[0], self.content_height + 2 * self.page_margin)
        doc_t = BaseDocTemplate(
            buff,
            pagesize=self.page_size,
            title=self.title,
            author=self.author,
            leftMargin=self.page_margin,
            rightMargin=self.page_margin,
            topMargin=self.page_margin,
            bottomMargin=self.page_margin,
        )
        doc_t.addPageTemplates(page_t)
        doc_t.build(story)
        self.content = buff

    def _section_wrapper(self, content):
        width_list = []
        for section in content:
            width_list.append(section.wrap(0, 0)[0])
        t = Table(
            [
                content
            ],
            style=extend_table_style(styles["il-citation-main-table"], [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]),
            colWidths=width_list
        )
        return [t]

    def _section_gen_table(self, title, content=None, header=None, footer=None, title_width=None, content_width=None):
        content_width = content_width if content_width else self.content_width
        title_width = title_width if title_width else self.title_width
        header_height = None if header else 0
        footer_height = None if footer else 0
        main_height = 0
        for table in content:
            main_height += table.wrap(0, 0)[1]
        ps = ParagraphStyle("il-citation-rotated-height", parent=styles["il-citation-rotated"], width=main_height)
        t = Table(
            [
                [
                    None,
                    header
                ],
                [
                    RotatedParagraph(title, style=ps),
                    [content]
                ],
                [
                    None,
                    footer
                ]
            ],
            style=extend_table_style(styles["il-citation-main-table"], [
                ("BACKGROUND", (0, 1), (0, 1), "black"),
            ]),
            colWidths=(title_width, content_width),
            rowHeights=[header_height, None, footer_height],
        )

        return t

    def save(self, fp):
        if self.content:
            self.content.seek(0)
            with open(fp, 'wb') as fh:
                fh.write(self.content.read())
        else:
            raise Exception("No report content has been created")

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class TrafficCitationReport(CitationReport):
    def __init__(self, citation_info, header, copy_type, copy_type_info=None, violation_text="", sections=None,
                 title=None,
                 author=None):
        if not sections:
            sections = [
                "header", "complaint_info", "defendant_info", "vehicle_info", "violation_info", "incident_info",
                "release_info", "court_info", "footer", "instructions"
            ]
        CitationReport.__init__(self, citation_info, sections, header, copy_type, copy_type_info, violation_text, title,
                                author)
        self.page_size = (4 * inch, 1 * inch)
        self.page_margin = 1.5 * mm
        self.title_width = 4.3 * mm
        self.content_width = self.page_size[0] - 2 * self.page_margin - self.title_width

    def _section_header(self):
        p = Paragraph(
            self.header, style=styles["il-citation-doc-header"]
        )
        return [p]

    def _section_footer(self):
        t = Table(
            [
                [
                    Paragraph(
                        "Under penalties as provided by law for false certification pursuant to Section 1-109 of the Code of Civil Procedure and perjury pursuant to Section 32-2 of the Criminal Code of 2012, the undersigned certifies that the statements set forth in this instrument are true and correct.",
                        style=styles["il-citation-main"]
                    ),
                ],
                [
                    Paragraph(
                        "Month",
                        style=styles["il-citation-main"]
                    ),
                    Paragraph(
                        "Day",
                        style=styles["il-citation-main"]
                    ),
                    Paragraph(
                        "Year",
                        style=extend_style(styles["il-citation-main"], alignment=TA_RIGHT)
                    ),
                    None,
                    Paragraph(
                        "Officer Signature",
                        style=styles["il-citation-main"]
                    ),
                    Paragraph(
                        "ID No.",
                        style=extend_style(styles["il-citation-main"], alignment=TA_RIGHT)
                    ),
                ],
            ],
            style=extend_table_style(styles["il-citation-main-table"], [
                ("LINEBELOW", (0, 0), (2, 0), 0.5, "black"),
                ("LINEBELOW", (4, 0), (-1, 0), 0.5, "black"),
                ("SPAN", (0, 0), (-1, 0)),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]),
            colWidths=(15 * mm, 10 * mm, 11 * mm, 3.5 * mm, 29.55 * mm, 29.55 * mm),
            rowHeights=(17.3 * mm, 2.5 * mm),
        )
        return [t]

    def _section_instructions(self):
        method_name = "_section_instructions_" + self.copy_type.lower().replace(" ", "")
        try:
            method = getattr(self, method_name)
        except AttributeError:
            print("No instructions for" + self.copy_type)
            return
        return method()

    def _section_instructions_violator(self):
        elems = list()
        elems.append(
            Paragraph("Read These Instructions Carefully", style=styles["il-citation-instructions-header"])
        )
        elems.append(
            Paragraph(self.copy_type_info["instructions_violator"], style=styles["il-citation-instructions"])
        )
        elems.append(Spacer(1, 10))
        elems.append(
            Paragraph("Method of Release - Failure to Appear",
                      style=extend_style(styles["il-citation-instructions-header"], alignment=TA_LEFT))
        )
        elems.append(
            Paragraph(
                "The method of release is noted in the \"Release\" section. The result of your failure to appear or pay this ticket is determined by the method of release identified below and whether your ticket is marked \"Court Appearance Required\" or \"<u>No</u> Court Appearance Required\" and may result in either a judgement of confliction being entered against you for fine, penalties, assessments, and costs as provided in the NOTICE OF CONSENT FOR ENTRY OF JUDGEMENT, or, the court may order other consequences identified below.",
                style=styles["il-citation-instructions"])
        )
        elems.append(Spacer(1, 5))
        elems.append(
            Paragraph(self.copy_type_info["instructions_release"], style=styles["il-citation-instructions"])
        )
        elems.append(Spacer(1, 10))
        elems.append(
            Table(
                [
                    [
                        Paragraph("Notice of Consent for Entry of Judgement",
                                  style=styles["il-citation-instructions-header"]),
                    ],
                    [
                        Paragraph(
                            "If you were charged with an offense which does not require a court appearance, YOU ARE HEREBY NOTIFIED THAT.",
                            style=styles["il-citation-instructions"]),
                    ],
                    [
                        Paragraph(
                            "If you do not satisfy the charge(s) against  you prior to the date set for your appearance or any date to which the case is continued, you do not submit a written plea of guilty to the Clerk at least three (3) days before the date, and you fail to answer the charge(s) or appear in court when required, you thereby consent to the entry of a judgement of conviction against you in the amount of the statutory minimum fine, plus the assesment in the applicable schedule for the charged offenses as provided in the Criminal and Traffic Assessment Act (705 ILCS 135/1 et seq.). The total amount assessed may be greater than the amount assessed on a guilty plea. Any cash bail or other security you have deposited will be applied toward payment. If you are an Illinois Driver and you fail to pay in full any judgements imposed, a notice will be sent to the Secretary of State and your driver's license will not be renewed, reissued, or reclassified, until full payment is received.",
                            style=styles["il-citation-instructions"]),
                    ]
                ],
                style=[
                    ("OUTLINE", (0, 0), (-1, -1), 1, "black"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 2 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 2 * mm),
                    ("TOPPADDING", (0, 0), (-1, -1), 2 * mm),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 2 * mm),
                    ("TOPPADDING", (0, 0), (-1, 0), 5 * mm),
                ],
                colWidths=80 * mm,
            )
        )
        return elems

    def _section_instructions_complaint(self):
        elems = list()
        elems.append(
            Paragraph("Read These Instructions Carefully", style=styles["il-citation-instructions-header"])
        )
        elems.append(
            Paragraph(self.copy_type_info["instructions_complaint"], style=styles["il-citation-instructions"])
        )
        elems.append(Spacer(1, 10))
        elems.append(
            Paragraph("Method of Release - Failure to Appear",
                      style=extend_style(styles["il-citation-instructions-header"], alignment=TA_LEFT))
        )
        elems.append(
            Paragraph(
                "The method of release is noted in the \"Release\" section. The result of your failure to appear or pay this ticket is determined by the method of release identified below and whether your ticket is marked \"Court Appearance Required\" or \"<u>No</u> Court Appearance Required\" and may result in either a judgement of confliction being entered against you for fine, penalties, assessments, and costs as provided in the NOTICE OF CONSENT FOR ENTRY OF JUDGEMENT, or, the court may order other consequences identified below.",
                style=styles["il-citation-instructions"])
        )
        elems.append(Spacer(1, 5))
        elems.append(
            Paragraph(self.copy_type_info["instructions_release"], style=styles["il-citation-instructions"])
        )
        elems.append(Spacer(1, 10))
        elems.append(
            Table(
                [
                    [
                        Paragraph("Notice of Consent for Entry of Judgement",
                                  style=styles["il-citation-instructions-header"]),
                    ],
                    [
                        Paragraph(
                            "If you were charged with an offense which does not require a court appearance, YOU ARE HEREBY NOTIFIED THAT.",
                            style=styles["il-citation-instructions"]),
                    ],
                    [
                        Paragraph(
                            "If you do not satisfy the charge(s) against  you prior to the date set for your appearance or any date to which the case is continued, you do not submit a written plea of guilty to the Clerk at least three (3) days before the date, and you fail to answer the charge(s) or appear in court when required, you thereby consent to the entry of a judgement of conviction against you in the amount of the statutory minimum fine, plus the assesment in the applicable schedule for the charged offenses as provided in the Criminal and Traffic Assessment Act (705 ILCS 135/1 et seq.). The total amount assessed may be greater than the amount assessed on a guilty plea. Any cash bail or other security you have deposited will be applied toward payment. If you are an Illinois Driver and you fail to pay in full any judgements imposed, a notice will be sent to the Secretary of State and your driver's license will not be renewed, reissued, or reclassified, until full payment is received.",
                            style=styles["il-citation-instructions"]),
                    ]
                ],
                style=[
                    ("OUTLINE", (0, 0), (-1, -1), 1, "black"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 2 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 2 * mm),
                    ("TOPPADDING", (0, 0), (-1, -1), 2 * mm),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 2 * mm),
                    ("TOPPADDING", (0, 0), (-1, 0), 5 * mm),
                ],
                colWidths=80 * mm,
            )
        )
        return elems

    def _section_instructions_courtcommunication(self):
        elems = list()
        elems.append(Spacer(1, 5))
        elems.append(
            Table(
                [
                    [
                        Paragraph(
                            "Avoid Multiple Court Appearances",
                            style=styles["il-citation-instructions-header"]),
                    ],
                    [
                        Table(
                            [
                                [
                                    Paragraph(
                                        "If you intend to plead <u>NOT GUILTY</u> to the ticket:",
                                        style=styles["il-citation-instructions"]),
                                    None
                                ],
                                [
                                    Paragraph(
                                        "1.",
                                        style=styles["il-citation-instructions"]),
                                    Paragraph(
                                        "Complete this form and mail at least TEN (10) work days before the date set for your court appearance noted on teh bottom half of the ticket (Court Place/Date Section).",
                                        style=styles["il-citation-instructions"]),
                                ],
                                [
                                    Paragraph(
                                        "2.",
                                        style=styles["il-citation-instructions"]),
                                    Paragraph(
                                        "Indicate what kind of trial you want - mark only one box, complete the address section below and follow the mailing instructions in number 3 below.",
                                        style=styles["il-citation-instructions"]),
                                ]
                            ],
                            style=extend_table_style(styles["il-citation-main-table"], [
                                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                ("SPAN", (0, 0), (-1, 0)),
                            ]),
                            colWidths=(4 * mm, (self.page_size[0] - 2 * self.page_margin) - 4 * mm - 4 * mm),
                        )
                    ],
                    [
                        Table(
                            [
                                [
                                    Paragraph(
                                        "I WISH TO PLEAD NOT GUILTY AND REQUEST:",
                                        style=styles["il-citation-instructions"]),
                                    None,
                                    None
                                ],
                                [
                                    None,
                                    XBox(8, 0),
                                    Paragraph(
                                        "A.  Trial by Judge",
                                        style=styles["il-citation-instructions"]),
                                ],
                                [
                                    None,
                                    XBox(8, 0),
                                    Paragraph(
                                        "B.  Trial by Jury",
                                        style=styles["il-citation-instructions"]),
                                ]
                            ],
                            style=extend_table_style(styles["il-citation-main-table"], [
                                ("SPAN", (0, 0), (-1, 0)),
                                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                ("ALIGN", (1, 0), (1, -1), "CENTER"),
                            ]),
                            colWidths=(31 * mm, 5 * mm, 25 * mm)
                        )
                    ],
                    [
                        Paragraph(
                            "A new appearance data will be set and you will be notified of the time and date of trial. <b>Do not come to court until you are notified.</b> When you are notified, you should come to court prepared for trial and bring anny witnesses you may have.",
                            style=styles["il-citation-instructions"]),
                    ],
                    [
                        Paragraph(
                            "Name",
                            style=styles["il-citation-instructions"]),
                    ],
                    [
                        Paragraph(
                            "Mailing Address",
                            style=styles["il-citation-instructions"]),
                    ],
                    [
                        Paragraph(
                            "City/State/Zip",
                            style=styles["il-citation-instructions"]),
                    ],
                    [
                        Paragraph(
                            "Telephone Number",
                            style=styles["il-citation-instructions"]),
                    ],
                    [
                        Table(
                            [
                                [
                                    Paragraph(
                                        "3.",
                                        style=styles["il-citation-instructions"]),
                                    Paragraph(
                                        "Mail this form to the Clerk of the Court, Traffic Section, at the address noted in the \"Court Place/Date\" section on the bottom half of the ticket.",
                                        style=styles["il-citation-instructions"]),
                                ],
                            ],
                            style=extend_table_style(styles["il-citation-main-table"], [
                                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ]),
                            colWidths=(4 * mm, (self.page_size[0] - 2 * self.page_margin) - 4 * mm - 4 * mm),
                        )
                    ],
                    [
                        Paragraph(
                            "DO NOT MAIL TO THE POLICE DEPARTMENT",
                            style=styles["il-citation-instructions-header"]),
                    ],
                ],
                style=[
                    ("OUTLINE", (0, 0), (-1, -1), 1, "black"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 2 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 2 * mm),
                    ("TOPPADDING", (0, 0), (-1, -1), 2 * mm),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 2 * mm),
                ],
                colWidths=self.page_size[0] - 2 * self.page_margin
            )
        )
        ps = extend_style(styles["il-citation-instructions"], alignment=TA_RIGHT)
        elems.append(
            Table(
                [
                    [
                        Paragraph(
                            "GUILTY PLEA",
                            style=styles["il-citation-instructions-header"]),
                    ],
                    [
                        Paragraph(
                            "If you intend to plead <u>GUILTY</u> to the ticket and <u>No</u> Court Appearance is Required.<br />"
                            "1. Complete this form.<br />"
                            "2. Mail this form, together with the applicable payment to the Clerk of the the Court, Traffic Section, at the address noted in the \"Court Place/Date\" section on the bottom half of the ticket. You must mail this completed form, with the total applicable payment <b> no earlier than ten (10) work days</b> after the ticket was issues (noted on othe top half <u>below \"Defendant\" section</u>, of thet ticket), <b>and no later than three (3) work days</b> before the court appearance date noted on the bottom half of the ticket in the \"Court Place/Date\" section or as may have been provided by the clerk of the court.",
                            style=styles["il-citation-instructions"]),
                    ],
                    [
                        Paragraph(
                            "<u>FINES, PENALTIES, ASSESSMENTS, AND COSTS</u><br />"
                            "The amount of payment for offenses where court appearances are not required is:<br />"
                            "<b>(a) $164.00 for any violation under the illinois Vehicle Code</b> (625 ILCS 5/1 et seq.) defined as a minor traffic offense pursuant to Supreme Court Rule 501(f), except (b) below; <br />"
                            "<b>(b) $260.00 plus hte minimum fine set by statute for truck overweight and permit violations</b> under 3-401(d), 15-111, 15-113, 15-113.2 or 15-113.3 of the Illinois Vhicle Code (625 ILCS 5/3-401(d), 15-111, 15-113.1, 15113.2 or 15-113.3); <br />"
                            "<b>(c) $195.00 for any violation defined as a Conservation Offense</b> under Supreme Courte Rules 501(c) for which civil penalties are not required.<br />"
                            "<b>Note: Payment must be by cash, money order, certified check, bank draft, or traveler's check unless otherwise auhtorized by the clerk of the court. (DO NOT SEND CASH IN THE MAIL; use cash only if paying in person.)</b>",
                            style=styles["il-citation-instructions"]),
                    ],
                    [
                        Paragraph(
                            "PLEA OF GUILTY AND WAIVER",
                            style=styles["il-citation-instructions-header"]),
                    ],
                    [
                        Paragraph(
                            "I, the undersigned, do hereby plead guilty to the charge noted on this ticket, which does not require a court appearance. I understand my right to a trial, that my signature to this plea of guilty will have the same force and effect as a conviction by the court and that this record will be sent to the Secretary of State of this State (or of the State where I received my license to drive). I hearby PLEAD GUILTY to the said offense on this ticket, GIVE UP my right to trial, and agree to pay the amount required.",
                            style=styles["il-citation-instructions"]),
                    ],
                    [
                        Table(
                            [
                                [
                                    Paragraph(
                                        "Defendants Signature",
                                        style=styles["il-citation-instructions"]),
                                    None,
                                    Paragraph(
                                        "Date",
                                        style=ps
                                    ),
                                ],
                                [
                                    Paragraph(
                                        "Mailing Address",
                                        style=styles["il-citation-instructions"]),
                                    None,
                                    Paragraph(
                                        "Street",
                                        style=ps
                                    )
                                ],
                                [
                                    Paragraph(
                                        "City",
                                        style=styles["il-citation-instructions"]),
                                    Paragraph(
                                        "State",
                                        style=ps
                                    ),
                                    Paragraph(
                                        "Zip",
                                        style=ps
                                    )
                                ]
                            ],
                            style=extend_table_style(styles["il-citation-main-table"], [
                                ("LINEABOVE", (0, 0), (-1, -1), 1, "black"),
                                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ]),
                            colWidths=31.4 * mm,
                            rowHeights=6 * mm
                        ),
                    ]

                ],
                style=[
                    ("OUTLINE", (0, 0), (-1, -1), 1, "black"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 2 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 2 * mm),
                    ("TOPPADDING", (0, 0), (-1, -1), 2 * mm),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 2 * mm),
                ],
                colWidths=self.page_size[0] - 2 * self.page_margin
            )
        )
        return elems

    def _section_complaint_info(self):
        bw = 0.26 - (0.01 * max(0, len(self.citation_info["ticket_number"]) - 5))
        t1 = Table(
            [
                [
                    None,
                    None,
                    None,
                    Paragraph(self.citation_info["ticket_number"], style=extend_style(
                        styles["il-citation-main"], fontSize=11, leading=12, alignment=TA_RIGHT
                    )),
                ],
                [
                    code39.Standard39(
                        self.citation_info["ticket_number"],
                        barWidth=bw * mm,
                        ratio=3,
                        barHeight=5.2 * mm,
                        checksum=0,
                        lquiet=1.75 * mm,
                        rquiet=1.75 * mm
                    ),
                    None,
                    Paragraph("DCN:", style=styles["il-citation-field-header"]),
                ],
                [
                    None,
                    Paragraph(self.copy_type, style=extend_style(
                        styles["il-citation-main"], fontSize=12, leading=12, alignment=TA_RIGHT, fontName="Arial-Bold"
                    )),
                ],
            ],
            style=extend_table_style(styles["il-citation-main-table"], [
                ("OUTLINE", (3, 1), (3, 1), 0.5, "black"),
                ("OUTLINE", (3, 1), (3, 1), 0.5, "black"),
                ("SPAN", (0, 1), (1, 1)),
                ("SPAN", (1, 2), (3, 2)),
                ("VALIGN", (0, 1), (0, 1), "MIDDLE"),
            ]),
            colWidths=(38 * mm, 7.8 * mm, 8.5 * mm, 37.2 * mm),
            rowHeights=(3.75 * mm, 5.6 * mm, 3.75 * mm),
        )
        hr = HRFlowable(width="100%", thickness=1, lineCap="butt", color="lightgrey", spaceAfter=1 * mm, dash=(5, 5))
        township = self.citation_info["complainant_municipality_township"] if self.citation_info[
            "complainant_municipality_township"] else ""
        t2 = Table(
            [
                [
                    SectionField("Case No.", styles["il-citation-field-header"],
                                 self.citation_info["case_number"], styles["il-citation-field-data"],
                                 offset=(2, -1.8 * mm)),
                    SectionField("ISP Dist Occ.", styles["il-citation-field-header"],
                                 self.citation_info["complainant_agency_report_number"],
                                 styles["il-citation-field-data"],
                                 offset=(2, -1.8 * mm)),
                    None,
                    SectionField("ISP Dist Assgn", styles["il-citation-field-header"],
                                 self.citation_info["complainant_document_control_number"],
                                 styles["il-citation-field-data"],
                                 offset=(2, -1.8 * mm)),
                ],
                [
                    SectionField("County of", styles["il-citation-field-header"],
                                 self.citation_info["municipality_county"], styles["il-citation-field-data"],
                                 offset=(2, -1.8 * mm)),
                    None,
                    SectionField("Township of", styles["il-citation-field-header"],
                                 township,
                                 styles["il-citation-field-data"],
                                 offset=(2, -1.8 * mm)),
                    None,
                    Paragraph("TWP. RD.", styles["il-citation-field-header"]),
                    XBox(7, self.citation_info["complainant_is_township_road"]),
                ]
            ],
            style=[
                ("BOX", (0, 0), (-1, -1), 0.5, "black"),
                ("INNERGRID", (0, 0), (3, -1), 0.5, "black"),
                ("LINEBELOW", (4, 0), (5, 0), 0.5, "black"),
                ("SPAN", (1, 0), (2, 0)),
                ("SPAN", (3, 0), (5, 0)),
                ("SPAN", (0, 1), (1, 1)),
                ("SPAN", (2, 1), (3, 1)),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (5, 1), (5, 1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 1),
                ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ],
            colWidths=(34 * mm, 7.5 * mm, 17 * mm, 23 * mm, 6 * mm, 6.8 * mm),
            rowHeights=4.5 * mm,
        )
        t3 = Table(
            [
                [
                    XBox(7, not self.citation_info["complainant_is_municipality"]),
                    Paragraph("PEOPLE STATE OF ILLINOIS", style=styles["il-citation-field-header"]),
                    XBox(7, self.citation_info["complainant_is_municipality"]),
                    Paragraph("CITY/VILLAGE OF MUNICIPAL CORPORATION PLAINTIFF",
                              style=styles["il-citation-field-header"]),
                    None,
                    Paragraph("VS.", style=styles["il-citation-field-header"])
                ]
            ],
            style=extend_table_style(styles["il-citation-main-table"], [
                ("OUTLINE", (0, 0), (-1, -1), 0.5, "black"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ]),
            colWidths=(6 * mm, 16 * mm, 6 * mm, 31 * mm, 30.8 * mm, 4.5 * mm),
            rowHeights=6 * mm,
        )
        return [self._section_gen_table(title="COMPLAINT", content=[t1, hr, t2, t3])]

    def _section_defendant_info(self):
        t1 = Table(
            [
                [
                    Paragraph("NAME", style=styles["il-citation-field-header"]),
                    None,
                    None,
                    Paragraph("SID #", style=styles["il-citation-field-header"]),
                ],
                [
                    SectionField("LAST", styles["il-citation-field-header-sm"],
                                 self.citation_info["defendant_last_name"], styles["il-citation-field-data"],
                                 offset=(0, 3 * mm)
                                 ),
                    SectionField("FIRST", styles["il-citation-field-header-sm"],
                                 self.citation_info["defendant_first_name"], styles["il-citation-field-data"],
                                 offset=(0, 3 * mm)
                                 ),
                    SectionField("MIDDLE NAME", styles["il-citation-field-header-sm"],
                                 self.citation_info["defendant_middle_initial"], styles["il-citation-field-data"],
                                 offset=(0, 3 * mm)
                                 ),
                ]
            ],
            style=[
                ("OUTLINE", (0, 0), (-1, -1), 0.5, "black"),
                ("SPAN", (0, 0), (2, 0)),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 1),
                ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ],
            colWidths=(27 * mm, 31.5 * mm, 12.8 * mm, 23 * mm,),
            rowHeights=(7 * mm, 2.5 * mm)
        )
        t2s1 = Table(
            [
                [
                    Paragraph("ADDRESS", style=styles["il-citation-field-header"]),
                ],
                [
                    SectionField("STREET", styles["il-citation-field-header-sm"],
                                 self.citation_info["defendant_address_street"], styles["il-citation-field-data"],
                                 offset=(0, 2 * mm)
                                 ),
                    SectionField("APT", styles["il-citation-field-header-sm"],
                                 self.citation_info["defendant_address_apartment"], styles["il-citation-field-data"],
                                 offset=(0, 2 * mm)
                                 ),
                ],
            ],
            style=[
                ("SPAN", (0, 0), (1, 0)),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 1),
                ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ],
            colWidths=(43 * mm, 16 * mm),
            rowHeights=(4.6 * mm, 2.4)
        )
        sex_m = 0
        sex_f = 0
        if self.citation_info["defendant_sex"] == "M":
            sex_m = 1
        elif self.citation_info["defendant_sex"] == "F":
            sex_f = 1
        address = self.citation_info["defendant_address_city"] + "    " + self.citation_info[
            "defendant_address_state"] + "    " + self.citation_info["defendant_address_zip"]
        dl_expiration = self.citation_info["defendant_driver_license_expiration_date"] if self.citation_info[
            "defendant_driver_license_expiration_date"] else ""
        t2 = Table(
            [
                [
                    t2s1,
                    None,
                    None,
                    SectionField("EYES", styles["il-citation-field-header"],
                                 self.citation_info["defendant_eye_color"], styles["il-citation-field-data"],
                                 ),
                    None,
                    None,
                    XBox(7, sex_f),
                    Paragraph("Female", style=styles["il-citation-field-header-sm"]),
                ],
                [
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    XBox(7, sex_m),
                    Paragraph("Male", style=styles["il-citation-field-header-sm"])
                ],
                [
                    SectionField("CITY STATE ZIP", styles["il-citation-field-header"],
                                 address, styles["il-citation-field-data"],
                                 ),
                    None,
                    None,
                    SectionField("HAIR", extend_style(styles["il-citation-field-header"], alignment=TA_CENTER),
                                 self.citation_info["defendant_hair_color"], styles["il-citation-field-data"],
                                 ),
                    SectionField("HEIGHT", extend_style(styles["il-citation-field-header"], alignment=TA_CENTER),
                                 self.citation_info["defendant_height"], styles["il-citation-field-data"],
                                 ),
                    None,
                    SectionField("WEIGHT", extend_style(styles["il-citation-field-header"], alignment=TA_CENTER),
                                 self.citation_info["defendant_weight"], styles["il-citation-field-data"],
                                 ),
                    None,
                ],
                [
                    SectionField("DR. LIC.", styles["il-citation-field-header"],
                                 self.citation_info["defendant_driver_license_number"],
                                 styles["il-citation-field-data"],
                                 ),
                    SectionField("STATE", extend_style(styles["il-citation-field-header"], alignment=TA_CENTER),
                                 self.citation_info["defendant_driver_license_state"], styles["il-citation-field-data"],
                                 ),
                    SectionField("CDL", extend_style(styles["il-citation-field-header"], alignment=TA_CENTER),
                                 str(self.citation_info["defendant_driver_license_is_commercial"]),
                                 styles["il-citation-field-data"],
                                 ),
                    SectionField("EXPIR. DATE", extend_style(styles["il-citation-field-header"], alignment=TA_CENTER),
                                 dl_expiration,
                                 styles["il-citation-field-data"],
                                 ),
                    None,
                    SectionField("DOB", extend_style(styles["il-citation-field-header"], alignment=TA_CENTER),
                                 str(self.citation_info["defendant_date_of_birth"]),
                                 styles["il-citation-field-data"],
                                 ),
                ]
            ],
            style=[
                ("INNERGRID", (0, 0), (5, -1), 0.5, "black"),
                ("INNERGRID", (0, 2), (-1, -1), 0.5, "black"),
                ("OUTLINE", (0, 0), (-1, -1), 0.5, "black"),
                ("LINEBEFORE", (6, 0), (6, 1), 0.5, "black"),
                ("LINEBELOW", (6, 1), (7, 1), 0.5, "black"),
                ("SPAN", (0, 0), (2, 1)),
                ("SPAN", (3, 0), (5, 1)),
                ("SPAN", (0, 2), (2, 2)),
                ("SPAN", (4, 2), (5, 2)),
                ("SPAN", (6, 2), (7, 2)),
                ("SPAN", (3, 3), (4, 3)),
                ("SPAN", (5, 3), (7, 3)),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (6, 0), (-1, 1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 1),
                ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ],
            colWidths=(43 * mm, 8 * mm, 8 * mm, 10.5 * mm, 5.8 * mm, 4.7 * mm, 4.5 * mm, 9.8 * mm),
            rowHeights=(3.5 * mm, 3.5 * mm, 6.7 * mm, 6.3 * mm)
        )
        return [self._section_gen_table(title="DEFENDANT", content=[t1, t2])]

    def _section_vehicle_info(self):
        ps = extend_style(styles["il-citation-field-header-sm"], alignment=TA_CENTER)
        t1s1 = Table(
            [
                [
                    Paragraph("COMMERCIAL MOTOR VEHICLE", style=styles["il-citation-field-header-sm"]),
                    Paragraph("YES", style=ps),
                    XBox(5, self.citation_info["vehicle_is_commercial"]),
                    Paragraph("NO", style=ps),
                    XBox(5, not self.citation_info["vehicle_is_commercial"]),
                ],
                [
                    Paragraph("PLACARDED HAZ. MATERIAL", style=styles["il-citation-field-header-sm"]),
                    Paragraph("YES", style=ps),
                    XBox(5, self.citation_info["vehicle_has_hazardous_materials_indicator"]),
                    Paragraph("NO", style=ps),
                    XBox(5, not self.citation_info["vehicle_has_hazardous_materials_indicator"]),
                ],
                [
                    Paragraph("16 OR MORE PASS. VEHICLE", style=styles["il-citation-field-header-sm"]),
                    Paragraph("YES", style=ps),
                    XBox(5, self.citation_info["vehicle_is_large_passenger_vehicle"]),
                    Paragraph("NO", style=ps),
                    XBox(5, not self.citation_info["vehicle_is_large_passenger_vehicle"]),
                ]
            ],
            style=extend_table_style(styles["il-citation-main-table"], [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (1, 0), (-1, -1), "CENTER"),
            ]),
            colWidths=(29 * mm, 3.5 * mm, 3 * mm, 3.5 * mm, 3 * mm),
            rowHeights=2.3 * mm
        )
        t1 = Table(
            [
                [
                    SectionField("REG. NO.", styles["il-citation-field-header"],
                                 self.citation_info["vehicle_plate"],
                                 styles["il-citation-field-data"],
                                 ),
                    SectionField("STATE", extend_style(styles["il-citation-field-header"], alignment=TA_CENTER),
                                 self.citation_info["vehicle_state"],
                                 styles["il-citation-field-data"],
                                 ),
                    SectionField("MO/YEAR", extend_style(styles["il-citation-field-header"], alignment=TA_CENTER),
                                 self.citation_info["vehicle_registration_expiration_date"],
                                 styles["il-citation-field-data"],
                                 ),
                    SectionField("US DOT #", styles["il-citation-field-header"],
                                 self.citation_info["vehicle_united_states_dot_number"],
                                 styles["il-citation-field-data"],
                                 ),
                ],
                [
                    SectionField("MAKE", styles["il-citation-field-header"],
                                 self.citation_info["vehicle_make"],
                                 styles["il-citation-field-data"],
                                 ),
                    None,
                    SectionField("YEAR", extend_style(styles["il-citation-field-header"], alignment=TA_CENTER),
                                 self.citation_info["vehicle_year"],
                                 styles["il-citation-field-data"],
                                 ),
                    SectionField("COLOR", styles["il-citation-field-header"],
                                 self.citation_info["vehicle_color"],
                                 styles["il-citation-field-data"],
                                 ),
                ],
                [
                    SectionField("TYPE", styles["il-citation-field-header"],
                                 self.citation_info["vehicle_type"],
                                 styles["il-citation-field-data"],
                                 ),
                    [
                        Paragraph("VEHICLE USE:", styles["il-citation-field-header"]),
                        t1s1,
                    ],
                ]
            ],
            style=[
                ("GRID", (0, 0), (-1, -1), 0.5, "black"),
                ("SPAN", (0, 1), (1, 1)),
                ("SPAN", (1, 2), (3, 2)),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 1),
                ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ],
            colWidths=(51.5 * mm, 8.5 * mm, 15.5 * mm, 18.8 * mm,),
            rowHeights=(6.25 * mm, 6.25 * mm, 9.6 * mm)
        )
        p1 = Paragraph(
            "The Undersigned states that on ____________________ at ____________________<br />"
            "Defendant did unlawfully operate:",
            style=styles["il-citation-table-header"])
        ps = extend_style(styles["il-citation-table-header"], fontSize=4.5, leading=4.5, fontName="Arial")
        fe = [
            Paragraph(
                "Or as a Pedestrian or Passenger, and upon a Public Highway, or other Location, Specifically",
                style=styles["il-citation-table-header"]
            ),
            HRFlowable(width="100%", thickness=0.5, lineCap="butt", color="black", spaceBefore=3.5 * mm, spaceAfter=0),
            Table(
                [
                    [
                        Paragraph(
                            "Located in the County and State Aforesaid and Did Then and There Commit the Following Offense",
                            style=ps
                        ),
                        XBox(5, self.citation_info["violation_is_in_urban_district"]),
                        Paragraph(
                            "URBAN DISTRICT",
                            style=styles["il-citation-field-header-sm"]
                        ),
                    ]
                ],
                style=extend_table_style(styles["il-citation-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ALIGN", (1, 0), (1, 0), "CENTER"),
                ]),
                colWidths=(76 * mm, 3 * mm, 15.3 * mm),
                rowHeights=2.5 * mm
            )
        ]
        return [self._section_gen_table(title="VEHICLE", content=[t1], header=p1, footer=fe)]

    def _section_violation_info(self):
        ps = extend_style(styles["il-citation-field-header"], fontName="Arial")
        t1s1 = Table(
            [
                [
                    XBox(6, True if self.citation_info["violation_type"] == "ILCS" else False),
                    Paragraph("ILCS", style=ps),
                    XBox(6, False if self.citation_info["violation_type"] == "ILCS" else True),
                    Paragraph("Local Ordinance", style=ps),
                ],
            ],
            style=extend_table_style(styles["il-citation-main-table"], [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (0, -1), 2.5 * mm),
            ]),
            colWidths=(6.5 * mm, 10.5 * mm, 5 * mm, 25 * mm),
            rowHeights=5 * mm,
        )
        ps = extend_style(styles["il-citation-field-header-sm"], fontName="Arial")
        p = Paragraph(self.violation_text, style=extend_style(ps, leftIndent=2.5 * mm, rightIndent=2.5 * mm))
        description = [self.citation_info["violation_description"][i:i + 70] for i in
                       range(0, len(self.citation_info["violation_description"]), 70)]
        t1s2_content = [
            [
                None,
                Paragraph("Nature of Offense:", style=ps),
                Paragraph(description[0], style=ps),
            ]
        ]
        for i in range(1, 4):
            try:
                if description[i]:
                    t1s2_content.append(
                        [
                            None,
                            Paragraph(description[i], style=ps),
                        ]
                    )
            except IndexError:
                t1s2_content.append([None, None, None, None])
        t1s2 = Table(
            t1s2_content,
            style=extend_table_style(styles["il-citation-main-table"], [
                ("LINEBELOW", (2, 0), (2, 0), 0.5, "black"),
                ("LINEBELOW", (1, 1), (2, -1), 0.5, "black"),
                ("SPAN", (1, 1), (2, 1)),
                ("SPAN", (1, 2), (2, 2)),
            ]),
            colWidths=(2.5 * mm, 16.5 * mm, 72.8 * mm, 2.5 * mm),
            rowHeights=(4 * mm, 4 * mm, 4 * mm, 2 * mm)
        )
        t1 = Table(
            [
                [
                    t1s1
                ],
                [
                    p
                ],
                [
                    t1s2
                ],
            ],
            style=extend_table_style(styles["il-citation-main-table"], [
                ("OUTLINE", (0, 0), (-1, -1), 0.5, "black"),
            ]),
        )

        return [self._section_gen_table(title="VIOLATION", content=[t1])]

    def _section_incident_info(self):
        visibility = field_string_from_flags(
            self.citation_info,
            ["incident_visibility_conditions_include_", "incident_visibility_includes_"]
        )
        conditions = field_string_from_flags(
            self.citation_info,
            ["incident_road_conditions_include_", "incident_road_conditions_includes_"]
        )
        methods = field_string_from_flags(
            self.citation_info,
            ["incident_method_includes_"]
        )
        ps = extend_style(styles["il-citation-field-header-sm"], fontName="Arial", alignment=TA_RIGHT)
        t1 = Table(
            [
                [
                    Paragraph("ACCIDENT TYPE:", styles["il-citation-field-header"]),
                    None,
                    Paragraph(self.citation_info["incident_accident_type"], styles["il-citation-field-data"]),
                    None,
                    None,
                ],
                [
                    Paragraph("Report No.:", ps),
                    Paragraph(self.citation_info["incident_report_number"], styles["il-citation-field-data"]),
                    None,
                    Paragraph("CAD No.:", ps),
                ],
                [
                    Paragraph("Visibility:", ps),
                    Paragraph(visibility, styles["il-citation-field-data"]),
                    None,
                    Paragraph("Road Conditions:", ps),
                    Paragraph(conditions, styles["il-citation-field-data"]),
                ],
                [
                    Paragraph("Method:", ps),
                    Paragraph(methods, styles["il-citation-field-data"]),
                    None,
                    Paragraph("Notations:", ps),
                    Paragraph(self.citation_info["incident_accident_notes"] if self.citation_info[
                        "incident_accident_notes"] else "", styles["il-citation-field-data"]),
                ],
            ],
            style=extend_table_style(styles["il-citation-main-table"], [
                ("OUTLINE", (0, 0), (-1, -1), 0.5, "black"),
                ("SPAN", (0, 0), (1, 0)),
                ("SPAN", (2, 0), (4, 0)),
                ("SPAN", (1, 1), (2, 1)),
                ("SPAN", (1, 2), (2, 2)),
                ("SPAN", (1, 3), (2, 3)),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 1),
                ("RIGHTPADDING", (0, 0), (-1, -1), 1),
            ]),
            colWidths=(11.25 * mm, 7.8 * mm, 17.3 * mm, 14.7 * mm, 43.25 * mm),
            rowHeights=(3.1 * mm, 3.3 * mm, 3.3 * mm, 3.3 * mm)
        )

        return [self._section_gen_table(title="INCIDENT", content=[t1])]

    def _section_release_info(self):
        release_method = field_string_from_flags(self.citation_info, ["bond_includes_"])
        t1 = Table(
            [
                [
                    SectionField("METHOD OF RELEASE:", styles["il-citation-field-header"],
                                 release_method, styles["il-citation-field-data"], offset=(25 * mm, 0)),
                    None,
                    Paragraph("Total Bond/Bail Posted:",
                              extend_style(styles["il-citation-field-header"], alignment=TA_RIGHT)),
                    Paragraph(str(self.citation_info["bond_amount"]), styles["il-citation-field-data"]),
                    None,
                ],
                [
                    Paragraph("WITHOUT ADMITTING GUILT, I promise to comply with the terms of this Ticket and Release",
                              styles["il-citation-field-header"]),
                ],
                [
                    Paragraph("Signature X: ",
                              styles["il-citation-field-header"]),
                ],
                [

                ],
            ],
            style=extend_table_style(styles["il-citation-main-table"], [
                ("OUTLINE", (0, 0), (-1, -1), 0.5, "black"),
                ("SPAN", (0, 0), (1, 0)),
                ("SPAN", (0, 1), (-1, 1)),
                ("SPAN", (1, 2), (3, 2)),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("VALIGN", (0, 1), (-1, 1), "MIDDLE"),
                ("LINEBELOW", (3, 0), (3, 0), 0.5, "black"),
                ("LINEBELOW", (1, 2), (3, 2), 0.5, "black"),
                ("LEFTPADDING", (0, 0), (-1, -1), 1),
                ("RIGHTPADDING", (0, 0), (-1, -1), 1),
            ]),
            colWidths=(13.6 * mm, 38.3 * mm, 26.9 * mm, 13.8 * mm, 1.7 * mm),
            rowHeights=(2.8 * mm, 15.6 * mm, 2.6 * mm, 0.9 * mm)
        )
        return [self._section_gen_table(title="RELEASE", content=[t1])]

    def _section_court_info(self):
        time = str(self.citation_info["hearing_time"]) if self.citation_info["hearing_time"] else ""
        ps = extend_style(styles["il-citation-field-header-sm"], fontName="Arial")
        t1 = Table(
            [
                [
                    Paragraph("CIRCUIT COURT LOCATION, DATE AND TIME", styles["il-citation-field-header"]),
                    None,
                    None,
                    None,
                ],
                [
                    Paragraph("Court Location:", ps),
                    Paragraph(self.citation_info["hearing_court_address"], styles["il-citation-field-data"]),
                ],
                [
                    Paragraph("Date:", ps),
                    Paragraph(str(self.citation_info["hearing_court_date"]), styles["il-citation-field-data"]),
                    Paragraph("Time:", ps),
                    Paragraph(time, styles["il-citation-field-data"]),
                ],
            ],
            style=extend_table_style(styles["il-citation-main-table"], [
                ("SPAN", (0, 0), (1, 0)),
                ("SPAN", (1, 1), (3, 1)),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 1),
                ("RIGHTPADDING", (0, 0), (-1, -1), 1),
            ]),
            colWidths=(13 * mm, 35 * mm, 10 * mm, 36.3 * mm),
            rowHeights=(8.7 * mm, 4.3 * mm, 4.3 * mm)
        )
        ps = extend_style(styles["il-citation-field-header"], fontSize=12, leading=12)
        t2 = Table(
            [
                [
                    None,
                    XBox(9, not self.citation_info["hearing_attendance_required"]),
                    Paragraph(
                        "NO COURT APPEARANCE REQUIRED",
                        style=ps
                    ),
                    None
                ],
                [
                    None,
                    XBox(9, self.citation_info["hearing_attendance_required"]),
                    None,
                    Paragraph(
                        "COURT APPEARANCE REQUIRED",
                        style=ps
                    )
                ],
                [
                    None,
                    Paragraph("SEE INSTRUCTIONS in the text below.",
                              extend_style(styles["il-citation-field-header"], alignment=TA_CENTER)),
                ],

            ],
            style=extend_table_style(styles["il-citation-main-table"], [
                ("OUTLINE", (1, 2), (-1, 2), 0.5, "black"),
                ("SPAN", (2, 0), (3, 0)),
                ("SPAN", (1, 1), (2, 1)),
                ("SPAN", (1, 2), (3, 2)),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (1, 0), (1, 1), "RIGHT"),
                ("LEFTPADDING", (0, 0), (-1, -1), 1),
                ("RIGHTPADDING", (0, 0), (-1, -1), 1),
            ]),
            colWidths=(1.1 * mm, 5 * mm, 5 * mm, 82.1 * mm),
            rowHeights=5.2 * mm
        )

        return [self._section_gen_table(title="Court Place/Date", content=[t1, t2])]


class OverweightCitationReport(CitationReport):
    def __init__(self, citation_info, header, copy_type, copy_type_info=None, overweight_text="", sections=None,
                 title=None, author=None):
        if not sections:
            sections = [
                "header", "complaint_info", "defendant_info", "vehicle_info", "violation_info", "weights_info",
                ["release_info", "court_info"], "instructions"
            ]
        CitationReport.__init__(self, citation_info, sections, header, copy_type, copy_type_info, overweight_text,
                                title, author)
        self.page_size = (4 * inch, 1 * inch)
        self.page_margin = 1.5 * mm
        self.title_width = 4.3 * mm
        self.content_width = self.page_size[0] - 2 * self.page_margin - self.title_width

    def _section_header(self):
        p = Paragraph(
            self.header, style=styles["il-citation-doc-header"]
        )
        return [p]

    def _section_instructions(self):
        method_name = "_section_instructions_" + self.copy_type.lower().replace(" ", "")
        try:
            method = getattr(self, method_name)
        except AttributeError:
            print("No instructions for" + self.copy_type)
            return
        return method()

    def _section_instructions_violator(self):
        elems = list()
        elems.append(
            Paragraph("Read These Instructions Carefully", style=styles["il-citation-instructions-header"])
        )
        elems.append(
            Paragraph(
                "1. If you wish to plead \"GUILTY\", complete the \"PLEA OF GUILTY AND WAIVER\" provided and follow those instructions. Mail the guilty plea with full payment in the applicable amount noted on the citation in the \"Release\" section on the \"Total Amount\" line.<br /><br />"
                "Payment Options<br />"
                "NOTE: Payment must be cash, money order, certified check, bank draft, or traveler\'s check unless otherwise authorized by the Clerk of court. (DO NOT SEND CASH IN THE MAIL; use cash only if paying in person.)<br />"
                "2. If you wish to plead \"NOT GUILTY\", complete the portion of the form entitled \"Avoid Multiple Court Appearances\" and follow those instructions. If you are found guilty, the total amount assessed may be greater than the amount assessed on a gulity plea.",
                style=styles["il-citation-instructions"])
        )
        elems.append(Spacer(1, 10))
        elems.append(
            Paragraph("Method of Release - Failure to Appear",
                      style=extend_style(styles["il-citation-instructions-header"], alignment=TA_LEFT))
        )
        elems.append(
            Paragraph(
                "The method of release is noted in the \"Release\" section. The result of your failure to appear or pay this ticket is determined by the method of release identified below and whether your ticket is marked \"Court Appearance Required\" or \"<u>No</u> Court Appearance Required\" and may result in either a judgement of confliction being entered against you for fine, penalties, assessments, and costs as provided in the NOTICE OF CONSENT FOR ENTRY OF JUDGEMENT, or, the court may order other consequences identified below.",
                style=styles["il-citation-instructions"])
        )
        elems.append(Spacer(1, 5))
        elems.append(
            Paragraph(self.copy_type_info["instructions_consequences"], style=styles["il-citation-instructions"])
        )
        elems.append(Spacer(1, 10))
        elems.append(
            Table(
                [
                    [
                        Paragraph("Notice of Consent for Entry of Judgement",
                                  style=styles["il-citation-instructions-header"]),
                    ],
                    [
                        Paragraph(
                            "If you were charged with an offense which does not require a court appearance, YOU ARE HEREBY NOTIFIED THAT.",
                            style=styles["il-citation-instructions"]),
                    ],
                    [
                        Paragraph(
                            "If you do not satisfy the charge(s) against  you prior to the date set for your appearance or any date to which the case is continued, you do not submit a written plea of guilty to the Clerk at least three (3) days before the date, and you fail to answer the charge(s) or appear in court when required, you thereby consent to the entry of a judgement of conviction against you in the amount of the statutory minimum fine, plus the assesment in the applicable schedule for the charged offenses as provided in the Criminal and Traffic Assessment Act (705 ILCS 135/1 et seq.). The total amount assessed may be greater than the amount assessed on a guilty plea. Any cash bail or other security you have deposited will be applied toward payment. If you are an Illinois Driver and you fail to pay in full any judgements imposed, a notice will be sent to the Secretary of State and your driver's license will not be renewed, reissued, or reclassified, until full payment is received.",
                            style=styles["il-citation-instructions"]),
                    ]
                ],
                style=[
                    ("OUTLINE", (0, 0), (-1, -1), 1, "black"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 2 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 2 * mm),
                    ("TOPPADDING", (0, 0), (-1, -1), 2 * mm),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 2 * mm),
                    ("TOPPADDING", (0, 0), (-1, 0), 5 * mm),
                ],
                colWidths=80 * mm,
            )
        )
        return elems

    def _section_instructions_complaint(self):
        elems = list()
        elems.append(
            Paragraph("Read These Instructions Carefully", style=styles["il-citation-instructions-header"])
        )
        elems.append(
            Paragraph(
                "1. If you wish to plead \"GUILTY\", complete the \"PLEA OF GUILTY AND WAIVER\" provided and follow those instructions. Mail the guilty plea with full payment in the applicable amount noted on the citation in the \"Release\" section on the \"Total Amount\" line.<br /><br />"
                "Payment Options<br />"
                "NOTE: Payment must be cash, money order, certified check, bank draft, or traveler\'s check unless otherwise authorized by the Clerk of court. (DO NOT SEND CASH IN THE MAIL; use cash only if paying in person.)<br />"
                "2. If you wish to plead \"NOT GUILTY\", complete the portion of the form entitled \"Avoid Multiple Court Appearances\" and follow those instructions. If you are found guilty, the total amount assessed may be greater than the amount assessed on a gulity plea.",
                style=styles["il-citation-instructions"])
        )
        elems.append(Spacer(1, 10))
        elems.append(
            Paragraph("Method of Release - Failure to Appear",
                      style=extend_style(styles["il-citation-instructions-header"], alignment=TA_LEFT))
        )
        elems.append(
            Paragraph(
                "The method of release is noted in the \"Release\" section. The result of your failure to appear or pay this ticket is determined by the method of release identified below and whether your ticket is marked \"Court Appearance Required\" or \"<u>No</u> Court Appearance Required\" and may result in either a judgement of confliction being entered against you for fine, penalties, assessments, and costs as provided in the NOTICE OF CONSENT FOR ENTRY OF JUDGEMENT, or, the court may order other consequences identified below.",
                style=styles["il-citation-instructions"])
        )
        elems.append(Spacer(1, 5))
        elems.append(
            Paragraph(self.copy_type_info["instructions_consequences"], style=styles["il-citation-instructions"])
        )
        elems.append(Spacer(1, 10))
        elems.append(
            Table(
                [
                    [
                        Paragraph("Notice of Consent for Entry of Judgement",
                                  style=styles["il-citation-instructions-header"]),
                    ],
                    [
                        Paragraph(
                            "If you were charged with an offense which does not require a court appearance, YOU ARE HEREBY NOTIFIED THAT.",
                            style=styles["il-citation-instructions"]),
                    ],
                    [
                        Paragraph(
                            "If you do not satisfy the charge(s) against  you prior to the date set for your appearance or any date to which the case is continued, you do not submit a written plea of guilty to the Clerk at least three (3) days before the date, and you fail to answer the charge(s) or appear in court when required, you thereby consent to the entry of a judgement of conviction against you in the amount of the statutory minimum fine, plus the assesment in the applicable schedule for the charged offenses as provided in the Criminal and Traffic Assessment Act (705 ILCS 135/1 et seq.). The total amount assessed may be greater than the amount assessed on a guilty plea. Any cash bail or other security you have deposited will be applied toward payment. If you are an Illinois Driver and you fail to pay in full any judgements imposed, a notice will be sent to the Secretary of State and your driver's license will not be renewed, reissued, or reclassified, until full payment is received.",
                            style=styles["il-citation-instructions"]),
                    ]
                ],
                style=[
                    ("OUTLINE", (0, 0), (-1, -1), 1, "black"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 2 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 2 * mm),
                    ("TOPPADDING", (0, 0), (-1, -1), 2 * mm),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 2 * mm),
                    ("TOPPADDING", (0, 0), (-1, 0), 5 * mm),
                ],
                colWidths=80 * mm,
            )
        )
        return elems

    def _section_instructions_courtcommunication(self):
        elems = list()
        elems.append(Spacer(1, 5))
        elems.append(
            Table(
                [
                    [
                        Paragraph(
                            "Avoid Multiple Court Appearances",
                            style=styles["il-citation-instructions-header"]),
                    ],
                    [
                        Table(
                            [
                                [
                                    Paragraph(
                                        "If you intend to plead <u>NOT GUILTY</u> to the ticket:",
                                        style=styles["il-citation-instructions"]),
                                    None
                                ],
                                [
                                    Paragraph(
                                        "1.",
                                        style=styles["il-citation-instructions"]),
                                    Paragraph(
                                        "Complete this form and mail at least TEN (10) work days before the date set for your court appearance noted on teh bottom half of the ticket (Court Place/Date Section).",
                                        style=styles["il-citation-instructions"]),
                                ],
                                [
                                    Paragraph(
                                        "2.",
                                        style=styles["il-citation-instructions"]),
                                    Paragraph(
                                        "Indicate what kind of trial you want - mark only one box, complete the address section below and follow the mailing instructions in number 3 below.",
                                        style=styles["il-citation-instructions"]),
                                ]
                            ],
                            style=extend_table_style(styles["il-citation-main-table"], [
                                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                ("SPAN", (0, 0), (-1, 0)),
                            ]),
                            colWidths=(4 * mm, (self.page_size[0] - 2 * self.page_margin) - 4 * mm - 4 * mm),
                        )
                    ],
                    [
                        Table(
                            [
                                [
                                    Paragraph(
                                        "I WISH TO PLEAD NOT GUILTY AND REQUEST:",
                                        style=styles["il-citation-instructions"]),
                                    None,
                                    None
                                ],
                                [
                                    None,
                                    XBox(8, 0),
                                    Paragraph(
                                        "A.  Trial by Judge",
                                        style=styles["il-citation-instructions"]),
                                ],
                                [
                                    None,
                                    XBox(8, 0),
                                    Paragraph(
                                        "B.  Trial by Jury",
                                        style=styles["il-citation-instructions"]),
                                ]
                            ],
                            style=extend_table_style(styles["il-citation-main-table"], [
                                ("SPAN", (0, 0), (-1, 0)),
                                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                ("ALIGN", (1, 0), (1, -1), "CENTER"),
                            ]),
                            colWidths=(31 * mm, 5 * mm, 25 * mm)
                        )
                    ],
                    [
                        Paragraph(
                            "A new appearance data will be set and you will be notified of the time and date of trial. <b>Do not come to court until you are notified.</b> When you are notified, you should come to court prepared for trial and bring anny witnesses you may have.",
                            style=styles["il-citation-instructions"]),
                    ],
                    [
                        Paragraph(
                            "Name",
                            style=styles["il-citation-instructions"]),
                    ],
                    [
                        Paragraph(
                            "Mailing Address",
                            style=styles["il-citation-instructions"]),
                    ],
                    [
                        Paragraph(
                            "City/State/Zip",
                            style=styles["il-citation-instructions"]),
                    ],
                    [
                        Paragraph(
                            "Telephone Number",
                            style=styles["il-citation-instructions"]),
                    ],
                    [
                        Table(
                            [
                                [
                                    Paragraph(
                                        "3.",
                                        style=styles["il-citation-instructions"]),
                                    Paragraph(
                                        "Mail this form to the Clerk of the Court, Traffic Section, at the address noted in the \"Court Place/Date\" section on the bottom half of the ticket.",
                                        style=styles["il-citation-instructions"]),
                                ],
                            ],
                            style=extend_table_style(styles["il-citation-main-table"], [
                                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ]),
                            colWidths=(4 * mm, (self.page_size[0] - 2 * self.page_margin) - 4 * mm - 4 * mm),
                        )
                    ],
                    [
                        Paragraph(
                            "DO NOT MAIL TO THE POLICE DEPARTMENT",
                            style=styles["il-citation-instructions-header"]),
                    ],
                ],
                style=[
                    ("OUTLINE", (0, 0), (-1, -1), 1, "black"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 2 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 2 * mm),
                    ("TOPPADDING", (0, 0), (-1, -1), 2 * mm),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 2 * mm),
                ],
                colWidths=self.page_size[0] - 2 * self.page_margin
            )
        )
        ps = extend_style(styles["il-citation-instructions"], alignment=TA_RIGHT)
        elems.append(
            Table(
                [
                    [
                        Paragraph(
                            "GUILTY PLEA",
                            style=styles["il-citation-instructions-header"]),
                    ],
                    [
                        Paragraph(
                            "If you intend to plead <u>GUILTY</u> to the ticket and <u>No</u> Court Appearance is Required.<br />"
                            "1. Complete this form.<br />"
                            "2. Mail this form, together with the applicable payment to the Clerk of the the Court, Traffic Section, at the address noted in the \"Court Place/Date\" section on the bottom half of the ticket. You must mail this completed form, with the total applicable payment <b> no earlier than ten (10) work days</b> after the ticket was issues (noted on othe top half <u>below \"Defendant\" section</u>, of thet ticket), <b>and no later than three (3) work days</b> before the court appearance date noted on the bottom half of the ticket in the \"Court Place/Date\" section or as may have been provided by the clerk of the court.",
                            style=styles["il-citation-instructions"]),
                    ],
                    [
                        Paragraph(
                            "PLEA OF GUILTY AND WAIVER",
                            style=styles["il-citation-instructions-header"]),
                    ],
                    [
                        Paragraph(
                            "I, the undersigned, do hereby plead guilty to the charge noted on this ticket, which does not require a court appearance. I understand my right to a trial, that my signature to this plea of guilty will have the same force and effect as a conviction by the court and that this record will be sent to the Secretary of State of this State (or of the State where I received my license to drive). I hearby PLEAD GUILTY to the said offense on this ticket, GIVE UP my right to trial, and agree to pay the amount required.",
                            style=styles["il-citation-instructions"]),
                    ],
                    [
                        Table(
                            [
                                [
                                    Paragraph(
                                        "Defendants Signature",
                                        style=styles["il-citation-instructions"]),
                                    None,
                                    Paragraph(
                                        "Date",
                                        style=ps
                                    ),
                                ],
                                [
                                    Paragraph(
                                        "Mailing Address",
                                        style=styles["il-citation-instructions"]),
                                    None,
                                    Paragraph(
                                        "Street",
                                        style=ps
                                    )
                                ],
                                [
                                    Paragraph(
                                        "City",
                                        style=styles["il-citation-instructions"]),
                                    Paragraph(
                                        "State",
                                        style=ps
                                    ),
                                    Paragraph(
                                        "Zip",
                                        style=ps
                                    )
                                ]
                            ],
                            style=extend_table_style(styles["il-citation-main-table"], [
                                ("LINEABOVE", (0, 0), (-1, -1), 1, "black"),
                                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ]),
                            colWidths=31.4 * mm,
                            rowHeights=6 * mm
                        ),
                    ]

                ],
                style=[
                    ("OUTLINE", (0, 0), (-1, -1), 1, "black"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 2 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 2 * mm),
                    ("TOPPADDING", (0, 0), (-1, -1), 2 * mm),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 2 * mm),
                ],
                colWidths=self.page_size[0] - 2 * self.page_margin
            )
        )
        return elems

    def _section_complaint_info(self):
        bw = 0.26 - (0.01 * max(0, len(self.citation_info["ticket_number"]) - 5))
        t1 = Table(
            [
                [
                    code39.Standard39(
                        self.citation_info["ticket_number"],
                        barWidth=bw * mm,
                        ratio=3,
                        barHeight=7.4 * mm,
                        checksum=0,
                        lquiet=1.75 * mm,
                        rquiet=1.75 * mm
                    ),
                    Paragraph(self.violation_text, style=extend_style(
                        styles["il-citation-main"], fontSize=11, leading=12, alignment=TA_RIGHT
                    )),
                ],
                [
                    None,
                    Paragraph(self.copy_type, style=extend_style(
                        styles["il-citation-main"], fontSize=12, leading=12, alignment=TA_RIGHT, fontName="Arial-Bold"
                    )),
                ],
            ],
            style=extend_table_style(styles["il-citation-main-table"], [
                ("SPAN", (0, 0), (0, 1)),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (0, -1), 1 * mm),
                ("RIGHTPADDING", (-1, 0), (-1, -1), 1 * mm),
            ]),
            colWidths=(39.3 * mm, 55 * mm),
            rowHeights=5.75 * mm,

        )
        field_offset = (2, -3 * mm)
        t2 = Table(
            [
                [
                    SectionField("Case No.", styles["il-citation-field-header"],
                                 self.citation_info["case_number"], styles["il-citation-field-data"],
                                 offset=field_offset),
                    SectionField("ISP Dist Occ.", styles["il-citation-field-header"],
                                 self.citation_info["complainant_agency_report_number"],
                                 styles["il-citation-field-data"],
                                 offset=field_offset),
                    XBox(7, 0),
                    Paragraph("Tollway", style=styles["il-citation-field-header"]),
                    SectionField("ISP Dist Assgn", styles["il-citation-field-header"],
                                 self.citation_info["complainant_document_control_number"],
                                 styles["il-citation-field-data"],
                                 offset=field_offset),
                ],
            ],
            style=extend_table_style(styles["il-citation-main-table"], [
                ("LINEABOVE", (0, 0), (-1, 0), 0.5, "black"),
                ("LINEAFTER", (0, 0), (0, -1), 0.5, "black"),
                ("LINEAFTER", (3, 0), (4, -1), 0.5, "black"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (1, 0), (-1, -1), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 1),
                ("RIGHTPADDING", (0, 0), (-1, -1), 1),
            ]),
            colWidths=(31.8 * mm, 20 * mm, 4.1 * mm, 7.9 * mm, 30.5 * mm),
            rowHeights=7 * mm,
        )
        township = self.citation_info["complainant_municipality_township"] if self.citation_info[
            "complainant_municipality_township"] else ""
        scale_no = self.citation_info["complainant_scale_number"] if self.citation_info[
            "complainant_scale_number"] else ""
        scale_op = self.citation_info["complainant_scale_operator"] if self.citation_info[
            "complainant_scale_operator"] else ""
        t3 = Table(
            [
                [
                    SectionField("County of", styles["il-citation-field-header"],
                                 self.citation_info["municipality_county"], styles["il-citation-field-data"],
                                 offset=field_offset),
                    SectionField("Township of", styles["il-citation-field-header"],
                                 township,
                                 styles["il-citation-field-data"],
                                 offset=field_offset),
                    XBox(7, self.citation_info["complainant_is_township_road"]),
                    Paragraph("TWP. RD.", styles["il-citation-field-header"]),
                    SectionField("Scale #", styles["il-citation-field-header"],
                                 scale_no, styles["il-citation-field-data"],
                                 offset=field_offset),
                    SectionField("Scale Operator", styles["il-citation-field-header"],
                                 scale_op, styles["il-citation-field-data"],
                                 offset=field_offset),
                ],
            ],
            style=extend_table_style(styles["il-citation-main-table"], [
                ("LINEABOVE", (0, 0), (-1, 0), 0.5, "black"),
                ("LINEAFTER", (0, 0), (0, -1), 0.5, "black"),
                ("LINEAFTER", (3, 0), (5, -1), 0.5, "black"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 1),
                ("RIGHTPADDING", (0, 0), (-1, -1), 1),
            ]),
            colWidths=(21 * mm, 16.4 * mm, 3.5 * mm, 9.5 * mm, 13.4 * mm, 30.5 * mm,),
            rowHeights=7 * mm,
        )
        t4 = Table(
            [
                [
                    XBox(7, not self.citation_info["complainant_is_municipality"]),
                    Paragraph("PEOPLE STATE OF ILLINOIS", style=styles["il-citation-field-header"]),
                    XBox(7, self.citation_info["complainant_is_municipality"]),
                    Paragraph("CITY/VILLAGE OF MUNICIPAL CORPORATION PLAINTIFF",
                              style=styles["il-citation-field-header"]),
                    None,
                    Paragraph("VS.", style=styles["il-citation-field-header"])
                ]
            ],
            style=extend_table_style(styles["il-citation-main-table"], [
                ("OUTLINE", (0, 0), (-1, -1), 0.5, "black"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ]),
            colWidths=(6 * mm, 16 * mm, 6 * mm, 31 * mm, 30.8 * mm, 4.5 * mm),
            rowHeights=6 * mm,
        )
        return [self._section_gen_table(title="COMPLAINT", content=[t1, t2, t3, t4])]

    def _section_defendant_info(self):
        t1 = Table(
            [
                [
                    Paragraph("NAME", style=styles["il-citation-field-header"]),
                    None,
                    None,
                    None,
                ],
                [
                    SectionField("LAST", styles["il-citation-field-header-sm"],
                                 self.citation_info["defendant_last_name"], styles["il-citation-field-data"],
                                 offset=(0, 3 * mm)
                                 ),
                    SectionField("FIRST", styles["il-citation-field-header-sm"],
                                 self.citation_info["defendant_first_name"], styles["il-citation-field-data"],
                                 offset=(0, 3 * mm)
                                 ),
                    SectionField("MIDDLE NAME", styles["il-citation-field-header-sm"],
                                 self.citation_info["defendant_middle_initial"], styles["il-citation-field-data"],
                                 offset=(0, 3 * mm)
                                 ),
                ]
            ],
            style=[
                ("OUTLINE", (0, 0), (-1, -1), 0.5, "black"),
                ("SPAN", (0, 0), (2, 0)),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 1),
                ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ],
            colWidths=(27 * mm, 31.5 * mm, 12.8 * mm, 23 * mm,),
            rowHeights=(7 * mm, 2.5 * mm)
        )
        t2s1 = Table(
            [
                [
                    Paragraph("ADDRESS", style=styles["il-citation-field-header"]),
                ],
                [
                    SectionField("STREET", styles["il-citation-field-header-sm"],
                                 self.citation_info["defendant_address_street"], styles["il-citation-field-data"],
                                 offset=(0, 2 * mm)
                                 ),
                    SectionField("APT", styles["il-citation-field-header-sm"],
                                 self.citation_info["defendant_address_apartment"], styles["il-citation-field-data"],
                                 offset=(0, 2 * mm)
                                 ),
                ],
            ],
            style=[
                ("SPAN", (0, 0), (1, 0)),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 1),
                ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ],
            colWidths=(43 * mm, 16 * mm),
            rowHeights=(4.6 * mm, 2.4)
        )
        sex_m = 0
        sex_f = 0
        if self.citation_info["defendant_sex"] == "M":
            sex_m = 1
        elif self.citation_info["defendant_sex"] == "F":
            sex_f = 1
        address = self.citation_info["defendant_address_city"] + "    " + self.citation_info[
            "defendant_address_state"] + "    " + self.citation_info["defendant_address_zip"]
        dl_expiration = self.citation_info["defendant_driver_license_expiration_date"] if self.citation_info[
            "defendant_driver_license_expiration_date"] else ""
        t2 = Table(
            [
                [
                    t2s1,
                    None,
                    None,
                    None,
                    SectionField("EYES", styles["il-citation-field-header"],
                                 self.citation_info["defendant_eye_color"], styles["il-citation-field-data"],
                                 ),
                    None,
                    None,
                    XBox(7, sex_f),
                    Paragraph("Female", style=styles["il-citation-field-header-sm"]),
                ],
                [
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    XBox(7, sex_m),
                    Paragraph("Male", style=styles["il-citation-field-header-sm"])
                ],
                [
                    SectionField("CITY STATE ZIP", styles["il-citation-field-header"],
                                 address, styles["il-citation-field-data"],
                                 ),
                    None,
                    None,
                    None,
                    SectionField("HAIR", extend_style(styles["il-citation-field-header"], alignment=TA_CENTER),
                                 self.citation_info["defendant_hair_color"], styles["il-citation-field-data"],
                                 ),
                    SectionField("HEIGHT", extend_style(styles["il-citation-field-header"], alignment=TA_CENTER),
                                 self.citation_info["defendant_height"], styles["il-citation-field-data"],
                                 ),
                    None,
                    SectionField("WEIGHT", extend_style(styles["il-citation-field-header"], alignment=TA_CENTER),
                                 self.citation_info["defendant_weight"], styles["il-citation-field-data"],
                                 ),
                    None,
                ],
                [
                    SectionField("DR. LIC.", styles["il-citation-field-header"],
                                 self.citation_info["defendant_driver_license_number"],
                                 styles["il-citation-field-data"],
                                 ),
                    SectionField("STATE", extend_style(styles["il-citation-field-header"], alignment=TA_CENTER),
                                 self.citation_info["defendant_driver_license_state"], styles["il-citation-field-data"],
                                 ),
                    SectionField("CDL", extend_style(styles["il-citation-field-header"], alignment=TA_CENTER),
                                 str(self.citation_info["defendant_driver_license_is_commercial"]),
                                 styles["il-citation-field-data"],
                                 ),
                    SectionField("CLASS", extend_style(styles["il-citation-field-header"], alignment=TA_CENTER),
                                 self.citation_info["defendant_driver_license_class"],
                                 styles["il-citation-field-data"],
                                 ),
                    SectionField("EXPIR. DATE", extend_style(styles["il-citation-field-header"], alignment=TA_CENTER),
                                 dl_expiration,
                                 styles["il-citation-field-data"],
                                 ),
                    None,
                    SectionField("DOB", extend_style(styles["il-citation-field-header"], alignment=TA_CENTER),
                                 str(self.citation_info["defendant_date_of_birth"]),
                                 styles["il-citation-field-data"],
                                 ),
                ]
            ],
            style=[
                ("INNERGRID", (0, 0), (6, -1), 0.5, "black"),
                ("INNERGRID", (0, 2), (-1, -1), 0.5, "black"),
                ("OUTLINE", (0, 0), (-1, -1), 0.5, "black"),
                ("LINEBEFORE", (7, 0), (7, 1), 0.5, "black"),
                ("LINEBELOW", (7, 1), (8, 1), 0.5, "black"),
                ("SPAN", (0, 0), (3, 1)),
                ("SPAN", (4, 0), (6, 1)),
                ("SPAN", (0, 2), (3, 2)),
                ("SPAN", (5, 2), (6, 2)),
                ("SPAN", (7, 2), (8, 2)),
                ("SPAN", (4, 3), (5, 3)),
                ("SPAN", (6, 3), (8, 3)),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (7, 0), (-1, 1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 1),
                ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ],
            colWidths=(35 * mm, 8 * mm, 8 * mm, 8 * mm, 10.5 * mm, 5.8 * mm, 4.7 * mm, 4.5 * mm, 9.8 * mm),
            rowHeights=(3.5 * mm, 3.5 * mm, 6.7 * mm, 6.3 * mm)
        )
        return [self._section_gen_table(title="DEFENDANT", content=[t1, t2])]

    def _section_vehicle_info(self):
        ps = extend_style(styles["il-citation-field-header-sm"], alignment=TA_CENTER)
        t1s1 = Table(
            [
                [
                    Paragraph("COMMERCIAL MOTOR VEHICLE", style=styles["il-citation-field-header-sm"]),
                    Paragraph("YES", style=ps),
                    XBox(5, self.citation_info["vehicle_is_commercial"]),
                    Paragraph("NO", style=ps),
                    XBox(5, not self.citation_info["vehicle_is_commercial"]),
                ],
                [
                    Paragraph("PLACARDED HAZ. MATERIAL", style=styles["il-citation-field-header-sm"]),
                    Paragraph("YES", style=ps),
                    XBox(5, self.citation_info["vehicle_has_hazardous_materials_indicator"]),
                    Paragraph("NO", style=ps),
                    XBox(5, not self.citation_info["vehicle_has_hazardous_materials_indicator"]),
                ],
                [
                    Paragraph("16 OR MORE PASS. VEHICLE", style=styles["il-citation-field-header-sm"]),
                    Paragraph("YES", style=ps),
                    XBox(5, self.citation_info["vehicle_is_large_passenger_vehicle"]),
                    Paragraph("NO", style=ps),
                    XBox(5, not self.citation_info["vehicle_is_large_passenger_vehicle"]),
                ]
            ],
            style=extend_table_style(styles["il-citation-main-table"], [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (1, 0), (-1, -1), "CENTER"),
            ]),
            colWidths=(29 * mm, 3.5 * mm, 3 * mm, 3.5 * mm, 3 * mm),
            rowHeights=2.3 * mm
        )
        t1 = Table(
            [
                [
                    SectionField("REG. NO.", styles["il-citation-field-header"],
                                 self.citation_info["vehicle_plate"],
                                 styles["il-citation-field-data"],
                                 ),
                    SectionField("STATE", extend_style(styles["il-citation-field-header"], alignment=TA_CENTER),
                                 self.citation_info["vehicle_state"],
                                 styles["il-citation-field-data"],
                                 ),
                    SectionField("MO/YEAR", extend_style(styles["il-citation-field-header"], alignment=TA_CENTER),
                                 self.citation_info["vehicle_registration_expiration_date"],
                                 styles["il-citation-field-data"],
                                 ),
                    SectionField("ICC or US DOT #", styles["il-citation-field-header"],
                                 self.citation_info["vehicle_united_states_dot_number"],
                                 styles["il-citation-field-data"],
                                 ),
                ],
                [
                    SectionField("MAKE", styles["il-citation-field-header"],
                                 self.citation_info["vehicle_make"],
                                 styles["il-citation-field-data"],
                                 ),
                    SectionField("YEAR", extend_style(styles["il-citation-field-header"], alignment=TA_CENTER),
                                 self.citation_info["vehicle_year"],
                                 styles["il-citation-field-data"],
                                 ),
                    SectionField("COLOR", styles["il-citation-field-header"],
                                 self.citation_info["vehicle_color"],
                                 styles["il-citation-field-data"],
                                 ),
                    SectionField("NO. AXLES", styles["il-citation-field-header"],
                                 self.citation_info["vehicle_number_of_axles"],
                                 styles["il-citation-field-data"],
                                 ),
                ],
                [
                    SectionField("TYPE", styles["il-citation-field-header"],
                                 self.citation_info["vehicle_type"],
                                 styles["il-citation-field-data"],
                                 ),
                    [
                        Paragraph("VEHICLE USE:", styles["il-citation-field-header"]),
                        t1s1,
                    ],
                ],
                [
                    Paragraph("VIN", styles["il-citation-field-header"]),
                ]
            ],
            style=[
                ("GRID", (0, 0), (-1, -1), 0.5, "black"),
                ("SPAN", (1, 2), (3, 2)),
                ("SPAN", (1, 2), (3, 3)),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 1),
                ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ],
            colWidths=(42.5 * mm, 12.5 * mm, 15.5 * mm, 23.8 * mm,),
            rowHeights=(6.25 * mm, 6.25 * mm, 5 * mm, 4.6 * mm)
        )
        p1 = Paragraph(
            "The Undersigned states that on ____________________ at ____________________<br />"
            "Defendant did unlawfully operate a motor vehicle of the second division:",
            style=styles["il-citation-table-header"])
        ps = extend_style(styles["il-citation-table-header"], fontSize=4.5, leading=4.5, fontName="Arial")
        fe = [
            Paragraph(
                "On a Public Highway, Namely or other Location, Specifically",
                style=styles["il-citation-table-header"]
            ),
            HRFlowable(width="100%", thickness=0.5, lineCap="butt", color="black", spaceBefore=3.5 * mm, spaceAfter=0),
            Table(
                [
                    [
                        Paragraph(
                            "Located in the County and State Aforesaid and Did Then and There Commit the Following Offense",
                            style=ps
                        ),
                        XBox(5, self.citation_info["violation_is_in_urban_district"]),
                        Paragraph(
                            "URBAN DISTRICT",
                            style=styles["il-citation-field-header-sm"]
                        ),
                    ]
                ],
                style=extend_table_style(styles["il-citation-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ALIGN", (1, 0), (1, 0), "CENTER"),
                ]),
                colWidths=(76 * mm, 3 * mm, 15.3 * mm),
                rowHeights=2.5 * mm
            )
        ]
        return [self._section_gen_table(title="VEHICLE", content=[t1], header=p1, footer=fe)]

    def _section_violation_info(self):
        permit_no = self.citation_info["violation_permit_number"] if self.citation_info[
            "violation_permit_number"] else ""
        ps = extend_style(styles["il-citation-field-header"], fontName="Arial")
        t1s1 = Table(
            [
                [
                    XBox(6, True if self.citation_info["violation_type"] == "ILCS" else False),
                    Paragraph("ILCS", style=ps),
                    XBox(6, False if self.citation_info["violation_type"] == "ILCS" else True),
                    Paragraph("Local Ordinance", style=ps),
                    Paragraph("Overweight On:", style=ps),
                    Paragraph(str(self.citation_info["violation_date"]), styles["il-citation-field-data"]),
                    Paragraph("Permit #", style=ps),
                    Paragraph(permit_no, styles["il-citation-field-data"]),
                ],
            ],
            style=extend_table_style(styles["il-citation-main-table"], [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (0, -1), 2.5 * mm),
            ]),
            colWidths=(4.5 * mm, 8.5 * mm, 3 * mm, 17 * mm, 17 * mm, 17 * mm, 8.5 * mm, 18.8 * mm),
            rowHeights=5 * mm,
        )
        ps = extend_style(styles["il-citation-field-header-sm"], fontName="Arial")
        p = Paragraph(self.violation_text, style=extend_style(ps, leftIndent=2.5 * mm, rightIndent=2.5 * mm))
        description = [self.citation_info["violation_description"][i:i + 70] for i in
                       range(0, len(self.citation_info["violation_description"]), 70)]
        t1s2_content = [
            [
                None,
                Paragraph("Nature of Offense:", style=ps),
                Paragraph(description[0], style=ps),
            ]
        ]
        for i in range(1, 4):
            try:
                if description[i]:
                    t1s2_content.append(
                        [
                            None,
                            Paragraph(description[i], style=ps),
                        ]
                    )
            except IndexError:
                t1s2_content.append([None, None, None, None])
        t1s2 = Table(
            t1s2_content,
            style=extend_table_style(styles["il-citation-main-table"], [
                ("LINEBELOW", (2, 0), (2, 0), 0.5, "black"),
                ("LINEBELOW", (1, 1), (2, -1), 0.5, "black"),
                ("SPAN", (1, 1), (2, 1)),
                ("SPAN", (1, 2), (2, 2)),
            ]),
            colWidths=(2.5 * mm, 16.5 * mm, 72.8 * mm, 2.5 * mm),
            rowHeights=(4 * mm, 4 * mm, 4 * mm, 2 * mm)
        )
        t1 = Table(
            [
                [
                    t1s1
                ],
                [
                    p
                ],
                [
                    t1s2
                ],
            ],
            style=extend_table_style(styles["il-citation-main-table"], [
                ("OUTLINE", (0, 0), (-1, -1), 0.5, "black"),
            ]),
        )

        return [self._section_gen_table(title="VIOLATION", content=[t1])]

    def _section_weights_info(self):
        ts = extend_table_style(styles["il-citation-main-table"], [
            ("LEFTPADDING", (0, 0), (-1, -1), 1),
            ("RIGHTPADDING", (0, 0), (-1, -1), 1),
        ])
        gross_weight = str(self.citation_info["weights_gross_weight"]) if self.citation_info[
            "weights_gross_weight"] else ""
        test_date = str(self.citation_info["weights_test_date"]) if self.citation_info["weights_test_date"] else ""
        weather = str(self.citation_info["weights_weather"]) if self.citation_info["weights_weather"] else ""
        axle_data = ast.literal_eval(self.citation_info["weights_axle_weights"])
        axle_data = [str(key) + ": " + str(axle_data[key]) for key in sorted(axle_data, key=lambda k: k)]
        axle_list = []
        ad_len = len(axle_data)
        split_on = int(round((ad_len + 1) / 2))
        axle_list.append(axle_data[:split_on])
        axle_list.append(axle_data[split_on:])
        axle_table_data = []
        for i in range(0, len(axle_list[0])):
            v1 = axle_list[0][i]
            try:
                v2 = axle_list[1][i]
            except IndexError:
                v2 = ""
            axle_table_data.append(
                [
                    Paragraph(
                        v1,
                        style=styles["il-citation-field-data"]
                    ),
                    Paragraph(
                        v2,
                        style=styles["il-citation-field-data"]
                    ),
                ]
            )
        axle_table_data.append(
            [
                Paragraph(
                    "GROSS WEIGHT " + gross_weight,
                    style=styles["il-citation-field-data"]
                ),
            ]
        )
        sticker_list = ast.literal_eval(self.citation_info["weights_scale_sticker_number"])
        sticker_list = ["Scale Sticker # " + s for s in sticker_list if s]
        sticker_table_data = []
        for i in range(0, len(sticker_list)):
            sticker_table_data.append(
                [
                    Paragraph(
                        sticker_list[i],
                        style=styles["il-citation-field-data"]
                    ),
                ]
            )
        sticker_table_data.append(
            [
                Paragraph(
                    "Test Date: " + test_date,
                    style=styles["il-citation-field-data"])
            ]
        )
        sticker_table_data.append(
            [
                Paragraph(
                    "Dist. between axles: " + str(self.citation_info["weights_distance_between_axles"]),
                    style=styles["il-citation-field-data"]
                )
            ]
        )
        sticker_table_data.append(
            [
                Table(
                    [
                        [
                            XBox(5, self.citation_info["weights_functioning_auxiliary_power_unit"]),
                            Paragraph(
                                "Functioning Aux Power Unit",
                                style=extend_style(styles["il-citation-field-data"], fontSize=6, leading=7)
                            )
                        ]
                    ],
                    style=extend_table_style(ts, [
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ]),
                    colWidths=(4 * mm, None)
                )
            ]
        )
        sticker_table_data.append(
            [
                Paragraph(
                    "Weather: " + weather,
                    style=styles["il-citation-field-data"]
                )
            ]
        )

        t1s1 = Table(
            axle_table_data,
            style=extend_table_style(ts, [
                ("GRID", (0, 0), (-1, -1), 0.5, "black"),
                ("SPAN", (0, 5), (-1, 5)),
            ]),
            colWidths=26.4 * mm,
            rowHeights=2.6 * mm,
        )
        t1s2 = Table(
            sticker_table_data,
            style=extend_table_style(ts, [
                ("GRID", (0, 0), (-1, -1), 0.5, "black"),
                ("SPAN", (0, 5), (-1, 5)),
            ]),
            colWidths=37.5 * mm,
            rowHeights=2.6 * mm,
        )
        t1 = Table(
            [
                [
                    t1s1,
                    t1s2,
                ]
            ],
            style=[
                ("OUTLINE", (0, 0), (-1, -1), 0.5, "black"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 1 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 1 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1 * mm),
            ],
        )

        return [self._section_gen_table(title="WEIGHTS", content=[t1])]

    def _section_release_info(self):
        release_method = field_string_from_flags(self.citation_info, ["bond_includes_"])
        excess_weight = str(self.citation_info["bond_total_weight_excess"]) if self.citation_info[
            "bond_total_weight_excess"] else ""
        ps = extend_style(styles["il-citation-field-data"], fontSize=6, leading=6)
        t1 = Table(
            [
                [
                    SectionField("Lbs. in Excess", styles["il-citation-field-header"],
                                 excess_weight, ps, offset=(14 * mm, 1)),
                ],
                [
                    SectionField("Assessment Schedule #:", styles["il-citation-field-header"],
                                 "", ps, offset=(24 * mm, 1)),
                ],
                [
                    SectionField("Assessments", styles["il-citation-field-header"],
                                 "", ps, offset=(13 * mm, 1)),
                ],
                [
                    SectionField("Fine", styles["il-citation-field-header"],
                                 str(self.citation_info["bond_amount"]), ps, offset=(5 * mm, 1)),
                ],
                [
                    SectionField("Total Amount", styles["il-citation-field-header"],
                                 str(self.citation_info["total_bond_amount"]), ps, offset=(13 * mm, 1)),
                ],
                [
                    SectionField("Notes", styles["il-citation-field-header"],
                                 "", ps, offset=(6 * mm, 1)),
                ],
                [
                    None
                ],
                [
                    None
                ],
                [
                    None
                ],
                [
                    None
                ],
                [
                    SectionField("Bond Type", styles["il-citation-field-header"],
                                 release_method, ps, offset=(11 * mm, 1)),
                ],
                [
                    SectionField("Company", styles["il-citation-field-header"],
                                 self.citation_info["bond_card_issued_by"], ps, offset=(1 * mm, -3 * mm)),
                ],
                [
                    None
                ],
                [
                    SectionField("Auth/ Ref #", styles["il-citation-field-header"],
                                 self.citation_info["bond_auth_number"], ps, offset=(11 * mm, 1)),
                ],
            ],
            style=extend_table_style(styles["il-citation-main-table"], [
                ("GRID", (0, 0), (-1, -1), 0.5, "black"),
                ("SPAN", (0, 11), (0, 12)),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("VALIGN", (0, 11), (0, 12), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 1),
                ("RIGHTPADDING", (0, 0), (-1, -1), 1),
            ]),
            colWidths=35 * mm,
            rowHeights=3.8 * mm,
        )

        return [self._section_gen_table(title="RELEASE", content=[t1], title_width=4.3 * mm,
                                        content_width=t1.wrap(0, 0)[0])]

    def _section_court_info(self):
        time = str(self.citation_info["hearing_time"]) if self.citation_info["hearing_time"] else ""
        date = str(self.citation_info["hearing_court_date"]) if self.citation_info["hearing_court_date"] else ""
        ps_header = extend_style(styles["il-citation-field-header-sm"], fontName="Arial")
        ps_text = extend_style(styles["il-citation-field-data"], fontSize=6, leading=6)
        t1 = Table(
            [
                [
                    Paragraph("CIRCUIT COURT LOCATION, DATE AND TIME", styles["il-citation-field-header"]),
                    None,
                    None,
                    None,
                ],
                [
                    Paragraph("Court Location:", ps_header),
                    None,
                    Paragraph(self.citation_info["hearing_court_address"], ps_text),
                ],
                [
                    Paragraph("Date:", ps_header),
                    Paragraph(date, ps_text),
                    Paragraph("Time:", ps_header),
                    Paragraph(time, ps_text),
                ],
            ],
            style=extend_table_style(styles["il-citation-main-table"], [
                ("OUTLINE", (0, 0), (-1, -1), 0.5, "black"),
                ("SPAN", (0, 0), (-1, 0)),
                ("SPAN", (0, 1), (1, 1)),
                ("SPAN", (2, 1), (3, 1)),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 1),
                ("RIGHTPADDING", (0, 0), (-1, -1), 1),
            ]),
            colWidths=(5 * mm, 7.4 * mm, 15.6 * mm, 27 * mm),
            rowHeights=(8.7 * mm, 10.6 * mm, 3.25 * mm)
        )
        ps = extend_style(styles["il-citation-main"], fontSize=5.5, leading=6)
        t2 = Table(
            [
                [
                    Paragraph(
                        "Under penalties as provided by law for false certification pursuant to Section 1-109 of the Code of Civil Procedure and perjury pursuant to Section 32-2 of the Criminal Code of 2012, the undersigned certifies that the statements set forth in this instrument are true and correct.",
                        style=ps
                    ),
                    None,
                    None,
                    None,
                ],
                [

                ],
                [
                    Paragraph(
                        "Month",
                        style=ps
                    ),
                    Paragraph(
                        "Day",
                        style=ps
                    ),
                    Paragraph(
                        "Year",
                        style=ps
                    ),
                ],
                [
                    Paragraph(
                        "Officer Signature",
                        style=ps
                    ),
                    None,
                    None,
                    Paragraph(
                        "ID No.",
                        style=extend_style(ps, alignment=TA_RIGHT)
                    ),
                ],
                [
                    Paragraph(
                        "WITHOUT ADMITTING GUILT, I promise to comply with the terms of this Ticket and Release",
                        ps),
                ],
                [
                    Paragraph(
                        "Signature of Violator",
                        style=extend_style(ps, alignment=TA_CENTER)
                    ),
                ]
            ],
            style=extend_table_style(styles["il-citation-main-table"], [
                ("LINEABOVE", (0, 2), (2, 2), 0.5, "black"),
                ("LINEABOVE", (0, 3), (-1, 3), 0.5, "black"),
                ("LINEABOVE", (0, 5), (-1, 5), 0.5, "black"),
                ("SPAN", (0, 0), (-1, 0)),
                ("SPAN", (0, 3), (2, 3)),
                ("SPAN", (0, 4), (-1, 4)),
                ("SPAN", (0, 5), (-1, 5)),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]),
            colWidths=(12 * mm, 10.4 * mm, 4.8 * mm, 25.8 * mm),
            rowHeights=[None, 5 * mm, 9.8 * mm, 4 * mm, 11.5 * mm, 3.3 * mm],
        )

        return [self._section_gen_table(title="Court Place/Date", footer=[t2], content=[t1], title_width=4.3 * mm,
                                        content_width=t1.wrap(0, 0)[0])]


class NonTrafficCitationReport(CitationReport):
    def __init__(self, citation_info, header, copy_type, copy_type_info=None, sections=None, title=None, author=None):
        if not sections:
            sections = [
                "header", "complaint_info", "defendant_info", "court_info", "bond_info", "footer", "instructions"
            ]
        CitationReport.__init__(self, citation_info, sections, header, copy_type, copy_type_info, "", title,
                                author)
        self.page_size = (4 * inch, 1 * inch)
        self.page_margin = 2 * mm
        self.title_width = 3.3 * mm
        self.content_width = self.page_size[0] - 2 * self.page_margin - self.title_width
