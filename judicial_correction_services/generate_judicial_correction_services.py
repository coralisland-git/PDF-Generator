# -*- coding: utf-8 -*-
import cStringIO

from document_specific_styles import *
from common.signatures import *
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT


def generate_judicial_correction_services():
    cr = FDCCAReport()
    buff = cStringIO.StringIO()
    return cr.create_report(buff)


class FDCCAReport:
    def __init__(self, title=None, author=None):
        self.page_size = landscape(letter)
        self.page_margin = (5.6 * mm, 9.4 * mm)
        self.sections = ["content_en", "content_sp"]
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
            pagesize=landscape(letter),
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

    def _section_content_en(self):
        elems = list()
        TEST_DATA = "<br /> Test Data"
        main_table = Table(
            [
                [                    
                    Table(
                        [
                            [
                                Paragraph("Last Name {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                Paragraph("First Name {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                None,
                                Paragraph("Middle Name {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                            ],
                            [
                                Paragraph("AKA: {}".format("Test Data"), styles["rc-aawp-main-content"]),
                                None, None, None, None, None
                            ],
                            [
                                Paragraph("Physical Address {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                Paragraph("City {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                Paragraph("State {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                Paragraph("Zip Code {}".format(TEST_DATA), styles["rc-aawp-main-content"])
                            ],
                            [
                                Paragraph("Mailing Address(if different) {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                Paragraph("City {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                Paragraph("State {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                Paragraph("Zip Code {}".format(TEST_DATA), styles["rc-aawp-main-content"])
                            ],
                            [
                                Paragraph("Home Number {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                Paragraph("Cell Number {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None, None,
                                Paragraph("Email Address {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                            ],
                            [
                                Paragraph("Emergency Contact Name {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                Paragraph("Emergency Contact Number {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None, None,
                                Paragraph("Relationship to You {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                            ],
                            [
                                Paragraph("Employer? Student? Or Unemployed? {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                Paragraph("Location {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None, 
                                Paragraph("Work Number {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                            ],
                            [
                                Table(
                                    [
                                        [
                                            Paragraph("Date of Birth {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                            Paragraph("Social Security Number {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                            Paragraph("Race {}".format(TEST_DATA), extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)),
                                            Paragraph("Sex {}".format(TEST_DATA), extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)),
                                            Paragraph("Hgt {}".format(TEST_DATA), extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)),
                                            Paragraph("Wgt {}".format(TEST_DATA), extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)),
                                            Paragraph("Eyes {}".format(TEST_DATA), extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)),
                                            Paragraph("Hair {}".format(TEST_DATA), extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)),
                                        ]
                                    ],
                                    style=extend_table_style(styles["rc-main-table_inner"], [
                                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                        ("INNERGRID", (0, 0), (-1, -1), .1, "black"),
                                    ]),
                                    colWidths=(37*mm, 53*mm, 17.3*mm, 17.3*mm, 17.4*mm, 17.3*mm, 17.3*mm, 17.3*mm),
                                    rowHeights=10.5*mm
                                ),
                                None, None, None, None , None
                            ],
                            [
                                Paragraph("Scars/Tattoos: {}".format("Test Data"), extend_style(styles["rc-aawp-main-content"], fontSize=9)),
                                Paragraph("Driver's License Number/State: {}".format("Test Data"), extend_style(styles["rc-aawp-main-content"], fontSize=9)),
                                None, None, None, None
                            ],
                            [
                                Paragraph("Currently on Probation/Parole:Where? {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                Paragraph("What for: {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                Paragraph("Officer's Name & Number: {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None
                            ],
                            [
                                Paragraph("<U>FOR OFFICER USE ONLY</U>", extend_style(styles["rc-aawp-main-content"], leftIndent=18.4*mm)),
                                None, None, None, None, None
                            ],
                            [
                                Paragraph("Case Number {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                Paragraph("First Appt {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                Paragraph("Probation Officer {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None
                            ],
                        ],
                        style=extend_table_style(styles["rc-main-table_inner"], [
                            ("OUTLINE", (0, 0), (-1, -1), 1.2, "black"),
                            ("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ("INNERGRID", (0, 0), (-1, -1), .1, "black"),
                            ("LEFTPADDING", (0, 7), (4, 7), 0),
                            ("RIGHTPADDING", (0, 7), (4, 7), 0),
                            ("TOPPADDING", (0, 7), (4, 7), 0),
                            ("TOPPADDING", (0, 10), (4, 10), 1.4*mm),
                            ("SPAN", (1, 0), (3, 0)),                            
                            ("SPAN", (4, 0), (5, 0)),
                            ("SPAN", (0, 1), (5, 1)),
                            ("SPAN", (0, 2), (1, 2)),
                            ("SPAN", (2, 2), (3, 2)),
                            ("SPAN", (0, 3), (1, 3)),
                            ("SPAN", (2, 3), (3, 3)),
                            ("SPAN", (1, 4), (3, 4)),
                            ("SPAN", (4, 4), (5, 4)),
                            ("SPAN", (1, 5), (3, 5)),
                            ("SPAN", (4, 5), (5, 5)),
                            ("SPAN", (0, 6), (1, 6)),
                            ("SPAN", (2, 6), (3, 6)),
                            ("SPAN", (4, 6), (5, 6)),
                            ("SPAN", (0, 7), (5, 7)),
                            ("SPAN", (1, 8), (5, 8)),
                            ("SPAN", (0, 9), (1, 9)),
                            ("SPAN", (2, 9), (3, 9)),
                            ("SPAN", (4, 9), (5, 9)),
                            ("SPAN", (0, 10), (5, 10)),
                            ("SPAN", (1, 11), (2, 11)),
                            ("SPAN", (3, 11), (5, 11)),
                        ]),
                        colWidths=(72*mm, 18*mm, 34*mm, 18*mm, 18*mm, 34*mm),
                        rowHeights=(9.5*mm, 5.5*mm, 10.5*mm, 10.5*mm, 9.5*mm, 9.5*mm, 9.5*mm, 10.5*mm, 5*mm, 9.5*mm, 6*mm, 9.5*mm)
                    )
                ]
            ],
            style=extend_table_style(styles["rc-main-table"], [
                ("OUTLINE", (0, 0), (-1, -1), 1.2, "black"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]),
        )
        elems += [
            Paragraph(
                "Judical Correction Services",
                extend_style(styles["rc-doc-header"], leftIndent=62*mm)
            ),
            Paragraph(
                "Dekalb County Recorders Court",
                extend_style(styles["rc-aawp-main-content"], spaceBefore=7, spaceAfter=1, leftIndent=75*mm)
            ),
            Table(
                [
                    [
                        main_table,
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                ]),
                colWidths=(194*mm, 74*mm)
            )
        ]
        
        return elems

    def _section_content_sp(self):
        elems = list()
        TEST_DATA = "<br /> Test Data"
        main_table = Table(
            [
                [                    
                    Table(
                        [
                            [
                                Paragraph("Apellido Nombre {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                Paragraph("Primer Nombre {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                None,
                                Paragraph("Sugundo Name {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                            ],
                            [
                                Paragraph("Tambien conocido/a como?: {}".format("Test Data"), styles["rc-aawp-main-content"]),
                                None, None, None, None, None
                            ],
                            [
                                Paragraph("Direccion Real {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                Paragraph("Ciudad {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                Paragraph("Estado {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                Paragraph("Codigo Postal {}".format(TEST_DATA), styles["rc-aawp-main-content"])
                            ],
                            [
                                Paragraph("Direccion Postal {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                Paragraph("Ciudad {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                Paragraph("Estado {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                Paragraph("Codigo Postal {}".format(TEST_DATA), styles["rc-aawp-main-content"])
                            ],
                            [
                                Paragraph("Numbero de telefono de casa {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                Paragraph("Numbero de telefono de cellular {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None, None, None, None,
                            ],
                            [
                                Paragraph("Nombre de contacto de emergencia {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                Paragraph("Número de contacto de emergencia {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None, None,
                                Paragraph("Relación con usted {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                            ],
                            [
                                Paragraph("Empleador {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                Paragraph("Ubicacion {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None, 
                                Paragraph("Numero de telefano de se trabajo {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                            ],
                            [
                                Table(
                                    [
                                        [
                                            Paragraph("Fecha de nacimiento {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                            Paragraph("Numbre de Seguro Social {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                            Paragraph("Raza {}".format(TEST_DATA), extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)),
                                            Paragraph("Sexo {}".format(TEST_DATA), extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)),
                                            Paragraph("Altura {}".format(TEST_DATA), extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)),
                                            Paragraph("Peso {}".format(TEST_DATA), extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)),
                                            Paragraph("Ojos {}".format(TEST_DATA), extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)),
                                            Paragraph("Cabello {}".format(TEST_DATA), extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)),
                                        ]
                                    ],
                                    style=extend_table_style(styles["rc-main-table_inner"], [
                                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                        ("INNERGRID", (0, 0), (-1, -1), .1, "black"),
                                    ]),
                                    colWidths=(36*mm, 52*mm, 17.3*mm, 17.3*mm, 17.4*mm, 17.3*mm, 17.3*mm, 17.3*mm),
                                    rowHeights=10.5*mm
                                ),
                                None, None, None, None , None
                            ],
                            [
                                Paragraph("Cicatriz/Tatuajes {}".format("Test Data"), extend_style(styles["rc-aawp-main-content"], fontSize=9)),
                                Paragraph("Nombre de su oficial de probatoria {}".format("Test Data"), extend_style(styles["rc-aawp-main-content"], fontSize=9)),
                                None, None, None, None
                            ],
                            [
                                Paragraph("Probatoria corriente/ Libertad condicional {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                Paragraph("Para que: {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                Paragraph("Nombre de su oficial de probatoria {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None
                            ],
                            [
                                Paragraph("<U>PARA USO OFICIAL SOLAMENTE</U>", extend_style(styles["rc-aawp-main-content"], leftIndent=73*mm)),
                                None, None, None, None, None
                            ],
                            [
                                Paragraph("Case Number {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                Paragraph("First Appt {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                Paragraph("Monthly Payment: {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None
                            ],
                            [
                                Paragraph("Probaban Officer: {}".format("Test Data"), styles["rc-aawp-main-content"]),
                                None, None, None, None, None
                            ],
                        ],
                        style=extend_table_style(styles["rc-main-table_inner"], [
                            ("OUTLINE", (0, 0), (-1, -1), 1.2, "black"),
                            ("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ("INNERGRID", (0, 0), (-1, -1), .1, "black"),
                            ("LEFTPADDING", (0, 7), (4, 7), 0),
                            ("RIGHTPADDING", (0, 7), (4, 7), 0),
                            ("TOPPADDING", (0, 7), (4, 7), 0),
                            ("TOPPADDING", (0, 10), (4, 10), 1.4*mm),
                            ("SPAN", (1, 0), (3, 0)),                            
                            ("SPAN", (4, 0), (5, 0)),
                            ("SPAN", (0, 1), (5, 1)),
                            ("SPAN", (0, 2), (1, 2)),
                            ("SPAN", (2, 2), (3, 2)),
                            ("SPAN", (0, 3), (1, 3)),
                            ("SPAN", (2, 3), (3, 3)),
                            ("SPAN", (1, 4), (3, 4)),
                            ("SPAN", (4, 4), (5, 4)),
                            ("SPAN", (1, 5), (3, 5)),
                            ("SPAN", (4, 5), (5, 5)),
                            ("SPAN", (0, 6), (1, 6)),
                            ("SPAN", (2, 6), (3, 6)),
                            ("SPAN", (4, 6), (5, 6)),
                            ("SPAN", (0, 7), (5, 7)),
                            ("SPAN", (1, 8), (5, 8)),
                            ("SPAN", (0, 9), (1, 9)),
                            ("SPAN", (2, 9), (3, 9)),
                            ("SPAN", (4, 9), (5, 9)),
                            ("SPAN", (0, 10), (5, 10)),
                            ("SPAN", (1, 11), (2, 11)),
                            ("SPAN", (3, 11), (5, 11)),
                            ("SPAN", (0, 12), (5, 12))
                        ]),
                        colWidths=(70*mm, 18*mm, 34*mm, 18*mm, 18*mm, 36*mm),
                        rowHeights=(9.5*mm, 5.5*mm, 10.5*mm, 10.5*mm, 9.5*mm, 9.5*mm, 9.5*mm, 10.5*mm, 5*mm, 9.5*mm, 6*mm, 9.5*mm, 6*mm)
                    )
                ]
            ],
            style=extend_table_style(styles["rc-main-table"], [
                ("OUTLINE", (0, 0), (-1, -1), 1.2, "black"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]),
        )
        elems += [
            PageBreak(),
            Paragraph(
                "Judicial Correction Services",
                extend_style(styles["rc-doc-header"], leftIndent=62*mm)
            ),
            Paragraph(
                "Brookhaven Municiple Court",
                extend_style(styles["rc-aawp-main-content"], spaceBefore=7, spaceAfter=1, leftIndent=75*mm)
            ),
            Table(
                [
                    [
                        main_table,
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                ]),
                colWidths=(194*mm, 74*mm)
            )
        ]
        
        return elems
