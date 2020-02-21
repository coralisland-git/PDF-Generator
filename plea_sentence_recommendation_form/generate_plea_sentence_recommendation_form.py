import cStringIO

from document_specific_styles import *
from common.signatures import *
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Flowable, Paragraph, Table, Spacer
from datetime import datetime

def generate_plea_sentence_recommendation_form():
    cr = PSRFReport()
    buff = cStringIO.StringIO()
    return cr.create_report(buff)

class PSRFReport:
    def __init__(self, title=None, author=None):
        self.page_size = letter
        self.page_margin = (12.4 * mm, 9.2 * mm)
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
                "CITY OF BROOKHAVEN <br />MUNICIPAL COURT",
                styles["rc-doc-header"]
            ),
            Paragraph(
                "<u>PLEA/SENTENCE RECOMMENDATION FORM</u>",
                styles["rc-doc-header-s"]
            )
        ]
        return elems

    def _section_content(self):
        space = "&nbsp;"*6
        today = datetime.today().strftime('%Y/%m/%d')
        elems = [
            Spacer(0, 4.2 * mm),
            Table(
                [
                    [
                        Paragraph(
                            "CITY OF BROOKHAVEN vs.",
                            styles["rc-aawp-main-content"]
                        ),
                        Paragraph(
                            "Test Data",
                            styles["rc-aawp-main-content"]
                        ),
                        None,
                        Paragraph(
                            "DOCKET/CIT. NO.",
                            styles["rc-aawp-main-content"]
                        ),
                        Paragraph(
                            "Test Data",
                            styles["rc-aawp-main-content"]
                        ),
                        None
                    ],
                ],
                style=extend_table_style(styles["rc-main-table"], [ 
                    ("LINEBELOW", (1, 0), (1, 0), 0.1, "black"),                    
                    ("LINEBELOW", (4, 0), (4, 0), 0.1, "black")
                ]),
                colWidths=(50*mm, 46*mm, 21*mm, 32*mm, 22*mm, 20*mm),
            ),
            Table(
                [
                    [
                        Paragraph(
                            "<u>Offense</u>",
                            styles["rc-aawp-main-content"]
                        ),
                        Paragraph(
                            "<u>Plea</u>",
                            styles["rc-aawp-main-content"]
                        ),
                        Paragraph(
                            "<u>Fine/Bond/Court Costs</u>",
                            styles["rc-aawp-main-content"]
                        )
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [ 
                    ("ALIGN", (0, 0), (-1, -1), "CENTER")
                ]),
                colWidths=(90*mm, 50*mm, 51*mm),
                rowHeights=12.4 * mm
            ),
        ]
        table_content = []
        table_style = []
        for idx in range(0, 6):
            table_content.append(
                [
                    Paragraph(
                        str(idx+1)+".",
                        styles["rc-aawp-main-content"]
                    ),
                    Paragraph(
                        "Test Data",
                        styles["rc-aawp-main-content"]
                    ),
                    None, 
                    Paragraph(
                        "Test Data",
                        styles["rc-aawp-main-content"]
                    ),
                    None,
                    Paragraph(
                        "Test Data",
                        styles["rc-aawp-main-content"]
                    )
                ]
            )
            table_style += [
                ("LINEBELOW", (1, idx), (1, idx), 0.1, "black"),
                ("LINEBELOW", (3, idx), (3, idx), 0.1, "black"),
                ("LINEBELOW", (5, idx), (5, idx), 0.1, "black")
            ]            
        elems += [
            Spacer(0, 2.4 * mm),
            Table(
                table_content,
                style=extend_table_style(styles["rc-main-table"], table_style),
                colWidths=(6 * mm, 58*mm, 19*mm , 19*mm, 38*mm , 51 * mm),
                rowHeights=5.8 * mm
            ),
            Spacer(0, 5.4 * mm),
            Table(
                [
                    [
                        Paragraph(
                            "Jail Service: "+"<u>100"+space*2+"</u>"+" Days",
                            styles["rc-aawp-main-content"]
                        ),
                        Paragraph(
                            "Community Service: "+"<u>100"+space*2+"</u>"+" Hrs.",
                            styles["rc-aawp-main-content"]
                        )
                    ],
                ],
                style=extend_table_style(styles["rc-main-table"]),
                colWidths=(84*mm , 107*mm),
            ),
            Spacer(0, 3.8 * mm),
            Table(
                [
                    [
                        Paragraph(
                            "Probation: "+"<u>100"+space*2+"</u>"+" Months-Early Termination: ",
                            extend_style(styles["rc-aawp-main-content"], fontSize=10)
                        ),
                        Choice(),
                        Paragraph(
                            "Non-Reporting upon completion: ",
                            extend_style(styles["rc-aawp-main-content"], fontSize=10)
                        ),
                        Choice()
                    ],
                ],
                style=extend_table_style(styles["rc-main-table"], [                    
                ]),
                colWidths=(73* mm, 30*mm, 49*mm, 39*mm),
            ),
            Spacer(0, 3.8 * mm),
            Table(
                [
                    [
                        XBox(7, True),
                        Paragraph(
                            "Apply Cash Bond",
                            styles["rc-aawp-main-content-s"]
                        )
                    ],
                ],
                style=extend_table_style(styles["rc-main-table"], [                    
                ]),
                colWidths=(3 * mm ,188*mm),
            ),
            Spacer(0, 2.6 * mm),
            Table(
                [
                    [
                        XBox(8, True),
                        Paragraph(
                            "Pretrial Diversion Program",
                            styles["rc-aawp-main-content-tb"]
                        )
                    ],
                    [
                        XBox(8, True),
                        Paragraph(
                            "Conditional Discharge",
                            styles["rc-aawp-main-content-tb"]
                        )
                    ],
                    [
                        XBox(8, True),
                        Paragraph(
                            "First Offender Treatment",
                            styles["rc-aawp-main-content-tb"]
                        )
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [                    
                ]),
                colWidths=(6 * mm ,172 * mm),
                rowHeights=5.4 * mm
            ),
            Spacer(0, 1.2 * mm),
            Paragraph(
                "<u>Additional Requirements</u>",
                extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER, fontSize=10)
            ),
            Spacer(0, 2.8 * mm),
            Table(
                [
                    [
                        XBox(7, True),
                        Paragraph(
                            "Alcohol Screening within 30 days",
                            styles["rc-aawp-main-content-s"]
                        ),
                        XBox(7, True),
                        Paragraph(
                            "DUI Risk Reduction within 120 day",
                            styles["rc-aawp-main-content-s"]
                        )
                    ],
                    [
                        XBox(7, True),
                        Paragraph(
                            "Drug/ Alcohol Abuse Evaluation and",
                            styles["rc-aawp-main-content-s"]
                        ),
                        XBox(7, True),
                        Paragraph(
                            "MADD Victim Impact Panel",
                            styles["rc-aawp-main-content-s"]
                        )
                    ],
                    [
                        None,
                        Paragraph(
                            "Recommended Treatment",
                            styles["rc-aawp-main-content-s"]
                        ),
                        XBox(7, True),
                        Paragraph(
                            "Ignition Interlock Required",
                            styles["rc-aawp-main-content-s"]
                        )
                    ],
                    [
                        XBox(7, True),
                        Paragraph(
                            "Random Drug/Alcohol Testing",
                            styles["rc-aawp-main-content-s"]
                        ),
                        XBox(7, True),
                        Paragraph(
                            "Surrender of license plate (2+ DUI)",
                            styles["rc-aawp-main-content-s"]
                        )
                    ],
                    [
                        XBox(7, True),
                        Paragraph(
                            "Drug I Alcohol Counseling (7 weeks)",
                            styles["rc-aawp-main-content-s"]
                        ),
                        XBox(7, True),
                        Paragraph(
                            "Shoplifter's Alternative Counseling w/in 30 days",
                            styles["rc-aawp-main-content-s"]
                        )
                    ],
                    [
                        XBox(7, True),
                        Paragraph(
                            "Drug Alcohol Counseling (17 weeks)",
                            styles["rc-aawp-main-content-s"]
                        ),
                        XBox(7, True),
                        Paragraph(
                            "Defensive Driving Class w/in 30 days",
                            styles["rc-aawp-main-content-s"]
                        )
                    ],
                    [
                        XBox(7, True),
                        Paragraph(
                            "Valid Driver's License to terminate probation",
                            styles["rc-aawp-main-content-s"]
                        ),
                        XBox(7, True),
                        Paragraph(
                            "Teen Defensive Driving Class",
                            styles["rc-aawp-main-content-s"]
                        )
                    ],
                    [
                        XBox(7, True),
                        Paragraph(
                            "Reimburse Court Appointed Attorney Fees of",
                            styles["rc-aawp-main-content-s"]
                        ),
                        XBox(7, True),
                        Paragraph(
                            "Anger Management Counseling",
                            styles["rc-aawp-main-content-s"]
                        )
                    ],
                    [
                        None,
                        Paragraph(
                            "$<u>100"+space*2+"</u>",
                            styles["rc-aawp-main-content-s"]
                        ),
                        XBox(7, True),
                        Paragraph(
                            "Domestic Violence Counseling",
                            styles["rc-aawp-main-content-s"]
                        )
                    ],
                    [
                        XBox(7, True),
                        Paragraph(
                            "Must be Fingerprinted",
                            styles["rc-aawp-main-content-s"]
                        ),
                        XBox(7, True),
                        Paragraph(
                            "Valid Driver's License at plea date",
                            styles["rc-aawp-main-content-s"]
                        )
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [                    
                ]),
                colWidths=(6*mm ,94*mm, 6*mm, 72*mm),
                rowHeights=4.8 * mm
            ),
            Spacer(0, 7.2 * mm),
            Table(
                [
                    [
                        Paragraph(
                            "Resets: 1.",
                            styles["rc-aawp-main-content"]
                        ),
                        Paragraph(
                            "Test Data",
                            styles["rc-aawp-main-content"]
                        ),
                        None,
                        Paragraph(
                            "2.",
                            styles["rc-aawp-main-content"]
                        ),
                        Paragraph(
                            "Test Data",
                            styles["rc-aawp-main-content"]
                        ),
                        None,
                        Paragraph(
                            "3.",
                            styles["rc-aawp-main-content"]
                        ),
                        Paragraph(
                            "Test Data",
                            styles["rc-aawp-main-content"]
                        ),
                        None
                    ],
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (1, 0), (1, 0), 0.1, "black"),
                    ("LINEBELOW", (4, 0), (4, 0), 0.1, "black"),
                    ("LINEBELOW", (7, 0), (7, 0), 0.1, "black")
                ]),
                colWidths=(16*mm, 30*mm, 25*mm, 4*mm, 30*mm, 30*mm, 4*mm, 30*mm, 23*mm),
            ),
            Spacer(0, 4.2 * mm),
            Paragraph(
                "Notes:",
                extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)
            ),
            Table(
                [
                    [  
                        Paragraph(
                            "Test Data",
                            styles["rc-aawp-main-content"]
                        ) 
                    ],
                    [ 
                        Paragraph(
                            "",
                            styles["rc-aawp-main-content"]
                        ) 
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [    
                    ("LINEBELOW", (0, 0), (0, 0), 0.1, "black"),                    
                    ("LINEBELOW", (0, 1), (0, 1), 0.1, "black")                    
                ]),
                rowHeights=8.2 * mm
            ),
            Spacer(0, 4.2 * mm),
            Table(
                [
                    [  
                        Paragraph(
                            "",
                            styles["rc-aawp-main-content"]
                        ),
                        None,
                        Paragraph(
                            today,
                            styles["rc-aawp-main-content"]
                        ),
                        None,
                        Paragraph(
                            "Plea Date",
                            styles["rc-aawp-main-content"]
                        ),
                        Paragraph(
                            today,
                            styles["rc-aawp-main-content"]
                        ),
                        None
                    ],
                    [ 
                        Paragraph(
                            "Solicitor",
                            styles["rc-aawp-main-content"]
                        ),
                        None,
                        Paragraph(
                            "Date",
                            styles["rc-aawp-main-content"]
                        ),
                        None, None, None, None
                    ],
                    [ None, None, None, None, None, None, None],
                    [  
                        Paragraph(
                            "",
                            styles["rc-aawp-main-content"]
                        ),
                        None,
                        Paragraph(
                            today,
                            styles["rc-aawp-main-content"]
                        ),
                        None,
                        Paragraph(
                            "Trial Date",
                            styles["rc-aawp-main-content"]
                        ),
                        Paragraph(
                            today,
                            styles["rc-aawp-main-content"]
                        ),
                        None
                    ],
                    [ 
                        Paragraph(
                            "Defense Attorney/Defendant",
                            styles["rc-aawp-main-content"]
                        ),
                        None,
                        Paragraph(
                            "Date",
                            styles["rc-aawp-main-content"]
                        ),
                        None, None, None, None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (0, 0), (0, 0), 0.1, "black"),
                    ("LINEBELOW", (2, 0), (2, 0), 0.1, "black"),
                    ("LINEBELOW", (5, 0), (5, 0), 0.1, "black"),
                    ("LINEBELOW", (0, 3), (0, 3), 0.1, "black"),
                    ("LINEBELOW", (2, 3), (2, 3), 0.1, "black"),
                    ("LINEBELOW", (5, 3), (5, 3), 0.1, "black"),
                ]),
                colWidths=(45*mm, 18*mm, 22*mm, 53*mm, 17*mm, 31*mm, 5*mm),
                rowHeights=5 * mm
            ),
            Spacer(0, 5.4 * mm),
            Paragraph(
                "<u>Note: All Flea/Sentence Recommendations are subject to the approval of the Court.</u>",
                extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER, fontSize=9, leftIndent=12*mm)
            ),
            Paragraph(
                "Revised: Aug 2018",
                extend_style(styles["rc-aawp-main-content"], spaceBefore=2, fontSize=7)
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


class Choice(Flowable):
    def __init__(self, checked=None):
        Flowable.__init__(self)
        self.checked = checked

    def draw(self):
        self.canv.saveState()
        self.canv.setLineWidth(0.1)        
        step = 0
        if self.checked == False:
            step = 7.8*mm
        self.canv.ellipse(-.4*mm+step, -.5*mm, 6.2*mm+step, 4.2*mm)
        self.canv.setFont('Times-Roman', 10)
        self.canv.drawString(0, .6*mm, "Yes / No")
        self.canv.restoreState()
