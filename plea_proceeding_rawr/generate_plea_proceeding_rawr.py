# coding=utf-8
import cStringIO

from document_specific_styles import *
from common.signatures import *
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT


def generate_plea_proceeding_rawr():
    cr = PPRReport()
    buff = cStringIO.StringIO()
    return cr.create_report(buff)

class PPRReport:
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
            Spacer(0, 10.6 * mm),
            Paragraph(
                "In the Municipal Court of Brookhaven <br />State of Georgia",
                styles["rc-header"]
            ),
            Spacer(0, 5.4 * mm),
            Table(
                [
                    [
                        Paragraph("CITY OF BROOKHAVEN", styles["rc-aawp-main-content"]),
                        Paragraph("CASE #", styles["rc-aawp-main-content"]),
                        Paragraph("Test Data", styles["rc-aawp-main-content"]),
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (2, 0), (2, 0), 0.1, "black"),
                ]),
                colWidths=(80*mm, 13*mm, 48*mm, 5*mm),
            ),            
            Table(
                [
                    [
                        Paragraph("Vs.", extend_style(styles["rc-aawp-main-content"], leftIndent=18*mm)), 
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (2, 0), (2, 0), 0.1, "black"),
                ]),
                colWidths=(75*mm, 76*mm),
            ),
            Spacer(0, 3.2*mm),
            Table(
                [
                    [
                        Paragraph("Test Data", extend_style(styles["rc-aawp-main-content"])),
                        None,
                    ],
                    [
                        Paragraph("Name", extend_style(styles["rc-aawp-main-content"])),
                        None,
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (0, 0), (0, 0), 0.1, "black")
                ]),
                colWidths=(50*mm, 112*mm),
            ),  
            Spacer(0, 6.4*mm),
            Paragraph("<u>PLEA PROCEEDING RECORD, ACKNOWLEDGEMENT AND WAIVER OF RIGHTS</u>", extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)),
            Paragraph(
                """
                I, the Defendant, acknowledge by the signing of this document and by entering a plea of GUILTY <u>Test Data</u> or 
                NOLO CONTENDERE <u>Test Data</u> to the charges against me that I:
                """,
                extend_style(styles["rc-aawp-main-content"])
            )
        ]
        text_list = [
            'Understand the nature of the charges;',
            'Give up the right to a trial by jury:',
            'Give up the presumption of innocence until proven guilty beyond a reasonable doubt;',
            'Give up the right to ask questions of those witnesses against me;',
            'Give up the right to subpoena witnesses to testify on my behalf, if I want them, and have the Court make them appear;',
            'Give up the right to testify in a trial and to offer other evidence;',
            'Give up the right to help of an attorney at trial;',
            'Give up the right to remain silent, and not to testify against myself, and, if I plead not guilty or remain silent, I would receive a trial by jury or judge;',
            'Acknowledge that this plea is entered into freely, voluntarily, and understandingly by me, and that no person has made any promise or threat to me to influence my decision to plead;',
            'Acknowledge that the plea of Guilty or Nolo Contendere has a factual basis, and the presentation to the Court is true;',
            'Realize that each charge or ticket received could result in the Judge sentencing me to a fine of up to $1,000 and up to 12 months in jail, but that is not necessarily the sentence that I would receive. (SEE EXCEPTIONS BELOW);',
            'Realize that if the charge or ticket received is for a second offense or more in five(5) years for driving without a license or driving while license suspended or revoked, it could result in the Judge sentencing me to a fine of up to $2,500 and up to 12 months in jail;',
            'Realize that if the charge or ticket received is for a third offense or more in ten (10) years for driving under the influence, it could result in the Judge sentencing me to a fine of up to $5,000 and up to 12 months in jail;',
            'Understand that if I am not a citizen of the United States, my plea of guilty or nolo contendre may have an impact on my immigration status.'
        ]
        table1 = []
        for idx, text in enumerate(text_list):
            table1.append(
                [   
                    None,
                    Paragraph('{})'.format(idx+1), styles["rc-aawp-main-content"]),
                    Paragraph(text, styles["rc-aawp-main-content"])
                ]
            )

        elems +=[
            Spacer(0, 4.8*mm),
            Table(
                table1,
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
                colWidths=(5*mm, 6*mm, 151*mm),
            ),
            Spacer(0, 6.8*mm),
            Table(
                [
                    [                        
                        Paragraph("", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("Test Data", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("Test Data", styles["rc-aawp-main-content"]),
                    ],
                    [                        
                        Paragraph("Defendant", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("Attorney", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("Date", styles["rc-aawp-main-content"]),
                    ],
                    [                        
                        Paragraph("", styles["rc-aawp-main-content"]),
                        None,
                        Table(
                            [
                                [
                                    Paragraph("Bar No.", styles["rc-aawp-main-content"]),
                                    Paragraph("Test Data", styles["rc-aawp-main-content"]),
                                ]
                            ],
                            style=extend_table_style(styles["rc-main-table"], [
                                ("LINEBELOW", (1, 0), (1, 0), 0.1, "black")                                
                            ]),
                            colWidths=(12*mm, 44*mm),
                        ),
                        None,
                        Paragraph("", styles["rc-aawp-main-content"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (0, 0), (0, 0), 0.1, "black"),
                    ("LINEBELOW", (2, 0), (2, 0), 0.1, "black"),
                    ("LINEBELOW", (4, 0), (4, 0), 0.1, "black")
                ]),
                colWidths=(60*mm, 8*mm, 56*mm, 8*mm, 30*mm),
            ),
            Paragraph(
                """
                I hereby certify that I have made an inquiry and am satisfied that there is factual basis 
                to support this Defendant's plea of Guilty or Nolo Contendere and that the Plea is knowingly, 
                freely, and voluntarily made by the Defendant, and that no promise, threat or force was used 
                to induce the Defendant to enter this plea.
                """, 
                extend_style(styles["rc-aawp-main-content"], spaceBefore=14)
            ),
            Spacer(0, 12.4*mm),
            Table(
                [
                    [
                        Paragraph("This", styles["rc-aawp-main-content"]),
                        Paragraph("", styles["rc-aawp-main-content"]),
                        Paragraph(" &nbsp;day of", styles["rc-aawp-main-content"]),
                        Paragraph("Test Data", styles["rc-aawp-main-content"]),
                        Paragraph(", 20", styles["rc-aawp-main-content"]),
                        Paragraph("XX", styles["rc-aawp-main-content"]),
                        Paragraph(".", styles["rc-aawp-main-content"]),
                        Paragraph("Test Data", styles["rc-aawp-main-content"])
                    ],
                    [
                        None, None, None, None, None, None, None,
                        Paragraph("Judge, Municipal Court of Brookhaven", styles["rc-aawp-main-content"])
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (1, 0), (1, 0), 0.1, "black"),
                    ("LINEBELOW", (3, 0), (3, 0), 0.1, "black"),
                    ("LINEBELOW", (5, 0), (5, 0), 0.1, "black"),
                    ("LINEBELOW", (7, 0), (7, 0), 0.1, "black")
                ]),
                colWidths=(8*mm, 13*mm, 12*mm, 28*mm, 6*mm, 6*mm, 6*mm, 84*mm),
            ),
            Spacer(0, 20.4 * mm),
            Paragraph("JAN, 2019", extend_style(styles["rc-aawp-main-content"], fontSize=5.5, spaceBefore=10))
        ]
        
        return elems

    def _section_content_sp(self):
        pre_space = "&nbsp;"*12
        elems = list()
        elems += [
            Spacer(0, 10.6 * mm),
            Paragraph(
                "En el Tribunal Municipal de Brookhaven <br />Estado de Georgia",
                styles["rc-header"]
            ),
            Spacer(0, 5.4 * mm),
            Table(
                [
                    [
                        Paragraph("CIUDAD DE BROOKHAVEN", styles["rc-aawp-main-content"]),
                        Paragraph("NO. DEL CASO:", styles["rc-aawp-main-content"]),
                        Paragraph("Test Data", styles["rc-aawp-main-content"])
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (2, 0), (2, 0), 0.1, "black"),
                ]),
                colWidths=(94*mm, 28*mm, 40*mm),
            ),            
            Table(
                [
                    [
                        Paragraph("Vs.", extend_style(styles["rc-aawp-main-content"], leftIndent=18*mm)), 
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (2, 0), (2, 0), 0.1, "black"),
                ]),
                colWidths=(75*mm, 84*mm),
            ),
            Spacer(0, 3.2*mm),
            Table(
                [
                    [
                        Paragraph("Test Data", extend_style(styles["rc-aawp-main-content"])),
                        None,
                    ],
                    [
                        Paragraph("Nombre del Acusado", extend_style(styles["rc-aawp-main-content"])),
                        None,
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (0, 0), (0, 0), 0.1, "black")
                ]),
                colWidths=(50*mm, 112*mm),
            ),  
            Spacer(0, 1.8*mm),
            Paragraph("<u>ACTA DE DECLARATORIA, RECONOCIMIENTO Y RENUNCIA DE DERECHOS</u>", extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)),
            Paragraph(
                """
                Yo, el ACUSADO, reconozco mediante la firma de este documento y al declararme CULPABLE <u>Test Data</u> o
                NOLO CONTENDERE (no lo disputo) <u>Test Data</u> a los cargos en contra mía, que;
                """,
                extend_style(styles["rc-aawp-main-content"])
            )
        ]
        text_list = [
            'Entiendo la naturaleza de los cargos de que se me acusa;',
            'Renuncio al derecho a juicio con jurado;',
            'Renuncio a la presunción de inocencia hasta demostrar que soy culpable fuera de una duda razonable;',
            'Renuncio al derecho a hacer preguntas a los testigos que declaren en mi contra;',
            'Renuncio al derecho a citar a testigos para que declaren a mi favor, si así lo deseo, y a que el Tribunal los haga comparecer;',
            'Renuncio al derecho a declarar durante el juicio y a ofrecer otras pruebas;',
            'Renuncio al derecho a contar con la ayuda de un abogado durante el juicio;',
            'Renuncio al derecho a permanecer en silencio y a no declarar en mi contra, y si me declaro inocente o permanezco en silencio, se me enjuiciaría con jurado o por juez;',
            'Reconozco que hago esta declaración libre y voluntariamente de mi parte, que la entiendo y que ninguna persona me ha hecho promesa alguna o me ha amenazado para influir mi decisión de declararme;',
            'Reconozco que la declaración de Culpable o Nolo Contendere tiene bases de hecho y que la presentación ante el Tribunal es verdadera;',
            'Entiendo que por cada uno de los cargos presentados en contra mía o las infracciones recibidas pudieran dar como resultado que el Juez me sentenciase a pagar hasta $1.000 de multa y hasta 12 meses de cárcel, pero que esa no es necesariamente la sentencia que se me va a imponer (VER LAS EXCEPCIONES SIGUIENTES);',
            'Entiendo que si el cargo presentado o la infracción recibida es por un segundo delito o más por conducir sin licencia en un periodo de cinco (5) años, o por conducir mientras que mi licencia esté suspendida o haya sido revocada, ello pudiera dar como resultado que el Juez me sentenciase a una multa de hasta $2.500 y hasta 12 meses de cárcel;',
            'Entiendo que si el cargo presentado o la infracción recibida es por un tercer delito o más por conducir bajo la influencia en diez (10) años, ello pudiera dar como resultado que el Juez me sentenciase a una multa de hasta $5.000 y hasta 12 meses de cárcel;',
            'Entiendo que si no soy un ciudadano estadounidense, mi declaración de Culpable o Nolo Contendere puede afectar mi estado migratorio.'
        ]
        table1 = []
        for idx, text in enumerate(text_list):
            table1.append(
                [   
                    None,
                    Paragraph('{})'.format(idx+1), styles["rc-aawp-main-content"]),
                    Paragraph(text, styles["rc-aawp-main-content"])
                ]
            )

        elems +=[
            Spacer(0, 1.8*mm),
            Table(
                table1,
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
                colWidths=(5*mm, 6*mm, 151*mm),
            ),
            Spacer(0, 6.8*mm),
            Table(
                [
                    [                        
                        Paragraph("", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("Test Data", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("Test Data", styles["rc-aawp-main-content"]),
                    ],
                    [                        
                        Paragraph("Firma del Acusado", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("Firma del Abogado", styles["rc-aawp-main-content"]),
                        None,
                        Paragraph("Fecha", styles["rc-aawp-main-content"]),
                    ],
                    [                        
                        Paragraph("", styles["rc-aawp-main-content"]),
                        None,
                        Table(
                            [
                                [
                                    Paragraph("Matrícula No.", styles["rc-aawp-main-content"]),
                                    Paragraph("Test Data", styles["rc-aawp-main-content"]),
                                ]
                            ],
                            style=extend_table_style(styles["rc-main-table"], [
                                ("LINEBELOW", (1, 0), (1, 0), 0.1, "black")                                
                            ]),
                            colWidths=(22*mm, 34*mm),
                        ),
                        None,
                        Paragraph("", styles["rc-aawp-main-content"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (0, 0), (0, 0), 0.1, "black"),
                    ("LINEBELOW", (2, 0), (2, 0), 0.1, "black"),
                    ("LINEBELOW", (4, 0), (4, 0), 0.1, "black")
                ]),
                colWidths=(60*mm, 8*mm, 56*mm, 8*mm, 30*mm),
            ),
            Paragraph(
                """
                I hereby certify that I have made an inquiry and am satisfied that there is factual basis to 
                support this Defendant's plea of Guilty or Nolo Contendere and that the Plea is knowingly, freely, 
                and voluntarily made by the Defendant, and that no promise, threat or force was used to induce 
                the Defendant to enter this plea.
                """, 
                extend_style(styles["rc-aawp-main-content"], spaceBefore=16)
            ),
            Spacer(0, 12.4*mm),
            Table(
                [
                    [
                        Paragraph("This", styles["rc-aawp-main-content"]),
                        Paragraph("", styles["rc-aawp-main-content"]),
                        Paragraph(" &nbsp;day of", styles["rc-aawp-main-content"]),
                        Paragraph("Test Data", styles["rc-aawp-main-content"]),
                        Paragraph(", 20", styles["rc-aawp-main-content"]),
                        Paragraph("XX", styles["rc-aawp-main-content"]),
                        Paragraph(".", styles["rc-aawp-main-content"]),
                        Paragraph("Test Data", styles["rc-aawp-main-content"])
                    ],
                    [
                        None, None, None, None, None, None, None,
                        Paragraph("Judge, Municipal Court of Brookhaven", styles["rc-aawp-main-content"])
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (1, 0), (1, 0), 0.1, "black"),
                    ("LINEBELOW", (3, 0), (3, 0), 0.1, "black"),
                    ("LINEBELOW", (5, 0), (5, 0), 0.1, "black"),
                    ("LINEBELOW", (7, 0), (7, 0), 0.1, "black")
                ]),
                colWidths=(8*mm, 13*mm, 12*mm, 28*mm, 6*mm, 6*mm, 6*mm, 84*mm),
            ),
            Spacer(0, 15.4 * mm),
            Paragraph("FEB, 2019", extend_style(styles["rc-aawp-main-content"], fontSize=5.5, spaceBefore=10))
        ]
        
        return elems