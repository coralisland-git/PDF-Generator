import cStringIO

from common.signatures import *
from document_specific_styles import *
import datetime

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


def generate_ignition_interlock_court_order(data_mapping):
    buff = cStringIO.StringIO()
    doc = SignatureDocTemplate(buff, pagesize=letter)
    f = Frame(gutters[0], gutters[2], usable_width, usable_height, showBoundary=0)
    
    story = []
    story += header(data_mapping)
    story += case_header(data_mapping)
    story+= body(data_mapping)

    main_template = PageTemplate(id="main_template", frames=[f])
    doc.addPageTemplates([main_template])
    doc.build(story, canvasmaker=PageNumCanvas)
    del doc

    buff.seek(0)
    return buff

def header(data_dict):
    story = []
    story.append(
        Table(
            [
                [
                    Image('brookhaven.jpg', 40 * mm, 14 * mm),
                    Table(
                        [
                            [
                                Paragraph(
                                    """                                        
                                    <b>BROOKHAVEN MUNICIPAL COURT</b> <br />
                                    2665 BUFORD HWY BROOKHAVEN, GA 30324 <br />
                                    PHONE: 404-637-0660 <br />
                                    FAX: (404) 671-3410
                                    """,
                                    extend_style(styles['rc-aawp-main-header'])
                                )
                            ],
                            [Spacer(0,7*mm)],
                            [
                                Paragraph(
                                    "IGNITION INTERLOCK COURT ORDER",
                                    styles["rc-doc-header"]
                                )
                            ],
                            [
                                Paragraph(
                                    """
                                    STATE OF GEORGIA <br />
                                    DEKALB COUNTY   <br />
                                    CITY OF BROOKHAVEN
                                    """,
                                    extend_style(styles["rc-doc-header"], fontSize=12)
                                )
                            ]
                        ],
                        style=extend_table_style(styles["rc-main-table"], [
                            ("VALIGN", (0, 0), (-1, -1), "TOP")
                        ]),
                    ),
                    Paragraph(
                        """
                        """,
                        extend_style(styles['rc-aawp-main-header'], alignment=TA_RIGHT, fontSize=9)
                    )
                ]
            ],
            style=extend_table_style(styles["rc-main-table"], [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (0, 0), 12 * mm),
                ("TOPPADDING", (2, 0), (2, 0), 1.2 * mm),
            ]),
            colWidths=(42 * mm, 112 * mm, 43 * mm)
        ),
    )
    return story

def case_header(data_dict):
    story = []
    story += [
        Table(
            [
                [
                    Table(
                        [
                            [
                                Paragraph(
                                    """
                                    <b>
                                    STATE OF GEORGIA <br />
                                    VS <br />
                                    %s <br />
                                    
                                    </b>
                                    """ % data_dict['name'],
                                    extend_style(styles['rc-aawp-main-content'])
                                )
                            ]
                        ],
                        style=extend_table_style(styles["rc-main-table"], [
                            ("VALIGN", (0, 0), (-1, -1), "TOP")
                        ]),
                    ),
                    Spacer(0,0),
                    Table(
                        [
                            [
                                Paragraph("<b>Case No.:</b> %s" % data_dict['case_number'], styles['rc-aawp-main-content']),
                            ],
                            [
                                Paragraph("<b>Citation No.:</b> %s" % ", ".join(data_dict['citation_number']), styles['rc-aawp-main-content']),
                            ],
                            [
                                Paragraph("<b>Lic. No.:</b> %s" % data_dict['license_number'], styles['rc-aawp-main-content']),
                            ]
                        ],
                        style=extend_table_style(styles["rc-main-table"], [
                            ("VALIGN", (0, 0), (-1, -1), "TOP")
                        ]),
                        rowHeights=6.2 * mm
                    ),
                ]
            ],
            style=extend_table_style(styles["rc-main-table"], [
                ("VALIGN", (0, 0), (-1, -1), "TOP")
            ]),
            colWidths=(90 * mm, 20 * mm, 90 * mm)
        ),
        Paragraph(
            """
            <b>Charge: </b> <br/>
            %s
            """ % "<br/>".join(data_dict['charge']),
            style=styles["rc-aawp-main-content"]
        )
    ]
    return story

def body(data_dict):
    story = []
    story += [
        Spacer(0,5*mm),
        Paragraph(
            """
            CERTIFICATE OF ELIGIBILITY FOR IGNITION <br/>
            INTERLOCK LIMITED DRIVING PERMIT
            """,
            extend_style(styles["rc-doc-header"], fontSize=12)
        ),
        Spacer(0,1.1*mm),
        Paragraph(
            """
            WHEREAS the above-named defendant is subject to a driver's license 
            suspension imposed pursuant to O.C.G.A. $40-5-63(a)(2) for a second conviction
            for a violation of O.C.G.A. $40-6-391 within five (5) years as calculated
            between the incident dates; and <br/>
            The Court having determined the following (please check only one box):
            """,
            extend_style(styles["rc-aawp-main-content"], fontSize=11)
        ),
        Spacer(0,5*mm),
        Table(
            [
                [
                    XBox(8,data_dict['check_box']['1']),
                    Paragraph(
                        """
                        The Defendant is authorized to obtain an ignition interlock 
                        limited driving permit, if eligible, because he/she served 
                        at least 120 days of the license suspension required for 
                        such conviction and is enrolled in a drug or DUI court
                        program in this Court;
                        """,
                        extend_style(styles["rc-aawp-main-content"], fontSize=11)
                    )
                ],
                [
                    XBox(8,data_dict['check_box']['2']),
                    Paragraph(
                        """
                        The Defendant is authorized to obtain to ignition interlock
                        limited driving permit, if eligible, because he/she has served
                        at least 120 days of the license suspension required for such
                        conviction and he/she is enrolled in clinical treatment as
                        provided in O.C.G.A $40-5-63.1 and 40-5-1 (16.2);
                        """,
                        style=extend_style(styles['rc-aawp-main-content'],alignment=TA_LEFT,fontSize=11)
                    )
                ],
                [
                    XBox(8,data_dict['check_box']['3']),
                    Paragraph(
                        """
                        The Defendant is not authorized to obtain an ignition interlock
                        limited driving permit until further notice from this Court;
                        """,
                        style=extend_style(styles['rc-aawp-main-content'], alignment=TA_LEFT,fontSize=11)
                    )
                ],
                [
                    XBox(8,data_dict['check_box']['4']),
                    Paragraph(
                        """
                        The Court waives the ignition interlock requirement because such would
                        subject the Defendant to undue financial hardship.
                        """,
                        style=extend_style(styles['rc-aawp-main-content'], alignment=TA_LEFT,fontSize=11)
                    )
                ]
            ],
            style=extend_table_style(styles["rc-main-table"], [
                ("VALIGN", (0, 0), (-1, -1), "TOP")
            ]),
            colWidths=(5*mm,180*mm),
        ),
        Spacer(0,5*mm),
        Paragraph(
            """
            The Court further finds as follows:
            """,
            style=extend_style(styles['rc-aawp-main-content'], alignment=TA_LEFT, fontSize=11)
        ),
        Paragraph(
            "%s" % data_dict["notes"],
            style=extend_style(styles['rc-aawp-main-content'], alignment=TA_LEFT, fontSize=9)
        ),
        Spacer(0,11*mm),
        Paragraph(
            """
            So ordered, this the {}.
            """.format(custom_strftime('{S} of %B, %Y', datetime.datetime.now())),
            style=extend_style(styles['rc-aawp-main-content'], alignment=TA_LEFT, fontSize=11)
        ),
        Spacer(0,5*mm),
        Table(
            [
                [
                    Paragraph("",
                              extend_style(styles['rc-aawp-main-content'], leftIndent=22 * mm)),
                    Paragraph("", styles['rc-aawp-main-content']),
                    Paragraph("", styles['rc-aawp-main-content']),
                ],
                [
                    None,
                    None,
                    Paragraph("Judge ", styles['rc-aawp-main-content']),
                ]
            ],
            style=extend_table_style(styles["rc-main-table"], [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LINEBELOW", (2, 0), (2, 0), 0.1, "black"),
            ]),
            colWidths=(100 * mm, 16 * mm, 81 * mm)
        ),

    ]
    return story

def suffix(d):
    return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))