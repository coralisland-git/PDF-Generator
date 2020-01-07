# coding=utf-8
import cStringIO
import io

from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    Table,
    Spacer,
    TableStyle,
    BaseDocTemplate,
    PageTemplate,
    Frame,
)

from common.signatures import *
from document_specific_styles import styles


def generate_check_request_form(pdf_dict, title=None, author=None):
    report = CheckRequestForm(title=title, author=author)
    try:
        buff = cStringIO.StringIO()
    except NameError:
        buff = None
    return report.create_report(pdf_dict, buff)


class PDFReport:
    def __init__(
        self,
        page_size=None,
        page_margin=None,
        page_padding=None,
        doc_template_type=None,
        sections=None,
        title=None,
        author=None,
        subject=None,
        creator=None,
    ):
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


class CheckRequestForm(PDFReport):
    def __init__(self, *args, **kwargs):
        PDFReport.__init__(
            self,
            *args,
            page_size=letter,
            page_margin=(19 * mm, 19 * mm),
            page_padding=(4.4 * mm, 0),
            doc_template_type=SignatureDocTemplate,
            **kwargs
        )
        self.min_invoice_lines = 8

    def _content_methods(self):
        methods = PDFReport._content_methods(self)
        methods.insert(0, methods.pop(methods.index("_section_doc_header")))
        return methods

    @staticmethod
    def _create_section_table(elems, style=None):
        if not style:
            style = styles["section-table"]
        t = Table([[elems]], style=style)
        return [Spacer(0, 3.6 * mm), t]

    @staticmethod
    def _create_field(label, label_width, value, value_width):
        t = Table(
            [
                [
                    Paragraph(label, styles["field-label"]),
                    Paragraph(value, styles["field-value"]),
                ]
            ],
            style=extend_table_style(
                styles["main-table"],
                [
                    ("VALIGN", (1, 0), (1, -1), "MIDDLE"),
                    ("LEFTPADDING", (1, 0), (1, -1), 0.7 * mm),
                    ("LINEBELOW", (1, 0), (1, -1), 0.5 * mm, "black", "butt"),
                ],
            ),
            colWidths=(label_width, value_width),
            rowHeights=6.025 * mm,
        )
        return t

    def _section_doc_header(self):
        elems = [
            Spacer(0, 6.2 * mm),
            Paragraph(
                "Check Request Form", extend_style(styles["main"], alignment=TA_CENTER)
            ),
            Spacer(0, 0.1 * mm),
            Paragraph(
                "<b>CITY OF BROOKHAVEN – CHECK REQUEST</b>", styles["doc-header"]
            ),
            Spacer(0, 0.2 * mm),
        ]
        return elems

    def _section_1(self):
        elems = [
            Paragraph("VENDOR INFORMATION", styles["sect-header"]),
            Table(
                [
                    [
                        self._create_field(
                            "Vendor #",
                            15.25 * mm,
                            "%s" % self.data["vendor_number"],
                            39.5 * mm,
                        ),
                        None,
                    ],
                    [
                        self._create_field(
                            "Name:",
                            12.7 * mm,
                            "%s" % self.data["vendor_name"],
                            83.6 * mm,
                        ),
                        None,
                    ],
                    [
                        self._create_field(
                            "Street 1:",
                            14.4 * mm,
                            "%s" % self.data["vendor_street1"],
                            81.1 * mm,
                        ),
                        self._create_field(
                            "Phone:",
                            12.1 * mm,
                            "%s" % self.data["vendor_phone1"],
                            49 * mm,
                        ),
                    ],
                    [
                        self._create_field(
                            "Street 2:",
                            14.4 * mm,
                            "%s" % self.data["vendor_street2"],
                            81.1 * mm,
                        ),
                        self._create_field(
                            "Phone:",
                            12.1 * mm,
                            "%s" % self.data["vendor_phone2"],
                            49 * mm,
                        ),
                    ],
                    [
                        self._create_field(
                            "City, ST Zip:",
                            19.1 * mm,
                            "%s" % self.data["vendor_city_state"],
                            76.3 * mm,
                        ),
                        self._create_field(
                            "Fax:", 7.2 * mm, "%s" % self.data["vendor_fax"], 53.9 * mm
                        ),
                    ],
                    [
                        self._create_field(
                            "FEI/SS #",
                            13.5 * mm,
                            "%s" % self.data["vendor_fei_ss"],
                            54.1 * mm,
                        ),
                        None,
                    ],
                ],
                style=extend_table_style(
                    styles["main-table"],
                    [
                        ("RIGHTPADDING", (1, 0), (1, -1), 2.4 * mm),
                        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                    ],
                ),
            ),
        ]
        return self._create_section_table(elems)

    def _section_2(self):
        def create_row(fund, dept, account, amount):
            row_data = [
                Paragraph("Fund", styles["field-label"]),
                Paragraph("%s" % fund, styles["invoice-field-value"]),
                None,
                Paragraph("Dept. Code:", styles["field-label"]),
                Paragraph("%s" % dept, styles["invoice-field-value"]),
                None,
                Paragraph("Acct", styles["field-label"]),
                Paragraph("%s" % account, styles["invoice-field-value"]),
                None,
                Paragraph("$", styles["field-label"]),
                Paragraph("%s" % amount, styles["invoice-field-value"]),
            ]
            return row_data

        elems = [
            Paragraph(
                "INVOICE INFORMATION (one invoice per request)", styles["sect-header"]
            ),
            Table(
                [
                    [
                        self._create_field(
                            "Invoice #",
                            15 * mm,
                            "%s" % self.data["invoice_number"],
                            46.7 * mm,
                        )
                    ],
                    [
                        Table(
                            [
                                [
                                    Paragraph(
                                        "Purchase Order / Encumbrance Number",
                                        styles["field-label"],
                                    ),
                                    Paragraph(
                                        "%s" % self.data["po_number"],
                                        styles["field-value"],
                                    ),
                                ],
                                [None, None],
                            ],
                            style=extend_table_style(
                                styles["main-table"],
                                [
                                    ("VALIGN", (1, 0), (1, -1), "MIDDLE"),
                                    ("LEFTPADDING", (1, 0), (1, -1), 1 * mm),
                                    (
                                        "LINEBELOW",
                                        (1, 0),
                                        (1, 0),
                                        0.5 * mm,
                                        "black",
                                        "butt",
                                    ),
                                    ("OUTLINE", (1, 0), (1, -1), 0.4, "black"),
                                ],
                            ),
                            colWidths=64.2 * mm,
                            rowHeights=(6 * mm, 0.7 * mm),
                        )
                    ],
                ],
                style=styles["main-table"],
            ),
        ]
        table_rows = list()
        invoice_lines = max(self.min_invoice_lines, len(self.data["invoice_lines"]))
        for i in range(0, invoice_lines):
            try:
                table_rows.append(
                    create_row(
                        self.data["invoice_lines"][i]["fund"],
                        self.data["invoice_lines"][i]["dept_code"],
                        self.data["invoice_lines"][i]["acct"],
                        self.data["invoice_lines"][i]["amount"],
                    )
                )
            except IndexError:
                table_rows.append(create_row("", "", "", ""))
        table_rows.append(
            [
                None,
                None,
                None,
                Paragraph(
                    "Subtotal From Additional Lines on Attached Page",
                    extend_style(styles["main"], fontSize=10),
                ),
                None,
                None,
                None,
                None,
                None,
                Paragraph("$", styles["field-label"]),
                Paragraph(
                    "%s" % self.data["invoice_additional_subtotal"],
                    styles["field-value"],
                ),
            ]
        )
        table_rows.append(
            [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                Paragraph(
                    "<b>TOTAL</b>",
                    extend_style(
                        styles["field-label"], alignment=TA_RIGHT, fontSize=12
                    ),
                ),
                None,
                Paragraph("$", styles["field-label"]),
                Paragraph("%s" % self.data["invoice_total"], styles["field-value"]),
            ]
        )
        elems.append(
            Table(
                table_rows,
                style=extend_table_style(
                    styles["main-table"],
                    [
                        ("VALIGN", (1, 0), (1, -3), "MIDDLE"),
                        ("LEFTPADDING", (1, 0), (1, -3), 0.5 * mm),
                        ("LINEBELOW", (1, 0), (1, -3), 0.5 * mm, "black", "butt"),
                        ("VALIGN", (4, 0), (4, -3), "MIDDLE"),
                        ("LEFTPADDING", (4, 0), (4, -3), 0.5 * mm),
                        ("LINEBELOW", (4, 0), (4, -3), 0.5 * mm, "black", "butt"),
                        ("VALIGN", (7, 0), (7, -3), "MIDDLE"),
                        ("LEFTPADDING", (7, 0), (7, -3), 0.5 * mm),
                        ("LINEBELOW", (7, 0), (7, -3), 0.5 * mm, "black", "butt"),
                        ("SPAN", (3, -2), (7, -2)),
                        ("VALIGN", (10, 0), (10, -1), "MIDDLE"),
                        ("LEFTPADDING", (10, 0), (10, -1), 0.5 * mm),
                        ("LINEBELOW", (10, 0), (10, -1), 0.5 * mm, "black", "butt"),
                    ],
                ),
                colWidths=(
                    8.8 * mm,
                    14.7 * mm,
                    None,
                    19.5 * mm,
                    17.5 * mm,
                    None,
                    7.8 * mm,
                    29.5 * mm,
                    None,
                    2.5 * mm,
                    22.5 * mm,
                ),
                rowHeights=6 * mm,
            )
        )
        return self._create_section_table(elems)

    def _section_3(self):
        elems = [
            Paragraph("SPECIAL INSTRUCTIONS", styles["sect-header"]),
            Spacer(0, 0.5 * mm),
            Table(
                [
                    [
                        Paragraph("Time Sensitive:", styles["main"]),
                        Paragraph(
                            "%s" % self.data["instructions_time_sensitive"],
                            extend_style(styles["field-label"], alignment=TA_CENTER),
                        ),
                    ]
                ],
                style=styles["main-table"],
                colWidths=(24 * mm, None),
            ),
            Table(
                [
                    [
                        Paragraph("Other:", styles["main"]),
                        Paragraph(
                            "%s" % self.data["instructions_other"],
                            extend_style(
                                styles["field-value"], fontSize=10, leading=13
                            ),
                        ),
                    ],
                    [
                        None,
                        Paragraph(
                            "(If invoice is for meals, travels, or entertainment, include purpose and attendees on this line.)",
                            extend_style(styles["main"], alignment=TA_CENTER),
                        ),
                    ],
                ],
                style=extend_table_style(
                    styles["main-table"],
                    [
                        ("LINEBELOW", (1, 0), (1, 0), 0.5 * mm, "black", "butt"),
                        ("VALIGN", (1, 0), (1, 0), "MIDDLE"),
                        ("LEFTPADDING", (1, 0), (1, 0), 0.5 * mm),
                    ],
                ),
                colWidths=(11.1 * mm, None),
                rowHeights=(5.8 * mm, 4.75 * mm),
            ),
        ]
        ts = extend_table_style(
            styles["section-table"], [("RIGHTPADDING", (-1, 0), (-1, -1), 3 * mm)]
        )
        return self._create_section_table(elems, style=ts)

    def _section_4(self):
        elems = [Paragraph("APPROVAL", styles["sect-header"]), Spacer(0, 0.5 * mm)]
        table_data = [
            [
                Paragraph(
                    "%s" % self.data["approval_preparer"],
                    styles["approval-field-value"],
                ),
                None,
                Paragraph(
                    "%s" % self.data["approval_date"], styles["approval-field-value"]
                ),
            ],
            [
                Paragraph("Preparer (Print Name)", styles["main"]),
                None,
                Paragraph("Date", styles["main"]),
            ],
            [
                SignatureRect(114 * mm, 5.4 * mm, label="Department", sig_id="DS-01"),
                None,
                SignatureDatetimeRect(36 * mm, 5.4 * mm, sig_id="DS-01"),
            ],
            [
                Paragraph("Department Authorization Signature", styles["main"]),
                None,
                Paragraph("Date", styles["main"]),
            ],
            [
                SignatureRect(
                    114 * mm, 5.4 * mm, label="City Manager", sig_id="CMS-01"
                ),
                None,
                SignatureDatetimeRect(36 * mm, 5.4 * mm, sig_id="CMS-01"),
            ],
            [
                Paragraph("City Manager (if required) Signature", styles["main"]),
                None,
                Paragraph("Date", styles["main"]),
            ],
            [
                SignatureRect(
                    114 * mm, 5.4 * mm, label="Finance Department", sig_id="FDS-01"
                ),
                None,
                SignatureDatetimeRect(36 * mm, 5.4 * mm, sig_id="FDS-01"),
            ],
            [
                Paragraph("Finance Department Authorization Signature", styles["main"]),
                None,
                Paragraph("Date", styles["main"]),
            ],
        ]
        row_heights = list()
        for i in range(0, len(table_data)):
            if i % 2 == 0:
                row_heights.append(5.8 * mm)
            else:
                row_heights.append(5 * mm)
        t = Table(
            table_data,
            style=styles["main-table"],
            colWidths=(115.5 * mm, None, 37 * mm),
            rowHeights=row_heights,
            spaceBefore=-0.3 * mm,
        )
        for i in range(0, t._nrows, 2):
            t.setStyle(
                TableStyle(
                    [
                        ("VALIGN", (0, i), (-1, i), "MIDDLE"),
                        ("LEFTPADDING", (0, i), (-1, i), 0.5 * mm),
                        ("LINEBELOW", (0, i), (0, i), 0.5 * mm, "black", "butt"),
                        ("LINEBELOW", (2, i), (2, i), 0.5 * mm, "black", "butt"),
                    ]
                )
            )
        elems.append(t)
        ts = extend_table_style(
            styles["section-table"],
            [
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0.7 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3 * mm),
            ],
        )
        return self._create_section_table(elems, style=ts)

    def _section_5(self):
        elems = [
            Table(
                [
                    [
                        None,
                        Paragraph(
                            "FINANCE USE ONLY",
                            extend_style(
                                styles["sect-header"],
                                backColor="lightgrey",
                                leading=14,
                                fontSize=11,
                            ),
                        ),
                        None,
                    ]
                ],
                style=styles["main-table"],
                colWidths=[None, 31 * mm, None],
            ),
            Paragraph("%s" % self.data["finance_note"], styles["main"]),
            Spacer(0, 4 * mm),
        ]
        return self._create_section_table(elems)
