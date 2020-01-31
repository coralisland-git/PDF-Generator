# coding=utf-8
from document_specific_styles import styles, extend_style, extend_table_style
from common.signatures import SignatureDocTemplate, SignatureRect, SignatureDatetimeRect
import io
import textwrap
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import registerFontFamily, stringWidth
from reportlab.platypus import Paragraph, Table, Spacer, BaseDocTemplate, PageTemplate, Frame, Image, Flowable

try:
    import cStringIO
except ModuleNotFoundError:
    pass

registerFontFamily(
    "Arial",
    normal="Arial",
    bold="Arial-Bold",
    italic="Arial-Italic",
    boldItalic="Arial-Bolditalic",
)


def generate_dds_correction_form(pdf_dict, title=None, author=None):
    report = DDSCorrectionForm(title=title, author=author)
    try:
        buff = cStringIO.StringIO()
    except NameError:
        buff = None
    return report.create_report(pdf_dict, buff)


class RadioButton(Flowable):
    def __init__(self, size=15, checked=None):
        Flowable.__init__(self)
        self.width = self.height = size
        self.checked = checked

    def draw(self):
        stroke_percent = 0.08
        size = self.width
        stroke_width = size * stroke_percent
        self.canv.saveState()

        offset = size / 2.0
        size = size - stroke_width
        self.canv.setLineWidth(stroke_width)
        self.canv.setStrokeColor(colors.black)
        self.canv.circle(offset, offset, size / 2)

        offset = stroke_width * 1.5
        size = size - (stroke_width / 2)
        self.canv.setStrokeColor(colors.grey)
        self.canv.arc(offset, offset, size, size, startAng=45, extent=180)
        self.canv.setStrokeColor(colors.lightgrey)
        self.canv.arc(offset, offset, size, size, startAng=225, extent=180)

        if self.checked:
            offset = self.width / 2.0
            size = (size - stroke_width * 2.5) / 2.0
            self.canv.setFillColor(colors.black)
            self.canv.circle(offset, offset, size / 2, stroke=0, fill=1)

        self.canv.restoreState()


class PDFReport:
    def __init__(self, page_size=None, page_margin=None, page_padding=None, doc_template_type=None, sections=None,
                 title=None, author=None, subject=None, creator=None):
        self.page_size = page_size if page_size else letter
        self.page_margin = page_margin if page_margin else (12.7 * mm, 12.7 * mm)
        self.page_padding = page_padding if page_padding else (0, 0)
        self.doc_template_type = (
            doc_template_type if doc_template_type else BaseDocTemplate
        )
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

    def _create_document(self, buff):
        page_t = PageTemplate(
            "normal",
            [
                Frame(
                    self.page_margin[0],
                    self.page_margin[1],
                    self.page_size[0] - self.page_margin[0] * 2,
                    self.page_size[1] - self.page_margin[1] * 2,
                    leftPadding=self.page_padding[0],
                    bottomPadding=self.page_padding[1],
                    rightPadding=self.page_padding[0],
                    topPadding=self.page_padding[1],
                )
            ],
        )
        doc_t = self.doc_template_type(
            buff,
            pagesize=letter,
            title=self.title,
            author=self.author,
            subject=self.subject,
            creator=self.creator,
            leftMargin=self.page_margin[0],
            rightMargin=self.page_margin[0],
            topMargin=self.page_margin[1],
            bottomMargin=self.page_margin[1],
        )
        doc_t.addPageTemplates(page_t)
        return doc_t


class DDSCorrectionForm(PDFReport):
    def __init__(self, *args, **kwargs):
        PDFReport.__init__(
            self,
            *args,
            page_size=letter,
            page_margin=(6.3 * mm, 6.3 * mm),
            page_padding=(2.2 * mm, 0),
            doc_template_type=SignatureDocTemplate,
            **kwargs
        )

    def _content_methods(self):
        methods = PDFReport._content_methods(self)
        methods.insert(0, methods.pop(methods.index("_section_doc_header")))
        return methods

    @staticmethod
    def _create_section_table(elems, style=None):
        if not style:
            style = styles["section-table"]
        return Table([[elems]], style=style, colWidths=194.6 * mm, hAlign="RIGHT")

    @staticmethod
    def _create_field(label, label_width, value, value_width):
        t = Table(
            [[
                Paragraph(label, styles["field-label"]),
                Paragraph(value, styles["field-value"]),
            ]],
            style=extend_table_style(styles["main-table"], [
                ("LEFTPADDING", (1, 0), (1, -1), 0.5 * mm),
                ("LINEBELOW", (1, 0), (1, -1), 0.25 * mm, "black", "butt"),
            ]),
            colWidths=(label_width, value_width),
            rowHeights=9.7 * mm,
        )
        return t

    @staticmethod
    def _create_radio_option(label, size, checked=None, style=None):
        ts = style if style else extend_table_style(styles["main-table"], [
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ])
        t = Table(
            [[
                RadioButton(size, checked),
                Paragraph("%s" % label, style=styles["main"])
            ]],
            style=ts,
            colWidths=(size * 1.25, None)
        )
        return t

    def _section_doc_header(self):
        max_height = 16.2 * mm
        elems = [
            Spacer(0, 6.3 * mm),
            Table(
                [[
                    Image("dds_logo.jpg", width=61 * mm, height=max_height, kind='proportional'),
                    None,
                    Paragraph("<b>Court Correction Request<br />Fax to %s</b>" % self.data["header_fax"],
                              styles["doc-header"]),
                    None
                ]],
                style=extend_table_style(styles["main-table"], [
                    ("ALIGN", (0, 0), (0, 0), "CENTER"),
                    ("BACKGROUND", (2, 0), (2, 0), "black"),
                    ("LEFTPADDING", (2, 0), (2, 0), 2.8 * mm),
                    ("BOTTOMPADDING", (2, 0), (2, 0), 2 * mm),
                    # ("HALIGN", (2, 0), (2, 0), "CENTER"),
                ]),
                colWidths=[66 * mm, 24.8 * mm, 82.8 * mm],
                rowHeights=max_height
            ),
            Spacer(0, 2.7 * mm),
        ]
        return [self._create_section_table(elems, styles["main-table"])]

    def _section_1(self):
        elems = list()
        dob_parts = self.data["defendant_dob"].split("/")
        ps = extend_style(styles["field-value"], alignment=TA_CENTER)
        t1 = Table(
            [[
                self._create_field("First Name:", 22.9 * mm, "%s" % self.data["defendant_firstname"], 84.8 * mm),
                None,
                self._create_field("Middle Name:", 27 * mm, "%s" % self.data["defendant_middlename"], 47 * mm),
                None
            ]],
            style=styles["main-table"]
        )
        t2 = Table(
            [[
                Paragraph("Date of Birth (MM/DD/YYYY):", styles["field-label"]),
                Paragraph(dob_parts[0], ps),
                Paragraph("/", ps),
                Paragraph(dob_parts[1], ps),
                Paragraph("/", ps),
                Paragraph(dob_parts[2], ps)
            ]],
            style=extend_table_style(styles["main-table"], [
                ("LEFTPADDING", (1, 0), (1, 0), 0.5 * mm),
                ("LINEBELOW", (1, 0), (1, 0), 0.25 * mm, "black", "butt"),
                ("LINEBELOW", (3, 0), (3, 0), 0.25 * mm, "black", "butt"),
                ("LINEBELOW", (5, 0), (5, 0), 0.25 * mm, "black", "butt"),
            ]),
            colWidths=(57.6 * mm, 16.5 * mm, 3.5 * mm, 19 * mm, 3.5 * mm, 35.5 * mm),
            rowHeights=9.7 * mm,
        )
        t3 = Table(
            [[
                self._create_field("Driver’s License  (state):", 45.5 * mm,
                                   "%s" % self.data["defendant_license_state"], 21.3 * mm),
                self._create_field("(number):", 19 * mm, "%s" % self.data["defendant_license_no"], 89.5 * mm),
            ]],
            style=styles["main-table"],
            colWidths=(69.1 * mm, None)
        ),
        elems.append(
            Table(
                [
                    [self._create_field("Defendant Information:  Last Name:", 66.9 * mm,
                                        "%s" % self.data["defendant_lastname"], 117.8 * mm)],
                    [t1],
                    [t2],
                    [t3],
                ],
                style=styles["main-table"],
            )
        )
        return [self._create_section_table(elems)]

    def _section_2(self):
        elems = list()
        table_data = list()
        table_data.append([
            Table(
                [[
                    self._create_field("Court", 11.5 * mm, "%s" % self.data["court_name"], 101.1 * mm),
                    self._create_field("Telephone #", 24.5 * mm, "%s" % self.data["court_phone"], 49.5 * mm),
                ]],
                style=styles["main-table"],
                colWidths=(113.8 * mm, None)
            )
        ])
        ps = extend_style(style=styles["main"], fontSize=10, leading=12)
        table_data.append([
            Table(
                [[
                    self._create_field("Citation Number", 31.6 * mm, "%s" % self.data["court_citation"], 103.5 * mm),
                    Paragraph("&nbsp;(if no citation, use case number)", style=ps)
                ]],
                style=styles["main-table"],
            )
        ])
        table_data.append([
            Table(
                [[
                    self._create_field("Original Charge", 30.5 * mm, "%s" % self.data["court_charge"], 89.5 * mm),
                    self._create_field("O.C.G.A. §", 21 * mm, "%s" % self.data["court_ocga"], 47 * mm),
                ]],
                style=styles["main-table"],
            )
        ])
        table_data.append([
            Table(
                [[
                    self._create_field("Disposition Date", 31.8 * mm, "%s" % self.data["court_disposition_date"],
                                       58.8 * mm),
                    self._create_field("Violation Date", 27.6 * mm, "%s" % self.data["court_violation_date"],
                                       61.2 * mm),
                ]],
                style=styles["main-table"],
                colWidths=(97.7 * mm, None)
            )
        ])
        option_list = ["Guilty", "Nolo Contendere", "Bond Forfeiture", "First Offender"]
        idx = option_list.index(self.data["court_disposition"])
        option_elems = list()
        for i in range(0, len(option_list)):
            checked = True if idx == i else False
            label = "<i>%s</i>" % option_list[i] if option_list[i] == "Nolo Contendere" else option_list[i]
            option_elems.append(self._create_radio_option(label, 4.42 * mm, checked=checked))
        option_elems.insert(0, Paragraph("Original Disposition:", styles["field-label"]))
        table_data.append([
            Table(
                [option_elems],
                style=styles["main-table"],
                colWidths=(40.5 * mm, 25.5 * mm, 45 * mm, 38 * mm, None),
            )
        ])
        elems.append(
            Table(
                table_data,
                style=styles["main-table"],
                rowHeights=9.7 * mm,
            )
        )
        return [self._create_section_table(elems)]

    def _section_3(self):
        elems = [
            Paragraph(
                "<i>For the above listed case only, please correct the charge(including the new O.C.G.A. Code Section) and/or disposition (if Rule Nisi, include new disposition date) to indicate:</i>",
                styles["main"]
            ),
        ]
        width = 188 * mm
        ps = styles["field-label"]
        if self.data["change_text"]:
            text_width = stringWidth(self.data["change_text"], ps.fontName, ps.fontSize)
            lines = textwrap.wrap(self.data["change_text"],
                                  int(len(self.data["change_text"]) / (text_width / int((width) + 1))))
            if len(lines) < 2:
                lines.append("")
        else:
            lines = ["", ""]
        table_data = list()
        for line in lines:
            table_data.append([Paragraph(line, ps)])
        elems.append(
            Table(
                table_data,
                style=extend_table_style(styles["main-table"], [
                    ("LINEBELOW", (0, 0), (-1, -1), 0.25 * mm, "black", "butt"),
                ]),
                rowHeights=9.7 * mm
            )
        )
        ts = extend_table_style(styles["main-table"], [
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "TOP")
        ])
        elems.append(
            Table(
                [
                    [
                        Paragraph("This change is being made pursuant to O.C.G.A. §§ 40-13-32 and 40-13-33 as follows:",
                                  style=styles["main"])
                    ],
                    [
                        self._create_radio_option(
                            "within  90 days of disposition at the court’s discretion",
                            4.42 * mm,
                            checked=self.data["change_reason_within90"],
                            style=ts
                        )
                    ],
                    [
                        self._create_radio_option(
                            "more than 90 days but not more than 180 days after disposition pursuant to the notification and hearing requirements of O.C.G.A. §40-13-32",
                            4.42 * mm,
                            checked=self.data["change_reason_within180"],
                            style=ts
                        )
                    ],
                    [
                        self._create_radio_option(
                            "to correct a clerical error (at any time) ",
                            4.42 * mm,
                            checked=self.data["change_reason_clerical"],
                            style=ts
                        )
                    ],
                ],
                style=extend_table_style(styles["main-table"], [
                    ("TOPPADDING", (0, 0), (-1, -1), 5 * mm),
                ]),
            )
        )
        elems.extend([
            Spacer(0, 5 * mm),
            self._create_field("Court Official Requesting Change (please print):", 91 * mm,
                               "%s" % self.data["change_court_official"], 96.5 * mm),
            self._create_field("Title of Official Requesting Change (please print):", 94 * mm,
                               "%s" % self.data["change_title_official"], 93.5 * mm),
            Spacer(0, 5 * mm),
        ])
        elems.append(
            Table(
                [[
                    Paragraph("Signature of Requesting Official:", styles["field-label"]),
                    SignatureRect(124 * mm, 9.5 * mm, label="Requesting Official", sig_id="RS-01"),
                ]],
                style=extend_table_style(styles["main-table"], [
                    ("LEFTPADDING", (1, 0), (1, -1), 0.5 * mm),
                    ("LINEBELOW", (1, 0), (1, -1), 0.25 * mm, "black", "butt"),
                ]),
                colWidths=(61.5 * mm, 126 * mm),
                rowHeights=9.7 * mm,
            )
        )
        elems.append(Spacer(0, 5 * mm))
        table_data = [
            [
                Table(
                    [[
                        Paragraph("Date of Request:", styles["field-label"]),
                        SignatureDatetimeRect(59 * mm, 9.5 * mm, sig_id="RS-01"),
                    ]],
                    style=extend_table_style(styles["main-table"], [
                        ("LEFTPADDING", (1, 0), (1, -1), 0.5 * mm),
                        ("LINEBELOW", (1, 0), (1, -1), 0.25 * mm, "black", "butt"),
                    ]),
                    colWidths=(32.5 * mm, 61 * mm),
                    rowHeights=9.7 * mm,
                ),
                # Image("dds_seal.jpg", width=30 * mm, height=15 * mm, kind='proportional'),
                Paragraph("<b>Court Seal Here</b>",
                          extend_style(styles["main"], textColor=colors.HexColor(0xC1C1C1), alignment=TA_CENTER)),

            ],
            [
                Paragraph("<i>DS-1195&nbsp;&nbsp;01/07</i>", extend_style(styles["main"], fontSize=6, leading=10)),
                None
            ]
        ]
        elems.append(
            Table(
                table_data,
                style=extend_table_style(styles["main-table"], [
                    ("SPAN", (1, 0), (1, 1)),
                    ("LEFTPADDING", (0, 1), (0, 1), 0.5 * mm),
                    ("TOPPADDING", (1, 0), (1, -1), 4.5 * mm),
                    ("LEFTPADDING", (1, 0), (1, -1), 28 * mm),
                    ("VALIGN", (1, 0), (1, -1), "MIDDLE"),
                    ("ALIGN", (1, 0), (1, -1), "CENTER"),
                ]),
                rowHeights=(9.7 * mm, 9.0 * mm)
            )
        )
        elems.append(Spacer(0, 0.9 * mm))
        return [self._create_section_table(elems)]
