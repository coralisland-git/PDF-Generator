# coding=utf-8
from document_specific_styles import styles, extend_style, extend_table_style
from common.signatures import SignatureDocTemplate, SignatureRect
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, Table, Spacer, BaseDocTemplate, PageTemplate, Frame, Flowable
import io

try:
    import cStringIO
except ModuleNotFoundError:
    pass


def generate_notice_of_withdrawal_of_suspension(pdf_dict, title=None, author=None):
    report = NoticeWithdrawalSuspension(title=title, author=author)
    try:
        buff = cStringIO.StringIO()
    except NameError:
        buff = None
    return report.create_report(pdf_dict, buff)


class CustomXBox(Flowable):
    def __init__(self, size=3.8 * mm, value=True):
        Flowable.__init__(self)
        self.width = self.height = size
        if value == "":
            self.value = True
        else:
            self.value = value

    def __repr__(self):
        return "CustomXBox(w=%s, h=%s, v=%s)" % (self.width, self.height, self.value)

    def draw(self):
        self.canv.saveState()
        self.canv.setLineWidth(self.width * 0.06)
        self.canv.rect(0, 0, self.width, self.height)
        if self.value:
            self.canv.setFont(styles["main"].fontName, self.height * 0.70)
            self.canv.drawCentredString(0.5 * self.width, 0.35 * self.height, "X")
        self.canv.restoreState()


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

    def _create_document(self, buff):
        page_t = PageTemplate(
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
        doc_t = self.doc_template_type(
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
        doc_t.addPageTemplates(page_t)
        return doc_t


class NoticeWithdrawalSuspension(PDFReport):
    def __init__(self, *args, **kwargs):
        PDFReport.__init__(
            self,
            *args,
            page_size=letter,
            page_margin=6.35 * mm,
            page_padding=[0, 0, 6.5 * mm, 0],
            doc_template_type=SignatureDocTemplate,
            **kwargs
        )

    def _content_methods(self):
        return ["_doc_wrapper"]

    def _doc_wrapper(self):
        methods = PDFReport._content_methods(self)
        methods.insert(0, methods.pop(methods.index("_section_doc_header")))
        methods.pop(methods.index("_section_doc_footer"))
        section_data = []
        for section in methods:
            elems = getattr(self, section)()
            section_data.append([elems])
        wrapper_elems = list()
        wrapper_elems.append(Spacer(0, 1.5 * mm))
        wrapper_elems.append(Table(section_data, style=styles["wrapper-table"]))
        wrapper_elems.extend(self._section_doc_footer())
        return wrapper_elems

    def _section_doc_header(self):
        elems = [
            Spacer(0, 3.75 * mm),
            Paragraph("<b><u>NOTICE OF WITHDRAWAL OF SUSPENSION</u></b>", styles["doc-header"]),
        ]
        return elems

    def _section_1(self):
        elems = list()
        elems.append(Spacer(0, 1.5 * mm))
        ps = extend_style(styles["main"], fontSize=8)
        t1 = Table(
            [
                [
                    Paragraph("The conditions of this suspension have been met.",
                              extend_style(ps, alignment=TA_JUSTIFY, justifyLastLine=True)),
                    None,
                ],
                [
                    Paragraph("Authorized Signature:", ps),
                    SignatureRect(35 * mm, 6 * mm)
                ],
                [
                    Paragraph("Date Settled: %s" % self.data["field-004"], ps),
                ]
            ],
            style=extend_table_style(styles["main-table"], [
                ("OUTLINE", (0, 0), (-1, -1), 0.3 * mm, "black"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (0, -1), 2.1 * mm),
                ("RIGHTPADDING", (0, 0), (-1, 0), 2.1 * mm),
                ("BOTTOMPADDING", (0, 2), (-1, 2), 1.5 * mm),
                ("SPAN", (0, 0), (1, 0)),
            ]),
            colWidths=(34 * mm, 43 * mm),
            rowHeights=(7 * mm, 6.5 * mm, 7.5 * mm),
        )
        elems.append(
            Table(
                [
                    [
                        None,
                        CustomXBox(value=self.data["field-001"]),
                        Paragraph("FAILURE TO APPEAR", styles["main"]),
                        t1
                    ],
                    [
                        None,
                        CustomXBox(value=self.data["field-002"]),
                        Paragraph("D/L IN LIEU OF BAIL", styles["main"]),
                        None
                    ],
                    [None],
                    [
                        [
                            Paragraph("GEORGIA", extend_style(
                                styles["main"], alignment=TA_CENTER, fontSize=14, leading=17)),
                            Paragraph("NONRESIDENT<br />VIOLATOR COMPACT", extend_style(
                                styles["main"], alignment=TA_CENTER, fontSize=9.75)),
                        ],
                        CustomXBox(value=self.data["field-003"]),
                        Paragraph("D/L AS COLLATERAL (MISDEMEANOR)", styles["main"]),
                        None,
                    ],
                ],
                style=extend_table_style(styles["main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (1, 0), (1, -1), 1.2 * mm),
                    ("VALIGN", (3, 0), (3, 0), "MIDDLE"),
                    ("SPAN", (3, 0), (3, 1)),
                ]),
                colWidths=(43.5 * mm, 7.5 * mm, 59 * mm, None),
                rowHeights=(19.5 * mm, 19.5 * mm, 2 * mm, 19 * mm),
            )
        )
        return elems

    def _section_2(self):
        elems = list()
        elems.append(Spacer(0, 2.5 * mm))
        ts = extend_table_style(styles["main-table"], [
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (0, -1), 1.9 * mm),
        ])
        t1 = Table(
            [
                [CustomXBox(size=4.2 * mm, value=self.data["field-014"]),
                 Paragraph("YES", style=styles["field-label"])],
                [CustomXBox(size=4.2 * mm, value=self.data["field-015"]), Paragraph("NO", style=styles["field-label"])],
                [CustomXBox(size=4.2 * mm, value=self.data["field-016"]),
                 Paragraph("UNKNOWN", style=styles["field-label"])],
            ],
            style=ts,
            colWidths=(8.2 * mm, None),
            rowHeights=5.7 * mm,
        )
        t2 = Table(
            [
                [CustomXBox(size=4.2 * mm, value=self.data["field-017"]),
                 Paragraph("YES", style=styles["field-label"])],
                [CustomXBox(size=4.2 * mm, value=self.data["field-018"]), Paragraph("NO", style=styles["field-label"])],
            ],
            style=ts,
            colWidths=(8.2 * mm, None),
            rowHeights=6 * mm,
            spaceBefore=2 * mm
        )
        t3 = Table(
            [
                [CustomXBox(size=4.2 * mm, value=self.data["field-019"]),
                 Paragraph("YES", style=styles["field-label"])],
                [CustomXBox(size=4.2 * mm, value=self.data["field-020"]), Paragraph("NO", style=styles["field-label"])],
            ],
            style=ts,
            colWidths=(8.2 * mm, None),
            rowHeights=6 * mm,
            spaceBefore=2 * mm
        )
        elems.append(
            Table(
                [
                    [
                        [
                            Paragraph("<u>CITATION NO.</u>", styles["field-label"]),
                            Paragraph("%s" % self.data["field-005"], styles["field-value"]),
                        ],
                        None,
                        [
                            Paragraph("<u>CASE NO</u>", styles["field-label"]),
                            Paragraph("%s" % self.data["field-006"], styles["field-value"]),
                        ],
                        [
                            Paragraph("<u>CITATION DATE</u>", styles["field-label"]),
                            Paragraph("%s" % self.data["field-007"], styles["field-value"]),
                        ],
                        [
                            Paragraph("<u>TRIAL DATE</u>", extend_style(styles["field-label"], alignment=TA_CENTER)),
                            Paragraph("%s" % self.data["field-008"],
                                      extend_style(styles["field-value"], alignment=TA_CENTER)),
                        ],
                        None,
                        None,
                        [
                            Paragraph("<u>NATIVE CODE</u>", styles["field-label"]),
                            Paragraph("%s" % self.data["field-009"], styles["field-value"]),  # field
                        ],
                    ],
                    [
                        [
                            Paragraph("<u>DESCRIPTION OF VIOLATION/CHARGE</u>", styles["field-label"]),
                            Paragraph("%s" % self.data["field-010"], styles["field-value"]),  # field
                        ],
                        None,
                        None,
                        None,
                        None,
                        [
                            Paragraph("<u>LOCATION OF VIOLATION</u>",
                                      extend_style(styles["field-label"], alignment=TA_CENTER)),
                            Paragraph("%s" % self.data["field-011"],
                                      extend_style(styles["field-value"], alignment=TA_CENTER)),
                        ],
                        None,
                        [
                            Paragraph("<u>FINES AND COSTS</u>",
                                      extend_style(styles["field-label"], alignment=TA_CENTER)),
                            Paragraph("%s" % self.data["field-012"],
                                      extend_style(styles["field-value"], alignment=TA_CENTER)),
                        ],
                    ],
                    [
                        [
                            Paragraph("<u>JURISDICTION</u>", extend_style(styles["field-label"], alignment=TA_CENTER)),
                            Paragraph("<b><u>%s</u></b>" % self.data["field-013"],
                                      extend_style(styles["field-value"], alignment=TA_CENTER, spaceBefore=0.5 * mm)),
                        ],
                        [
                            Paragraph("<u>CDL HOLDER?</u>", styles["field-label"]),
                            t1
                        ],
                        None,
                        [
                            Paragraph("<u>COMMERCIAL VEHICLE</u>", styles["field-label"]),
                            t2
                        ],
                        None,
                        [
                            Paragraph("<u>HAZMAT</u>", styles["field-label"]),
                            t3
                        ],
                        [
                            Paragraph("<u>ACD CODE</u>", styles["field-label"]),
                            Paragraph("<b><u>%s</u></b>" % self.data["field-021"], extend_style(
                                styles["field-value"], spaceBefore=0.5 * mm, leftIndent=10 * mm)),
                        ],
                        None,
                    ],
                    [
                        [
                            Paragraph("<u>COURT TYPE</u>", extend_style(styles["field-label"], alignment=TA_CENTER)),
                            Paragraph("%s" % self.data["field-022"], extend_style(
                                styles["field-value"], alignment=TA_CENTER, spaceBefore=1.5 * mm,
                                fontSize=styles["field-value"].fontSize * 0.8)),
                        ],
                        None,
                        None,
                        None,
                        None,
                        None,
                        [
                            Paragraph("<u>ACD DETAIL (FOR DDS USE ONLY)</u>", extend_style(
                                styles["field-label"], fontSize=styles["field-label"].fontSize * 0.85)),
                            Paragraph("%s" % self.data["field-023"], extend_style(
                                styles["field-value"],
                                fontSize=styles["field-value"].fontSize * 0.85, spaceBefore=0.5 * mm)),
                        ],
                        None,
                    ],
                ],
                style=extend_table_style(styles["main-table"], [
                    ("GRID", (0, 0), (-1, -1), 0.3 * mm, "black"),
                    ("SPAN", (0, 0), (1, 0)),
                    ("SPAN", (4, 0), (6, 0)),
                    ("SPAN", (0, 1), (4, 1)),
                    ("SPAN", (5, 1), (6, 1)),
                    ("SPAN", (6, 2), (7, 2)),
                    ("SPAN", (6, 3), (7, 3)),
                    ("SPAN", (1, 2), (2, 3)),
                    ("SPAN", (3, 2), (4, 3)),
                    ("SPAN", (5, 2), (5, 3)),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("TOPPADDING", (0, 0), (-1, -1), 1.7 * mm),
                    ("TOPPADDING", (0, 3), (0, 3), 0),
                    ("LEFTPADDING", (0, 0), (-1, -1), 2 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 2 * mm),
                ]),
                colWidths=(29.4 * mm, 6.1 * mm, 29.6 * mm, 37.9 * mm, 4.3 * mm, 35.8 * mm, 8.4 * mm, None),
                rowHeights=(14.8 * mm, 14.8 * mm, 12.5 * mm, 10.5 * mm),
            )
        )
        return elems

    def _section_3(self):
        def row_helper(data, col_widths=None, height=14.6 * mm):
            t = Table(
                [data],
                style=extend_table_style(styles["main-table"], [
                    ("GRID", (0, 0), (-1, -1), 0.3 * mm, "black"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("TOPPADDING", (0, 0), (-1, -1), 1.8 * mm),
                    ("LEFTPADDING", (0, 0), (-1, -1), 1.9 * mm),
                ]),
                colWidths=col_widths,
                rowHeights=height
            )
            return t

        t1_rows = list()
        t1_rows.append(
            row_helper([
                [
                    Paragraph("<u>DLN</u>", styles["field-label"]),
                    Paragraph("%s" % self.data["field-024"], styles["field-value"]),
                ],
                [
                    Paragraph("<u>STATE</u>", styles["field-label"]),
                    Paragraph("%s" % self.data["field-025"], styles["field-value"]),
                ],
                [
                    Paragraph("<u>DATE OF BIRTH</u>", styles["field-label"]),
                    Paragraph("%s" % self.data["field-026"], styles["field-value"]),
                ]
            ], [35.7 * mm, 16.9 * mm, None])
        )
        t1_rows.append(
            row_helper([
                [
                    Paragraph("<u>DEFENDANT FULLNAME</u>", styles["field-label"]),
                    Paragraph("%s" % self.data["field-027"], styles["field-value"]),
                ],
                [
                    Paragraph("<u>SEX</u>", styles["field-label"]),
                    Paragraph("%s" % self.data["field-028"], styles["field-value"]),
                ]
            ], [86.3 * mm, None])
        )
        t1_rows.append(
            row_helper([
                [
                    Paragraph("<u>STREET ADDRESS</u>", styles["field-label"]),
                    Paragraph("%s" % self.data["field-029"], styles["field-value"]),
                ]
            ])
        )
        t1_rows.append(
            row_helper([
                [
                    Paragraph("<u>CITY</u>", styles["field-label"]),
                    Paragraph("%s" % self.data["field-030"], styles["field-value"]),
                ],
                [
                    Paragraph("<u>STATE</u>", styles["field-label"]),
                    Paragraph("%s" % self.data["field-031"], styles["field-value"]),
                ],
                [
                    Paragraph("<u>ZIP CODE</u>", styles["field-label"]),
                    Paragraph("%s" % self.data["field-032"], styles["field-value"]),
                ]
            ], [50 * mm, 15 * mm, None])
        )
        t1_rows.append(
            row_helper([
                [
                    Paragraph("<u>TAG NO</u>", styles["field-label"]),
                    Paragraph("%s" % self.data["field-033"], styles["field-value"]),
                ],
                [
                    Paragraph("<u>STATE</u>", styles["field-label"]),
                    Paragraph("%s" % self.data["field-034"], styles["field-value"]),
                ],
                [
                    Paragraph("<u>YEAR</u>", styles["field-label"]),
                    Paragraph("%s" % self.data["field-035"], styles["field-value"]),
                ],
                [
                    Paragraph("<u>VEHICLE DESCRIPTION</u>", styles["field-label"]),
                    Paragraph("%s" % self.data["field-036"], styles["field-value"]),
                ]
            ], [23 * mm, 14.5 * mm, 15 * mm, None])
        )
        t2_rows = list()
        t2_rows.append(
            row_helper([
                [
                    Paragraph("<u>NAME OF COURT</u>", styles["field-label"]),
                    Paragraph("%s" % self.data["field-037"], styles["field-value"]),
                ],
                [
                    Paragraph("<u>COURT CODE #</u>", styles["field-label"]),
                    Paragraph("%s" % self.data["field-038"], styles["field-value"]),
                ]
            ], [57 * mm, None])
        )
        t2_rows.extend([
            row_helper([[
                Paragraph("<u>MAILING ADDRESS</u>", styles["field-label"]),
                Paragraph("%s" % self.data["field-039"], styles["field-value"]),
            ]]),
            row_helper([[
                Paragraph("<u>CITY, STATE, ZIP CODE</u>", styles["field-label"]),
                Paragraph("%s" % self.data["field-040"], styles["field-value"]),
            ]]),
            row_helper([[
                Paragraph("<u>TELEPHONE NUMBER</u>", styles["field-label"]),
                Paragraph("%s" % self.data["field-041"], styles["field-value"]),  # field
            ]])
        ])
        t2_rows.append(
            row_helper([
                [
                    Paragraph("<u>CERTIFIED BY:</u>", styles["field-label"]),
                    Paragraph("%s" % self.data["field-042"], styles["field-value"]),  # field
                ],
                [
                    Paragraph("<u>DATE</u>", styles["field-label"]),
                    Paragraph("%s" % self.data["field-043"], styles["field-value"]),  # field
                ]
            ], [61 * mm, None])
        )
        t3 = Table(
            [
                [t1_rows, None, t2_rows]
            ],
            style=extend_table_style(styles["main-table"], [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]),
            colWidths=(98.75 * mm, None, 89.7 * mm),
        )
        return [t3, Spacer(0, 6.5 * mm)]

    def _section_doc_footer(self):
        elems = [Spacer(0, 3 * mm)]
        elems.append(
            Table(
                [[
                    Paragraph("Copy 1 = Defendant Notice", styles["doc-footer"]),
                    Paragraph("Copy 2 = Home Jurisdiction Copy", styles["doc-footer"]),
                ]],
                style=extend_table_style(styles["main-table"], [
                    ("LEFTPADDING", (0, 0), (0, 0), 41.5 * mm),
                    ("LEFTPADDING", (1, 0), (1, 0), 3 * mm),
                ])
            )
        )
        elems.append(Spacer(0, 12 * mm))
        elems.append(Paragraph("%s<br />%s<br />%s<br />%s %s, %s" % (
            self.data["field-005"], self.data["field-044"], self.data["field-029"], self.data["field-030"],
            self.data["field-032"], self.data["field-032"]
        ), extend_style(styles["doc-footer"], leftIndent=19 * mm)))
        return elems
