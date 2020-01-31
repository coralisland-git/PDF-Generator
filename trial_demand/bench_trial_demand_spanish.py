# -*- coding: utf-8 -*-
import cStringIO
import datetime

from document_specific_styles import *


def bench_trial_demand_spanish(title=None, author=None):
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
            Spacer(0, 6.4 * mm),
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
                "<u>PETICIÓN PARA CELEBRAR UN JUICIO ANTE UN JUEZ <br />RENUNCIA AL DERECHO A TRANSFERIR EL CASO</u>",
                extend_style(styles["rc-header"], fontSize=11 ,spaceBefore=4)
            ),
            Spacer(0, 3 * mm)
        ]
            
        return elems

    def _section_content(self):
        pre_dash = "_"*4 + " "
        elems = [
            Paragraph(
                "El(la) susodicho(a) acusado(a) ha comparecido ante el Juez el día de hoy, "+'_'*5+" de "+'_'*11+" de 20"+'_'*4+", para responder a su(s) cargo(s) y se ha declarado inocente.",
                extend_style(styles["rc-tdwp-main"], fontSize=11)
            ),
        ]        
        elems += [
            Paragraph(
                "*" * 102,
                extend_style(styles["rc-tdwp-main"], leading=9, spaceBefore=4)
            ),
            Table(
                [
                    [   
                        Paragraph(pre_dash, extend_style(styles["rc-tdwp-main"])),
                        Paragraph(
                            "Entiendo que tengo derecho constitucional a que este caso se transfiera al Tribunal Estatal del Condado de DeKalb y a que se celebre allí un juicio bien sea por jurado o ante un juez sin jurado.",
                            extend_style(styles["rc-tdwp-main"], spaceBefore=0)
                        )        
                    ],
                    [   
                        Paragraph(pre_dash, extend_style(styles["rc-tdwp-main"])),
                        Paragraph(
                            "Entiendo que, al solicitar un juicio por jurado en el Tribunal Municipal de la Ciudad de Brookhaven, renuncio al derecho a transferir este caso al Tribunal Estatal y a mi derecho a un juicio por jurado.",
                            styles["rc-tdwp-main"]
                        )
                    ],
                    [   
                        Paragraph(pre_dash, extend_style(styles["rc-tdwp-main"])),
                        Paragraph(
                            "Entiendo que tengo derecho a tener asistencia legal particular o a solicitar un abogado de oficio designado por el Tribunal para que me represente en el juicio; pero antes de la fecha del juicio debo haber contratado a un abogado, si elijo ser representado por un abogado particular.",
                            styles["rc-tdwp-main"]
                        )
                    ],
                    [   
                        Paragraph(pre_dash, extend_style(styles["rc-tdwp-main"])),
                        Paragraph(
                            "Entiendo la naturaleza de los cargos en mi contra, así como las penas mínimas y máximas que pueden imponerse por cada uno de tales cargos.",
                            styles["rc-tdwp-main"]
                        )
                    ],
                    [   
                        Paragraph(pre_dash, extend_style(styles["rc-tdwp-main"])),
                        Paragraph(
                            "Entiendo que se me aplicarán las normas de presentación de pruebas, a pesar de que no sea abogado",
                            styles["rc-tdwp-main"]
                        )
                    ],
                    [   
                        Paragraph(pre_dash, extend_style(styles["rc-tdwp-main"])),
                        Paragraph(
                            "Entiendo que <u>no</u> tengo que declarar y que tengo derecho de permanecer en silencio. Entiendo, además, que, si no deseo declarar, ello no podrá utilizarse en mi contra.",
                            styles["rc-tdwp-main"]
                        )
                    ],
                    [   
                        Paragraph(pre_dash, extend_style(styles["rc-tdwp-main"])),
                        Paragraph(
                            "Entiendo que tengo derecho a utilizar los poderes de este tribunal para citar judicialmente a cualquier testigo(s) para que comparezca(n) en el juicio.",
                            styles["rc-tdwp-main"]
                        )
                    ],
                    [   
                        Paragraph(pre_dash, extend_style(styles["rc-tdwp-main"])),
                        Paragraph(
                            "Entiendo que, en la fecha de mi juicio, tengo que traer y tener en mi posesión <u>todas</u> las pruebas que desee utilizar.",
                            styles["rc-tdwp-main"]
                        )
                    ]
                ],
                colWidths=(8.5 * mm, 182 * mm),                
                style=(
                    ('VALIGN', (0, 0), (1, 7), 'TOP'),
                    ("LEFTPADDING", (0, 0), (1, 7), 0.0 * mm),
                    ("RIGHTPADDING", (0, 0), (1, 7), 0.0 * mm),
                    ("BOTTOMPADDING", (0, 0), (1, 7), 2.5 * mm)
                )
            ),
            Paragraph(
                "*" * 102,
                extend_style(styles["rc-tdwp-main"], leading=9, spaceBefore=0)
            ),
            Table(
                [
                    [
                        Paragraph(pre_dash, extend_style(styles["rc-tdwp-main"])),
                        Paragraph(
                            "En este momento deseo celebrar un juicio ante un juez en este tribunal.",
                            extend_style(styles["rc-tdwp-main"], spaceBefore=0)
                        )
                    ],
                    [
                        Paragraph(pre_dash, extend_style(styles["rc-tdwp-main"])),
                        Paragraph(
                            "Acuso recibo, al firmar esta petición, de una copia de la misma.",
                            styles["rc-tdwp-main"]
                        )
                    ],
                    [
                        Paragraph(pre_dash, extend_style(styles["rc-tdwp-main"])),
                        Paragraph(
                            "Reconozco, al firmar esta petición, que debo comparecer ante el tribunal en la fecha y hora programadas y que renuncio a mi derecho a pagar por adelantado de tal fecha.",
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
                "<b>RECONOZCO que la fecha de mi juicio ante un juez es el día "+'_'*4+" de "+'_'*8+" de 20"+'_'*2+" a las <u>8:30 AM</u></b>",
                extend_style(styles["rc-tdwp-main"], spaceBefore=4)
            ),
            Paragraph(
                "JURO, so pena de perjurio, que estas declaraciones son verdaderas y correctas.",
                extend_style(styles["rc-tdwp-main"], spaceBefore=6)
            ),
            Paragraph(
                "DOY FE de que, al firmar esta petición, no se me ha prometido ni amenazado de ninguna forma para que renuncie a mi derecho a tener un abogado, ni a que renuncie a mi derecho a celebrar un juicio por jurado. Además, doy fe de que he leído —o se me ha leído— este documento en su totalidad y entiendo su contenido.",
                extend_style(styles["rc-tdwp-main"], spaceBefore=6)
            ),
            Spacer(0, 4 * mm),
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
            Paragraph(
                "REVISED 02/2019",
                extend_style(styles["rc-tdwp-main"], fontSize=6)
            )
        ]

        return elems
