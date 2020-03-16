import cStringIO

from document_specific_styles import *
from common.signatures import *
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Flowable, Paragraph, Table, Spacer

def generate_application_for_aoc():
    cr = AAOCReport()
    buff = cStringIO.StringIO()
    return cr.create_report(buff)

class AAOCReport:
    def __init__(self, title=None, author=None):
        self.page_size = letter
        self.page_margin = (26.4 * mm, 8.4 * mm)
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
            page_num.wrapOn(canv, self.page_size[0]-22.4*mm, 0)
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
        TEST_DATA = "&nbsp;"*10 + "Test Data" + "&nbsp;"*10
        TEST_DATA_S = "&nbsp;"*4 + "Test Data" + "&nbsp;"*4
        elems = list()
        elems += [
            Spacer(0, 18.6 * mm),
            Paragraph(
                "IN THE MUNICIPAL COURT OF THE CITY OF BROOKHAVEN <br />STATE OF GEORGIA",
                styles["rc-header"]
            ),
            Spacer(0, 5.4 * mm),
            Table(
                [
                    [
                        Paragraph("CITY OF BROOKHAVEN", styles["rc-aawp-main-content"]),
                        Paragraph("Application number:", styles["rc-aawp-main-content"])
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [                    
                ]),
                colWidths=(86*mm, 77*mm)
            ),
            Table(
                [                    
                    [
                        None,
                        Paragraph("CASE NO.", styles["rc-aawp-main-content"]),
                        Paragraph("Test Data", styles["rc-aawp-main-content"]),                        
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (2, 0), (2, 0), 0.1, "black"),
                ]),
                colWidths=(89*mm, 18*mm, 26*mm, 30*mm)
            ),
            Table(
                [
                    [
                        Paragraph("V", extend_style(styles["rc-aawp-main-content"], leftIndent=18*mm)), 
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (2, 0), (2, 0), 0.1, "black"),
                ]),                
            ),
            Table(
                [                    
                    [
                        None,
                        Paragraph("CHARGES", styles["rc-aawp-main-content"]),
                        Paragraph("Test Data", styles["rc-aawp-main-content"]),                        
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (2, 0), (2, 0), 0.1, "black"),
                ]),
                colWidths=(89*mm, 19*mm, 30*mm, 25*mm)
            ),            
            Table(
                [
                    [
                        Paragraph("Test Data", extend_style(styles["rc-aawp-main-content"])),
                        None,
                        Paragraph("Test Data", extend_style(styles["rc-aawp-main-content"])),
                        None,
                    ]                    
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (0, 0), (0, 0), 0.1, "black"),
                    ("LINEBELOW", (2, 0), (2, 0), 0.1, "black")
                ]),
                colWidths=(50*mm, 39*mm, 50*mm, 24*mm)
            ),
            Spacer(0, 5.8*mm),
            Table(
                [
                    [
                        Paragraph("In Jail", extend_style(styles["rc-aawp-main-content"])),
                        Paragraph("Test Data", extend_style(styles["rc-aawp-main-content"])),
                        None,
                        Paragraph("Arrest Date", extend_style(styles["rc-aawp-main-content"])),
                        Paragraph("Test Data", extend_style(styles["rc-aawp-main-content"])),
                        None,
                    ]                    
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (1, 0), (1, 0), 0.1, "black"),
                    ("LINEBELOW", (4, 0), (4, 0), 0.1, "black")
                ]),
                colWidths=(10*mm, 24*mm, 30*mm, 18*mm, 28*mm, 53*mm)
            ),  
            Spacer(0, 2*mm),
            Paragraph(
                "APPLICATION FOR APPOINTMENT OF COUNSEL AND CERTIFICATE OF <br />FINANCIAL RESOURCES", 
                extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)),
            Spacer(0, 6.2*mm),
            Paragraph(
                """
                I am the defendant in the above—styled action. I am charged with the offense(s) of <br />
                <u>{}</u>,
                which is I are a misdemeanor. I can I cannot afford to hire a lawyer to assist me. I do / 
                do not want the court to determine my eligibility for a Court-Appointed lawyer to defend 
                me on the above charges.
                """.format(TEST_DATA),
                extend_style(styles["rc-aawp-main-content"], leading=18)
            ),
        ]
        table_list_front = [
            Table(
                [
                    [
                        Paragraph(
                            "Name <u>{}</u> Phone No. <u>{}</u>".format(TEST_DATA, TEST_DATA), 
                            styles["rc-aawp-main-content-tb"])
                    ],[
                        Paragraph(
                            "Mailing Address <u>{}</u>".format(TEST_DATA, TEST_DATA), 
                            styles["rc-aawp-main-content-tb"])
                    ],[
                        Paragraph(
                            "Birth Date <u>{}</u> Age <u>{}</u> SS No. <u>{}</u>-<u>{}</u>-<u>{}</u>".format(TEST_DATA_S, TEST_DATA_S, TEST_DATA_S, TEST_DATA_S, TEST_DATA_S), 
                            styles["rc-aawp-main-content-tb"])
                    ],[
                        Paragraph(
                            "Highest grade completed in school <u>{}</u> Sex <u>{}</u> Race <u>{}</u>".format(TEST_DATA_S, TEST_DATA_S, TEST_DATA_S), 
                            styles["rc-aawp-main-content-tb"])
                    ],[
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")                    
                ]),
            ),            
            Table(
                [
                    [
                        Paragraph(
                            """Secondary contact: Name <u>{}</u> Phone No. <u>{}</u>""".format(TEST_DATA, TEST_DATA), 
                            styles["rc-aawp-main-content-tb"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
            ),
            Table(
                [
                    [
                        Paragraph(
                            """If employed, name of company <u>{}</u> City / State <u>{}</u>""".format(TEST_DATA, TEST_DATA), 
                            styles["rc-aawp-main-content-tb"]),
                    ],
                    [
                        Paragraph(
                            """
                            a. &nbsp; Net take home pay is (gross pay minus state, federal and social security taxes) <br />
                            <u>{}</u> (weekly) $ <u>{}</u> (monthly)
                            """.format(TEST_DATA, TEST_DATA), 
                            extend_style(styles["rc-aawp-main-content-tb"], leftIndent=16)),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
            ),
            Table(
                [
                    [
                        Paragraph(
                            """If employed, how long? <u>{}</u> List other sources of income such as 
                            unemployment compensation, welfare or disability income and the amounts received per week or month
                            <u>{}</u>.""".format(TEST_DATA, TEST_DATA), 
                            styles["rc-aawp-main-content-tb"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
            ),
            Table(
                [
                    [
                        Paragraph(
                            """Are you married? <u>{}</u>. Is your spouse employed? <u>{}</u>.""".format(TEST_DATA_S, TEST_DATA_S), 
                            styles["rc-aawp-main-content-tb"]),
                    ],
                    [
                        Paragraph(
                            """If so, by whom? <u>{}</u>.""".format(TEST_DATA, TEST_DATA), 
                            styles["rc-aawp-main-content-tb"]),
                    ],
                    [
                        Paragraph(
                            """Spouse's net income $ <u>{}</u>. (week) $ <u>{}</u>. (Bi-weekly)""".format(TEST_DATA_S, TEST_DATA_S), 
                            styles["rc-aawp-main-content-tb"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
            ),
            Table(
                [
                    [
                        Paragraph(
                            """Number of children living in home <u>{}</u> Ages <u>{}</u>""".format(TEST_DATA_S, TEST_DATA), 
                            styles["rc-aawp-main-content-tb"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
            ),
            Table(
                [
                    [
                        Paragraph(
                            """Dependants other than spouse or children in your home (names, relationship and amount contributed to support)""", 
                            styles["rc-aawp-main-content-tb"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]),
            )
        ]

        table_list_back = [
            Table(
                [
                    [
                        Paragraph(
                            """Do you own or arc purchasing a motor vehicle? Yes / No. Year and model<u>{}</u>""".format(TEST_DATA), 
                            styles["rc-aawp-main-content-tb"]),
                    ],
                    [
                        Paragraph(
                            """How much do you owe on it? <u>{}</u>""".format(TEST_DATA), 
                            styles["rc-aawp-main-content-tb"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
            ),
            Table(
                [
                    [
                        Paragraph(
                            """Do you own a home? Yes / No. Value $ <u>{}</u> Amount owed on it $ <u>{}</u>""".format(TEST_DATA_S, TEST_DATA_S), 
                            styles["rc-aawp-main-content-tb"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
            ),
            Table(
                [
                    [
                        Paragraph(
                            """Amount of mortgage or rent payment per month S<u>{}</u>""".format(TEST_DATA), 
                            styles["rc-aawp-main-content-tb"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
            ),
            Table(
                [
                    [
                        Paragraph(
                            """List checking, savings or other deposit accounts with any bank or financial institutions and the amount in each account:""", 
                            styles["rc-aawp-main-content-tb"]),
                    ],
                    [
                        Table(
                            [
                                [
                                    Paragraph("", styles["rc-aawp-main-content-tb"]),
                                    Paragraph("Amount", extend_style(styles["rc-aawp-main-content-tb"], leftIndent=20)), None,
                                    Paragraph("Banking institution", extend_style(styles["rc-aawp-main-content-tb"], leftIndent=20))
                                ],
                                [
                                    Paragraph("Checking: $", extend_style(styles["rc-aawp-main-content-tb"], leading=13)),
                                    Paragraph("Test Data", extend_style(styles["rc-aawp-main-content-tb"], leading=13)), None,
                                    Paragraph("Test Data", extend_style(styles["rc-aawp-main-content-tb"], leading=13))
                                ],
                                [
                                    Paragraph("Savings: &nbsp;&nbsp;$", extend_style(styles["rc-aawp-main-content-tb"], leading=13)),
                                    Paragraph("Test Data", extend_style(styles["rc-aawp-main-content-tb"], leading=13)), None,
                                    Paragraph("Test Data", extend_style(styles["rc-aawp-main-content-tb"], leading=13))
                                ],
                                [
                                    Paragraph("Other: &nbsp;&nbsp;&nbsp;&nbsp; $", extend_style(styles["rc-aawp-main-content-tb"], leading=13)),
                                    Paragraph("Test Data", extend_style(styles["rc-aawp-main-content-tb"], leading=13)), None,
                                    Paragraph("Test Data", extend_style(styles["rc-aawp-main-content-tb"], leading=13))
                                ],
                                [
                                    None, None, None, None
                                ]
                            ],
                            style=extend_table_style(styles["rc-main-table"], [
                                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                ("LINEBELOW", (1, 1), (1, 1), 0.1, "black"),
                                ("LINEBELOW", (3, 1), (3, 1), 0.1, "black"),
                                ("LINEBELOW", (1, 2), (1, 2), 0.1, "black"),
                                ("LINEBELOW", (3, 2), (3, 2), 0.1, "black"),
                                ("LINEBELOW", (1, 3), (1, 3), 0.1, "black"),
                                ("LINEBELOW", (3, 3), (3, 3), 0.1, "black"),
                                ("TOPPADDING", (0, 2), (-1, -2), 2.4 * mm),
                            ]),
                            colWidths=(19*mm, 48*mm, 3*mm, 48*mm)
                        ),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
            ),
            Table(
                [
                    [
                        Paragraph(
                            """List any other assets or property; including real estate, jewelry, notes, bonds or stocks?""".format(TEST_DATA, TEST_DATA), 
                            styles["rc-aawp-main-content-tb"]),
                    ],
                    [
                        Paragraph("Test Data", extend_style(styles["rc-aawp-main-content-tb"], leading=13))
                    ],
                    [
                        Paragraph("Test Data", extend_style(styles["rc-aawp-main-content-tb"], leading=13))
                    ],
                    [ None ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEBELOW", (0, 1), (0, 1), 0.1, "black"),
                    ("LINEBELOW", (0, 2), (0, 2), 0.1, "black"),                    
                    ("TOPPADDING", (0, 2), (0, 2), 2.4 * mm),
                ]),
            ),
            Table(
                [
                    [
                        Paragraph(
                            """List indebtedness and amount of payments<u>{}</u>""".format(TEST_DATA), 
                            styles["rc-aawp-main-content-tb"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
            ),
            Table(
                [
                    [
                        Paragraph(
                            """List any extraordinary living expenses and amount (such as regularly occurring medical bills)""", 
                            styles["rc-aawp-main-content-tb"]),
                    ],
                    [
                        Paragraph("Test Data", extend_style(styles["rc-aawp-main-content-tb"], leading=13))
                    ],
                    [
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEBELOW", (0, 1), (0, 1), 0.1, "black"),                    
                ]),
            ),
            Table(
                [
                    [
                        Paragraph(
                            """Child support payable under any court order<u>{}</u>""".format(TEST_DATA), 
                            styles["rc-aawp-main-content-tb"]),
                    ],
                    [
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
            ),
            Table(
                [
                    [
                        Paragraph(
                            """***Do you understand that whether you are convicted or acquitted, the City Of Brookhaven may seek 
                                reimbursement of attorney's fees paid for you if you become financially able to pay or reimburse the city?
                                <u>{}</u>(defendant's initials) <br />
                                I have read (had read to me) the above questions and answers, and they are correct and true.
                                The undersigned swears that the information given herein is true and correct and understands that a 
                                false answer to any item may result in a charge of perjury.
                            """.format(TEST_DATA_S), 
                            styles["rc-aawp-main-content-tb"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
            )
        ]
        table_front = []
        for idx, sub_table in enumerate(table_list_front):
            table_front.append(
                [   
                    None,
                    Paragraph('{}.'.format(idx+1), styles["rc-aawp-main-content"]),
                    sub_table
                ]
            )
        table_back = []
        table_back.append(
            [
                None, 
                None,
                Table(
                    [
                        [
                            Paragraph("Test Data", extend_style(styles["rc-aawp-main-content-tb"], leading=13))
                        ],
                        [
                            Paragraph("Test Data", extend_style(styles["rc-aawp-main-content-tb"], leading=13))
                        ],
                        [
                            None
                        ]
                    ],
                    style=extend_table_style(styles["rc-main-table"], [
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("LINEBELOW", (0, 0), (0, 0), 0.1, "black"),
                        ("LINEBELOW", (0, 1), (0, 1), 0.1, "black"),
                        ("TOPPADDING", (0, 1), (0, 1), 2.4 * mm),
                    ]),
                )
            ]
        )
        for idx, sub_table in enumerate(table_list_back):
            table_back.append(
                [   
                    None,
                    Paragraph('{}.'.format(idx+8), styles["rc-aawp-main-content"]),
                    sub_table
                ]
            )

        elems +=[
            Spacer(0, 4.8*mm),
            Table(
                table_front,
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
                colWidths=(6*mm, 6*mm, 151*mm),
            ),
            PageBreak(),
            Spacer(0, 14.6*mm),
            Table(
                table_back,
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
                colWidths=(6*mm, 6*mm, 151*mm),
            ),
            Spacer(0, 3.2*mm),
            Paragraph(
                "This <u> Test Data </u> day of<u> Test Data </u>200<u> Test Data</u>.", 
                extend_style(styles["rc-aawp-main-content-tb"], leftIndent=35)
            ),
            Spacer(0, 6.4*mm),
            Table(
                [                    
                    [   None,
                        Paragraph("Defendants Signature", styles["rc-aawp-main-content"]),
                        None
                    ]                    
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEABOVE", (1, 0), (1, 0), 0.1, "black"),
                    ("TOPPADDING", (0, 0), (-1, -1), 1.4 * mm),
                ]),
                colWidths=(75*mm, 78*mm, 10*mm)
            ),
            Paragraph(
                """
                Interview performed by: <u>{}</u>
                Date: <u>{}</u>""".format(TEST_DATA, TEST_DATA), 
                extend_style(styles["rc-aawp-main-content-tb"], spaceBefore=24, leftIndent=22)
            ),
            Spacer(0, 6.4*mm),
            Table(
                [                    
                    [   
                        None,
                        XBox(8, True),
                        Paragraph("APPROVED", extend_style(styles["rc-aawp-main-content"], leading=11)),
                        None,
                        XBox(8),
                        Paragraph("DENIED", extend_style(styles["rc-aawp-main-content"], leading=11)),
                        None
                    ]                    
                ],
                style=extend_table_style(styles["rc-main-table"], [
                ]),
                colWidths=(45*mm, 4*mm, 22*mm, 18*mm, 4*mm, 16*mm, 30*mm)
            ),
        ]
        
        return elems

    def _section_content_sp(self):        
        TEST_DATA = "&nbsp;"*10 + "Test Data" + "&nbsp;"*10
        TEST_DATA_S = "&nbsp;"*4 + "Test Data" + "&nbsp;"*4
        elems = list()
        elems += [
            PageBreak(),
            Spacer(0, 10.6 * mm),
            Paragraph(
                "En el Tribunal Municipal de la Ciudad de Brookhaven <br />Estado de Georgia",
                extend_style(styles["rc-header"], leading=24)
            ),
            Spacer(0, 7.2 * mm),
            Table(
                [
                    [
                        Paragraph("CIUDAD DE BROOKHAVEN", styles["rc-aawp-main-content"]),
                        Paragraph("Solicitud No.:", styles["rc-aawp-main-content"])
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [                    
                ]),
                colWidths=(86*mm, 77*mm)
            ),
            Table(
                [                    
                    [
                        None,
                        Paragraph("CASO NO.:", styles["rc-aawp-main-content"]),
                        Paragraph("Test Data", styles["rc-aawp-main-content"]),                        
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (2, 0), (2, 0), 0.1, "black"),
                ]),
                colWidths=(89*mm, 20*mm, 26*mm, 28*mm)
            ),
            Table(
                [
                    [
                        Paragraph("V", extend_style(styles["rc-aawp-main-content"], leftIndent=18*mm)), 
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (2, 0), (2, 0), 0.1, "black"),
                ]),                
            ),
            Table(
                [                    
                    [
                        None,
                        Paragraph("CARGO(S):", styles["rc-aawp-main-content"]),
                        Paragraph("Test Data", styles["rc-aawp-main-content"]),                        
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (2, 0), (2, 0), 0.1, "black"),
                ]),
                colWidths=(89*mm, 21*mm, 30*mm, 23*mm)
            ),            
            Table(
                [
                    [
                        Paragraph("Test Data", extend_style(styles["rc-aawp-main-content"])),
                        None,
                        Paragraph("Test Data", extend_style(styles["rc-aawp-main-content"])),
                        None,
                    ]                    
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (0, 0), (0, 0), 0.1, "black"),
                    ("LINEBELOW", (2, 0), (2, 0), 0.1, "black")
                ]),
                colWidths=(50*mm, 39*mm, 50*mm, 24*mm)
            ),
            Spacer(0, 5.8*mm),
            Table(
                [
                    [
                        Paragraph("Se Encuentra Detenido(a)?", extend_style(styles["rc-aawp-main-content"])),
                        Paragraph("Test Data", extend_style(styles["rc-aawp-main-content"])),
                        None,
                        Paragraph("Fecha de Arresto", extend_style(styles["rc-aawp-main-content"])),
                        Paragraph("Test Data", extend_style(styles["rc-aawp-main-content"])),
                        None,
                    ]                    
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (1, 0), (1, 0), 0.1, "black"),
                    ("LINEBELOW", (4, 0), (4, 0), 0.1, "black")
                ]),
                colWidths=(42*mm, 24*mm, 12*mm, 28*mm, 28*mm, 29*mm)
            ),  
            Spacer(0, 2*mm),
            Paragraph(
                "SOLICITUD PARA ASIGNACION DE ABOGADO DE OFICIO Y <br />CERTIFICADO DE RECURSOS FINANCIEROS", 
                extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)),
            Spacer(0, 2.4*mm),
            Paragraph(
                """
                Yo soy el(la) acusado(a) en caso arriba citado. Se me acusa de los cargos de: <br />
                <u>{}</u>,
                los cuales se consideran delitos menores.
                Yo tengo / no tengo recursos financieros para contratar a un abogado que me ayude. Yo deseo / no 
                deseo que el Juez determine si califico para que se me asigne un abogado de oficio para que me 
                defienda en los cargos arriba citados.
                """.format(TEST_DATA),
                extend_style(styles["rc-aawp-main-content"], leading=18)
            ),
        ]
        table_list_front = [
            Table(
                [
                    [
                        Paragraph(
                            "Nombre Completo <u>{}</u> Teléfono <u>{}</u>".format(TEST_DATA, TEST_DATA), 
                            styles["rc-aawp-main-content-tb"])
                    ],[
                        Paragraph(
                            "Dirección de Domicilio <u>{}</u>".format(TEST_DATA), 
                            styles["rc-aawp-main-content-tb"])
                    ],[
                        Paragraph(
                            "Fecha de Nacimiento <u>{}</u> Edad <u>{}</u> No. Social. <u>{}</u>-<u>{}</u>-<u>{}</u>".format(TEST_DATA_S, TEST_DATA_S, TEST_DATA_S, TEST_DATA_S, TEST_DATA_S), 
                            styles["rc-aawp-main-content-tb"])
                    ],[
                        Paragraph(
                            "Nivel más alto de educación completado <u>{}</u> Sexo <u>{}</u> Raza <u>{}</u>".format(TEST_DATA_S, TEST_DATA_S, TEST_DATA_S), 
                            styles["rc-aawp-main-content-tb"])
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")                    
                ]),
            ),            
            Table(
                [
                    [
                        Paragraph(
                            """Contacto Secundario: Nombre Completo <u>{}</u> Teléfono <u>{}</u>""".format(TEST_DATA, TEST_DATA), 
                            styles["rc-aawp-main-content-tb"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
            ),
            Table(
                [
                    [
                        Paragraph(
                            """Si está empleado, nombre de la compañía <u>{}</u> Ciudad/Estado <u>{}</u>""".format(TEST_DATA_S, TEST_DATA_S), 
                            styles["rc-aawp-main-content-tb"]),
                    ],
                    [
                        Paragraph(
                            """
                            a. &nbsp; Net take home pay is (gross pay minus state, federal and social security taxes) <br />
                            <u>{}</u> (semanalmente) $ <u>{}</u> (mensualmente)
                            """.format(TEST_DATA, TEST_DATA), 
                            extend_style(styles["rc-aawp-main-content-tb"], leftIndent=16)),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
            ),
            Table(
                [
                    [
                        Paragraph(
                            """Si trabaja, cuánto tiempo lleva trabajando? <u>{}</u> Cite otras fuentes de ingresos, 
                            por ejemplo, indemnización laboral, asistencia social o por discapacidad, con sus respectivos valores 
                            semanalmente o mensualmente <u>{}</u>.""".format(TEST_DATA, TEST_DATA), 
                            styles["rc-aawp-main-content-tb"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
            ),
            Table(
                [
                    [
                        Paragraph(
                            """Está Ud. casado(a)? <u>{}</u>. Su esposa(o) trabaja? <u>{}</u>.""".format(TEST_DATA_S, TEST_DATA_S), 
                            styles["rc-aawp-main-content-tb"]),
                    ],
                    [
                        Paragraph(
                            """Si es así, para quién trabaja? <u>{}</u>.""".format(TEST_DATA, TEST_DATA), 
                            styles["rc-aawp-main-content-tb"]),
                    ],
                    [
                        Paragraph(
                            """Ingreso neto de su esposa(o) $ <u>{}</u>(semanalmente) $ <u>{}</u> (quincenalmente)""".format(TEST_DATA_S, TEST_DATA_S), 
                            styles["rc-aawp-main-content-tb"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
            ),
            Table(
                [
                    [
                        Paragraph(
                            """No. de niños que viven en casa <u>{}</u> Edades <u>{}</u>""".format(TEST_DATA_S, TEST_DATA), 
                            styles["rc-aawp-main-content-tb"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
            )
        ]

        table_list_back = [
            Table(
                [
                    [
                        Paragraph(
                            """Dependientes fuera de su esposa(o) o niños que viven con Ud, en su casa (nombre, parentesco y 
                            valor que contribuye por cada uno para su sustento)""", 
                            styles["rc-aawp-main-content-tb"]),
                    ],
                    [
                        Paragraph("Test Data", extend_style(styles["rc-aawp-main-content-tb"], leading=13))
                    ],
                    [
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEBELOW", (0, 1), (0, 1), 0.1, "black"),
                ]),
            ),
            Table(
                [
                    [
                        Paragraph(
                            """Es Ud. propietario o está comprando un vehículo? Si / No. Año y modelo<u>{}</u>""".format(TEST_DATA), 
                            styles["rc-aawp-main-content-tb"]),
                    ],
                    [
                        Paragraph(
                            """Cuánto debe en este vehículo? <u>{}</u>""".format(TEST_DATA), 
                            styles["rc-aawp-main-content-tb"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
            ),
            Table(
                [
                    [
                        Paragraph(
                            """Es Ud. dueño de una casa/apartamento? Sí / No. Valor $ <u>{}</u> Cantidad que debe $ <u>{}</u>""".format(TEST_DATA_S, TEST_DATA_S), 
                            styles["rc-aawp-main-content-tb"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
            ),
            Table(
                [
                    [
                        Paragraph(
                            """Valor de la hipoteca o pago de renta mensual $<u>{}</u>""".format(TEST_DATA), 
                            styles["rc-aawp-main-content-tb"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
            ),
            Table(
                [
                    [
                        Paragraph(
                            """Cite todas sus cuentas bancarias corrientes, de ahorros u de alguna otra clase, junto con el nombre de la entidad financiera y el valor en depósito por cuenta:""", 
                            styles["rc-aawp-main-content-tb"]),
                    ],
                    [
                        Table(
                            [
                                [
                                    Paragraph("", styles["rc-aawp-main-content-tb"]), None,
                                    Paragraph("Valor", extend_style(styles["rc-aawp-main-content-tb"])), None,
                                    Paragraph("Entidad financiera", extend_style(styles["rc-aawp-main-content-tb"]))
                                ],
                                [
                                    Paragraph("Cuenta corriente:", extend_style(styles["rc-aawp-main-content-tb"], leading=13)),
                                    Paragraph("$", extend_style(styles["rc-aawp-main-content-tb"], leading=13)),
                                    Paragraph("Test Data", extend_style(styles["rc-aawp-main-content-tb"], leading=13)), None,
                                    Paragraph("Test Data", extend_style(styles["rc-aawp-main-content-tb"], leading=13))
                                ],
                                [
                                    Paragraph("Cuenta de ahorros:", extend_style(styles["rc-aawp-main-content-tb"], leading=13)),
                                    Paragraph("$", extend_style(styles["rc-aawp-main-content-tb"], leading=13)),
                                    Paragraph("Test Data", extend_style(styles["rc-aawp-main-content-tb"], leading=13)), None,
                                    Paragraph("Test Data", extend_style(styles["rc-aawp-main-content-tb"], leading=13))
                                ],
                                [
                                    Paragraph("Otra clase:", extend_style(styles["rc-aawp-main-content-tb"], leading=13)),
                                    Paragraph("$", extend_style(styles["rc-aawp-main-content-tb"], leading=13)),
                                    Paragraph("Test Data", extend_style(styles["rc-aawp-main-content-tb"], leading=13)), None,
                                    Paragraph("Test Data", extend_style(styles["rc-aawp-main-content-tb"], leading=13))
                                ],
                                [
                                    None, None, None, None
                                ]
                            ],
                            style=extend_table_style(styles["rc-main-table"], [
                                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                ("LINEBELOW", (2, 1), (2, 1), 0.1, "black"),
                                ("LINEBELOW", (4, 1), (4, 1), 0.1, "black"),
                                ("LINEBELOW", (2, 2), (2, 2), 0.1, "black"),
                                ("LINEBELOW", (4, 2), (4, 2), 0.1, "black"),
                                ("LINEBELOW", (2, 3), (2, 3), 0.1, "black"),
                                ("LINEBELOW", (4, 3), (4, 3), 0.1, "black"),
                                ("TOPPADDING", (0, 2), (-1, -2), 2.4 * mm),
                            ]),
                            colWidths=(40*mm, 2*mm, 23*mm, 9*mm, 48*mm)
                        ),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
            ),
            Table(
                [
                    [
                        Paragraph(
                            """Cite cualquier otros activos o propiedad que posea; incluya bienes inmuebles, joyas, bonos o acciones:""".format(TEST_DATA, TEST_DATA), 
                            styles["rc-aawp-main-content-tb"]),
                    ],
                    [
                        Paragraph("Test Data", extend_style(styles["rc-aawp-main-content-tb"], leading=13))
                    ],
                    [ None ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEBELOW", (0, 1), (0, 1), 0.1, "black"),
                    ("TOPPADDING", (0, 2), (0, 2), 2.4 * mm),
                ]),
            ),
            Table(
                [
                    [
                        Paragraph(
                            """Cite deudas pendientes y valor correspondiente de pago:<u>{}</u>""".format(TEST_DATA), 
                            styles["rc-aawp-main-content-tb"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
            ),
            Table(
                [
                    [
                        Paragraph(
                            """Cite cualquier gasto extraordinario de manutención y valor correspondiente (por ejemplo cuentas 
                            médicas actuales) <u>{}</u>""".format(TEST_DATA), 
                            styles["rc-aawp-main-content-tb"]),
                    ],
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]),
            ),
            Table(
                [
                    [
                        Paragraph(
                            """Manutención infantil a pagar por orden judicial <u>{}</u>""".format(TEST_DATA), 
                            styles["rc-aawp-main-content-tb"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
            ),
            Table(
                [
                    [
                        Paragraph(
                            """*** Entiende Ud. que aunque Ud. sea condenado o absuelto, la Ciudad de Brookhaven puede exigir a que Ud. 
                            le reembolse los honorarios del abogado si Ud. posteriormente tiene los medios para pagarle o reembolsarle tales 
                            honorarios a la ciudad? <u>{}</u> (iniciales del(la) acusado(a)) <br />
                            Yo he leido (o me han leído) todas las preguntas anteriores con sus respuestas correspondientes, las cuales son 
                            verdaderas y correctas. <br />
                            El suscrito jura que la información proporcionada aquí es verdadera y correcta y entiende que cualquier respuesta 
                            falsa a cualquier pregunta puede resultar en un cargo de perjurio.

                            """.format(TEST_DATA_S), 
                            styles["rc-aawp-main-content-tb"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
            )
        ]
        table_front = []
        for idx, sub_table in enumerate(table_list_front):
            table_front.append(
                [   
                    None,
                    Paragraph('{}.'.format(idx+1), styles["rc-aawp-main-content"]),
                    sub_table
                ]
            )
        table_back = []
        for idx, sub_table in enumerate(table_list_back):
            table_back.append(
                [   
                    None,
                    Paragraph('{}.'.format(idx+7), styles["rc-aawp-main-content"]),
                    sub_table
                ]
            )

        elems +=[
            Spacer(0, 5.4*mm),
            Table(
                table_front,
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
                colWidths=(6*mm, 6*mm, 151*mm),
            ),
            PageBreak(),
            Spacer(0, 10.6*mm),
            Table(
                table_back,
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
                colWidths=(6*mm, 6*mm, 151*mm),
            ),
            Spacer(0, -3.2*mm),
            Paragraph(
                "Dado este día <u> Test Data </u>del mes de<u> Test Data </u>20<u>XX</u>.", 
                extend_style(styles["rc-aawp-main-content-tb"], leftIndent=35)
            ),
            Spacer(0, 4.2*mm),
            Table(
                [                    
                    [   None,
                        Paragraph("Firma del(a) Acusado(a)", styles["rc-aawp-main-content"]),
                        None
                    ]                    
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEABOVE", (1, 0), (1, 0), 0.1, "black"),
                    ("TOPPADDING", (0, 0), (-1, -1), 1.4 * mm),
                ]),
                colWidths=(75*mm, 78*mm, 10*mm)
            ),
            Paragraph(
                """
                Interview performed by: <u>{}</u>
                Date: <u>{}</u>""".format(TEST_DATA, TEST_DATA), 
                extend_style(styles["rc-aawp-main-content-tb"], spaceBefore=24, leftIndent=22)
            ),
            Spacer(0, 6.4*mm),
            Table(
                [                    
                    [   
                        None,
                        XBox(8, True),
                        Paragraph("APPROVED", extend_style(styles["rc-aawp-main-content"], leading=11)),
                        None,
                        XBox(8),
                        Paragraph("DENIED", extend_style(styles["rc-aawp-main-content"], leading=11)),
                        None
                    ]                    
                ],
                style=extend_table_style(styles["rc-main-table"], [
                ]),
                colWidths=(45*mm, 4*mm, 22*mm, 18*mm, 4*mm, 16*mm, 30*mm)
            ),
        ]
        
        return elems


class XBox(Flowable):
    def __init__(self, size, checked=None):
        Flowable.__init__(self)
        self.width = size
        self.height = size
        self.size = size
        self.checked = checked

    def draw(self):
        self.canv.saveState()
        self.canv.setLineWidth(0.11 * self.size)
        self.canv.rect(0, 0, self.width, self.height)
        if self.checked is True:
            self.check()
        self.canv.restoreState()

    def check(self):
        self.canv.setFont('Times-Bold', self.size * 0.95)
        to = self.canv.beginText(self.width * 0.13, self.height * 0.155)
        to.textLine("X")
        self.canv.drawText(to)