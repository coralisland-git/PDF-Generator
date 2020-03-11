# coding=utf-8
import cStringIO

from document_specific_styles import *
from common.signatures import *
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT


def generate_defendants_right_to_an_attorney():
    cr = DRTAReport()
    buff = cStringIO.StringIO()
    return cr.create_report(buff)

class DRTAReport:
    def __init__(self, title=None, author=None):
        self.page_size = letter
        self.page_margin = (26.4 * mm, 4.8 * mm)
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

        def page_number(canv, doc):
            page_num = Paragraph(
                str(doc.page),
                extend_style(styles["rc-aawp-main-content"], alignment=TA_RIGHT, fontSize=5),
            )
            page_num.wrapOn(canv, self.page_size[0]-26.4*mm, 0)
            page_num.drawOn(canv, 0, 5.8*mm)

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
        ], onPage=page_number)
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

    def _section_content_en(self):
        pre_space = "&nbsp;"*12
        elems = list()
        elems += [
            Spacer(0, 8.6 * mm),
            Paragraph(
                "In the Municipal Court of Brookhaven <br />State of Georgia",
                styles["rc-header"]
            ),
            Spacer(0, 5.4 * mm),
            Table(
                [
                    [
                        Paragraph("City of Brookhaven", styles["rc-aawp-main-header"]),
                        Paragraph("Citation No.", styles["rc-aawp-main-header"]),
                        Paragraph("Test Data", styles["rc-aawp-main-header"]),
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (2, 0), (2, 0), 0.1, "black"),
                ]),
                colWidths=(75*mm, 20*mm, 50*mm, 6*mm),
            ),            
            Table(
                [
                    [
                        Paragraph("Vs.", extend_style(styles["rc-aawp-main-header"], leftIndent=12*mm)), 
                        Paragraph("Charges:", styles["rc-aawp-main-header"]),
                        Paragraph("Test Data", styles["rc-aawp-main-header"]),
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (2, 0), (2, 0), 0.1, "black"),
                ]),
                colWidths=(75*mm, 16*mm, 54*mm, 6*mm),
            ),
            Spacer(0, 3.2*mm),
            Table(
                [
                    [
                        Paragraph("Test Data", extend_style(styles["rc-aawp-main-header"])),
                        None,

                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (0, 0), (0, 0), 0.1, "black")
                ]),
                colWidths=(60*mm, 91*mm),
            ),  
            Paragraph("<u>DEFENDANT'S RIGHT TO AN ATTORNEY</u>", extend_style(styles["rc-header"], spaceBefore=10)),
            Paragraph(
                """{}
                As a person accused of a crime, you have the right to be represented by an attorney under the United States 
                and Georgia Constitutions at all critical stages of the criminal process, including your arraignment. If you 
                cannot afford an attorney, you have the right to have an attorney appointed to represent you. If you wish to 
                be interviewed to determine whether you qualify financially for a court appointed attorney, you may apply and 
                be interviewed by a member of the court staff.
                """.format(pre_space),
                extend_style(styles["rc-aawp-main-content"])
            ),
            Paragraph(
                """{}
                Although you may waive the right to an attorney, you should be aware that an attorney can help you understand:
                """.format(pre_space),
                extend_style(styles["rc-aawp-main-content"])
            ),
        ]
        text_list = [
            'The nature of the charges against you;',
            'The possibility of lesser-included offenses to these charges;',
            'The range of possible punishments for the charges, including a jail sentence for up to 12 months on each misdemeanor and 6 months on each local ordinance;',
            'The possible defenses to your case;',
            'The rights that you give up when you enter a plea;',
            'Circumstances that may reduce the punishment;',
            'The strategies for defending or trying the case; and',
            'Any other facts necessary for a broad understanding of the matter.'
        ]
        table1 = []
        for idx, text in enumerate(text_list):
            table1.append(
                [   
                    None,
                    Paragraph('{}.'.format(idx+1), styles["rc-aawp-main-content"]),
                    Paragraph(text, styles["rc-aawp-main-content"])
                ]
            )

        text_list2 = [
            'The rules governing the admissibility of evidence will be enforced by the judge;',
            'You must make decisions with regard to the calling of witnesses to testify on your behalf;',
            'You must decide whether you want to testify on your own behalf. You <b>are not</b> required to testify at trial, but if you do testify, you would be subject to cross-examination;',
            'The Prosecution has the burden of proving its case beyond a reasonable doubt;',
            'Issues must be properly preserved by way of timely objections and, in order to raise them on appeal, secure a record of the proceedings.'
        ]
        table2 = []
        for idx, text in enumerate(text_list2):
            table2.append(
                [
                    None,
                    Paragraph('{}.'.format(idx+1), styles["rc-aawp-main-content"]),
                    Paragraph(text, styles["rc-aawp-main-content"])
                ]
            )

        text_list3 = [
            'I have read and fully understand the above statements;',
            'I am not under the influence of alcohol or drugs, and I am not suffering from any mental or physical disability that hampers my ability to understand these proceedings or to present a defense to the charges against me;',
            'I understand that I may speak with the prosecutor, but am under no obligation to do so. <b>Anything I say to the prosecutor can be used as evidence against me</b>.',
            'I HAVE TAKEN THE TIME TO THOROUGHLY READ THE ABOVE AND I CHOOSE TO WAIVE MY RIGHT TO AN ATTORNEY, AND AT THIS TIME WISH TO REPRESENT MYSELF.'
        ]
        table3 = []
        for idx, text in enumerate(text_list3):
            table3.append(
                [
                    None,
                    Paragraph('{}.'.format(idx+1), styles["rc-aawp-main-content"]),
                    Paragraph(text, styles["rc-aawp-main-content"])
                ]
            )

        elems +=[
            Spacer(0, 3.2*mm),
            Table(
                table1,
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
                colWidths=(24*mm, 6*mm, 132*mm),
            ),
            Paragraph(
                """{}
                If you waive your right to an attorney, you must also understand that at trial:
                """.format(pre_space), 
                extend_style(styles["rc-aawp-main-content"])),
            Spacer(0, 3.2*mm),
            Table(
                table2,
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
                colWidths=(18*mm, 6*mm, 138*mm),
            ),
            Paragraph(
                """{}
                The judge cannot assist you in identifying or developing any of the above matters, 
                because the judge must remain impartial between you and the prosecutor. The judge 
                cannot assist either side against the other. Even if you chose to waive your right 
                to an attorney now, you can change your mind and obtain an attorney later. But you 
                must act diligently in obtaining an attorney, either appointed or retained. If you 
                do not act diligently, it is possible that you might later be deemed to have waived 
                your right to an attorney.
                """.format(pre_space), 
                extend_style(styles["rc-aawp-main-content"])),
            Paragraph(
                """{}
                I swear under penalties of perjury that;
                """.format(pre_space), 
                extend_style(styles["rc-aawp-main-content"])),
            Spacer(0, 3.2*mm),
            Table(
                table3,
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]),
                colWidths=(18*mm, 6*mm, 138*mm),
            ),
            Spacer(0, 2.4*mm),
            Table(
                [
                    [
                        None,
                        Paragraph("This", styles["rc-aawp-main-content"]),
                        Paragraph("", styles["rc-aawp-main-content"]),
                        Paragraph(" &nbsp;day of", styles["rc-aawp-main-content"]),
                        Paragraph("", styles["rc-aawp-main-content"]),
                        Paragraph(", 20", styles["rc-aawp-main-content"]),
                        Paragraph("XX", styles["rc-aawp-main-content"]),
                        Paragraph(".", styles["rc-aawp-main-content"])
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (2, 0), (2, 0), 0.1, "black"),
                    ("LINEBELOW", (4, 0), (4, 0), 0.1, "black"),
                    ("LINEBELOW", (6, 0), (6, 0), 0.1, "black")
                ]),
                colWidths=(65*mm, 8*mm, 13*mm, 12*mm, 18*mm, 6*mm, 6*mm, 1*mm),
            ),
            Spacer(0, 12.4 * mm),
            Table(
                [
                    [
                        None, Paragraph("Defendant", styles["rc-aawp-main-content"]), None
                    ],
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEABOVE", (1, 0), (1, 0), 0.1, "black"),
                ]),
                colWidths=(65*mm, 56*mm, 8*mm),
            ),
            Paragraph("JAN, 2019", extend_style(styles["rc-aawp-main-content"], fontSize=5.5, spaceBefore=10))
        ]
        
        return elems

    def _section_content_sp(self):
        pre_space = "&nbsp;"*12
        elems = list()
        elems += [
            Spacer(0, 8.6 * mm),
            Paragraph(
                "En el Tribunal Municipal de Brookhaven <br />Estado de Georgia",
                styles["rc-header"]
            ),
            Spacer(0, 3.4 * mm),
            Table(
                [
                    [
                        Paragraph("Ciudad de Brookhaven", styles["rc-aawp-main-header"]),
                        Paragraph("No. del Caso:", styles["rc-aawp-main-header"]),
                        Paragraph("Test Data", styles["rc-aawp-main-header"])
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (2, 0), (2, 0), 0.1, "black"),
                ]),
                colWidths=(93*mm, 22*mm, 48*mm),
            ),            
            Table(
                [
                    [
                        Paragraph("Vs.", extend_style(styles["rc-aawp-main-header"], leftIndent=16*mm)), 
                        Paragraph("Cargo(s):", styles["rc-aawp-main-header"]),
                        Paragraph("Test Data", styles["rc-aawp-main-header"])
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (2, 0), (2, 0), 0.1, "black"),
                ]),
                colWidths=(93*mm, 16*mm, 54*mm),
            ),
            Spacer(0, 1.2*mm),
            Table(
                [
                    [
                        Paragraph("Test Data", extend_style(styles["rc-aawp-main-header"])),
                        None
                    ],
                    [
                        Paragraph("Nombre del Acusado", extend_style(styles["rc-aawp-main-header"])),
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (0, 0), (0, 0), 0.1, "black")
                ]),
                colWidths=(60*mm, 103*mm),
            ),  
            Paragraph("<u>DERECHO DEL ACUSADO A UN ABOGADO</u>", extend_style(styles["rc-header"], spaceBefore=5)),
            Paragraph(
                """{}
               Como persona acusada de un delito, usted tiene el derecho, conforme a las Constituciones de los Estados 
               Unidos y de Georgia, a ser representado por un abogado en todas las etapas cruciales del proceso penal, 
               incluyendo cuando comparezca ante el Juez para leerle los cargos. Si no puede pagar un abogado, tendrá 
               derecho a que se nombre uno para que le represente. Si desea ser entrevistado para determinar si califica 
               financieramente para tener un abogado de oficio designado por el Tribunal, puede solicitarlo y ser entrevistado
                por un miembro del personal del Tribunal.
                """.format(pre_space),
                extend_style(styles["rc-aawp-main-content"])
            ),
            Paragraph(
                """{}
                Aunque usted puede renunciar al derecho a un abogado, debe tener en cuenta que el abogado puede ayudarlo a entender:
                """.format(pre_space),
                extend_style(styles["rc-aawp-main-content"])
            ),
        ]
        text_list = [
            'La naturaleza de los cargos de que se le acusa;',
            'La posibilidad de delitos menores a los imputados;',
            'El rango de castigos posibles para los cargos, incluyendo hasta 12 meses de cárcel por cada delito menor y 6 meses por infracción de cada ordenanza municipal;',
            'Las defensas posibles para su caso;',
            'Los derechos a los que renuncia cuando realiza una declaración ;',
            'Las circunstancias que pueden reducir el castigo;',
            'Las estrategias para defender o juzgar el caso; y',
            'Cualquier otro hecho necesario para que pueda entender bien el caso.'
        ]
        table1 = []
        for idx, text in enumerate(text_list):
            table1.append(
                [   
                    None,
                    Paragraph('{}.'.format(idx+1), styles["rc-aawp-main-content"]),
                    Paragraph(text, styles["rc-aawp-main-content"])
                ]
            )

        text_list2 = [
            'El Juez hará cumplir las normas que rigen la admisibilidad de las pruebas;',
            'Deberá tomar decisiones en cuanto a convocar testigos para que declaren en su defensa;',
            'Deberá decidir si quiere declarar en su propio nombre. <b>No se le exige</b> que declare durante el juicio, pero si desea hacerlo, estará sujeto a contrainterrogatorio;',
            'El fiscal que le acusa tendrá que demostrar su culpabilidad más allá de una duda razonable; ',
            'Los asuntos legales deben atenderse adecuadamente, objetándolos a tiempo, y para poder presentarlos en la apelación hay que asegurarse que haya un registro de ellos en autos.'
        ]
        table2 = []
        for idx, text in enumerate(text_list2):
            table2.append(
                [
                    None,
                    Paragraph('{}.'.format(idx+1), styles["rc-aawp-main-content"]),
                    Paragraph(text, styles["rc-aawp-main-content"])
                ]
            )

        text_list3 = [
            'He leído y entiendo plenamente lo anteriormente expuesto;',
            'No me encuentro actualmente bajo los efectos del alcohol ni de las drogas, y no sufro enfermedad mental ni incapacitación física alguna que pudiera obstaculizar mi capacidad para entender estos actos procesales, ni para presentar una defensa ante los cargos que se me imputan;',
            'Entiendo que puedo hablar con el fiscal, pero que no estoy obligado a hacerlo. <b>Todo lo que yo le diga al fiscal podrá usarse como prueba en mi contra</b>.',
            'HE TOMADO TIEMPO PARA LEER DETALLADAMENTE LO ANTERIOR Y OPTO POR RENUNCIAR A MI DERECHO A UN ABOGADO Y -EN ESTE MOMENTO- DESEO REPRESENTARME POR MÍ MISMO.'
        ]
        table3 = []
        for idx, text in enumerate(text_list3):
            table3.append(
                [
                    None,
                    Paragraph('{}.'.format(idx+1), styles["rc-aawp-main-content"]),
                    Paragraph(text, styles["rc-aawp-main-content"])
                ]
            )

        elems +=[
            Spacer(0, 1.2*mm),
            Table(
                table1,
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
                colWidths=(24*mm, 6*mm, 132*mm),
            ),
            Paragraph(
                """{}
                Si renuncia a su derecho a un abogado, <b>usted</b> debe entender también que durante el juicio:
                """.format(pre_space), 
                extend_style(styles["rc-aawp-main-content"])),
            Spacer(0, 1.2*mm),
            Table(
                table2,
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
                colWidths=(18*mm, 6*mm, 138*mm),
            ),
            Paragraph(
                """{}
                El Juez no puede ayudarle a identificar ni a desarrollar los temas anteriores, porque debe permanecer 
                imparcial entre usted y la fiscalía. El Juez no puede ayudar a ninguna de las partes en contra de la otra. 
                Incluso si usted opta por renunciar ahora a su derecho a un abogado, posteriormente puede cambiar de 
                opinión y tener uno. Pero debe actuar rápidamente para tener un abogado, bien sea nombrado por el Tribunal o 
                contratado por usted. Si usted no actúa rápidamente, es posible que se considere más tarde que ha renunciado 
                a su derecho a tener un abogado.
                """.format(pre_space), 
                extend_style(styles["rc-aawp-main-content"])),
            Paragraph(
                """{}
                Declaro so pena de perjurio que:
                """.format(pre_space), 
                extend_style(styles["rc-aawp-main-content"])),
            Spacer(0, 1.2*mm),
            Table(
                table3,
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]),
                colWidths=(18*mm, 6*mm, 138*mm),
            ),
            Spacer(0, 2.4*mm),
            Table(
                [
                    [
                        None,
                        Paragraph("Firmado hoy, ", styles["rc-aawp-main-content"]),
                        Paragraph("", styles["rc-aawp-main-content"]),
                        Paragraph(" &nbsp;de", styles["rc-aawp-main-content"]),
                        Paragraph("", styles["rc-aawp-main-content"]),
                        Paragraph(" &nbsp;de 20", styles["rc-aawp-main-content"]),
                        Paragraph("XX", styles["rc-aawp-main-content"]),
                        Paragraph(".", styles["rc-aawp-main-content"])
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (2, 0), (2, 0), 0.1, "black"),
                    ("LINEBELOW", (4, 0), (4, 0), 0.1, "black"),
                    ("LINEBELOW", (6, 0), (6, 0), 0.1, "black")
                ]),
                colWidths=(65*mm, 20*mm, 13*mm, 5*mm, 30*mm, 10*mm, 6*mm, 1*mm),
            ),
            Spacer(0, 12.4 * mm),
            Table(
                [
                    [
                        None, Paragraph("Firma del Acusado", styles["rc-aawp-main-content"]), None
                    ],
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEABOVE", (1, 0), (1, 0), 0.1, "black"),
                ]),
                colWidths=(65*mm, 66*mm, 19*mm),
            ),
            Paragraph("FEB, 2019", extend_style(styles["rc-aawp-main-content"], fontSize=5.5, spaceBefore=6))
        ]
        
        return elems
