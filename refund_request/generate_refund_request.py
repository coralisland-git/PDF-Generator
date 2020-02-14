# coding=utf-8
# from global_vars import *
from document_specific_styles import styles, extend_style, extend_table_style
from common.signatures import SignatureDocTemplate, SignatureRect, SignatureDatetimeRect
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import Paragraph, Table, Spacer, BaseDocTemplate, PageTemplate, Frame
from reportlab.platypus.flowables import HRFlowable, Flowable
import io
import textwrap

try:
    import cStringIO
except ModuleNotFoundError:
    pass

DOC_LANG = "en"
TRANSLATION_TEXT = {
    "en": {
        "text-001": "IN THE MUNICIPAL COURT OF THE CITY OF BROOKHAVEN<br />DEKALB COUNTY<br />STATE OF GEORGIA",
        "text-002": "CITY OF BROOKHAVEN",
        "text-003": "Case Numbers(s):",
        "text-004": "Bond Amount:",
        "text-005": "REFUND REQUEST",
        "text-006": "My name is",
        "text-007": "and I am the surety on the above listed case(s) and I request:",
        "text-008": "the bond be applied, in full, to any fine or fees associated to the cases.",
        "text-009": "be applied to any fine or fees associated to the cases and the balance be refunded.",
        "text-010": "the bond, in full, be refunded.",
        "text-011": "Note: All refund checks will be mailed or may be picked up after you are notified via telephone or email.",
        "text-012": "Please select one option:",
        "text-013": "I request that the refund check be mailed to me at:",
        "text-014": "Address",
        "text-015": "City",
        "text-016": "State",
        "text-017": "Zip",
        "text-018": "I request to be notified by phone when the check is available and my phone number is:",
        "text-019": "I understand that I will pick up the check at 2665 Buford Hwy, Brookhaven GA.",
        "text-020": "I request to be notified by email when the check is available and my email address is:",
        "text-021": "I understand that I will pick up the check at 2665 Buford Hwy, Brookhaven GA.",
        "text-022": "Surety's Signature",
        "text-023": "Date",
        "text-024": "BROOKHAVEN MUNICIPAL COURT",
        "text-025": "PHONE",
        "text-026": "FAX",
    },
    "es": {
        "text-001": "EN LA CORTE MUNICIPAL DE LA CIUDAD DE BROOKHAVEN<br />CONDADO DE DEKALB<br />ESTADO DE GEORGIA",
        "text-002": "CIUDAD DE BROOKHAVEN",
        "text-003": "Número(s) de Caso(s):",
        "text-004": "Valor de la Fianza:",
        "text-005": "SOLICITUD PARA REEMBOLSO",
        "text-006": "Mi nombre es",
        "text-007": "y soy el fiador del caso (o casos) arriba mencionado(s) y por medio de la presente solicito que:",
        "text-008": "Se endose la fianza en su totalidad para efectos de cubrir el pago de cualquier multa, cuotas o gastos relacionados con el(los) caso(s).",
        "text-009": "de dicha fianza se endose para efectos de cubrir el pago de cualquier multa, cuotas o gastos relacionados con el(los) caso(s) y que el saldo remanente se reembolse.",
        "text-010": "Se reembolse la fianza en su totalidad.",
        "text-011": "Nota: Todos los cheques se enviarán por correo o se pueden recogner después que se le notifique por teléfono",
        "text-012": "Por favor seleccione una opción:",
        "text-013": "Solicito que el cheque del reembolso se envie por correo a mi nombre:",
        "text-014": "Dirección",
        "text-015": "Ciudad",
        "text-016": "Estado",
        "text-017": "Código Postal",
        "text-018": "Solicito que se me notifique por teléfono cuando el cheque esté listo y mi número de teléfono es:",
        "text-019": "Yo lo voy a recoger personalmente en 2664 Buford Hwy, Brookhaven GA.",
        "text-020": "Solicito que se me notifique por correo electrónico cuando el cheque esté listo y mi dirección de correo electrónico es:",
        "text-021": "Yo lo voy a recoger personalmente en 2664 Buford Hwy, Brookhaven GA.",
        "text-022": "Firma del Fiador",
        "text-023": "Fecha",
        "text-024": "BROOKHAVEN MUNICIPAL COURT",
        "text-025": "PHONE",
        "text-026": "FAX",
    },
}


def translation(string_name, raise_missing=True):
    lang_text = TRANSLATION_TEXT[DOC_LANG]
    try:
        translated = lang_text[string_name]
    except KeyError:
        if raise_missing:
            raise
        else:
            translated = ""
    return translated


_ = translation


def generate_refund_request_english(pdf_dict, title=None, author=None):
    global DOC_LANG
    DOC_LANG = "en"
    return generate_refund_request(pdf_dict, title=title, author=author)


def generate_refund_request_spanish(pdf_dict, title=None, author=None):
    global DOC_LANG
    DOC_LANG = "es"
    return generate_refund_request(pdf_dict, title=title, author=author)


def generate_refund_request(pdf_dict, title=None, author=None):
    report = RefundRequest(title=title, author=author)
    try:
        buff = cStringIO.StringIO()
    except NameError:
        buff = None
    return report.create_report(pdf_dict, buff)


class CustomXBox(Flowable):
    def __init__(self, size=3.5 * mm, value=True):
        Flowable.__init__(self)
        self.width = self.height = size
        self.value = value

    def __repr__(self):
        return "CustomXBox(w=%s, h=%s, v=%s)" % (self.width, self.height, self.value)

    def draw(self):
        self.canv.saveState()

        box_share = 0.85
        line_width = self.width * 0.05
        self.canv.setLineWidth(line_width)

        size = (self.width * box_share) - line_width
        self.canv.rect((line_width / 2), (line_width / 2), size + 0.1, size + 0.1)

        edge_len = (((self.width * (1 - box_share)) ** 2) * 2) ** (0.5)
        self.canv.wedge(
            edge_len * -1, self.height * box_share - edge_len,
            edge_len, self.height * box_share + edge_len,
            0, 45, stroke=0, fill=1
        )
        self.canv.rect(
            self.width * (1 - box_share), self.height * box_share,
            self.width * box_share, self.height * (1 - box_share),
            stroke=0, fill=1
        )
        self.canv.wedge(
            self.width * box_share - edge_len, edge_len * -1,
            self.width * box_share + edge_len, edge_len,
            45, 45, stroke=0, fill=1
        )
        self.canv.rect(
            self.width * box_share, self.height * (1 - box_share),
            self.width * (1 - box_share), self.height * box_share,
            stroke=0, fill=1
        )

        if self.value:
            self.canv.setFont(styles["main"].fontName, (self.height * box_share) * 0.80)
            self.canv.drawCentredString(0.5 * (self.width * box_share), 0.25 * (self.height * box_share), "X")

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


class RefundRequest(PDFReport):
    def __init__(self, *args, **kwargs):
        PDFReport.__init__(
            self,
            *args,
            page_size=letter,
            page_margin=[12.7 * mm, 6.35 * mm, 12.7 * mm, 6.35 * mm],
            page_padding=[0, 0, 1 * mm, 0],
            doc_template_type=SignatureDocTemplate,
            **kwargs
        )

    def _content_methods(self):
        methods = PDFReport._content_methods(self)
        methods.insert(0, methods.pop(methods.index("_section_doc_header")))
        methods.append(methods.pop(methods.index("_section_doc_footer")))
        return methods

    def _create_section_spacer(self):
        ps = styles["main"]
        spacer = "*"
        spacer_width = stringWidth(spacer, ps.fontName, ps.fontSize),
        section_width = (self.page_size[0] - self.page_margin[0] - self.page_margin[2] - self.page_padding[0] -
                         self.page_padding[2])
        num_spacers = int(section_width / spacer_width[0] * 0.69)
        table_data = [[Paragraph("<b>*</b>", style=styles["main"])] * num_spacers]
        return Table(table_data, style=styles["main-table"])

    def _section_doc_header(self):
        elems = list()
        elems.extend([
            Spacer(0, 2.5 * mm),
            Paragraph("<b>%s</b>" % _("text-001"), styles["doc-header"]),
            Spacer(0, 5.5 * mm),
        ])
        t1 = Table(
            [
                [
                    Paragraph(_("text-002"), styles["main-narrow"]),
                ],
                [
                    Paragraph("VS.", styles["main-narrow"]),
                ],
                [
                    Paragraph(self.data["field-001"], styles["field-value"]),
                ],
                [
                    HRFlowable(width=66 * mm, thickness=0.2 * mm, lineCap='round', color="black")
                ]
            ],
            style=extend_table_style(styles["main-table"], [
                ("LEFTPADDING", (0, 1), (-1, 1), 16.5 * mm),
                ("VALIGN", (0, 2), (-1, 2), "MIDDLE"),
            ]),
            rowHeights=[5 * mm, 5 * mm, 9.75 * mm, 0.5 * mm]
        )
        t2 = Table(
            [
                [
                    Paragraph(_("text-003"), styles["main-narrow-right"]),
                    Paragraph(self.data["field-002"], styles["field-value"]),
                ],
                [
                    Paragraph(_("text-004"), styles["main-right"]),
                    Paragraph(self.data["field-003"], styles["field-value"]),
                ]
            ],
            style=extend_table_style(styles["main-table"], [
                ("LINEBELOW", (1, 0), (1, -1), 0.2 * mm, "black"),
                ("RIGHTPADDING", (0, 0), (0, -1), 2 * mm),
            ]),
            rowHeights=5 * mm
        )
        elems.append(
            Table(
                [[t1, t2]],
                style=extend_table_style(styles["main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]),
            )
        )
        return elems

    def _section_1(self):
        elems = list()
        elems.extend([
            Spacer(0, 0.5 * mm),
            Paragraph("<b><u>%s</u></b>" % _("text-005"), styles["section-header"]),
            Spacer(0, 14 * mm),
        ])

        ps = styles["section-main"]
        ps_value = extend_style(styles["field-value"], alignment=TA_CENTER)
        first_col_text = _("text-006")
        second_col_text = _("text-007")

        col_widths = [
            stringWidth(first_col_text, ps.fontName, ps.fontSize) + 1 * mm,
            76.5 * mm
        ]
        col_widths.extend([188 * mm - col_widths[0] - col_widths[1], None])

        text_width = stringWidth(second_col_text, ps_value.fontName, ps_value.fontSize),
        num_chars = int(len(second_col_text) / (text_width[0] / int(col_widths[2] + 1)))
        lines = textwrap.wrap(second_col_text, num_chars - 2)

        table_data = [
            [
                Paragraph(first_col_text, ps),
                Paragraph(self.data["field-004"], ps_value),
                Paragraph(lines[0], ps),
                None,
            ]
        ]
        elems.append(
            Table(
                table_data,
                style=extend_table_style(styles["main-table"], [
                    ("LINEBELOW", (1, 0), (1, 0), 0.2 * mm, "black"),
                    ("LEFTPADDING", (2, 0), (2, 0), 2 * mm,),
                    ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
                ]),
                colWidths=col_widths,
                rowHeights=5 * mm,
                spaceAfter=1 * mm
            )
        )
        if len(lines) > 1:
            joined_lines = ', '.join(lines[1:])
            elems.append(Paragraph(joined_lines, ps))
        elems.append(
            Table(
                [
                    [
                        Paragraph(self.data["field-005"], extend_style(
                            styles["field-value"], firstLineIndent=5 * mm, leading=11)),
                        Spacer(0, 5 * mm)
                    ]
                ],
                style=styles["main-table"],
                colWidths=[None, 1 * mm],
            )
        )
        col_widths = [4 * mm, 2 * mm, 21 * mm, None]
        elems.append(
            Table(
                [
                    [
                        CustomXBox(2.7 * mm, value=self.data["field-006"]),
                        Paragraph(_("text-008"), ps),
                        None,
                        None
                    ],
                ],
                style=extend_table_style(styles["main-table"], [
                    ("VALIGN", (0, 0), (0, -1), "TOP"),
                    ("TOPPADDING", (0, 0), (0, -1), 0.7 * mm),
                    ("SPAN", (1, 0), (3, 0)),
                ]),
                colWidths=col_widths,
                spaceBefore=0.75 * mm,
            )
        )
        text = _("text-009")
        col_width = 162 * mm
        text_width = stringWidth(text, ps.fontName, ps.fontSize),
        num_chars = int(len(text) / (text_width[0] / int(col_width + 1)))
        lines = textwrap.wrap(text, num_chars)
        table_data = [
            [
                CustomXBox(2.7 * mm, value=self.data["field-007"]),
                Paragraph("$", ps),
                Paragraph(self.data["field-008"], ps_value),
                Paragraph(lines[0], ps),
            ],
        ]
        ts_items = [
            ("LINEBELOW", (2, 0), (2, 0), 0.2 * mm, "black"),
            ("VALIGN", (0, 0), (0, -1), "TOP"),
            ("TOPPADDING", (0, 0), (0, -1), 0.7 * mm),
        ]
        if len(lines) > 1:
            table_data.append([None, ' '.join(lines[1:])])
            ts_items.append(("SPAN", (1, 1), (-1, 1)), )
        elems.append(
            Table(
                table_data,
                style=extend_table_style(styles["main-table"], ts_items),
                colWidths=col_widths,
                spaceBefore=0.75 * mm,
            )
        )
        elems.append(
            Table(
                [
                    [
                        CustomXBox(2.7 * mm, value=self.data["field-009"]),
                        Paragraph(_("text-010"), ps),
                    ]
                ],
                style=extend_table_style(styles["main-table"], [
                    ("VALIGN", (0, 0), (0, -1), "TOP"),
                    ("TOPPADDING", (0, 0), (0, -1), 0.7 * mm),
                ]),
                colWidths=(4 * mm, None),
                spaceBefore=0.75 * mm,
                spaceAfter=6.25 * mm
            )
        )
        elems.append(Paragraph("<b>%s</b>" % _("text-011"), style=styles["main"]))
        elems.extend([
            Spacer(0, 6 * mm),
            self._create_section_spacer(),
            Spacer(0, 1 * mm),
        ])
        return elems

    def _section_2(self):
        elems = list()
        ps = styles["section-main"]
        ps_value = styles["field-value"]
        elems.extend([
            Spacer(0, 0.5 * mm),
            Paragraph(_("text-012"), ps),
            Spacer(0, 1 * mm),
        ])
        elems.append(
            Table(
                [
                    [
                        CustomXBox(2.7 * mm, value=self.data["field-010"]),
                        Paragraph("1.", ps),
                        Paragraph(_("text-013"), ps),
                    ],
                    [
                        None,
                        None,
                        Table(
                            [
                                [None,None,None],
                                [
                                    Paragraph(self.data["field-011"], ps_value),
                                    None,
                                    None
                                ],
                                [
                                    Paragraph(_("text-014"), ps),
                                ],
                                [
                                    Paragraph(self.data["field-012"], ps_value),
                                    Paragraph(self.data["field-013"], ps_value),
                                    Paragraph(self.data["field-014"], ps_value),
                                ],
                                [
                                    Paragraph(_("text-015"), ps),
                                    Paragraph(_("text-016"), ps),
                                    Paragraph(_("text-017"), ps),
                                ]
                            ],
                            style=extend_table_style(styles["main-table"], [
                                ("LINEBELOW", (0, 1), (-1, 1), 0.2 * mm, "black"),
                                ("LINEBELOW", (0, 3), (-1, 3), 0.2 * mm, "black"),
                            ]),
                            colWidths=[37 * mm, 26 * mm, 31 * mm],
                            rowHeights=[1 * mm, 9 * mm, 6.5 * mm, 9 * mm, 6.5 * mm],
                        )
                    ],
                ],
                style=extend_table_style(styles["main-table"], [
                    ("LEFTPADDING", (2, 1), (2, 1), 2.5 * mm),
                ]),
                colWidths=[4 * mm, 6 * mm, None],
                spaceAfter=9.5 * mm
            )
        )
        col_text = _("text-018")
        col_width = stringWidth(col_text, ps.fontName, ps.fontSize) + 1 * mm
        elems.append(
            Table(
                [
                    [
                        CustomXBox(2.7 * mm, value=self.data["field-015"]),
                        Paragraph("2.", ps),
                        Paragraph(col_text, ps),
                        Paragraph(self.data["field-016"], ps_value),
                        None
                    ],
                    [
                        Paragraph(_("text-019"), ps),
                    ],
                    [None],
                    [
                        CustomXBox(2.7 * mm, value=self.data["field-017"]),
                        Paragraph("3.", ps),
                        Paragraph(_("text-020"), ps),
                    ],
                    [
                        Paragraph(self.data["field-018"], ps_value)
                    ],
                    [
                        Paragraph(_("text-021"), ps),
                    ],

                ],
                style=extend_table_style(styles["main-table"], [
                    ("LINEBELOW", (3, 0), (3, 0), 0.2 * mm, "black"),
                    ("SPAN", (0, 1), (-1, 1)),
                    ("SPAN", (2, 3), (3, 3)),
                    ("LINEBELOW", (0, 4), (-1, 4), 0.2 * mm, "black"),
                    ("SPAN", (0, 4), (-1, 4)),
                    ("SPAN", (0, 5), (-1, 5)),
                ]),
                colWidths=[4 * mm, 4.5 * mm, col_width, 31.5 * mm, None],
                rowHeights=5 * mm
            )
        )
        elems.extend([
            Spacer(0, 5 * mm),
            self._create_section_spacer(),
            Spacer(0, 2 * mm),
        ])

        return elems

    def _section_3(self):
        elems = list()
        elems.append(
            Table(
                [
                    [
                        SignatureRect(99 * mm, 14 * mm, leftIndent=1 * mm, sig_id="SURETY-01"),
                        None,
                        SignatureDatetimeRect(48 * mm, 14 * mm, leftIndent=1 * mm, sig_id="SURETY-01"),
                    ],
                    [
                        Paragraph(_("text-022"), styles["main"]),
                        None,
                        Paragraph(_("text-023"), styles["main"]),
                    ]
                ],
                style=extend_table_style(styles["main-table"], [
                    ("LINEBELOW", (0, 0), (0, 0), 0.2 * mm, "black"),
                    ("LINEBELOW", (2, 0), (2, 0), 0.2 * mm, "black"),
                ]),
                colWidths=(101.7 * mm, 24.7 * mm, 50 * mm),
                rowHeights=[None, 6 * mm],
                hAlign="LEFT"
            )
        )
        return elems

    def _section_doc_footer(self):
        elems = [
            Paragraph(_("text-024"), styles["doc-footer"]),
            Paragraph("2665 BUFORD HWY", styles["doc-footer"]),
            Paragraph("BROOKHAVEN, GA 30324", styles["doc-footer"]),
            Paragraph("%s: 404-637-0660" % _("text-025"), styles["doc-footer"]),
            Paragraph("%s: 404 637-0665" % _("text-026"), styles["doc-footer"]),
            Spacer(0, 7 * mm),
            Paragraph("REVISED MAR 2018", extend_style(styles["doc-footer"], alignment=TA_LEFT)),
        ]
        return elems
