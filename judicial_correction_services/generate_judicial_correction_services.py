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
                                Paragraph("<b>Last Name</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                Paragraph("<b>First Name</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                None,
                                Paragraph("<b>Middle Name</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                            ],
                            [
                                Paragraph("<b>AKA:</b> {}".format("Test Data"), styles["rc-aawp-main-content"]),
                                None, None, None, None, None
                            ],
                            [
                                Paragraph("<b>Physical Address</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                Paragraph("<b>City</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                Paragraph("<b>State</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                Paragraph("<b>Zip Code</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"])
                            ],
                            [
                                Paragraph("<b>Mailing Address (if different)</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                Paragraph("<b>City</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                Paragraph("<b>State</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                Paragraph("<b>Zip Code</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"])
                            ],
                            [
                                Paragraph("<b>Home Number</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                Paragraph("<b>Cell Number</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None, None,
                                Paragraph("<b>Email Address</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                            ],
                            [
                                Paragraph("<b>Emergency Contact Name</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                Paragraph("<b>Emergency Contact Number</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None, None,
                                Paragraph("<b>Relationship to You</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                            ],
                            [
                                Paragraph("<b>Employer? Student? Or Unemployed?</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                Paragraph("<b>Location</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None, 
                                Paragraph("<b>Work Number</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                            ],
                            [
                                Table(
                                    [
                                        [
                                            Paragraph("<b>Date of Birth</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                            Paragraph("<b>Social Security Number</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                            Paragraph("<b>Race</b> {}".format(TEST_DATA), extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)),
                                            Paragraph("<b>Sex</b> {}".format(TEST_DATA), extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)),
                                            Paragraph("<b>Hgt</b> {}".format(TEST_DATA), extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)),
                                            Paragraph("<b>Wgt</b> {}".format(TEST_DATA), extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)),
                                            Paragraph("<b>Eyes</b> {}".format(TEST_DATA), extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)),
                                            Paragraph("<b>Hair</b> {}".format(TEST_DATA), extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)),
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
                                Paragraph("<b>Scars/Tattoos:</b> {}".format("Test Data"), extend_style(styles["rc-aawp-main-content"], fontSize=9)),
                                Paragraph("<b>Driver's License Number/State:</b> {}".format("Test Data"), extend_style(styles["rc-aawp-main-content"], fontSize=9)),
                                None, None, None, None
                            ],
                            [
                                Paragraph("<b>Currently on Probation/Parole: Where?</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                Paragraph("<b>What for:</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                Paragraph("<b>Officer's Name & Number:</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None
                            ],
                            [
                                Paragraph("<b><U>FOR OFFICER USE ONLY</U></b>", extend_style(styles["rc-aawp-main-content"], leftIndent=18.4*mm)),
                                None, None, None, None, None
                            ],
                            [
                                Paragraph("<b>Case Number</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                Paragraph("<b>First Appt</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                Paragraph("<b>Probation Officer</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
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
                                Paragraph("<b>Apellido Nombre</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                Paragraph("<b>Primer Nombre</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                None,
                                Paragraph("<b>Sugundo Name</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                            ],
                            [
                                Paragraph("<b>Tambien conocido/a como?:</b> {}".format("Test Data"), styles["rc-aawp-main-content"]),
                                None, None, None, None, None
                            ],
                            [
                                Paragraph("<b>Direccion Real</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                Paragraph("<b>Ciudad</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                Paragraph("<b>Estado</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                Paragraph("<b>Codigo Postal</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"])
                            ],
                            [
                                Paragraph("<b>Direccion Postal</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                Paragraph("<b>Ciudad</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                Paragraph("<b>Estado</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                Paragraph("<b>Codigo Postal</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"])
                            ],
                            [
                                Paragraph("<b>Numbero de telefono de casa</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                Paragraph("<b>Numbero de telefono de cellular</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None, None, None, None,
                            ],
                            [
                                Paragraph("<b>Nombre de contacto de emergencia</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                Paragraph("<b>Número de contacto de emergencia</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None, None,
                                Paragraph("<b>Relación con usted</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                            ],
                            [
                                Paragraph("<b>Empleador</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                Paragraph("<b>Ubicacion</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None, 
                                Paragraph("<b>Numero de telefano de se trabajo</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                            ],
                            [
                                Table(
                                    [
                                        [
                                            Paragraph("<b>Fecha de nacimiento</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                            Paragraph("<b>Numbre de Seguro Social</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                            Paragraph("<b>Raza</b> {}".format(TEST_DATA), extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)),
                                            Paragraph("<b>Sexo</b> {}".format(TEST_DATA), extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)),
                                            Paragraph("<b>Altura</b> {}".format(TEST_DATA), extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)),
                                            Paragraph("<b>Peso</b> {}".format(TEST_DATA), extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)),
                                            Paragraph("<b>Ojos</b> {}".format(TEST_DATA), extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)),
                                            Paragraph("<b>Cabello</b> {}".format(TEST_DATA), extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)),
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
                                Paragraph("<b>Cicatriz/Tatuajes</b> {}".format("Test Data"), extend_style(styles["rc-aawp-main-content"], fontSize=9)),
                                Paragraph("<b>Nombre de su oficial de probatoria</b> {}".format("Test Data"), extend_style(styles["rc-aawp-main-content"], fontSize=9)),
                                None, None, None, None
                            ],
                            [
                                Paragraph("<b>Probatoria corriente/ Libertad condicional</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                Paragraph("<b>Para que:</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                Paragraph("<b>Nombre de su oficial de probatoria</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None
                            ],
                            [
                                Paragraph("<b><U>PARA USO OFICIAL SOLAMENTE</U></b>", extend_style(styles["rc-aawp-main-content"], leftIndent=73*mm)),
                                None, None, None, None, None
                            ],
                            [
                                Paragraph("<b>Case Number</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                Paragraph("<b>First Appt</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None,
                                Paragraph("<b>Monthly Payment:</b> {}".format(TEST_DATA), styles["rc-aawp-main-content"]),
                                None
                            ],
                            [
                                Paragraph("<b>Probation Officer:</b> {}".format("Test Data"), styles["rc-aawp-main-content"]),
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
