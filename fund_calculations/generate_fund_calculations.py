# This Python file uses the following encoding: utf-8
import cStringIO

from document_specific_styles import *

ROW_HEIGHT = 6 * mm
table_row_num = 0


def generate_fund_calculations(pdf_dict):
    buff = cStringIO.StringIO()
    doc = BaseDocTemplate(buff, pagesize=letter)
    f = Frame(gutters[0], gutters[2], usable_width, usable_height, showBoundary=0, topPadding=15, )

    story = _create_story()

    main_template = PageTemplate(id="main_template", frames=[f])
    doc.addPageTemplates([main_template])
    doc.build(story, canvasmaker=FirstPageOnlyDatePageNumCanvas)
    # del doc

    buff.seek(0)
    return buff


def _create_story():
    story = []

    story.append(
        Paragraph("""<b>BROOKHAVEN MUNICIPAL COURT</b>""",
                  style=styles["heading"]
                  )
    )
    story.append(
        Paragraph("""<b>FUND CALCULATIONS FOR June 2019</b>""",
                  style=styles["subheading"]
                  )
    )

    doc_body = _create_main_table()
    story.append(doc_body)

    bottom_table = _create_bottom_table()
    story.append(bottom_table)

    return story


def _create_footer():
    data = [
        [
            Paragraph('', style=text_style),
            Paragraph('Chief Magistrate Judge Phinia Aten', style=text_style)
        ]
    ]

    table = Table(data, spaceBefore=20, colWidths=(None, 50 * mm))
    table.setStyle(extend_table_style(
        styles['iv-main-table'],
        [
            ('LINEABOVE', (1, 0), (1, 0), 1, colors.black)
        ]
    ))

    return table


def _create_main_table():
    data = [
        [  # 0
            '', '', '', '', '', ''
        ],
        [  # 1
            '',
            Paragraph('<b>Fund Name1</b>', style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('<b>Description</b>', style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('<b>No. of Cases</b>', style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('<b>Fund Amount Disbursed</b>', style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('<b>Total Fund Amount Disbursed</b>', style=extend_style(text_style, alignment=TA_CENTER)),
        ],

        [  # 2
            Paragraph('1', style=text_style),
            Paragraph('Peace Officer Annuity & benefit (deducted from base-line)', style=text_style),
            Paragraph('$4.01 - $ 25.00', style=text_style),
            Paragraph('46', style=text_style),
            Paragraph('$138', style=text_style),
            Paragraph('', style=text_style),
        ],
        [  # 3
            Paragraph('1', style=text_style),
            '',
            Paragraph('$25.01 - $50.00', style=text_style),
            Paragraph('52', style=text_style),
            Paragraph('208', style=text_style),
            Paragraph('', style=text_style),
        ],
        [  # 4
            Paragraph('1', style=text_style),
            '',
            Paragraph('$50.01 - $100.00', style=text_style),
            Paragraph('62', style=text_style),
            Paragraph('310', style=text_style),
            Paragraph('', style=text_style),
        ],
        [  # 5
            Paragraph('1', style=text_style),
            '',
            Paragraph('$100.01 AND OVER', style=text_style),
            Paragraph('268', style=text_style),
            Paragraph('3899.59', style=text_style),
            Paragraph('', style=text_style),
        ],
        [  # 6
            Paragraph('1', style=text_style),
            '',
            Paragraph('Partial Payments', style=text_style),
            Paragraph('7', style=text_style),
            Paragraph('145.51', style=text_style),
            Paragraph('4701.10', style=text_style),
        ],
        [  # 7
            Paragraph('2', style=text_style),
            Paragraph('Peace Officer Training <br /> 15-21-73(A) (Surcharge)', style=text_style),
            Paragraph('$1.00 - $499.00', style=text_style),
            Paragraph('334', style=text_style),
            Paragraph('4046.26', style=text_style),
            Paragraph('', style=text_style),
        ],

        [  # 8
            Paragraph('2', style=text_style),
            '',
            Paragraph('$500+', style=text_style),
            Paragraph('59', style=text_style),
            Paragraph('2950', style=text_style),
            Paragraph('', style=text_style),
        ],
        [  # 9
            Paragraph('2', style=text_style),
            '',
            Paragraph('Partial Payments', style=text_style),
            Paragraph('10', style=text_style),
            Paragraph('208.12', style=text_style),
            Paragraph('', style=text_style),
        ],
        [  # 10
            Paragraph('2', style=text_style),
            Paragraph('Appearance Bond Forfeited', style=text_style),
            Paragraph('Less than $1000', style=text_style),
            Paragraph('0', style=text_style),
            Paragraph('0.00', style=text_style),
            Paragraph('', style=text_style),
        ],
        [  # 11
            Paragraph('2', style=text_style),
            '',
            Paragraph('Greater than $1000', style=text_style),
            Paragraph('0', style=text_style),
            Paragraph('0.00', style=text_style),
            Paragraph('7204.38', style=text_style),
        ],
        [  # 12
            Paragraph('3', style=text_style),
            Paragraph('Indigent Defense Fund <br /> 15-21-73(B) (Surcharge)', style=text_style),
            Paragraph('Full Pays', style=text_style),
            Paragraph('393', style=text_style),
            Paragraph('8212.67', style=text_style),
            Paragraph('', style=text_style),
        ],

        [  # 13
            Paragraph('3', style=text_style),
            '',
            Paragraph('Partial Payments', style=text_style),
            Paragraph('9', style=text_style),
            Paragraph('181.45', style=text_style),
            Paragraph('', style=text_style),
        ],
        [  # 14
            Paragraph('3', style=text_style),
            Paragraph('Appearance Bond Forfeitures', style=text_style),
            Paragraph('Less than $1000', style=text_style),
            Paragraph('0', style=text_style),
            Paragraph('0.00', style=text_style),
            Paragraph('', style=text_style),
        ],
        [  # 15
            Paragraph('3', style=text_style),
            Paragraph('Appearance Bond Forfeitures', style=text_style),
            Paragraph('Greater than $1000', style=text_style),
            Paragraph('0', style=text_style),
            Paragraph('0.00', style=text_style),
            Paragraph('8394.12', style=text_style),
        ],
        [  # 16
            Paragraph('4', style=text_style),
            Paragraph('GA Crime Victimes Emergency <br /> 15-21-112(Surcharge)', style=text_style),
            Paragraph('$25', style=text_style),
            Paragraph('4', style=text_style),
            Paragraph('0.00', style=text_style),
            Paragraph('', style=text_style),
        ],
        [  # 17
            Paragraph('4', style=text_style),
            '',
            Paragraph('$26', style=text_style),
            Paragraph('0', style=text_style),
            Paragraph('0.00', style=text_style),
            Paragraph('', style=text_style),
        ],
        [  # 18
            Paragraph('4', style=text_style),
            '',
            Paragraph('Partial Payments', style=text_style),
            Paragraph('0', style=text_style),
            Paragraph('0', style=text_style),
            Paragraph('104.00', style=text_style),
        ],
        [  # 19
            Paragraph('5', style=text_style),
            Paragraph('Local Victim Assistance (all cases)<br /> 15-21-131(Surcharge)', style=text_style),
            Paragraph('$0.01 AND OVER', style=text_style),
            Paragraph('384', style=text_style),
            Paragraph('3973.32', style=text_style),
            Paragraph('', style=text_style),
        ],
        [  # 20
            Paragraph('5', style=text_style),
            '',
            Paragraph('Partial Payments', style=text_style),
            Paragraph('9', style=text_style),
            Paragraph('162.92', style=text_style),
            Paragraph('4136.24', style=text_style),
        ],
        [  # 21
            Paragraph('6', style=text_style),
            Paragraph('Probate Judges Retirement <br />(deducted from base-fine) <br />47-11-51', style=text_style),
            Paragraph('$0.01 - $4.01', style=text_style),
            Paragraph('46', style=text_style),
            Paragraph('$138', style=text_style),
            Paragraph('', style=text_style),
        ],
        [  # 22
            Paragraph('6', style=text_style),
            '',
            Paragraph('$4.01 - $ 25.00', style=text_style),
            Paragraph('46', style=text_style),
            Paragraph('$138', style=text_style),
            Paragraph('', style=text_style),
        ],
        [  # 23
            Paragraph('6', style=text_style),
            '',
            Paragraph('$25.01 - $50.00', style=text_style),
            Paragraph('52', style=text_style),
            Paragraph('208', style=text_style),
            Paragraph('', style=text_style),
        ],
        [  # 24
            Paragraph('6', style=text_style),
            '',
            Paragraph('$50.01 - $100.00', style=text_style),
            Paragraph('62', style=text_style),
            Paragraph('310', style=text_style),
            Paragraph('', style=text_style),
        ],
        [  # 25
            Paragraph('6', style=text_style),
            '',
            Paragraph('$100.01 AND OVER', style=text_style),
            Paragraph('268', style=text_style),
            Paragraph('3899.59', style=text_style),
            Paragraph('', style=text_style),
        ],
        [  # 26
            Paragraph('6', style=text_style),
            '',
            Paragraph('Partial Payments', style=text_style),
            Paragraph('7', style=text_style),
            Paragraph('145.51', style=text_style),
            Paragraph('4701.10', style=text_style),
        ],
        [  # 27
            Paragraph('7', style=text_style),
            Paragraph('Sheriffs Retirement <br />47-16-60', style=text_style),
            Paragraph('$0.01 AND OVER', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
        ],
        [  # 28
            Paragraph('7', style=text_style),
            '',
            Paragraph('Partial Payments', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('0.00', style=text_style),
        ],
        [  # 29
            Paragraph('8', style=text_style),
            Paragraph('County Law Library <br />36-15-9 (Surcharge)', style=text_style),
            Paragraph('$0.01 AND OVER', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
        ],
        [  # 30
            Paragraph('8', style=text_style),
            '',
            Paragraph('Partial Payments', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('0.00', style=text_style),
        ],
        [  # 31
            Paragraph('9', style=text_style),
            Paragraph('County Jail <br />15-21-93 (Surcharge)', style=text_style),
            Paragraph('$0.01 AND OVER', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
        ],
        [  # 32
            Paragraph('9', style=text_style),
            '',
            Paragraph('Partial Payments', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('0.00', style=text_style),
        ],
        [  # 33
            Paragraph('10', style=text_style),
            Paragraph('County Drug Abuse Treatment/Educ. <br />15-21-100 (Surcharge)', style=text_style),
            Paragraph('$0.01 AND OVER', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
        ],
        [  # 34
            Paragraph('10', style=text_style),
            '',
            Paragraph('Partial Payments', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('0.00', style=text_style),
        ],
        [  # 35
            Paragraph('11', style=text_style),
            Paragraph('Brain and Spinal Injury <br />15-21-149 (Surcharge)', style=text_style),
            Paragraph('$0.01 AND OVER', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
        ],
        [  # 36
            Paragraph('11', style=text_style),
            '',
            Paragraph('Partial Payments', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('0.00', style=text_style),
        ],
        [  # 37
            Paragraph('12', style=text_style),
            Paragraph('Crime Lab Fee <br />42-8-34 (Surcharge)', style=text_style),
            Paragraph('$0.01 AND OVER', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
        ],
        [  # 38
            Paragraph('12', style=text_style),
            '',
            Paragraph('Partial Payments', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('0.00', style=text_style),
        ],
        [  # 39
            Paragraph('13', style=text_style),
            Paragraph('Driver Education and Training Fund <br />15-21-179 (Surcharge)', style=text_style),
            Paragraph('$0.01 AND OVER', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
        ],
        [  # 40
            Paragraph('13', style=text_style),
            '',
            Paragraph('Partial Payments', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('0.00', style=text_style),
        ],
        [  # 41
            Paragraph('TOTAL STATE FUNDS: $25664.02', style=extend_style(
                styles['body'],
                leftIndent=5,
                rightIndent=5,
                fontSize=9,
                leading=11,
                spaceBefore=5,
                alignment=TA_RIGHT
            )),
            '',
            '',
            '',
            '',
            '',
        ],
    ]
    global table_row_num
    table_row_num = len(data)
    table = Table(
        data,
        colWidths=(10 * mm, 55 * mm, None, 30 * mm, 25 * mm, 45 * mm),
        rowHeights=_get_row_heights()
    )
    table.setStyle(extend_table_style(
        styles['iv-main-table'],
        [
            ('SPAN', (1, 2), (1, 6)),
            ('SPAN', (0, 2), (0, 6)),
            ('SPAN', (0, 2), (0, 6)),

            ('SPAN', (1, 7), (1, 9)),
            ('SPAN', (1, 10), (1, 11)),
            ('SPAN', (0, 7), (0, 11)),

            ('SPAN', (1, 12), (1, 13)),
            ('SPAN', (1, 14), (1, 15)),
            ('SPAN', (0, 12), (0, 15)),

            ('SPAN', (1, 16), (1, 18)),
            ('SPAN', (0, 16), (0, 18)),

            ('SPAN', (1, 19), (1, 20)),
            ('SPAN', (0, 19), (0, 20)),

            ('SPAN', (1, 21), (1, 26)),
            ('SPAN', (0, 21), (0, 26)),

            ('SPAN', (1, 27), (1, 28)),
            ('SPAN', (0, 27), (0, 28)),

            ('SPAN', (1, 29), (1, 30)),
            ('SPAN', (0, 29), (0, 30)),

            ('SPAN', (1, 31), (1, 32)),
            ('SPAN', (0, 31), (0, 32)),

            ('SPAN', (1, 33), (1, 34)),
            ('SPAN', (0, 33), (0, 34)),

            ('SPAN', (1, 35), (1, 36)),
            ('SPAN', (0, 35), (0, 36)),

            ('SPAN', (1, 37), (1, 38)),
            ('SPAN', (0, 37), (0, 38)),

            ('SPAN', (1, 39), (1, 40)),
            ('SPAN', (0, 39), (0, 40)),

            ('SPAN', (0, 41), (5, 41)),

            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            # ('VALIGN', (0,2), (0,-2), 'TOP'),
            # ('VALIGN', (1,5), (1,18), 'TOP')
            # ('VALIGN', (1,22), (1,27), 'TOP'),

            ('BACKGROUND', (0, table_row_num), (0, table_row_num), colors.black),

            ('INNERGRID', (0, 1), (-1, -1), 0.3, colors.black),

            ('LINEABOVE', (0, 1), (6, 1), 1, colors.black),
            ('LINEBELOW', (0, 6), (6, 6), 1, colors.black),
            ('LINEBELOW', (0, 11), (6, 11), 1, colors.black),
            ('LINEBELOW', (0, 15), (6, 15), 1, colors.black),
            ('LINEBELOW', (0, 18), (6, 18), 1, colors.black),
            ('LINEBELOW', (0, 20), (6, 20), 1, colors.black),
            ('LINEBELOW', (0, 26), (6, 26), 1, colors.black),
            ('LINEBELOW', (0, 28), (6, 28), 1, colors.black),
            ('LINEBELOW', (0, 30), (6, 30), 1, colors.black),
            ('LINEBELOW', (0, 32), (6, 32), 1, colors.black),
            ('LINEBELOW', (0, 34), (6, 34), 1, colors.black),
            ('LINEBELOW', (0, 36), (6, 36), 1, colors.black),
            ('LINEBELOW', (0, 38), (6, 38), 1, colors.black),
            ('LINEBELOW', (0, 40), (6, 40), 1, colors.black),
            ('LINEBELOW', (0, 41), (6, 41), 1, colors.black),
        ]
    )
    )
    return table


def _create_bottom_table():
    data = [
        [
            Paragraph('Summary Breakdown of monies collected and disbursed for this month',
                      style=extend_style(text_style, alignment=TA_LEFT)),
        ],
        [
            '',
            ''
        ],
        [  # 1
            Table(
                [
                    [
                        Paragraph('79,206.22',
                                  style=extend_style(text_style, alignment=TA_RIGHT)),
                        Paragraph('BASE - FINES',
                                  style=extend_style(text_style, alignment=TA_LEFT)),
                    ]
                ],
                style=styles['iv-main-table'],
                colWidths=(20 * mm, 70 * mm)

            ),
            Table(
                [
                    [
                        Paragraph('97,665.86',
                                  style=extend_style(text_style, alignment=TA_RIGHT)),
                        Paragraph('TOTAL DISBURSEMENTS',
                                  style=extend_style(text_style, alignment=TA_LEFT)),
                    ]
                ],
                style=styles['iv-main-table'],
                colWidths=(20 * mm, 70 * mm)

            ),
        ],
        [  # 2
            Table(
                [
                    [
                        Paragraph('18,459.04',
                                  style=extend_style(text_style, alignment=TA_RIGHT)),
                        Paragraph('STATE SURCHARGES ONLY',
                                  style=extend_style(text_style, alignment=TA_LEFT)),
                    ]
                ],
                style=styles['iv-main-table'],
                colWidths=(20 * mm, 70 * mm)

            ),
            Table(
                [
                    [
                        Paragraph('-25664.02',
                                  style=extend_style(text_style, alignment=TA_RIGHT)),
                        Paragraph('TOTAL STATE FEES (surcharges and others)',
                                  style=extend_style(text_style, alignment=TA_LEFT)),
                    ]
                ],
                style=styles['iv-main-table'],
                colWidths=(20 * mm, 70 * mm)

            )
        ],
        [  # 3
            Table(
                [
                    [
                        Paragraph('00.0',
                                  style=extend_style(text_style, alignment=TA_RIGHT)),
                        Paragraph('PROC - FEES',
                                  style=extend_style(text_style, alignment=TA_LEFT)),
                    ]
                ],
                style=styles['iv-main-table'],
                colWidths=(20 * mm, 70 * mm)

            ),
            Table(
                [
                    [
                        Paragraph('0.00',
                                  style=extend_style(text_style, alignment=TA_RIGHT)),
                        Paragraph('PROC - FEES',
                                  style=extend_style(text_style, alignment=TA_LEFT)),
                    ]
                ],
                style=styles['iv-main-table'],
                colWidths=(20 * mm, 70 * mm)

            )
        ],
        [  # 4
            Table(
                [
                    [
                        Paragraph('16188.73',
                                  style=extend_style(text_style, alignment=TA_RIGHT)),
                        Paragraph('OTHER CHARGES',
                                  style=extend_style(text_style, alignment=TA_LEFT)),
                    ]
                ],
                style=styles['iv-main-table'],
                colWidths=(20 * mm, 70 * mm)

            ),
            Table(
                [
                    [
                        Paragraph('-16188.73',
                                  style=extend_style(text_style, alignment=TA_RIGHT)),
                        Paragraph('OTHER CHARGES',
                                  style=extend_style(text_style, alignment=TA_LEFT)),
                    ]
                ],
                style=styles['iv-main-table'],
                colWidths=(20 * mm, 70 * mm)

            )
        ],
        [  # 5
            Table(
                [
                    [
                        Paragraph('0.00',
                                  style=extend_style(text_style, alignment=TA_RIGHT)),
                        Paragraph('ADM FEES',
                                  style=extend_style(text_style, alignment=TA_LEFT)),
                    ]
                ],
                style=styles['iv-main-table'],
                colWidths=(20 * mm, 70 * mm)

            ),
            Table(
                [
                    [
                        Paragraph('0.00',
                                  style=extend_style(text_style, alignment=TA_RIGHT)),
                        Paragraph('ADM FEES',
                                  style=extend_style(text_style, alignment=TA_LEFT)),
                    ]
                ],
                style=styles['iv-main-table'],
                colWidths=(20 * mm, 70 * mm)

            )
        ],
        [  # 6
            Table(
                [
                    [
                        Paragraph('0.00',
                                  style=extend_style(text_style, alignment=TA_RIGHT)),
                        Paragraph('TECH FEES',
                                  style=extend_style(text_style, alignment=TA_LEFT)),
                    ]
                ],
                style=styles['iv-main-table'],
                colWidths=(20 * mm, 70 * mm)

            ),
            Table(
                [
                    [
                        Paragraph('0.00',
                                  style=extend_style(text_style, alignment=TA_RIGHT)),
                        Paragraph('TECH FEES',
                                  style=extend_style(text_style, alignment=TA_LEFT)),
                    ]
                ],
                style=styles['iv-main-table'],
                colWidths=(20 * mm, 70 * mm)

            )
        ],
        [
            # 7
            Table(
                [
                    [
                        Paragraph('<b>97,665.86</b>',
                                  style=extend_style(text_style, alignment=TA_RIGHT)),
                        Paragraph('<b>TOTAL DISBURSEMENTS</b>',
                                  style=extend_style(text_style, alignment=TA_LEFT)),
                    ]
                ],
                style=styles['iv-main-table'],
                colWidths=(20 * mm, 70 * mm)

            ),
            Table(
                [
                    [
                        Paragraph('<b>72001.84</b>',
                                  style=extend_style(text_style, alignment=TA_RIGHT)),
                        Paragraph('<b>NET DISBURSEMENTS</b>      (City General Fund)',
                                  style=extend_style(text_style, alignment=TA_LEFT)),
                    ]
                ],
                style=styles['iv-main-table'],
                colWidths=(20 * mm, 70 * mm)

            )
        ]
    ]
    table = Table(
        data,
        colWidths=(60 * mm, 90 * mm),
        rowHeights=[10 * mm, 1 * mm, 4 * mm, 4 * mm, 4 * mm, 4 * mm, 4 * mm, 4 * mm, 4 * mm]
    )
    table.setStyle(extend_table_style(
        styles['iv-main-table'],
        [
            ('SPAN', (0, 0), (1, 0)),
        ]
    )
    )
    return table


def _get_row_heights():
    row_heights = [ROW_HEIGHT] * table_row_num
    row_heights[1] = 10 * mm
    return row_heights
