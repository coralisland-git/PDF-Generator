import cStringIO

from document_specific_styles import *
from common.signatures import *
from reportlab.platypus import NextPageTemplate

def generate_probationers_right_to_counsel():
    cr =PRTCReport()
    buff = cStringIO.StringIO()
    return cr.create_report(buff)

class PRTCReport:
    def __init__(self, title=None, author=None):
        self.page_size = letter
        self.page_margin = (25.4 * mm, 26 * mm)
        self.page_margin_sp = (11.8 * mm, 14.4 * mm)
        self.sections = ["header", "front", "back"]
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
                extend_style(styles["rc-tdwp-main"], alignment=TA_CENTER, fontSize=11),
            )
            page_num.wrapOn(canv, self.page_size[0], 0)
            page_num.drawOn(canv, 0, 14.4*mm)
        
        if not buff:
            buff = io.BytesIO()

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
        page_t_sp = PageTemplate('normal_sp', [
            Frame(
                self.page_margin_sp[0],
                self.page_margin_sp[1],
                self.page_size[0] - self.page_margin_sp[0] * 2,
                self.page_size[1] - self.page_margin_sp[1] * 2,
                leftPadding=0,
                bottomPadding=0,
                rightPadding=0,
                topPadding=0,
            )
        ], onPage=page_number)

        story = []
        for section in self.sections:
            elems = get_method(section)()
            for elem in elems:
                story.append(elem)

        story.append(NextPageTemplate('normal_sp'))
        story.append(PageBreak())

        for section in self.sections:
            elems = get_method(section+'_sp')()
            for elem in elems:
                story.append(elem)

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
        doc_t.addPageTemplates([page_t, page_t_sp])
        doc_t.build(story)

        buff.seek(0)
        return buff

    def _section_header(self):
        elems = list()
        elems += [
            Paragraph(
                "BROOKHAVEN MUNICIPAL COURT <br /> STATE OF GEORGIA",
                extend_style(styles["rc-doc-header"])
            ),
            Spacer(0, 5.6 * mm),
            Table(
                [
                    [
                        Paragraph("City of Brookhaven <br /> &nbsp;", styles["rc-tdwp-main"]),
                        Paragraph("Probation Revocation/Modification <br />Hearing", styles["rc-tdwp-main"])
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
                colWidths=(102*mm, 63*mm)
            ),
            Paragraph("vs.", extend_style(styles["rc-tdwp-main"], spaceBefore=0)),
            Table(
                [
                    [
                        None,
                        Paragraph("Date:", styles["rc-tdwp-main"]),
                        Paragraph("Test Data", styles["rc-tdwp-main"]),
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEBELOW", (2, 0), (2, 0), 0.1, "black"),
                ]),
                colWidths=(102*mm, 10*mm, 49*mm, 4*mm)
            ),
            Table(
                [
                    [
                        Paragraph("Test Data", styles["rc-tdwp-main"]),
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEBELOW", (0, 0), (0, 0), 0.1, "black"),
                ]),
                colWidths=(65*mm, 100*mm)
            ),
            Spacer(0, 9.8 * mm),
            Paragraph(
                "PROBATIONER'S RIGHT TO COUNSEL",
                styles["rc-header"]
            )
        ]
            
        return elems

    def _section_front(self):
        pre_space = "&nbsp;"*11
        elems = [
            Paragraph(
                pre_space + """
                    The Probation Office for the City of Brookhaven (the "City") has filed a petition (the 
                    "Petition") seeking the revocation and/or modification of your probation. As a probationer, you 
                    have the right to be represented by an attorney, either retained or appointed, at the hearing on the 
                    Petition. If you cannot afford to hire an attorney, you have the right to ask the Court to appoint an 
                    attorney to represent you at public expense. If the Court determines (1) that you are unable to 
                    afford an attorney to represent you, <u>and</u> (2) that fundamental fairness (due process) requires it in 
                    your case, the Court will appoint an attorney to represent you at public expense. <b>Notify the judge 
                    if you wish to apply for a Court-appointed attorney to represent you.</b>
                """,
                styles["rc-tdwp-main"]
            ),
            Paragraph(
                pre_space + """
                    If you choose to hire an attorney to represent you or if the Court appoints counsel to 
                    represent you, <b>the hearing on the Petition may be postponed.</b> If you are incarcerated, the judge 
                    will decide whether you remain incarcerated until the hearing or whether you are released from 
                    custody prior to the hearing.
                """,
                styles["rc-tdwp-main"]
            ),
            Paragraph(
                pre_space + """
                    Although you have the right to speak with the City and/or Solicitor about your case, you 
                    are under no obligation to do so. <b>Anything you say to the City and/or Solicitor can be used as 
                    evidence against you.</b> Although you may waive the right to an attorney, it is important that you 
                    be aware that an attorney can help you understand and present:
                """,
                styles["rc-tdwp-main"]
            ),
            Spacer(0, 4.2 * mm),
            Table(
                [
                    [
                        Paragraph("1.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            "The nature of the allegations against you;",
                            styles["rc-tdwp-main-tb"]
                        )
                    ],
                    [
                        Paragraph("2.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            """The range of possible consequences, including for example incarceration, if you are 
                            found to have violated the terms of your probation;""",
                            styles["rc-tdwp-main-tb"]
                        )
                    ],
                    [
                        Paragraph("3.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            "Possible defenses to the allegations against you;",
                            styles["rc-tdwp-main-tb"]
                        )
                    ],
                    [
                        Paragraph("4.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            """Possible mitigating circumstances for the allegations against you, for example 
                            presenting evidence of a financial hardship;""",
                            styles["rc-tdwp-main-tb"]
                        )
                    ],
                    [
                        Paragraph("5.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            "Arguments in favor of alternatives to incarceration;",
                            styles["rc-tdwp-main-tb"]
                        )
                    ],
                    [
                        Paragraph("6.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            "The rights you have to a hearing on the allegations against you;",
                            styles["rc-tdwp-main-tb"]
                        )
                    ],
                    [
                        Paragraph("7.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            """The rights you would have at a hearing on the allegations against you, such as 
                            questioning witnesses, presenting evidence on your behalf, or remaining silent 
                            throughout the hearing;""",
                            styles["rc-tdwp-main-tb"]
                        )
                    ],
                    [
                        Paragraph("8.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            "Certain strategies for defending yourself; and",
                            styles["rc-tdwp-main-tb"]
                        )
                    ],
                    [
                        Paragraph("9.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            "Any other facts necessary for a broad understanding of the matter.",
                            styles["rc-tdwp-main-tb"]
                        )
                    ]
                ],
                colWidths=(23 * mm, 142 * mm),                
                style=(
                    ('VALIGN', (0, 0), (1, 8), 'TOP'),
                    ("LEFTPADDING", (0, 0), (0, 8), 12.5 * mm),
                    ("BOTTOMPADDING", (0, 0), (1, 8), 0.15 * mm),
                    ("TOPPADDING", (0, 0), (1, 8), 0.15 * mm)
                )
            ),
            PageBreak()
        ]

        return elems

    def _section_back(self):
        pre_space = "&nbsp;"*11
        elems = [
            Paragraph(
                pre_space + """
                    The judge cannot assist you in identifying or developing these matters because the judge 
                    must remain impartial between you and the City. The judge cannot assist either side.
                """,
                styles["rc-tdwp-main"]
            ),
            Paragraph(
                pre_space + """
                    If you waive your right to an attorney, you must also understand that during the hearing:
                """,
                styles["rc-tdwp-main"]
            ),
            Spacer(0, 4.2 * mm),
            Table(
                [
                    [
                        Paragraph("1.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            "The rules of evidence will be enforced by the Court;",
                            styles["rc-tdwp-main-tb"]
                        )
                    ],
                    [
                        Paragraph("2.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            """You must make decisions about calling witnesses, questioning witnesses, and what, 
                            if any, evidence you present on your own behalf;""",
                            styles["rc-tdwp-main-tb"]
                        )
                    ],
                    [
                        Paragraph("3.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            "You must decide whether you will testify on your own behalf;",
                            styles["rc-tdwp-main-tb"]
                        )
                    ],
                    [
                        Paragraph("4.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            """You are not required to testify at the hearing, but if you do testify, you would be 
                            placed under oath to tell the truth under the penalty of perjury and you would be 
                            subject to cross examination by the Solicitor;""",
                            styles["rc-tdwp-main-tb"]
                        )
                    ],
                    [
                        Paragraph("5.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            """The City has the burden of proving its allegations against you by a preponderance 
                            of the evidence, in other words that it is more likely than not that you violated the 
                            terms of your probation as alleged in the Petition;""",
                            styles["rc-tdwp-main-tb"]
                        )
                    ],
                    [
                        Paragraph("6.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            """Issues must be properly preserved by timely objections in order to raise them on 
                            appeal if you are dissatisfied with the outcome of the hearing.""",
                            styles["rc-tdwp-main-tb"]
                        )
                    ]
                ],
                colWidths=(23 * mm, 142 * mm),                
                style=(
                    ('VALIGN', (0, 0), (1, 5), 'TOP'),
                    ("LEFTPADDING", (0, 0), (0, 5), 12.5 * mm),
                    ("BOTTOMPADDING", (0, 0), (1, 5), 0.15 * mm),
                    ("TOPPADDING", (0, 0), (1, 5), 0.15 * mm)
                )
            ),
            Paragraph(
                pre_space + """
                    Even if you choose to waive your right to an attorney now, you may be able to change your 
                    mind and obtain an attorney later. But you must act diligently in obtaining an attorney, either 
                    appointed or retained. If you do not act diligently, it is possible that you might later be deemed to 
                    have waived your right to an attorney.
                """,
                styles["rc-tdwp-main"]
            ),
            Paragraph(
                pre_space + """
                    <b>I swear under penalty of perjury that:</b>
                """,
                styles["rc-tdwp-main"]
            ),
            Spacer(0, 4.2 * mm),
            Table(
                [
                    [
                        Paragraph("1.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            "I have thoroughly read and fully understand the above statements;",
                            styles["rc-tdwp-main-tb"]
                        )
                    ],
                    [
                        Paragraph("2.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            """No one has offered me anything, promised me anything, or threatened me in any 
                            way to get me to waive my rights; and""",
                            styles["rc-tdwp-main-tb"]
                        )
                    ],
                    [
                        Paragraph("3.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            """
                            I am not under the influence of alcohol or drugs, and I am not suffering from any 
                            mental or physical disability that would impair my ability to understand what is happening;
                            """,
                            styles["rc-tdwp-main-tb"]
                        )
                    ]
                ],
                colWidths=(23 * mm, 142 * mm),                
                style=(
                    ('VALIGN', (0, 0), (1, 2), 'TOP'),
                    ("LEFTPADDING", (0, 0), (0, 2), 12.5 * mm),
                    ("BOTTOMPADDING", (0, 0), (1, 2), 0.15 * mm),
                    ("TOPPADDING", (0, 0), (1, 2), 0.15 * mm)
                )
            ),
            Paragraph(
                pre_space + """
                    <b>Therefore, <u>I knowingly, intelligently, and voluntarily choose to waive my right to an attorney.</u></b>
                """,
                styles["rc-tdwp-main"]
            ),
            Spacer(0, 8.4 * mm),
            Table(
                [
                    [
                        Paragraph("This", styles["rc-tdwp-main"]),
                        Paragraph("", styles["rc-tdwp-main"]),
                        Paragraph("day of", styles["rc-tdwp-main"]),
                        Paragraph("Test Data", styles["rc-tdwp-main"]),
                        Paragraph(", 20", styles["rc-tdwp-main"]),
                        Paragraph("XX", styles["rc-tdwp-main"]),
                        Paragraph(".", styles["rc-tdwp-main"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEBELOW", (1, 0), (1, 0), 0.1, "black"),
                    ("LINEBELOW", (3, 0), (3, 0), 0.1, "black"),
                    ("LINEBELOW", (5, 0), (5, 0), 0.1, "black")
                ]),
                colWidths=(8*mm, 8*mm, 12*mm, 44*mm, 7*mm, 9*mm, 77*mm)
            ),
            Spacer(0, 18.2 * mm),
            Table(
                [
                    [
                        Paragraph("Probationer", styles["rc-tdwp-main"]),
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEABOVE", (0, 0), (0, 0), 0.1, "black"),
                ]),
                colWidths=(88*mm, 77*mm)
            ),
        ]

        return elems

    def _section_header_sp(self):
        elems = list()
        elems += [
            Spacer(0, 2.4* mm),
            Paragraph(
                "TRIBUNAL MUNICIPAL DE LA CIUDAD DE BROOKHAVEN <br />ESTADO DE GEORGIA",
                extend_style(styles["rc-doc-header"],leading=34)
            ),
            Spacer(0, -2.2 * mm),
            Table(
                [
                    [
                        Paragraph("Ciudad de Brookhaven <br /> &nbsp;", styles["rc-tdwp-main"]),
                        Paragraph("Audiencia de Revocacion/Modificacion de <br />la Libertard Condicional", styles["rc-tdwp-main"])
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
                colWidths=(90*mm, 102*mm)
            ),
            Paragraph("vs.", extend_style(styles["rc-tdwp-main"], spaceBefore=0)),
            Table(
                [
                    [
                        Paragraph("Test Data", styles["rc-tdwp-main"]),
                        None,
                        Paragraph("Fecha:", styles["rc-tdwp-main"]),
                        Paragraph("Test Data", styles["rc-tdwp-main"]),
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (0, 0), (0, 0), 0.1, "black"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEBELOW", (3, 0), (3, 0), 0.1, "black"),
                ]),
                colWidths=(65*mm, 25*mm, 12*mm, 50*mm, 40*mm)
            ),
            Spacer(0, 9.8 * mm),
            Paragraph(
                """DERECHO DE LA PERSONA QUE HA SIDO CONDENADA A UN REGIMEN DE LIBERTAD <br />
                CONDICIONAL A TENER UN ABOGADO
                """,
                styles["rc-header"]
            )
        ]
            
        return elems

    def _section_front_sp(self):
        pre_space = "&nbsp;"*11
        elems = [
            Paragraph(
                pre_space + """
                    La Oficina de Libertad Condicional asignada a la Ciudad de Brookhaven (la "Ciudad") ha presentado una 
                    peticiOn (la "Peticion") por medio de la cual se pide la revocaciOn y/o modificacion de su libertad condicional. 
                    Como individuo que ha sido condenado a un regimen de libertad condicional, Ud. tiene el derecho de ser 
                    representado por medio de un abogado en la audiencia de la Peticion, bien sea contratado o de oficio. Si Ud. 
                    no tiene suficiente dinero para contratar a un abogado, Ud. tiene el derecho de solicitarle al Juez a que le 
                    asigne un abogado de oficio pago por la ciudadania. Si el Juez determina (1) que Ud. no tiene suficiente dinero 
                    para contratar a un abogado que lo represente, y (2) las garantias procesales de su caso meritan que lo tenga, 
                    el Juez le asignard un abogado para que lo represente pago por la ciudadania. <b>Ud. tiene que notificarle al juez si Ud. 
                    desea llenar una solicitud para que le asignen un abogado de oficio.</b>
                """,
                styles["rc-tdwp-main"]
            ),
            Paragraph(
                pre_space + """
                    Si Ud. decide contratar a un abogado para que lo represente, o si el Juez le asigna un abogado de oficio, <b>la audiencia 
                    para tal Petition puede set aplazada.</b> Si Ud. se encuentra encarcelado, el juez va a decidir si Ud. va a seguir 
                    encarcelado hasta tal audiencia o si se le deja en libertad antes de la misma.
                """,
                styles["rc-tdwp-main"]
            ),
            Paragraph(
                pre_space + """
                    A pesar de que Ud. tiene el derecho de hablar con la Ciudad y/o el Fiscal, Ud. no tiene ninguna obligacion de hacerlo. 
                    <b>Cualquier cosy que Ud. le diga a la Ciudad y/o at Fiscal puede ser utilizada como prueba en su contra.</b> Aunque Ud. puede 
                    renunciar al derecho de tener un abogado, es importante que Ud. sepa que un abogado le puede ayudar a entender y a exponer 
                    lo siguiente:
                """,
                styles["rc-tdwp-main"]
            ),
            Spacer(0, 4.2 * mm),
            Table(
                [
                    [
                        Paragraph("1.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            "La naturaleza de los alegatos en su contra;",
                            styles["rc-tdwp-main-tb"]
                        )
                    ],
                    [
                        Paragraph("2.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            """El rango de las consecuencias posibles, incluyendo por ejemplo encarcelamiento, si se 
                            determina que Ud. ha infringido las condiciones de su libertad condicional;""",
                            styles["rc-tdwp-main-tb"]
                        )
                    ],
                    [
                        Paragraph("3.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            "Posibles defensas a los alegatos en su contra;",
                            styles["rc-tdwp-main-tb"]
                        )
                    ],
                    [
                        Paragraph("4.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            """Posibles circunstancias mitigantes de los alegatos en su contra, por ejemplo al presentar 
                            pruebas de dificultades economicas;""",
                            styles["rc-tdwp-main-tb"]
                        )
                    ],
                    [
                        Paragraph("5.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            "Argumentos a favor de alternativas al encarcelamiento;",
                            styles["rc-tdwp-main-tb"]
                        )
                    ],
                    [
                        Paragraph("6.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            "Los derechos que Ud. tiene para poder celebrar una audiencia sobre los alegatos en su contra;",
                            styles["rc-tdwp-main-tb"]
                        )
                    ],
                    [
                        Paragraph("7.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            """Los derechos a los cuales Ud. tendria derecho en una audiencia sobre los alegatos en su contra, 
                            por ejemplo, examen de los testigos, presentar pruebas en su nombre, o el hecho de poder permanecer 
                            en silencio durante la audiencia.""",
                            styles["rc-tdwp-main-tb"]
                        )
                    ],
                    [
                        Paragraph("8.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            "Ciertas estrategias para que Ud. mismo pueda defenderse en su nombre; y",
                            styles["rc-tdwp-main-tb"]
                        )
                    ],
                    [
                        Paragraph("9.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            "Cualesquier otros datos necesarios para tener un amplio entendimiento del asunto.",
                            styles["rc-tdwp-main-tb"]
                        )
                    ]
                ],
                colWidths=(23 * mm, 169 * mm),
                style=(
                    ('VALIGN', (0, 0), (1, 8), 'TOP'),
                    ("LEFTPADDING", (0, 0), (0, 8), 12.5 * mm),
                    ("BOTTOMPADDING", (0, 0), (1, 8), 0.15 * mm),
                    ("TOPPADDING", (0, 0), (1, 8), 0.15 * mm)
                )
            ),
            PageBreak()
        ]

        return elems

    def _section_back_sp(self):
        pre_space = "&nbsp;"*11
        elems = [
            Paragraph(
                pre_space + """
                    El juez no puede ayudarle a tid. el identificar o desarrollar estos asuntos siendo que el juez 
                    debe permanecer imparcial entre Ud. y la. Ciudad. El juez no puede ayudarle a ninguna de las partes.
                """,
                styles["rc-tdwp-main"]
            ),
            Paragraph(
                pre_space + """
                    Si Ud. renuncia al derecho de tener un abogado, Ud. tambien debe entender que durante la audiencia:
                """,
                styles["rc-tdwp-main"]
            ),
            Spacer(0, 4.2 * mm),
            Table(
                [
                    [
                        Paragraph("1.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            "Las normas de admisibilidad de pruebas van a hacerse cumplir por parte del Juez.",
                            styles["rc-tdwp-main-tb"]
                        )
                    ],
                    [
                        Paragraph("2.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            """Ud. debe tomar decisiones acerca de presentar a los testigos, interrogarlos y que tipo de 
                            pruebas -si es que las tiene- va a presentar a su favor;""",
                            styles["rc-tdwp-main-tb"]
                        )
                    ],
                    [
                        Paragraph("3.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            "Ud. debe decidir si va a dar testimonio en su propio nombre o no;",
                            styles["rc-tdwp-main-tb"]
                        )
                    ],
                    [
                        Paragraph("4.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            """Ud. no esta obligado a dar testimonio en la audiencia, pero si lo hace, Ud. tendra que prestar 
                            juramento de tener que decir la verdad bajo pena de perjura y va a ser sujeto a que la Fiscalia le 
                            haga contra-interrogatorio;""",
                            styles["rc-tdwp-main-tb"]
                        )
                    ],
                    [
                        Paragraph("5.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            """La Ciudad tiene la carga de demostrar los alegatos en su contra por preponderancia de la prueba, 
                            en otras palabras, que es mas probable que no lo sea asi, que Ud. incumpliO las condiciones de su libertad 
                            condicional tal y como se alega en la PeticiOn;""",
                            styles["rc-tdwp-main-tb"]
                        )
                    ],
                    [
                        Paragraph("6.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            """Los asuntos se deben asegurar debidamente para poder utilizarlos en proceso de apelacian si Ud. queda 
                            insatisfecho del resultado de la audiencia.""",
                            styles["rc-tdwp-main-tb"]
                        )
                    ]
                ],
                colWidths=(23 * mm, 169 * mm),
                style=(
                    ('VALIGN', (0, 0), (1, 5), 'TOP'),
                    ("LEFTPADDING", (0, 0), (0, 5), 12.5 * mm),
                    ("BOTTOMPADDING", (0, 0), (1, 5), 0.15 * mm),
                    ("TOPPADDING", (0, 0), (1, 5), 0.15 * mm)
                )
            ),
            Paragraph(
                pre_space + """
                    Aunque Ud. decida renunciar a su derecho de tener abogado ahora mismo, es posible que Ud. pueda cambiar de opinion y consiga 
                    un abogado posteriormente. Pero Ud. debe actuar de una manera diligente para conseguir a un abogado, Bien sea contratado, 
                    o de oficio. Si Ud. no act-Cm de manera diligente, es posible que a Ud. se le considere posteriormente como si hubiera 
                    renunciado a su derecho de tener abogado.
                """,
                styles["rc-tdwp-main"]
            ),
            Paragraph(
                pre_space + """
                    <b>Yo juro bajo pena de perjura que:</b>
                """,
                styles["rc-tdwp-main"]
            ),
            Spacer(0, 4.2 * mm),
            Table(
                [
                    [
                        Paragraph("1.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            "He leido y entiendo en su totalidad todas las declaraciones anteriores;",
                            styles["rc-tdwp-main-tb"]
                        )
                    ],
                    [
                        Paragraph("2.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            """Nadie me ha ofrecido nada, prometido nada, a amenazado de ninguna forma para que yo renuncie a mis derechos, y""",
                            styles["rc-tdwp-main-tb"]
                        )
                    ],
                    [
                        Paragraph("3.", extend_style(styles["rc-tdwp-main-tb"])),
                        Paragraph(
                            """
                            No me encuentro bajo los efectos del alcohol, o estupefacientes y no sufro de ninguna discapacidad mental o 
                            fisica que me impida poder entender lo que esta ocurriendo;
                            """,
                            styles["rc-tdwp-main-tb"]
                        )
                    ]
                ],
                colWidths=(23 * mm, 169 * mm),
                style=(
                    ('VALIGN', (0, 0), (1, 2), 'TOP'),
                    ("LEFTPADDING", (0, 0), (0, 2), 12.5 * mm),
                    ("BOTTOMPADDING", (0, 0), (1, 2), 0.15 * mm),
                    ("TOPPADDING", (0, 0), (1, 2), 0.15 * mm)
                )
            ),
            Paragraph(
                pre_space + """
                    <b>Por lo tanto, <u>Yo decido renunciar a sabiendas, inteligentemente v voluntariamente a mi derecho de tener un abogado.</u></b>
                """,
                styles["rc-tdwp-main"]
            ),
            Spacer(0, 8.4 * mm),
            Table(
                [
                    [
                        Paragraph("El dia", styles["rc-tdwp-main"]),
                        Paragraph("", styles["rc-tdwp-main"]),
                        Paragraph("del mes de", styles["rc-tdwp-main"]),
                        Paragraph("Test Data", styles["rc-tdwp-main"]),
                        Paragraph(", 20", styles["rc-tdwp-main"]),
                        Paragraph("XX", styles["rc-tdwp-main"]),
                        Paragraph(".", styles["rc-tdwp-main"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEBELOW", (1, 0), (1, 0), 0.1, "black"),
                    ("LINEBELOW", (3, 0), (3, 0), 0.1, "black"),
                    ("LINEBELOW", (5, 0), (5, 0), 0.1, "black")
                ]),
                colWidths=(12*mm, 8*mm, 19*mm, 44*mm, 7*mm, 9*mm, 93*mm)
            ),
            Spacer(0, 10.2 * mm),
            Table(
                [
                    [
                        Paragraph("Persona que ha sido condenada a un regimen de libertad condicional", styles["rc-tdwp-main"]),
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEABOVE", (0, 0), (0, 0), 0.1, "black"),
                ]),
                colWidths=(116*mm, 76*mm)
            )
        ]

        return elems
        
