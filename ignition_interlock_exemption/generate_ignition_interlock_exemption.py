import cStringIO
from document_specific_styles import *

class IIEReport:
    def __init__(self, pdf_dict, title=None, author=None):
        self.page_size = letter
        self.page_margin = (9.4 * mm, 7.8 * mm)
        self.sections = ["head", "content"]
        self.title = title
        self.author = author
        self.data = None
        self.pdf_dict = pdf_dict

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
                extend_style(styles["rc-aawp-main-content"], alignment=TA_CENTER, fontSize=8),
            )
            page_num.wrapOn(canv, self.page_size[0], 0)
            page_num.drawOn(canv, 0, 4.8 * mm)

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

    def _section_head(self):
        elems = list()
        # TEST_DATA = "Test Data"
        elems += [
            Table(
                [
                    [
                        Image('brookhaven.jpg', 16 * mm, 14 * mm),
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
                                [
                                    None
                                ],
                                [
                                    Paragraph(
                                        "IGNITION INTERLOCK EXEMPTION",
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
                                ],
                            ],
                            style=extend_table_style(styles["rc-main-table"], [
                                ("VALIGN", (0, 0), (-1, -1), "TOP")
                            ]),
                        ),
                        Paragraph(
                            "",
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
            Spacer(0, 2 * 4.2 * mm),
        ]

        return elems

    def _section_content(self):
        pre_space = "&nbsp;" * 11
        elems = [
            Table(
                [
                    [
                        Paragraph(
                            """
                            <b>Case Number:</b>
                            %s <br />
                            <br />
                            """ % self.pdf_dict["case_number"],
                            extend_style(styles["rc-main-rmt-addr"])
                        ),

                        Paragraph(
                            """
                            CITY OF BROOKHAVEN<br />
                            VS<br />
                            %s, Defendant
                            """ % self.pdf_dict["defendant_name"],
                            extend_style(styles["rc-main-rmt-addr"])
                        ),
                    ],
                ],
                colWidths=(98 * mm, 82 * mm),
                style=(
                    ('VALIGN', (0, 0), (0, 0), 'TOP'),
                )
            ),
            Spacer(0, 2 * 4.2 * mm),
        ]

        charges_data = \
            [
                [
                    Paragraph("<b>Charges:</b>", extend_style(styles["rc-main-rmt-addr"], alignment=TA_RIGHT)),
                    Paragraph(
                        """
                        %s<br />
                        """ % self.pdf_dict["charges"][0],
                        extend_style(styles["rc-main-rmt-addr"])
                    )
                ]
            ]
        for i in range(1, len(self.pdf_dict["charges"])):
            charges_data += \
                [
                    [
                        Paragraph("", extend_style(styles["rc-main-rmt-addr"], alignment=TA_RIGHT)),
                        Paragraph(
                            """
                             %s<br />
                             """ % self.pdf_dict["charges"][i],
                            extend_style(styles["rc-main-rmt-addr"])
                        )
                    ]
                ]

        elems += [
            Table(
                charges_data,
                colWidths=(35 * mm, 173 * mm),
                style=(
                    ('VALIGN', (0, 0), (0, 0), 'TOP'),
                )
            ),
        ]

        order_date = self.pdf_dict["order_date"]
        order_year_str = order_date.year
        order_month_str = order_date.strftime('%B')
        order_day = order_date.day
        if order_day % 10 == 1 and order_day // 10 != 1:
            order_day_str = str(order_day) + "st"
        elif order_day % 10 == 2 and order_day // 10 != 1:
            order_day_str = str(order_day) + "nd"
        elif order_day % 10 == 3 and order_day // 10 != 1:
            order_day_str = str(order_day) + "rd"
        else:
            order_day_str = str(order_day) + "th"

        order_date_string = "%s of %s, %s" % (order_day_str, order_month_str, order_year_str)

        elems += [
            Spacer(0, 4 * 4.2 * mm),
            Paragraph(
                "Order Exempting Defendant",
                styles["rc-header"]
            ),
            Paragraph(
                "From Ignition Interlock Device",
                styles["rc-header"]
            ),
            Paragraph(
                "Requirements of O.C.G.A & 42-8-111",
                styles["rc-header"]
            ),

            Spacer(0, 4.2 * mm),
            Paragraph(
                pre_space + """
                This court finds that imposition of the ignition interlock device requirements set forth in O.C.G.A & 42-8-111 would 
                subject the above named defendant to undue financial hardship. Accordingly, the court hereby exempts said defendant
                from the ignition interlock device requirements of O.C.G.A & 42-8-111.
            """,
                styles["rc-tdwp-main"]
            ),

            Spacer(0, 4.2 * mm),
            Paragraph(
                pre_space + """So ordered. this the %s.""" % order_date_string,
                styles["rc-tdwp-main"]
            ),

            Spacer(0, 2 * 12.4 * mm),
            Table(
                [
                    [
                        None, Paragraph("Judge", styles["judge-signature"]), None
                    ],
                    [
                        None, Paragraph("BROOKHAVEN MUNICIPAL COURT", styles["judge-signature"]), None
                    ],
                ],
                style=extend_table_style(styles["rc-main-table"], [
                    ("LINEABOVE", (1, 0), (1, 0), 0.1, "black"),
                ]),
                colWidths=(85 * mm, 96 * mm, 8 * mm),
            )
        ]
        return elems


def generate_ignition_interlock_exemption(pdf_dict):
    cr = IIEReport(pdf_dict)
    buff = cStringIO.StringIO()
    return cr.create_report(buff)