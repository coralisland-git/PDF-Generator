# -*- coding: utf-8 -*-
import cStringIO
import datetime

from document_specific_styles import *


def non_jury_trial_demand_spanish(title=None, author=None):
    cr =TDReport(title, author)
    buff = cStringIO.StringIO()
    return cr.create_report(buff)


class TDReport:
    def __init__(self, title=None, author=None):
        self.page_size = letter
        self.page_margin = (12.4 * mm, 12.4 * mm)
        self.sections = ["header", "content"]
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
            pagesize=letter,
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

    def _section_header(self):
        elems = list()
        elems += [
            Paragraph(
                "En el Tribunal Municipal de Brookhaven <br />Estado de Georgia",                
                extend_style(styles["rc-doc-header"], fontSize=14, leading=14.5)
            ),
            Spacer(0, 9.8 * mm),
            Table(
                [
                    [
                        Paragraph("Ciudad de Brookhaven", styles["rc-tdwp-main-tb"]),
                        None,
                        Paragraph("No. de Caso/ Infracción "+'_'*20, styles["rc-tdwp-main-tb"])
                    ],
                    [
                        None,
                        None,
                        None
                    ],
                    [
                        Paragraph("Versus", styles["rc-tdwp-main-tb"]),
                        None,
                        Paragraph("Cargo(s): "+'_'*27, styles["rc-tdwp-main-tb"])
                    ],
                    [
                        None,
                        None,
                        None
                    ],
                    [
                        None,
                        None,
                        None
                    ],
                    [
                        Paragraph("Acusado", styles["rc-tdwp-main-tb"]),
                        None,
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 5), (-1, -1), "TOP"),
                    ("TOPPADDING", (0, 5), (-1, -1), 0.2 * mm),
                    ("LINEBELOW", (0, 4), (0, 4), 0.1, "black"),
                ]),
                colWidths=(52 * mm, 42 * mm, 96 * mm),
                rowHeights=4.2 * mm
            ),
            Paragraph(
                "<u>EMGENCIA PARA CELEBRAR UN JUICIO ANTE UN JUEZ</u>",
                extend_style(styles["rc-header"], fontSize=11 ,spaceBefore=4)
            ),
            Spacer(0, 1 * mm)
        ]
            
        return elems

    def _section_content(self):
        pre_dash = "_"*4 + " "
        elems = [
            Paragraph(
                "El(la) susodicho(a) acusado(a) ha compadecido ante el Juez este día "+'_'*5+" de "+'_'*11+", 201"+'_'*4+" para responder a su(s) cargo(s) y se ha declarado inocente.",
                extend_style(styles["rc-tdwp-main"], fontSize=11)
            ),
        ]        
        elems += [
            Paragraph(
                "*" * 102,
                extend_style(styles["rc-tdwp-main"], leading=9, spaceBefore=9)
            ),
            Table(
                [
                    [
                        Paragraph(pre_dash, extend_style(styles["rc-tdwp-main"])),
                        Paragraph(
                            "Yo entiendo que tengo un derecho Constitucional de celebrar un juicio por jurado y que, al exigir un juicio ante un juez, renuncio al derecho de celebrar un juicio por jurado.",
                            extend_style(styles["rc-tdwp-main"], spaceBefore=0)
                        )
                    ],
                    [
                        Paragraph(pre_dash, extend_style(styles["rc-tdwp-main"])),
                        Paragraph(
                            "Yo entiendo que tengo el derecho de tener asistencia legal particular, y en su defecto, tengo el derecho a llenar una solicitud para que me represente un abogado de oficio en el juicio; pero antes de la fecha del juicio ya debo haber contratado a un abogado si elijo ser representado por un abogado particular.",
                            styles["rc-tdwp-main"]
                        ),
                    ],
                    [
                        Paragraph(pre_dash, extend_style(styles["rc-tdwp-main"])),
                        Paragraph(
                            "Yo entiendo la naturaleza de los cargos en mi contra, lo mismo que la penas mínimas y máximas posibles a imponerse por cada uno de ellos.",
                            styles["rc-tdwp-main"]
                        )
                    ],
                    [
                        Paragraph(pre_dash, extend_style(styles["rc-tdwp-main"])),
                        Paragraph(
                            "Yo entiendo que las normas de presentación de pruebas me aplican a pesar de que yo no sea abogado.",
                            styles["rc-tdwp-main"]
                        )
                    ],
                    [
                        Paragraph(pre_dash, extend_style(styles["rc-tdwp-main"])),
                        Paragraph(
                            "Yo entiendo que <u>no</u> tengo que dar testimonio y mantengo el derecho de permanecer en silencio. Además entiendo que por el hecho de que yo permanezca en silencio, eso no puede utilizarse en mi contra.",
                            styles["rc-tdwp-main"]
                        )
                    ],
                    [
                        Paragraph(pre_dash, extend_style(styles["rc-tdwp-main"])),
                        Paragraph(
                            "Yo entiendo que tengo el derecho de utilizar los poderes de esta corte para citar judicialmente a cualquier testigo(s) para que compadeica(n) al juicio.",
                            styles["rc-tdwp-main"]
                        )
                    ],
                    [
                        Paragraph(pre_dash, extend_style(styles["rc-tdwp-main"])),
                        Paragraph(
                            "Yo entiendo que en la fecha de mi juicio tengo que traer y tener en mi posesión todas las pruebas que quiera utilizar para tal efecto.",
                            styles["rc-tdwp-main"]
                        )
                    ],
                ],
                colWidths=(8.5 * mm, 182 * mm),                
                style=(
                    ('VALIGN', (0, 0), (1, 6), 'TOP'),
                    ("LEFTPADDING", (0, 0), (1, 6), 0.0 * mm),
                    ("RIGHTPADDING", (0, 0), (1, 6), 0.0 * mm),
                    ("BOTTOMPADDING", (0, 0), (1, 6), 2.5 * mm)
                )
            ),
            Paragraph(
                "*" * 102,
                extend_style(styles["rc-tdwp-main"], leading=9, spaceBefore=4)
            ),
            Table(
                [
                    [   
                        Paragraph(pre_dash, extend_style(styles["rc-tdwp-main"])),
                        Paragraph(
                            "En este momento deseo celebrar un juicio ante un juez en esta corte.",
                            extend_style(styles["rc-tdwp-main"], spaceBefore=0)
                        )
                    ],
                    [   
                        Paragraph(pre_dash, extend_style(styles["rc-tdwp-main"])),
                        Paragraph(
                            "Al firmar esta exigencia, yo acuso recibo de una copia de la misma.",
                            styles["rc-tdwp-main"]
                        )
                    ],
                    [   
                        Paragraph(pre_dash, extend_style(styles["rc-tdwp-main"])),
                        Paragraph(
                            "Al firmar esta exigencia, yo reconozco que debo comparecer ante la corte en la fecha y hora programadas y renuncio a mi derecho de pagar anticipadamente a tal fecha.",
                            styles["rc-tdwp-main"]
                        )
                    ]
                ],
                colWidths=(8.5 * mm, 182 * mm),                
                style=(
                    ('VALIGN', (0, 0), (1, 2), 'TOP'),
                    ("LEFTPADDING", (0, 0), (1, 2), 0.0 * mm),
                    ("RIGHTPADDING", (0, 0), (1, 2), 0.0 * mm),
                    ("BOTTOMPADDING", (0, 0), (1, 2), 2.5 * mm)
                )
            ),
            Paragraph(
                "<b>YO RECONOZCO que la fecha de mi juicio ante un juez va ser el día "+'_'*4+" de "+'_'*8+", 201"+'_'*2+" a las <u>8:30 AM</u></b>",
                extend_style(styles["rc-tdwp-main"], spaceBefore=4)
            ),
            Paragraph(
                "YO JURO bajo pena de perjurio que estas declaraciones son verdaderas y correctas.",
                extend_style(styles["rc-tdwp-main"], spaceBefore=8)
            ),
            Paragraph(
                "YO DOY FE de que al firmar esta exigencia, no se me ha prometido ni amenazado de ninguna forma a que renuncie a mi derecho de tener un abogado, o a que renuncie a mi derecho de celebrar un juicio por jurado. Además, doy fe de que he leído — o se me ha leído — este documento en su totalidad y entiendo su contenido.",
                extend_style(styles["rc-tdwp-main"], spaceBefore=8)
            ),
            Spacer(0, 8 * mm),
            Table(
                [        
                    [
                        None, None, None, None, None, None
                    ],
                    [
                        Paragraph("<b>Firma del Acusado</b>", styles["rc-tdwp-main-tb"]),
                        None,
                        Paragraph("<b>Teléfono</b>", styles["rc-tdwp-main-tb"]),
                        None,
                        Paragraph("<b>Fecha</b>", styles["rc-tdwp-main-tb"]),
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 1), (-1, -1), "TOP"),
                    ("TOPPADDING", (0, 1), (-1, -1), 0.2 * mm),
                    ("LINEABOVE", (0, 1), (0, 1), 0.1, "black"),
                    ("LINEABOVE", (2, 1), (2, 1), 0.1, "black"),
                    ("LINEABOVE", (4, 1), (4, 1), 0.1, "black"),
                ]),
                colWidths=(40 * mm, 20 * mm, 38 * mm, 26 * mm , 38 * mm, 29 * mm),
                rowHeights=2.2 * mm
            ),
            Spacer(0, 3 * mm),
            Paragraph(
                "REVISED 02/2019",
                extend_style(styles["rc-tdwp-main"], fontSize=6)
            )
        ]

        return elems
