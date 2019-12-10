# This Python file uses the following encoding: utf-8
import cStringIO

from document_specific_styles import *


def generate_cash_appearance_bond_report():
    buff = cStringIO.StringIO()
    doc = BaseDocTemplate(buff, pagesize=letter)
    f = Frame(x, y, usable_width, usable_height, showBoundary=0,
              topPadding=0.76*cm, bottomPadding=0.76*cm,
              rightPadding=1.27*cm, leftPadding=1.27*cm
              )

    story = _create_story()

    main_template = PageTemplate(id="main_template", frames=[f])
    doc.addPageTemplates([main_template])
    doc.build(story, canvasmaker=PageNumCanvas)

    buff.seek(0)
    return buff


def _create_story():
    story = []

    story.append(
        Paragraph(
            "APPEARANCE BOND – CITY OF BROOKHAVEN – DEKALB COUNTY – STATE OF GEORGIA",
            style = extend_style(
                styles["heading"],
                fontName="Arial-Bold",
                fontSize=11,
                spaceAfter=10
            )
        )
    )

    story.append(
        Paragraph(
            """
            Be it known that <u><b>{}</b></u>, <b>Principal</b> and <u><b>{}</b></u> <b>Surety</b>,
            are held and firmly bound to the City of Brookhaven, and if transferred,
            to his Excellency, Governor of the State of Georgia, and its successors in office,
            in the penal sum written below, for payment whereof, we firmly bind ourselves,
            our heirs, executors and administrators, jointly and severally.
            """.format("ANA MEDRANO-SORIA", "IVO FRANCISCO BAKOVIC GUZMAR"),
            style = extend_style(
                styles["detail-mini"],
                fontName="Arial",
                leading=10.8
            )
        )
    )

    story.append(
        Paragraph("BOND TYPE: CASH",
                  style=extend_style(
                      styles["body"],
                      fontName="Arial-Bold",
                      fontSize=11,
                      leading=13,
                      alignment=TA_CENTER,
                      spaceBefore=10
                  )
        )
    )

    bond_table = _create_bond_type_table()
    story.append(bond_table)

    story.append(
        Paragraph("<u>CONDITIONS OF BOND</u>",
                  style=extend_style(
                      styles["body"],
                      fontName="Arial-Bold",
                      fontSize=11,
                      leading=13,
                      alignment=TA_CENTER,
                      spaceBefore=10,
                      spaceAfter=15
                  )
        )
    )

    conditions = _get_bond_conditions()
    story.append(conditions)

    story.append(
        Paragraph(
            """
            IN WITNESS WHEREOF, Surety has executed this bail bond at Brookhaven, Georgia, DeKalb County, Georgia,
            on the date above and acknowledges receipt of the same.
            """,
            style = extend_style(
                styles["detail-mini"],
                fontName="Arial",
                leading=10.8,
                spaceBefore=10
            )
        )
    )

    info_table = _create_general_info_table()
    story.append(info_table)

    story.append(
        Paragraph(
            """
            NOTE:  SHOULD DEFENDANT OR SURETY’S MAILING ADDRESS CHANGE, IT SHALL BE THE INDIVIDUAL’S RESPONSIBILITY TO
            NOTIFY THE CLERK OF COURT IN WHICH THE CHARGES ARE PENDING.  FAILING TO NOTIFY THE CLERK’S OFFICE OR FAILURE
            TO APPEAR MAY RESULT IN THE ISSUANCE OF A BENCH WARRANT AGAINST THE DEFENDANT FOR HIS/HER REARREST AS REQUIRED
            BY LAW, SUSPENSION OF HIS/HER DRIVER’S LICENSE AND FORFEITURE OF CASH BOND BY OPERATION OF LAW.
            IF APPLICABLE, REFUNDS ARE PROCESSED 30 DAYS AFTER FINAL DISPOSITION. QUESTIONS, CALL 404-637-0660.
            """,
            style=extend_style(
                styles["body"],
                fontName="Arial-Bold",
                fontSize=10,
                leading=12,
                spaceBefore=0,
                leftIndent=0,
                rightIndent=0,
                spaceAfter=10
            )
        )
    )

    footer = _create_footer()
    story.append(footer)

    return story


def _create_footer():
    data = [
        [
            Paragraph("ORIGINAL-COURT", style=extend_style(
                styles["body"],
                fontName="Arial-Bold",
                fontSize=10,
                leading=13,
                spaceBefore=10
            )),
            Paragraph("COPY-SURETY/DEFENDANT", style=extend_style(
                styles["body"],
                fontName="Arial-Bold",
                fontSize=10,
                leading=13,
                spaceBefore=10
            ))
        ]
    ]

    table = Table(data)
    table.setStyle(extend_table_style(
        styles['iv-main-table'],
        [
            ('LEFTPADDING', (0, 0), (0, 0), 120)
        ]
    )
    )

    return table


def _create_general_info_table():
    data = [
        [
            Paragraph("", style = extend_style(styles["detail-mini"], fontName="Arial", leading=10.8)),
            "",
            Paragraph("CASH BOND may be applied to fine", style = extend_style(styles["detail-mini"], fontName="Arial", leading=10.8))
        ],
        [
            Paragraph("Principal (or) Surety’s Signature", style = extend_style(styles["detail-mini"], fontName="Arial", leading=10.8)),
            "",
            Paragraph("<u>{}</u>-<u>{}</u>=<u>{}</u>".format("&nbsp;"*16, "&nbsp;"*24, "&nbsp;"*24),
                      style = extend_style(styles["detail-mini"], fontName="Arial", leading=10.8))
        ],
        [
            Paragraph("Current Street Address", style = extend_style(styles["detail-mini"], fontName="Arial", leading=10.8)),
            "",
            Paragraph("<b>OR</b>", style = extend_style(styles["detail-mini"], fontName="Arial", leading=10.8))
        ],
        [
            Paragraph("Current City, State, Zip", style = extend_style(styles["detail-mini"], fontName="Arial", leading=10.8)),
            "",
            Paragraph("CASH BOND may be refunded to", style = extend_style(styles["detail-mini"], leading=10.8))
        ],
        [
            Paragraph("Current Phone Number", style = extend_style(styles["detail-mini"], fontName="Arial", leading=10.8)),
            "",
            Paragraph("<u>{}</u>Surety OR<u>{}</u>Principal".format("&nbsp;"*10, "&nbsp;"*12),
                      style = extend_style(styles["detail-mini"], fontName="Arial", leading=10.8))
        ],
        [
            Paragraph("Signed and Acknowledged in the presence of:", style = extend_style(styles["detail-mini"], fontName="Arial", leading=10.8)),
            "", ""
        ],
        [
            Paragraph("City of Brookhaven Representative", style = extend_style(styles["detail-mini"], fontName="Arial", leading=10.8)),
            "", ""
        ]
    ]

    row_heights=[11*mm]*6
    row_heights[0] = 8*mm
    row_heights.append(8*mm)
    table = Table(data, colWidths=[190, 100, None], rowHeights=row_heights)
    table.setStyle(
        extend_table_style(
            styles['iv-main-table'],
            [
                ('LINEABOVE', (0, 1), (0, 4), 1, colors.black),
                ('LINEABOVE', (0, -1), (0, -1), 1, colors.black),
                ('VALIGN', (0, 1), (0, -1), 'TOP'),
                ('LEFTPADDING', (2, 2), (2, 2), 60)
            ]
        )
    )

    return table


def _get_bond_conditions():
    list_ = ListFlowable(
        [
        ListItem(
            Paragraph(
                """
                If the above bound Principal shall personally be and appear before the <b>Municipal
                Court of Brookhaven</b>, or any other Court in which the case may be transferred or pending,
                from day to day, and from term to term, to then and there answer to an indictment
                and/or accusation for the offender (s) named above, or any included or related offenses
                therein with which he/she may stand charged and shall not depart thence without leave
                of Court, then the above obligation to be null and void, else to remain in full force and
                virtue; and
                """,
                style=extend_style(
                    styles["detail-mini"],
                    fontName="Arial",
                    leading=10.8,
                    spaceAfter=10
                )
            )
        ),
        ListItem(
            Paragraph(
                """
                Principal and Surety agree and covenant that this cash bond is conditioned upon
                the appearance of the Principal before the Court at the time fixed for his/her
                arraignment as required by the Code of Georgia Sec. 17-6-17 and Sec. 17-7-91; and
                """,
                style=extend_style(
                    styles["detail-mini"],
                    fontName="Arial",
                    leading=10.8,
                    spaceAfter=10
                )
            )
        ),
        ListItem(
            Paragraph(
                """
                Principal <b>MUST APPEAR</b> before the <b>Municipal Court of Brookhaven</b> on <i><b>{}</b></i>
                AT <i><b>{}</b></i> to answer to the above charges.  If the Principal at any time fail to appear at his/her
                arraignment or pending trial a bench warrant will issue for his/her arrest.
                Failing to appear will result in a <b>non-refundable</b> ${} FTA fee and <b>non-refundable</b>
                ${} WARRANT fee applied to the case.
                """.format("3/28/2016", "1 PM", "100", "100"),
                style=extend_style(
                    styles["detail-mini"],
                    fontName="Arial",
                    leading=10.8,
                    spaceAfter=10
                )
            )
        ),
        ListItem(
            Paragraph(
                """
                <u>THE CASH BOND POSTED ABOVE ON BEHALF OF THE PRINCIPAL IS AN AGREEMENT BETWEEN THE PRINCIPAL AND SURETY.
                IF PRINCIPAL FAIL TO APPEAR FOR TRIAL AND THIS BOND IS FORFEITED, THE UNDERSIGNED SURETY HEREBY WAIVE
                SEIRE FACIAS, RULE NISI, RULE ABSOLUTE, JUDGEMENT AND AGREE THAT THE CASH BOND BE PUT UP AT ONCE, WITHOUT
                ANY NOTICE WHATEVER AND DISTRIBUTED AS THE LAW PROVIDES FOR THE PERFECTED FORFEITED RECOGNIZANCES.</u>
                """,
                style=extend_style(
                    styles["detail-mini"],
                    fontName="Arial-Bold",
                    leading=10.8
                )
            )
        )
        ],
        style=extend_list_style(bulletFontName="Arial", bulletFontSize=9)
    )

    data = [[list_]]
    table = Table(data)
    table.setStyle(
        extend_table_style(
            styles['iv-main-table'],
            [
                ('LEFTPADDING', (0, 0), (0, 0), 20)
            ]
        )
    )

    return table


def _create_bond_type_table():
    data = [
        [
            Paragraph("DATE: <u><i><b>{}</b></i></u>".format("02-25-2016"),
                      style=extend_style(
                          styles["detail"],
                          fontName="Arial",
                          leading=12,
                          leftIndent=0,
                          rightIndent=0,
                      )
            ),
            Paragraph("BOND AMOUNT: $ <u><i><b>{}</b></i></u>".format("908.00"),
                      style=extend_style(
                          styles["detail"],
                          fontName="Arial",
                          leading=12,
                          leftIndent=0,
                          rightIndent=0,
                      )
            )
        ],
        [
            Paragraph("CHARGES: <u><i><b>{}</b></i></u>".format("NO LICENSE & CROSSWALKS"),
                      style=extend_style(
                          styles["detail"],
                          fontName="Arial",
                          leading=12,
                          leftIndent=0,
                          rightIndent=0,
                      )
            ),
            Paragraph("CASE/CITATION No. (s) <u><i><b>{}</b></i></u>".format("E25670 & E25672"),
                      style=extend_style(
                          styles["detail"],
                          fontName="Arial",
                          leading=12,
                          leftIndent=0,
                          rightIndent=0,
                      )
            )
        ]
    ]

    table = Table(data, spaceBefore=0, rowHeights=[7*mm, 10*mm])
    table.setStyle(styles['iv-main-table'])

    return table
