import cStringIO

from document_specific_styles import *
from common.signatures import *
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Flowable, Paragraph, Table, Spacer


def generate_notice_of_revocation():
    cr = NORReport()
    buff = cStringIO.StringIO()
    return cr.create_report(buff)

class NORReport:
    def __init__(self, title=None, author=None):
        self.page_size = letter
        self.page_margin = (12.5 * mm, 14.8 * mm)
        self.sections = ["header", "section_1", "section_2"]
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
                "GEORGIA DEPARTMENT OF DRIVER SERVICES <br />P.O. BOX 80447 <br />CONYERS, GEORGIA 30013",
                styles["rc-doc-header-nor"]
            ),
            Paragraph(
                "OFFICIAL NOTICE OF REVOCATION AND SERVICE BY COURT",
                extend_style(styles["rc-doc-header-nor"], spaceBefore=6)
            ),
            Paragraph(
                "NOTICE: READ INSTRUCTIONS ON REVERSE SIDE BEFORE COMPLETING FORM.",
                extend_style(styles["rc-doc-header-nor-s"], spaceBefore=6)
            )
        ]
        return elems

    def _section_section_1(self):
        elems = [
            Spacer(0, .25 * mm),
            Table(
                [
                    [
                        Paragraph("Name"+"&nbsp;"*5+"<u><b>TAM1CA SHEREE JOHNSON"+"&nbsp;"*26+"</b></u>", styles["rc-aawp-main-content"]),
                        Paragraph("DOB:"+"&nbsp;"*5+"<u><b>07/06/1969"+"&nbsp;"*54+"</b></u>", styles["rc-aawp-main-content"])
                    ],
                    [
                        Paragraph("Address"+"&nbsp;"*2+"<u><b>2086 GRAMERCY CIR"+"&nbsp;"*38+"</b></u>", styles["rc-aawp-main-content"]),
                        Paragraph("DL#:"+"&nbsp;"*5+"<u><b>GA 060274748"+"&nbsp;"*49+"</b></u>", styles["rc-aawp-main-content"])
                    ],
                    [
                        Paragraph("City"+"&nbsp;"*9+"<u><b>ATLANTA"+"&nbsp;"*58+"</b></u>", styles["rc-aawp-main-content"]),                        
                        Paragraph("State"+"&nbsp;"*5+"<u><b>GA &nbsp;</b></u>"+"&nbsp;"*2+"Zip"+"&nbsp;"*2+"<u><b>30341"+"&nbsp;"*46+"</b></u>", styles["rc-aawp-main-content"])
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [                    
                ]),
                colWidths=(91 * mm ,100 * mm),
                rowHeights=6.2 * mm
            ),
            Paragraph(
                """YOU ARE HEREBY NOTIFIED that as of this date you have been declared a Habitual Violator of the laws relating to 
                motor vehicles and traffic pursuant to the Driver's Licensing Act (Ga. Code 40-5-58, as amended) and that henceforth it 
                shall be unlawful for you to operate a motor vehicle in the STATE OF GEORGIA""",
                extend_style(styles["rc-aawp-main-content"])
            ),
            Paragraph(
                """
                Your license and privilege to operate a motor vehicle in this State is revoked for a minimum of five (5) years from 
                07/16/2019 (see item 4 of instructions), and will remain revoked until requirements of Code Section 40-5-62 are complied 
                with. If you should be convicted of operating a motor vehicle while your license is under revocation as provided herein, 
                you may be subject to confinement in the penitentiary for not less than one nor more than five years.
                """,
                extend_style(styles["rc-aawp-main-content"])
            ),
            Paragraph(
                """
                YOU ARE HEREBY ORDERED to surrender any learner's, operator's, chauffeur's, and / or veteran's license in your possession 
                and particularly the below numbered license(s), to the clerk of this court to be forwarded to the Department of 
                Driver Services, P.O. Box 80447, Conyers, Georgia 30013.
                """,
                extend_style(styles["rc-aawp-main-content"])
            ),
            Paragraph(
                "<b>I HAVE PERSONALLY RECEIVED SERVICE OF HABITUAL VIOLATOR REVOCATION ORDER.</b>",
                extend_style(styles["rc-aawp-main-content"],  spaceBefore=8, alignment=TA_CENTER)
            ),
            Spacer(0, 8.4 * mm),
            Table(
                [
                    [
                        Paragraph("Date", styles["rc-aawp-main-content-tb"]),
                        Paragraph("07/16/2019", extend_style(styles["rc-aawp-main-content-tb"], alignment=TA_CENTER)),
                        None, None, None
                    ],
                    [
                        None, None, None,
                        Paragraph("Signature of Licensee", styles["rc-aawp-main-content-tb"]), None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (1, 0), (1, 0), 0.1, "black"),
                    ("LINEBELOW", (3, 0), (3, 0), 0.1, "black"),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER")
                ]),
                colWidths=(11 * mm, 30*mm, 62*mm , 68*mm, 16*mm),
                rowHeights=5.8 * mm
            ),
            Table(
                [
                    [
                        Paragraph("License picked up?", styles["rc-aawp-main-content"]),
                        Paragraph("Yes", styles["rc-aawp-main-chk"]), XBox(11, True), 
                        Paragraph("No", styles["rc-aawp-main-chk"]), XBox(11),
                        Paragraph("Lost License Affidavit", styles["rc-aawp-main-content"]),
                        Paragraph("Yes", styles["rc-aawp-main-chk"]), XBox(11, True), 
                        Paragraph("No", styles["rc-aawp-main-chk"]), XBox(11)
                    ]
                ],
                style=styles["rc-main-table"],
                colWidths=(37*mm, 10*mm, 8*mm, 8*mm, 20*mm, 41 * mm, 10*mm, 8*mm, 8*mm, 40*mm),
                rowHeights=5.8 * mm
            ),
            Spacer(0, 1.2 * mm),
            Table(
                [
                    [ 
                        Paragraph("Other &nbsp;&nbsp;", extend_style(styles["rc-aawp-main-content-tb"], alignment=TA_RIGHT)),
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (1, 0), (1, 0), 0.1, "black")                    
                ]),
                colWidths=(70*mm, 100*mm),
                rowHeights=6.4 * mm
            ),
            Spacer(0, 8.4 * mm),
            Table(
                [
                    [ 
                        None,
                        Paragraph("07/16/2019", extend_style(styles["rc-aawp-main-content-tb"], alignment=TA_CENTER)),
                        None
                    ],
                    [ 
                        Paragraph("Serving Official's Signature", styles["rc-aawp-main-content-tb"]),
                        Paragraph("Date", extend_style(styles["rc-aawp-main-content-tb"], alignment=TA_CENTER)),
                        Paragraph("Print Name and Title", extend_style(styles["rc-aawp-main-content-tb"], alignment=TA_CENTER))
                    ],
                    [ None, None, None],                    
                    [ 
                        None,
                        Paragraph("07/16/2019", extend_style(styles["rc-aawp-main-content-tb"], alignment=TA_CENTER)),
                        None
                    ],
                    [ 
                        Paragraph("Signature of Witness", styles["rc-aawp-main-content-tb"]),
                        Paragraph("Date", extend_style(styles["rc-aawp-main-content-tb"], alignment=TA_CENTER)),
                        Paragraph("Print Name and Title", extend_style(styles["rc-aawp-main-content-tb"], alignment=TA_CENTER))
                    ],
                    [ 
                        Paragraph("BROOKHAVEN MUNICIPAL COURT", styles["rc-aawp-main-content-tb"]),
                        None,
                        Paragraph("404-637-0660", extend_style(styles["rc-aawp-main-content-tb"], alignment=TA_CENTER))
                    ],
                    [ 
                        Paragraph("Agency Serving Order", styles["rc-aawp-main-content-tb"]),
                        None,
                        Paragraph("Telephone Number", extend_style(styles["rc-aawp-main-content-tb"], alignment=TA_CENTER))
                    ],
                    [ 
                        Paragraph("2665 BUFORD HWY", styles["rc-aawp-main-content-tb"]),
                        None,
                        Paragraph("BROOKHAVEN, GA 30324", extend_style(styles["rc-aawp-main-content-tb"], alignment=TA_CENTER))
                    ],
                    [ 
                        Paragraph("Agency Mailing Address", styles["rc-aawp-main-content-tb"]),
                        None,
                        Paragraph("City, State, Zip", extend_style(styles["rc-aawp-main-content-tb"], alignment=TA_CENTER))
                    ],

                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEBELOW", (0, 0), (2, 0), 0.1, "black"),
                    ("LINEBELOW", (0, 3), (2, 3), 0.1, "black"),
                    ("LINEBELOW", (0, 5), (2, 5), 0.1, "black"),
                    ("LINEBELOW", (0, 7), (2, 7), 0.1, "black")
                ]),
                colWidths=(70*mm, 40*mm, 80*mm),
                rowHeights=(6.2*mm, 6.2*mm, 10.4*mm, 6.2*mm, 6.2*mm, 6.2*mm, 6.2*mm, 6.2*mm, 6.2*mm )
            ),
            Spacer(0, 13 * mm),
            Paragraph(
                "<b>DS-1189 (04/06)</b>",
                extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)
            ),
        ]

        return elems


    def _section_section_2(self):
        elems = [
            Spacer(0, 12.2 * mm),
            Paragraph(
                "INSTRUCTIONS FOR COMPLETING FRONT OF THIS FORM",
                extend_style(styles["rc-doc-header-nor"], alignment=TA_LEFT)
            ),
            Spacer(0, 2.4 * mm),
            Table(
                [
                    [
                        Paragraph("1.", styles["rc-aawp-main-content"]),
                        Paragraph("Print or type all information.", styles["rc-aawp-main-content"]),
                    ],
                    [
                        Paragraph("2.", styles["rc-aawp-main-content"]),
                        Paragraph("Complete in Duplicate", styles["rc-aawp-main-content"]),
                    ],
                    [
                        None,
                        Paragraph(
                            """
                            a. Original to the Department of Driver Services <br />
                            b. Copy to the Habitual Violator
                            """, 
                            styles["rc-aawp-main-content"]),
                    ],
                    [
                        Paragraph("3.", styles["rc-aawp-main-content"]),
                        Paragraph("Attach to this Order the following:.", styles["rc-aawp-main-content"]),
                    ],
                    [
                        None,
                        Paragraph(
                            """
                            a.  Department of Driver Services copy of the Uniform Traffic Citation or DS-32C <br />
                            b.  Driver's License or Lost License Affidavit <br />
                            c. Mail all items within three (3) days to address in paragraph 3 on front.
                            """, 
                            styles["rc-aawp-main-content"]),
                    ],
                    [
                        Paragraph("4.", styles["rc-aawp-main-content"]),
                        Paragraph(
                            """
                            Conviction date is to show as date of declaration provided license is picked up by Court, or lost license affidavit is 
                            completed and attached . or license is presently being held by the Department of Driver Services.
                            """, 
                            styles["rc-aawp-main-content"]),
                    ],
                    [
                        Paragraph("5.", styles["rc-aawp-main-content"]),
                        Paragraph("Fill in all blanks with the requested information.", styles["rc-aawp-main-content"]),
                    ],
                    [
                        Paragraph("6.", styles["rc-aawp-main-content"]),
                        Paragraph("If this form is duplicated, information concerning hearing must be on the back of all forms or service will be invalid.", styles["rc-aawp-main-content"]),
                    ],
                    [
                        Paragraph("7.", styles["rc-aawp-main-content"]),
                        Paragraph(
                            '''
                            THIS ORDER AND ABOVE DOCUMENTS MUST NOT BE MAILED WITH REGULAR CONVICTION REPORTS. IT 
                            IS SUGGESTED THAT THE WORD "EXPEDITE" BE WRITTEN IN RED ON THE ENVELOPE CONTAINING SAME.
                            ''', 
                            styles["rc-aawp-main-content"]),
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("TOPPADDING", (0, 0), (-1, -1), .75 * mm),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), .75 * mm)
                ]),
                colWidths=(8*mm, 182*mm)                
            ),
            Spacer(0, 1.2 * mm),
            Paragraph(
                "<b>HEARING</b>",
                extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)
            ),
            Paragraph(
                """
               Any person adversely affected by any decision or action of the Department and who is entitled to have that decision or 
               action reviewed may file a request for a hearing with the Department, within ten (10) days of the receipt of this order, in 
               accordance with the provisions of Rule 570.1-.06 of the Rule and Regulations of the Department of Driver Services. This 
               request should describe specifically the decision or action to which it relates, state the change in decision or action the 
               requester desires and the basis upon which the requester considers himself to be entitled to have such decision or action 
               changed. If the person desires a hearing, a request therefore should be specifically made.
                """,
                styles["rc-aawp-main-content"]
            ),
            Paragraph(
                """
                The Department will respond to all requests for hearings with notice of the grant of the requested change, notice of 
                refusal to make a requested change, or notice scheduling a hearing. Any notice of refusal to make a requested change 
                will state the reason for refusal. If a hearing is granted it will be scheduled within a reasonable time after the request 
                therefore is received by the Department.
                """,
                styles["rc-aawp-main-content"]
            ),
            Paragraph(
                """
                The hearing shall be scheduled in such a manner as to allow for adequate investigation of the controversy.
                """,
                styles["rc-aawp-main-content"]
            ),
            Paragraph(
                "<b>REQUEST FOR HEARING IS TO BE MAILED TO:</b>",
                extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)
            ),
            Paragraph(
                "<b>GEORGIA DEPARTMENT OF DRIVER SERVICES <br />P.O. BOX 80447 <br />CONYERS, GEORGIA 30013</b>",
                extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)
            ),
            Spacer(0, 38.4 * mm),
            Paragraph(
                "<b>DS-1189 (04/06)</b>",
                extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER)
            )
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