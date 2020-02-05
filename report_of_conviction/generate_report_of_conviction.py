# -*- coding: utf-8 -*-
import cStringIO
import datetime

from document_specific_styles import *
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Flowable, Paragraph, Table, Spacer


def generate_report_of_conviction(title=None, author=None):
    cr =ROCReport(title, author)
    buff = cStringIO.StringIO()
    return cr.create_report(buff)


class ROCReport:
    def __init__(self, title=None, author=None):
        self.page_size = letter
        self.page_margin = (10.4 * mm, 10.4 * mm)
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
                "State of Georgia Report of Conviction",                
                extend_style(styles["rc-doc-header-roc"])
            ),
            Spacer(0, 5.2 * mm),
        ]
            
        return elems

    def _section_content(self):        
        elems = [
            Table(
                [
                    [
                        Paragraph("Name &nbsp; <u>TAMICA SHEREE JOHNSON"+"&nbsp;"*41+"</u>", styles["rc-tdwp-main"]),
                        Paragraph("Operator I Drivers License Number / Class &nbsp; <u>060274748 / C"+"&nbsp;"*24+"</u>", styles["rc-tdwp-main"])
                    ],
                    [
                        Paragraph("Street Address &nbsp; <u>2086 GRAMERCY CIR"+"&nbsp;"*38+"</u>", styles["rc-tdwp-main"]),
                        Paragraph("Country / State Of License &nbsp; <u>GA"+"&nbsp;"*68+"</u>", styles["rc-tdwp-main"])
                    ],
                    [
                        Paragraph("City&nbsp; <u>ATLANTA"+"&nbsp;"*20+"</u>"+"&nbsp;"*6+"State&nbsp; <u>GA&nbsp;&nbsp;</u>"+"&nbsp;"*4+"Zip Code&nbsp; <u>30341-1</u>", styles["rc-tdwp-main"]),
                        Paragraph("Date of Birth &nbsp; <u>07/06/1969"+"&nbsp;"*10+"</u> &nbsp; Gender &nbsp; <u>Female"+"&nbsp;"*37+"</u>", styles["rc-tdwp-main"]),
                    ]
                ],
                style=styles["rc-main-table"],
                colWidths=(96 * mm, 100 * mm),
                rowHeights=6.4 * mm
            ),
            Spacer(0, 3.6 * mm),
            Table(
                [
                    [
                        Paragraph("Commercial Driver?", styles["rc-tdwp-main-chk"]),
                        XBox(9), Paragraph("Yes", styles["rc-tdwp-main-chk"]),
                        XBox(9), Paragraph("No", styles["rc-tdwp-main-chk"]),
                        None,
                        Paragraph("License Attached?", styles["rc-tdwp-main-chk"]),
                        XBox(9), Paragraph("Yes", styles["rc-tdwp-main-chk"]),
                        XBox(9), Paragraph("No", styles["rc-tdwp-main-chk"]),
                        XBox(9), Paragraph("Lost License Affidavit", styles["rc-tdwp-main-chk"]),
                    ],
                    [
                        Paragraph("Commercial Vehicle?", styles["rc-tdwp-main-chk"]),
                        XBox(9), Paragraph("Yes", styles["rc-tdwp-main-chk"]),
                        XBox(9), Paragraph("No", styles["rc-tdwp-main-chk"]),
                        None,
                        Paragraph("Involved in an Accident?", styles["rc-tdwp-main-chk"]),
                        XBox(9), Paragraph("Yes", styles["rc-tdwp-main-chk"]),
                        XBox(9), Paragraph("No", styles["rc-tdwp-main-chk"]),
                        None
                    ],
                    [
                        Paragraph("16+ Passengers?", styles["rc-tdwp-main-chk"]),
                        XBox(9), Paragraph("Yes", styles["rc-tdwp-main-chk"]),
                        XBox(9), Paragraph("No", styles["rc-tdwp-main-chk"]),
                        None,
                        Paragraph("If Accident, Injuries?", styles["rc-tdwp-main-chk"]),
                        XBox(9), Paragraph("Yes", styles["rc-tdwp-main-chk"]),
                        XBox(9), Paragraph("No", styles["rc-tdwp-main-chk"]),
                        None
                    ],
                    [
                        Paragraph("Hazardous Materials Violatioin / Placard(s)", styles["rc-tdwp-main-chk"]),
                        XBox(9), Paragraph("Yes", styles["rc-tdwp-main-chk"]),
                        XBox(9), Paragraph("No", styles["rc-tdwp-main-chk"]),
                        None,
                        Paragraph("If Accident, Fatality?", styles["rc-tdwp-main-chk"]),
                        XBox(9), Paragraph("Yes", styles["rc-tdwp-main-chk"]),
                        XBox(9), Paragraph("No", styles["rc-tdwp-main-chk"]),
                        None
                    ],
                    [
                        Paragraph("Interlock Device Ordered?", styles["rc-tdwp-main-chk"]),
                        XBox(9), Paragraph("Yes", styles["rc-tdwp-main-chk"]),
                        XBox(9), Paragraph("No", styles["rc-tdwp-main-chk"]),
                        None,
                        Paragraph("2-Lane Road?", styles["rc-tdwp-main-chk"]),
                        XBox(9), Paragraph("Yes", styles["rc-tdwp-main-chk"]),
                        XBox(9), Paragraph("No", styles["rc-tdwp-main-chk"]),
                        None
                    ]
                ],
                style=styles["rc-main-table"],
                colWidths=(63 * mm, 4.5 * mm, 8 * mm, 4.5 * mm, 8 * mm, 4 * mm,
                    40 * mm, 4.5 * mm, 8 * mm, 4.5 * mm, 10 * mm, 4 * mm, 33 * mm),
                rowHeights=4.6 * mm
            ),
            Spacer(0, 3 * mm),
            Table(
                [
                    [
                        Paragraph("Blood Alcohol Concentration, if applicable &nbsp; <u>"+"&nbsp;"*28+"</u>", styles["rc-tdwp-main"]),
                        Paragraph("If applicable, Actual Speed &nbsp; <u>********</u> &nbsp; Speed Limit &nbsp; <u>********</u>", styles["rc-tdwp-main"]),
                    ],
                    [
                        Paragraph("Date of Violation / Offense  &nbsp; <u>07/10/2019"+"&nbsp;"*35+"</u>", styles["rc-tdwp-main"]),
                        Paragraph("County Of Violation &nbsp; <u>DEKALB"+"&nbsp;"*76+"</u>", styles["rc-tdwp-main"]),
                    ]
                ],
                style=styles["rc-main-table"],
                colWidths=(91 * mm, 105 * mm),
                rowHeights=5.4 * mm
            ),
            Spacer(0, 3 * mm),
            Table(
                [
                    [
                        Table(
                            [
                                [
                                    Paragraph("WHAT IS THE CODE SECTION OF THE OFFENSE FOR WHICH THE VIOLATOR WAS CONVICTED?", extend_style(styles["rc-tdwp-main-tt"], leading=11)),
                                ]
                            ],
                                style=extend_table_style(styles["rc-main-table"], [
                                    ("OUTLINE", (0, 0), (-1, -1), 0.45, "gray"),
                                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                            ]),
                            colWidths=(148 * mm),
                            rowHeights=4.4 * mm
                        )
                    ],
                    [
                        Paragraph("O.C.G.A. Section: &nbsp; <u>40-5-121"+"&nbsp;"*18+"</u> &nbsp; Description of Offense: &nbsp; <u>DRIVING WHILE LIC. SUSPENDED OR REVOKED (MANDATORY COURT)</u>", styles["rc-tdwp-main-tt"]),

                    ],
                ],
                    style=extend_table_style(styles["rc-main-table"], [
                        ("OUTLINE", (0, 0), (-1, -1), 1, "black"),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("VALIGN", (0, 0), (-1, -1), "CENTER"),
                ]),
                rowHeights=(4.4 * mm, 9.4 * mm)
            ),
            Spacer(0, 3 * mm),
            Paragraph("Date of Disposition &nbsp; <u>"+"&nbsp;"*94+"</u>", extend_style(styles["rc-tdwp-main"], spaceBefore=0)),
            Paragraph("Disposition Code  &nbsp; <u>"+"&nbsp;"*74+"</u>", styles["rc-tdwp-main"]),
            Paragraph("Sentence Amount Fine / Forfeiture Amount &nbsp; <u>$0.00"+"&nbsp;"*21+"</u> &nbsp; Name of Arresting Officer &nbsp; <u>BROWN"+"&nbsp;"*71+"</u>", styles["rc-tdwp-main"]),
            Paragraph("Department / Issuing Agency &nbsp; <u> / NCIC # GA044201J"+"&nbsp;"*149+"</u>", styles["rc-tdwp-main"]),
            Spacer(0, 3 * mm),
            Table(
                [
                    [
                        Table(
                            [
                                [
                                    Paragraph("CHECK THE APPROPRIATE BOX (ONLY ONE) AND FILL IN THE REQUIRED INFORMATION", extend_style(styles["rc-tdwp-main-tt"], leading=11)),
                                ]
                            ],
                                style=extend_table_style(styles["rc-main-table"], [
                                    ("OUTLINE", (0, 0), (-1, -1), 0.45, "gray"),
                                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                            ]),
                            colWidths=(148 * mm),
                            rowHeights=4.4 * mm
                        )
                    ],
                    [
                        Table(
                            [
                                [
                                    Table(
                                        [
                                            [
                                                Paragraph("Zero Points Court Order Issued per 0.C.G.A. 40-5-57(c)(1)(C)?", styles["rc-tdwp-main-chk"]),
                                                XBox(9), Paragraph("Yes", styles["rc-tdwp-main-chk"]),
                                                XBox(9), Paragraph("No", styles["rc-tdwp-main-chk"]),
                                            ],
                                            [
                                                Paragraph("License Suspension Court Ordered as a Condition of Probation?", styles["rc-tdwp-main-chk"]),
                                                XBox(9), Paragraph("Yes", styles["rc-tdwp-main-chk"]),
                                                XBox(9), Paragraph("No", styles["rc-tdwp-main-chk"]),
                                            ],
                                            []
                                        ],
                                        style=extend_table_style(styles["rc-main-table"], [
                                            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                                        ]),
                                        colWidths=(89 * mm, 4.5 * mm, 10 * mm, 4.5 * mm, 10 * mm),
                                        rowHeights=4.6 * mm
                                    ),
                                    Table(
                                        [                                               
                                            [Paragraph("If yes, Court Ordered License Suspension Duration", styles["rc-tdwp-main"])],
                                            [Paragraph("_"*5+"Years / Months / Days", styles["rc-tdwp-main"])]
                                        ],
                                        style=extend_table_style(styles["rc-main-table"], [
                                            ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
                                            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                                        ]),
                                        rowHeights=4.6 * mm
                                    ),
                                ]
                            ],
                                style=extend_table_style(styles["rc-main-table"], [
                                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                                    ("VALIGN", (0, 0), (-1, -1), "CENTER"),
                                    ("LEFTPADDING", (0, 0), ( 0, 0), 1.2 * mm )
                            ]),
                            rowHeights=(12 * mm)
                        ),                    
                    ],
                ],
                    style=extend_table_style(styles["rc-main-table"], [
                        ("OUTLINE", (0, 0), (-1, -1), 1, "black"),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("VALIGN", (0, 0), (-1, -1), "CENTER"),
                ]),
                rowHeights=(4.4 * mm, 16 * mm)
            ),
            Spacer(0, 3 * mm),
            Paragraph("Court Case Number &nbsp; <u>E67963"+"&nbsp;"*55+"</u> &nbsp; Citation Number &nbsp; <u>E67963"+"&nbsp"*86+"</u>", extend_style(styles["rc-tdwp-main"], spaceBefore=0)),
            Paragraph("Court &nbsp; <u>BROOKHAVEN MUNICIPAL COURT / NCIC  #  GA044201J"+"&nbsp;"*126+"</u>", extend_style(styles["rc-tdwp-main"], spaceBefore=0)),
            Paragraph("Mailing Address of Court &nbsp;&nbsp;&nbsp; <u>BROOKHAVEN MUNICIPAL COURT 2665 BUFORD HWY BROOKHAVEN, GA 30324"+"&nbsp;"*49+"</u>", extend_style(styles["rc-tdwp-main"], spaceBefore=0)),
            Paragraph("Physical Address of Court &nbsp;&nbsp; <u>BROOKHAVEN MUNICIPAL COURT 2665 BUFORD HWY BROOKHAVEN, GA 30324"+"&nbsp;"*48+"</u>", extend_style(styles["rc-tdwp-main"], spaceBefore=0)),
            Spacer(0, 7.4 * mm),
            Paragraph("Signature of Judge, Court Clerk or Court Official "+"&nbsp;"*4+"<u>"+"&nbsp;"*64+"</u>", styles["rc-tdwp-main"]),
            Paragraph(
                "Mail to: Georgia Department of Driver Services, Conviction Processing Unit, P.O. Box 80447, Conyers, GA 30013",
                extend_style(styles["rc-doc-header-roc"], fontSize=8.5, spaceBefore=8)
            ),            
            Paragraph("<b>DDS-32C (11/2009)</b>", extend_style(styles["rc-tdwp-main"],spaceBefore=4)),
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