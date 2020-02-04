# coding=utf-8
from document_specific_styles import styles, extend_style, extend_table_style
import io
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, Table, Spacer, BaseDocTemplate, PageTemplate, Frame

try:
    import cStringIO
except ModuleNotFoundError:
    pass


def generate_fee_bill(pdf_dict, title=None, author=None):
    report = FeeBill(title=title, author=author)
    try:
        buff = cStringIO.StringIO()
    except NameError:
        buff = None
    return report.create_report(pdf_dict, buff)


class RoundRectTable(Table):
    def __init__(self, *args, **kwargs):
        self.backColor = None
        self.cornerRadius = 0
        self.leftIndent = 0
        attrs = ["backColor", "cornerRadius", "leftIndent"]
        for attr in attrs:
            if attr in kwargs:
                setattr(self, attr, kwargs[attr])
                del kwargs[attr]
        Table.__init__(self, *args, **kwargs)

    def draw(self):
        self.canv.saveState()
        self.canv.setFillColor("lightgrey")
        self.canv.roundRect(
            0 + self.leftIndent, 0, self._width - self.leftIndent, self._height,
            self.cornerRadius, stroke=0, fill=1
        )
        self.canv.restoreState()
        Table.draw(self)


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


class FeeBill(PDFReport):
    def __init__(self, *args, **kwargs):
        PDFReport.__init__(
            self,
            *args,
            page_size=letter,
            page_margin=(12.7 * mm, 12.7 * mm),
            page_padding=(2.2 * mm, 0),
            doc_template_type=BaseDocTemplate,
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
        return Table([[elems]], style=style, colWidths=135.5 * mm, hAlign="LEFT")

    def _section_doc_header(self):
        elems = [
            Spacer(0, 0.2 * mm),
            Paragraph("<b>Fee Bill - BROOKHAVEN MUNICIPAL COURT</b>", styles["doc-header"]),
            Spacer(0, 1 * mm),
        ]
        return [self._create_section_table(elems, styles["main-table"])]

    def _section_1(self):
        elems = list()
        elems.append(
            Table(
                [
                    [
                        Paragraph("Clerk:", styles["field-label"]),
                        Paragraph("%s" % self.data["clerk"], styles["field-value"]),
                    ],
                    [
                        Paragraph("Inst Type:", styles["field-label"]),
                        Paragraph("%s" % self.data["inst_type"], styles["field-value"])
                    ],
                    [
                        Paragraph("Paid By:", styles["field-label"]),
                        Paragraph("%s" % self.data["paid_by"], styles["field-value"])
                    ],
                    [
                        Paragraph("Trans ID:", styles["field-label"]),
                        Paragraph("%s" % self.data["trans_id"], styles["field-value"])
                    ]
                ],
                style=styles["main-table"],
                colWidths=(17.5 * mm, None),
                rowHeights=6.1 * mm,
            )
        )
        t1 = Table(
            [
                [
                    Paragraph("Posting Date:", styles["field-label"]),
                    Paragraph("%s" % self.data["posting_date"], styles["field-value"]),
                ],
                [
                    Paragraph("Report Date:", styles["field-label"]),
                    Paragraph("%s" % self.data["report_date"], styles["field-value"])
                ],
            ],
            style=styles["main-table"],
            colWidths=(24 * mm, 45 * mm),
            rowHeights=5.6 * mm,
        )
        t2 = Table(
            [
                [
                    Table(
                        [[
                            Paragraph("Type:", styles["field-label"]),
                            Paragraph("%s" % self.data["type"], styles["field-value"]),
                        ]],
                        style=styles["main-table"],
                        colWidths=(11.5 * mm, None)
                    )
                ],
                [
                    Table(
                        [[
                            Paragraph("Case Number:", styles["field-label"]),
                            Paragraph("%s" % self.data["case_number"], styles["field-value"]),
                        ]],
                        style=styles["main-table"],
                        colWidths=(27 * mm, None)
                    )
                ]
            ],
            style=styles["main-table"],
            rowHeights=5.6 * mm,
        )
        elems.append(Table([[t1, t2]], style=styles["main-table"]))
        elems.append(
            Table(
                [
                    [
                        Paragraph("Comment:", styles["field-label"]),
                        Paragraph("%s" % self.data["comment"], styles["field-value"]),
                        Paragraph("%s" % self.data["name"], styles["field-value"]),
                    ]
                ],
                style=extend_table_style(styles["main-table"], [
                    ("VALIGN", (0, -1), (-1, -1), "TOP"),
                    ("TOPPADDING", (0, -1), (-1, -1), 0.6 * mm),
                ]),
                colWidths=(18 * mm, 51 * mm, None),
                rowHeights=25.5 * mm
            )
        )
        return [self._create_section_table(elems)]

    def _section_2(self):
        ps_label = styles["field-label"]
        ps_value = styles["field-value"]
        ps_label_right = extend_style(ps_label, alignment=TA_RIGHT)
        ps_value_right = extend_style(ps_value, alignment=TA_RIGHT)
        elems = list()
        table_data = [[
            Paragraph("Description", ps_label),
            Paragraph("Fees", ps_label_right),
            Paragraph("Payments", ps_label_right),
            None
        ]]
        row_heights = [6 * mm]
        if self.data["line_items"]:
            for item in self.data["line_items"]:
                table_data.append([
                    Paragraph("%s" % item["description"], ps_value),
                    Paragraph("%s" % item["fee"], ps_value_right),
                    Paragraph("%s" % item["payment"], ps_value_right),
                    None
                ])
                row_heights.append(6.35 * mm)
        else:
            table_data.append([
                Paragraph("", ps_value),
                Paragraph("", ps_value),
                Paragraph("", ps_value),
                None
            ])
            row_heights.append(6.35 * mm)
        table_data.append([None, None, None, None])
        row_heights.append(1 * mm)
        elems.append(
            Table(
                table_data,
                style=extend_table_style(styles["main-table"], [
                    ("VALIGN", (0, 0), (-1, 0), "TOP"),
                    ("LINEBELOW", (0, 0), (-1, 0), 0.5 * mm, "black"),
                    ("LINEBELOW", (0, -1), (-1, -1), 0.5 * mm, "black"),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 1.5 * mm),
                ]),
                rowHeights=row_heights,
                colWidths=(67 * mm, 18 * mm, 25.5 * mm, None)
            )
        )
        elems.append(Spacer(0, 0.7 * mm))
        elems.append(
            Table(
                [
                    [
                        Paragraph("Case Beginning Balance:", ps_label_right),
                        Paragraph("%s" % self.data["beginning_balance"], ps_value_right),
                    ],
                    [
                        Paragraph("Total Charges:", ps_label_right),
                        Paragraph("%s" % self.data["total_charges"], ps_value_right),
                    ],
                    [
                        Paragraph("Total Payments:", ps_label_right),
                        Paragraph("%s" % self.data["total_payments"], ps_value_right),
                    ],
                    [
                        Paragraph("Change:", ps_label_right),
                        Paragraph("%s" % self.data["change"], ps_value_right),
                    ],
                    [
                        Paragraph("Case Ending Balance:", ps_label_right),
                        Paragraph("%s" % self.data["ending_balance"], ps_value_right),
                    ],
                ],
                style=extend_table_style(styles["main-table"], [
                    ("RIGHTPADDING", (0, 0), (-1, -1), 1.5 * mm)
                ]),
                rowHeights=5.9 * mm,
                colWidths=(67 * mm, 18 * mm)
            )
        )
        elems.append(Spacer(0, 0.5 * mm))
        elems.append(
            RoundRectTable(
                [
                    [
                        Paragraph("Balance All Cases:", ps_label_right),
                        Paragraph("%s" % self.data["all_balance"], ps_label_right),
                    ],
                    [
                        Paragraph("Next Payment Due:", ps_label_right),
                        Paragraph("%s" % self.data["next_payment_due"], ps_label_right),
                    ],
                    [None]
                ],
                style=extend_table_style(styles["main-table"], [
                    ("RIGHTPADDING", (0, 0), (-1, -1), 1.5 * mm),
                    ("LEFTPADDING", (0, 0), (0, -1), 29 * mm)
                ]),
                rowHeights=(6.75 * mm, 5.75 * mm, 1 * mm),
                colWidths=(67 * mm, 18 * mm),
                leftIndent=29 * mm,
                cornerRadius=1 * mm,
                backColor="lightgrey"
            )
        )
        return [self._create_section_table(elems)]
