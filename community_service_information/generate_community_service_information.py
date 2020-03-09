import cStringIO

from document_specific_styles import *
from common.signatures import *
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT

def generate_community_service_information():
    cr =CSIReport()
    buff = cStringIO.StringIO()
    return cr.create_report(buff)


class CSIReport:
    def __init__(self, title=None, author=None):
        self.page_size = letter
        self.page_margin = (11.4 * mm, 8.4 * mm)
        self.sections = ["content_front", "content_back"]
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
            page_num.drawOn(canv, 0, 3.8*mm)
        
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


    def _section_content_front(self):
        pre_space = "&nbsp;"
        elems = [
            Spacer(0, 5.8 * mm),
            Table(
                [
                    [
                        Image('brookhaven.jpg', 48 * mm, 20* mm),
                        Table(
                            [
                                [
                                    Paragraph(
                                        """
                                        Judicial Correction Services, Inc. <br />
                                        34 Peachtree Street <br />
                                        Suite 1000 <br />
                                        Atlanta, GA 30303 <br />
                                        (404) 591-3180    Fax (404)478-9515
                                        """, 
                                        styles["rc-tdwp-main-header-box"]
                                    )
                                ],
                            ],
                            style=extend_table_style(styles["rc-main-table"], [
                                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                ("OUTLINE", (0, 0), (-1, -1), .1, "black"),
                                ("TOPPADDING", (0, 0), (-1, -1), 1.4 * mm),
                                ("BOTTOMPADDING", (0, 0), (-1, -1), 1.4 * mm),
                            ]),
                            colWidths=(82 * mm)
                        ),
                        None
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP")
                ]),
                colWidths=(60*mm, 82*mm, 51*mm)
            ),
            Paragraph(
                "COMMUNTITY SERVICE INFORMATION",                
                styles["rc-tdwp-main-header"]
            ),            
            Paragraph(
                pre_space*6 + """You are responsible for requesting a statement on agency letterhead providing the 
                supervisor's name, telephone number, and confirming that they are a non-profit organization.""",
                extend_style(styles["rc-tdwp-main"], fontSize=12)
            ),
            Paragraph(
                "** All hours ordered must be done with the same agency, unless approved in advance by your probation officer.",
                extend_style(styles["rc-tdwp-main"], spaceBefore=12)
            ),
            Paragraph(
                "<u>The following types of activities qualify as Community Service Work possibilities:</u>",
                extend_style(styles["rc-tdwp-main"], spaceBefore=10)
            ),
            Spacer(0, 3.6 * mm),
            Table(
                [
                    [
                        Paragraph("1. American Canner Society", styles["rc-tdwp-main-tb"]),
                        Paragraph("6. Parks-city, county", styles["rc-tdwp-main-tb"])
                    ],
                    [
                        Paragraph("2. Disable Veteran's Center", styles["rc-tdwp-main-tb"]),
                        Paragraph("7. Public Library", styles["rc-tdwp-main-tb"])
                    ],
                    [
                        Paragraph("3. American Red Cross", styles["rc-tdwp-main-tb"]),
                        Paragraph("8. Salvation Army", styles["rc-tdwp-main-tb"])
                    ],
                    [
                        Paragraph("4. Civil Defense", styles["rc-tdwp-main-tb"]),
                        Paragraph("9. YMCA", styles["rc-tdwp-main-tb"])
                    ],
                    [
                        Paragraph("5. Government Agencies", styles["rc-tdwp-main-tb"]),
                        Paragraph("10. Community Centers", styles["rc-tdwp-main-tb"])
                    ],
                    [
                        Paragraph(
                            """
                            a. Police Departments <br />
                            b. Fire Departments <br />
                            c. Sheriff Departments
                            """, 
                            extend_style(styles["rc-tdwp-main-tb"], leftIndent=38)),
                        Paragraph("11. Homeless Shelters", styles["rc-tdwp-main-tb"])
                    ],
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 5), (-1, -1), "TOP"),
                ]),
                colWidths=(75*mm, 118*mm)
            ),
            Paragraph(
                "<u>No: Online, churches, hospitals, nursing homes, or schools are approved community service locations.</u>",
                extend_style(styles["rc-tdwp-main"], fontSize=12, spaceBefore=12)
            ),
            Paragraph(
                "These activities must be performed for a NON-PROFIT 501c3 or GOVERNMENTAL organization and at no time can payment for these services be given. You can find additional volunteer locations at <u>WWW.UnitedWay.ORG</u>.",
                extend_style(styles["rc-tdwp-main"], spaceBefore=12)
            ),
            Paragraph(
                "The types of work can range from:",
                extend_style(styles["rc-tdwp-main"], spaceBefore=10)
            ),
            Table(
                [
                    [
                        Paragraph("1.", styles["rc-tdwp-main-tb"]),
                        Paragraph("Clerical work", styles["rc-tdwp-main-tb"])                        
                    ],
                    [
                        Paragraph("2.", styles["rc-tdwp-main-tb"]),
                        Paragraph("Grounds maintenance, litter pick-up, yard work; gardening, landscape, making highway signs, street and highway maintenance.", styles["rc-tdwp-main-tb"])
                    ],
                    [
                        Paragraph("3.", styles["rc-tdwp-main-tb"]),
                        Paragraph("Custodial and building maintenance, janitorial work, painting.", styles["rc-tdwp-main-tb"])
                    ],
                    [
                        Paragraph("4.", styles["rc-tdwp-main-tb"]),
                        Paragraph("General labor, processing recyclable items, housekeeping, warehouse work, packing and distributing food, serving meals, kitchen help, carpentry, graphics and research:", styles["rc-tdwp-main-tb"])
                    ],
                    [
                        Paragraph("5.", styles["rc-tdwp-main-tb"]),
                        Paragraph("Human services, patient services, visiting senior citizens, assisting disabled veterans and seniors, teacher's aide", styles["rc-tdwp-main-tb"])                        
                    ]
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]),
                colWidths=(7*mm, 166*mm)
            ),
            Paragraph(
                """
                The person supervising your activity must certify the volunteer work that you perform by verifying and signing your timesheet each day you volunteer.
                <u>A final letter of verification on the agency letterhead or stationary must be provided once the required number of hours has been completed.</u>
                """, 
                extend_style(styles["rc-tdwp-main"], spaceBefore=12, fontSize=12)
            ),
            Spacer(0, .8 * mm),
            Table(
                [
                    [
                        Table(
                            [
                                [
                                    Paragraph("Agency", styles["rc-tdwp-main-tb"]),
                                    Paragraph("Telephone Number", styles["rc-tdwp-main-tb"])                        
                                ],
                                [
                                    Paragraph("Atlanta Food Bank", styles["rc-tdwp-main-tb"]),
                                    Paragraph("404 892-9822", styles["rc-tdwp-main-tb"])
                                ],
                                [
                                    Paragraph("Fulton County Parks and Recreation", styles["rc-tdwp-main-tb"]),
                                    Paragraph("770 306-3010, 404 808-5564", styles["rc-tdwp-main-tb"])
                                ],
                                [
                                    Paragraph("NFCC Thrift Store", styles["rc-tdwp-main-tb"]),
                                    Paragraph("770 640-0399", styles["rc-tdwp-main-tb"])
                                ],
                                [
                                    Paragraph("Project Open Hand Atlanta", styles["rc-tdwp-main-tb"]),
                                    Paragraph("404 872 8089", styles["rc-tdwp-main-tb"])
                                ],
                                [
                                    Paragraph("Atlanta Humans Society", styles["rc-tdwp-main-tb"]),
                                    Paragraph("404 974-2842", styles["rc-tdwp-main-tb"])
                                ],
                                [
                                    Paragraph("Salvation Army", styles["rc-tdwp-main-tb"]),
                                    Paragraph("770-830-0120", styles["rc-tdwp-main-tb"])
                                ],
                                [
                                    Paragraph("College Park City Recreation Dept", styles["rc-tdwp-main-tb"]),
                                    Paragraph(
                                        """
                                        Brady Center 404 669-3776 <br />
                                        Conley Center 404 669-3993 <br />
                                        Godby Road 404 669-9206 <br />
                                        """, styles["rc-tdwp-main-tb"])
                                ],
                                [
                                    Paragraph("Atlanta Center for Self Sufficiency 458 Edgewood", styles["rc-tdwp-main-tb"]),
                                    Paragraph("404 446-4680 or 874 8001 Ext 1120 Alison Maddox", styles["rc-tdwp-main-tb"])
                                ],
                                [
                                    Paragraph("Fulton County Public Library 1 Margaret Mitchell", styles["rc-tdwp-main-tb"]),
                                    Paragraph("404 730-1965", styles["rc-tdwp-main-tb"])
                                ],
                                [
                                    Paragraph("Mark Wade Fulton Country Jail", styles["rc-tdwp-main-tb"]),
                                    Paragraph("404 472-5639", styles["rc-tdwp-main-tb"])
                                ],
                                [
                                    Paragraph("Daily Bread for A.ll Credo Credolawson 8 to 6 pm 770905-2866", styles["rc-tdwp-main-tb"]),
                                    Paragraph("1234 Beaver Ruin Rd Suite 204 Norcross; 385 Born St. Ste D Lawrenceville; 5891 New P'tree Rd. Dorvaille", styles["rc-tdwp-main-tb"])
                                ]
                            ],
                            style=extend_table_style(styles["rc-main-table"], [
                                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                ("GRID", (0, 0), (-1, -1), 0.1 * mm, "black"),
                                ("LEFTPADDING", (0, 0), (-1, -1), 2 * mm),
                                ("RIGHTPADDING", (0, 0), (-1, -1), 2 * mm),
                            ]),
                            colWidths=(80*mm, 85*mm)
                        ),
                        None
                    ]
                ],
                style=styles["rc-main-table"],
                colWidths=(170*mm, 28*mm)
            ),
            PageBreak()
        ]
        return elems

    def _section_content_back(self):
        elems = [
            Paragraph(
                """
                AMERICAN CANCER SOCIETY - 770/419-DOE3  <br />
                AMERICAN HEART ASSOCIATION - 678/224-2000  <br />
                AMERICAN HUMAN SOCIETY 404 974-2847 01:32 WEDNESDAY 9:30 <br />
                AMERCIAN LEGIN-AWARDALE EST 404 292-288 <br />
                AMERICAN RED CROSS - 770/852-4318 <br />
                ANGEL FLIGHT- DEKAL PEACHTREE AIRPORT- 770/452-7958 <br />
                ANIMAL SHELTERS / ANIMAL RESCUE ORGANIZATIONS  <br />
                ATLANTA BOTANICAL GARDENS - 404/591-1548 <br />
                ATLANTA COMMUNITY FOOD BANK - 404/892-3333 <br />
                ATLANTA MISSION - ATLANTA - 404/588-4000 <br />
                ATLANTA MISSION/MARIETTA THRIFT STORE - MARIETTA - 404/357-3920 <br />
                ATLANTA WILD ANIMAL RESCUE - LITHONIA - (<u>www.awareone.org</u>) 678/418-1111 <br />
                AUTREY MILL NATURE PRESERVE & HERITAGE CENTER - JOHN'S CREEK - 678/366-3511 <br /> 
                BE SOMEONE, INC. - STONE MOUNTAIN -770/465-644S <br />
                BLESSED ANGELS, INC - AUSTELL - 404/323-1156 - (CHRISTINE WASHINGTON) <br />
                BOY SCOUTS OF AMERICA - ATLANTA - 770/956-3176 <br />
                BOYS & GIRLS CLUB OF ATLANTA - 404/527-7115 <br />
                BUCKHEAD CHRISTIAN MINISTRY 404/239-0058 x 111 <br />
                CHASTIAN PARK CONSERVANCY - 404/237-2177 <br />
                CHEROKEE COUNTY HUMANE SOCIETY THRIFT STORE - ACWOFCTH - 770/592-8072  <br />
                CHILDREN'S RESTORATION NETWORK - ROSWELL - 770/393-7117 <br />
                CHILDREN'S WISH FOUNDATION - ATLANTA - 770/393-0683 <br /><br />
                COBS CHRISTMAS - MARIETTA - 678/439-9627 <br />
                COMMUNITY FELLOWSHIP HOMELESS MINISTRY - 404/428-8243  <br />
                DAUSET TRAILS NATURE CENTER - BUTTS COUNTY - 770/775-6798  <br />
                DIABETES ASSOC - ATLANTA 404/527-7150 x 119 <br />
                ELACHEE NATURE SCIENCE CENTER - GAINESVILLE - 770/535-1976 <br />
                FAIR OAKS UNITED METHODIST CHURCH - MARIETTA - 770/428-2658 (ENGLISH/SPANISH/BRAZILLAN)  <br />
                FAITH EQUESTRIAN THERAPEUTIC CENTER - EFFINGHAM COUNTY - 912/728-3728 <br />
                FEED MY LAMBS - MARIETTA - 770/795-9349  <br />
                FEEDING GOD'S CHILDREN MINISTRY - MARIETTA - 404/384-5095 (PASTOR BYNUM)  <br />
                FORGOTTEN PAWS RESCUE (<u>www.forgottenpaws.com</u>) <br />
                FORT YARGO STATE PARK - WINDER - 770/867-3489 <br />
                FOUNDATION FOR HOSPITAL ART - ATLANTA - (<u>www.hospitalart.com</u>) 678/324-1705  <br />
                GIRL SCOUTS OF GREATER ATLANTA - 770/702-9100  <br />
                HABITAT FOR HUMANITY METRO ATLANTA - 770/432-7954 <br />
                HAND MAIDANS MMISTRIES FOOD PAHTN 770 990-2373
                HANDS ON ATLANTA - 404/979-2800 <br />
                HELPING IN HIS NAME MINISTRIES FOOD PANTRY - HENRY COUNTY - 678/565-6135  <br />
                HAVEN HILLS THERAPEUTIC RIDING CENTER - FAIRBURN - 578/296-9693 <br />
                HOMELESS PETS FOUNDATION - MARIETTA - 770/971-0100 <br />
                H.O.P.E. THROUGH DIVINE INTERVENTION - ATLANTA - 404/748-4375 <br />
                HOSEA FEED THE HUNGRY - ATLANTA - 404/755-3353 x 315 <br />
                IN THE MEAN TIME MINISTRIES (SHEPHERD'S HOUSE) - MARIETTA - 770/792-0097 (<u>www.inthemeantime.org</u>) <br />
                JERUSALEM HOUSE - ATLANTA - 404/377-3443 <br />
                KEEP SMYRNA BEAUTIFUL(RECYCLING CENTER) - SIVIYRINLA - 770/431-2863 <br />
                KENNESAW MOUNTAIN NATIONAL PARK - 770/427-4685 <br />
                LIFELINE ANIMAL PROJECT - ATLANTA - (<u>www.info@atlantapets.org</u>) - 404/292-8800 <br />
                LOAVES & FISHES @ ST.JOHN'S ORTHODOX CHURCH - ATLANTA - 404/577-6330  <br />
                MCFCENNA FARMS - DALLAS - 770/433-9672 (<u>www.mckennafarmstherapy.org</u>) <br />
                MAKE A WAY HOUSING - ATLANTA - 404/792-3011 <br />
                MARCH OF DIMES - 404/350-9800 <br />
                MOSTLY MUTTS - KENNESAW - 770/325-7387 <br />
                MUST MINISTRIES - 770/427-9862 <br />
                NEVER ALONE MINISTRIES - WOODSTOCK - 770/363-5272 (<u>www.neveralone.org</u>) <br />
                NOAH'S ARK - LOCUST GROVE - 770/957-0888 <br />
                NORTH FULTON COMMUNITY CHARITIES - RDSWELL 770/64D-0399  <br />
                OUR FATHER'S HANDS - POWDER SPRINGS - 770/222/6775 <br />
                OUR PAL'S PLACE - MARIETTA - 678/795-0202 <br />
                P.A.L.S (PETS ARE LOVING SUPPORT) - ATLANTA - 404/875-PALS  <br />
                PAWS ATLANTA - DECATUR - 770/593-115S <br />
                PICK OF THE LITTER - HIRAM -678/977-4925 (<u>www.ourpickofthelitter.com</u>)  <br />
                PREDMONT PANK CANSENANCY 404 875-7275 ext 247 <br />
                RIGHT IN THE COMMUNITY - MARIETTA - 770/427-8401 <br />
                ROSWELL RECYCLING CENTER 770 442-8822 <br />
                SAFERIDE - 404 888-0887 <br />
                SCATTERING RESOURCES - SMYRNA - 678/729-7228 <br /> 
                """,
                extend_style(styles["rc-tdwp-main-list"])
            )            
        ]
        return elems