import cStringIO

from common.signatures import *
from document_specific_styles import *
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Flowable, Paragraph, Table, Spacer

def generate_sentence_recommendation():
    cr = ORFReport()
    buff = cStringIO.StringIO()
    return cr.create_report(buff)


class ORFReport:
    def __init__(self, title=None, author=None):
        self.page_size = letter
        self.page_margin = (28.4 * mm, 8.4 * mm)
        self.sections = ["content"]
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
                topPadding=8.4*mm,
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

    def get_lines(self, description):
        description = description.replace('\n','').replace('\t', '')
        w_temp = description.split(' ')
        word_list = []
        for word in w_temp:
            if word != '':
                word_list.append(word)
        lines = []
        begin_idx = 0
        idx = 0        
        while idx <= len(word_list):
            line = ' '.join(word_list[begin_idx:idx])
            t_len = stringWidth(line, "Times-Roman", 10)
            if t_len > 328.0:
                if t_len > 328.0:
                    line = ' '.join(word_list[begin_idx:idx-1])
                    begin_idx = idx-1
                else:
                    begin_idx = idx
                lines += [
                    [   
                        None,
                        Paragraph(line,
                            extend_style(styles["rc-aawp-main-content-tb"], leading=14),
                        )
                    ]
                ]
            idx += 1
        lines += [
            [
                None,
                Paragraph(line,
                    extend_style(styles["rc-aawp-main-content-tb"], leading=14),
                )
            ]
        ]
        return lines

    def _section_content(self):
        pre_space = "&nbsp;" * 4
        TEST_DATA = pre_space + "test Data" + pre_space
        elems = list()
        elems += [
            Paragraph(
                "IN THE MAGISTRATE COURT OF ROCKDALE COUNTY <br />STATE OF GEORGIA",
                extend_style(styles["rc-doc-header"])
            ),
            Spacer(0, 8.4*mm),
            Table(
                [
                    [
                        Paragraph("ROCKDALE COUNTY,", styles["rc-aawp-main-content-tb"]), None,
                        Paragraph(")", styles["rc-aawp-main-content-tb"]), None, None
                    ],
                    [
                        None, None, Paragraph(")", styles["rc-aawp-main-content-tb"]),
                        Paragraph("ORDINANCE  NO:", styles["rc-aawp-main-content-tb"]),
                        Paragraph("", styles["rc-aawp-main-content-tb"]),
                    ],
                    [
                        Paragraph("v", styles["rc-aawp-main-content-tb"]), None,
                        Paragraph(")", styles["rc-aawp-main-content-tb"]), None, None
                    ],
                    [
                        None, None, Paragraph(")", styles["rc-aawp-main-content-tb"]), None, None
                    ],
                    [
                        Paragraph("", styles["rc-aawp-main-content-tb"]), None,
                        Paragraph(")", styles["rc-aawp-main-content-tb"]), None, None
                    ],
                    [
                        None, None, Paragraph(")", styles["rc-aawp-main-content-tb"]), None, None
                    ],
                    [
                        Paragraph("Defendant.", extend_style(styles["rc-aawp-main-content-tb"], alignment=TA_CENTER)), 
                        None, Paragraph(")", styles["rc-aawp-main-content-tb"]), None, None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (0, 4), (0, 4), 0.1, "black"),
                    ("LINEBELOW", (-1, 1), (-1, 1), 0.1, "black"),                    
                ]),
                colWidths=(44*mm, 34*mm, 12*mm, 34*mm, 35*mm)
            ),
            Spacer(0, 8.4*mm),
            Table(
                [
                    [
                        Paragraph("SENTENCE RECOMMENDATION", extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)), 
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (0, 0), (0, 0), 0.1, "black"),
                    ("LINEABOVE", (0, 0), (0, 0), 0.1, "black"),
                    ("TOPPADDING", (0, 0), ( -1, -1), 4 * mm ),
                    ("BOTTOMPADDING", (0, 0), ( -1, -1), 1.8 * mm )
                ])
            ),
            Spacer(0, 5.8*mm),
            Paragraph(
                """{} COMES NOW the County of Rockdale, by and through the assistant county attorney, and hereby files the following 
                sentence recommendation in the above-referenced case.""".format(pre_space*3),
                extend_style(styles["rc-aawp-main-content"], leading=26)
            ),
            Paragraph(
                "1.",extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)
            ),
            Paragraph(
                "Defendant is charged with <u>{}</u>.".format(TEST_DATA),
                extend_style(styles["rc-aawp-main-content"], leftIndent=14*mm)
            ),
            Paragraph(
                "2.",extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)
            ),
            Paragraph(
                "Rockdale County recommends a sentence of the following:",
                extend_style(styles["rc-aawp-main-content"], leftIndent=14*mm)
            ),
            Spacer(0, 4.2*mm),
            Table(
                [
                    [
                        Paragraph("1.", extend_style(styles["rc-aawp-main-content"], alignment=TA_RIGHT)), 
                        Paragraph("""
                            Ten (10) days confinement SUSPENDED upon payment of fines in the amount of $<u>{}</u>
                            dollars plus surcharges in the amount of $<u>{}</u> for a total of $<u>{}</u>.
                            """.format(TEST_DATA, TEST_DATA, TEST_DATA), 
                        styles["rc-aawp-main-content"])
                    ],
                    [
                        Paragraph("2.", extend_style(styles["rc-aawp-main-content"], alignment=TA_RIGHT)), 
                        Paragraph("""
                            Total fines shall be paid by <u>{}</u>
                            for a <u>{}</u> compliance hearing on <u>{}</u> if not paid.
                            """.format(TEST_DATA, TEST_DATA, TEST_DATA),
                        styles["rc-aawp-main-content"])
                    ],
                    [
                        Paragraph("3.", extend_style(styles["rc-aawp-main-content"], alignment=TA_RIGHT)), 
                        Table(
                            [
                                [Paragraph("Special Conditions:", styles["rc-aawp-main-content"])],
                            ],
                            style=extend_table_style(styles["rc-main-table"], [
                            ])                            
                        )
                    ],

                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("RIGHTPADDING", (0, 0), ( 0, -1), 3.2*mm ),
                    ("BOTTOMPADDING", (0, 0), ( -1, -1), 3*mm ),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]),
                colWidths=(20*mm, 139*mm)
            ),
            Spacer(0, -6*mm)
        ]        
        conditions = """Test Data"""
        lines = self.get_lines(conditions)
        for line in lines:
            elems += [
                Table(                
                    [line],
                    style=extend_table_style(styles["rc-main-table"], [
                        ("LINEBELOW", (1, 0), (1, 0), 0.1, "black")
                    ]),
                    colWidths=(20*mm, 139*mm),
                    rowHeights=8.2 * mm
                )
            ]
        elems +=[
            Spacer(0, 8.4 * mm),            
            Paragraph(
                "Respectfully submitted this <u>{}</u> day of <u>{}</u>, 2019".format(TEST_DATA, TEST_DATA),
                extend_style(styles["rc-aawp-main-content"], leftIndent=14*mm)
            ),
            Table(
                [
                    [
                        None,
                        Paragraph("",styles["rc-aawp-main-content-tb"])
                    ],
                    [
                        None,
                        Paragraph(
                            """
                            CHERYL R. FREEMAN <br />
                            Attorney for Rockdale County <br />
                            Georgia Bar No.: 428312
                            """,
                        styles["rc-aawp-main-content-tb"])
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEABOVE", (-1, -1), (-1, -1), 0.1, "black"),                    
                ]),
                colWidths=(100*mm, 59*mm)
            )
        ]
        
        return elems