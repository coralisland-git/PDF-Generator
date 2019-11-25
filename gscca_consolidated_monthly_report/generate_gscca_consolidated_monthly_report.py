# This Python file uses the following encoding: utf-8
import cStringIO

from document_specific_styles import *


ROW_HEIGHT = 6 * mm


def generate_gscca_consolidated_monthly_report():
    buff = cStringIO.StringIO()
    doc = BaseDocTemplate(buff, pagesize=letter)
    f = Frame(gutters[0], gutters[2], usable_width, usable_height, showBoundary=0, topPadding=15, )

    story = _create_story()

    main_template = PageTemplate(id="main_template", frames=[f])
    doc.addPageTemplates([main_template])
    doc.build(story, canvasmaker=PageNumCanvas)
    #del doc

    buff.seek(0)
    return buff


def _create_story():
    story = []

    story.append(
        Paragraph("""<b>CONSOLIDATED MONTHLY REMITTANCE REPORT – MAGISTRATE COURT</b>""",
                  style=styles["heading"]
        )
    )

    doc_body = _create_main_table()
    story.append(doc_body)

    bottom_table = _create_bottom_table()
    story.append(bottom_table)

    story.append(
        Paragraph(
            """
            Pursuant to O.C.G.A. § 15-21A-8 et. seq, I, the undersigned clerk/court officer of the above-named court, hereby certify that, to the best of my
            knowledge, the above and foregoing is a true and correct account of all above-referenced funds collected for the month specified.
            """,
            style=text_style
        )
    )

    footer = _create_footer()
    story.append(footer)

    return story


def _create_footer():
    data = [
        [
            Paragraph('', style=text_style),
            Paragraph('Chief Magistrate Judge Phinia Aten', style=text_style)
        ]
    ]

    table = Table(data, spaceBefore=20, colWidths=(None, 50*mm))
    table.setStyle(extend_table_style(
        styles['iv-main-table'],
        [
            ('LINEABOVE', (1,0), (1,0), 1, colors.black)
        ]
    ))

    return table


def _create_bottom_table():
    data = [
        [
            Paragraph('Please make all checks payable to:', style=text_style),
            Paragraph('<b>Georgia Superior Court Clerks’ Cooperative Authority (GSCCCA)</b>', style=text_style),
            ''
        ],
        [
            Paragraph('Please mail all checks and forms to:', style=text_style),
            Paragraph('<b>GSCCCA Fines and Fees Division, P.O. Box 29645, Atlanta, GA 30359</b>', style=text_style),
            ''
        ],
        [
            Paragraph('CHECK NUMBER(S): 2728', style=text_style),
            '',
            Paragraph('CHECK AMOUNTS: $4877.70', style=text_style)
        ]
    ]

    table = Table(
        data,
        spaceBefore=7,
        colWidths=(50*mm, 100*mm, None),
        rowHeights=[5*mm, 5*mm, 10*mm]
    )
    table.setStyle(
        extend_table_style(styles['iv-main-table'],
        [
            ('VALIGN', (0,2), (-1,-1), 'MIDDLE')
        ]
    ))

    return table


def _create_main_table():
    data = [
        [#0
            Paragraph('Report Month: August&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Report Year: 2019', style=text_style),
            '',
            '',

            Paragraph('Report Date: {}. {}, {}'.format('Sept','16', '2019'), style=text_style),
            '',

            Paragraph('County: {}'.format('ROCKDALE'), style=text_style),
            ''
        ],
        [#1
            Paragraph('Clerk/Court Officer Filing Report: HON. PHINIA ATEN', style=text_style),
            '',
            '',
            Paragraph('Phone: 770-278-7799', style=text_style),
            '',
            Paragraph('ORI: 122033J', style=text_style)
        ],
        [#2
            '', '',
            Paragraph('<b>(1)</b>', style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('<b>(2)</b>', style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('<b>(3)</b>', style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('<b>(4)</b>', style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('<b>(5)</b>', style=extend_style(text_style, alignment=TA_CENTER))
        ],
        [#3
            '', '',
            Paragraph('<b>No. of Cases</b>', style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('<b>Amount of Original Fine and/or Bond Forfeiture</b>', style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('<b>Total Amount of Fines and/or Bond Forfeitures</b>', style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('<b>Computation of Amount Collected</b>', style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('<b>Amount Collected</b>', style=extend_style(text_style, alignment=TA_CENTER))
        ],
        [#4
            Paragraph('SECTION 1 - CRIMINAL', style=extend_style(text_style, textColor=colors.white)),
            '', '', '', '', '', ''
        ],
        [#5
            Paragraph('1', style=text_style),
            Paragraph('<b>POPIDF-A (f/k/a POPTF)</b> (OCGA 15-21-73(a)(1)(A))', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('$1 - $499.99', style=text_style),
            Paragraph('$0.00', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style)
        ],
        [#6
            '', '',
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('$50 x column (1)', style=text_style),
            Paragraph('', style=text_style)
        ],
        [#7
            '', '',
            Paragraph('20', style=text_style),
            Paragraph('Partial Payments', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('$357.50', style=text_style)
        ],
        [#8
            '',
            Paragraph('<b>POPIDF-A (f/k/a POPTF)</b> (OCGA 15-21-73(a)(2)(A) ) - <b>Bond Forfeitures</b>', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('Less than $1000', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('10% x Column (3)', style=text_style),
            Paragraph('$0.00', style=text_style)
        ],
        [#9
            '', '',
            Paragraph('', style=text_style),
            Paragraph('Greater than $1000', style=text_style),
            Paragraph('$0.00', style=text_style),
            Paragraph('$100', style=text_style),
            Paragraph('$0.00', style=text_style)
        ],
        [#10
            Paragraph('2', style=text_style),
            Paragraph('<b>Georgia Crime Victims Emergency Fund</b> (OCGA 15-21-112 for conviction of OCGA 40-6-391 (DUI of alcohol/drugs))', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('$26', style=text_style),
            Paragraph('$0.00', style=text_style),
            Paragraph('Column (1) x $26 for July 1, 2004 or later offenses', style=text_style),
            Paragraph('$0.00', style=text_style)
        ],
        [#11
            '', '',
            Paragraph('', style=text_style),
            Paragraph('$25', style=text_style),
            Paragraph('$0.00', style=text_style),
            Paragraph('Column (1) x $25 for pre July 1, 2004 offenses', style=text_style),
            Paragraph('$0.00', style=text_style)
        ],
        [#12
            '', '',
            Paragraph('', style=text_style),
            Paragraph('Partial Payments', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('$0.00', style=text_style)
        ],

        [#13
            Paragraph('3', style=text_style),
            Paragraph('<b>Brain and Spinal Injury Trust Fund</b> (OCGA 15-21-149 and 15-21-151)', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('Full Payments', style=text_style),
            Paragraph('$0.00', style=text_style),
            Paragraph('10% x Column (3)', style=text_style),
            Paragraph('$0.00', style=text_style)
        ],

        [#14
            '', '',
            Paragraph('', style=text_style),
            Paragraph('Partial Payments', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('$0.00', style=text_style)
        ],

        [#15
            Paragraph('4', style=text_style),
            Paragraph('<b>Crime Lab Fee</b> (OCGA 42-8-34)', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('Felony', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('$50 x column (1)', style=text_style),
            Paragraph('$0.00', style=text_style)
        ],

        [#16
            '', '',
            Paragraph('', style=text_style),
            Paragraph('Misdemeanor', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('$25 x column (1)', style=text_style),
            Paragraph('$0.00', style=text_style)
        ],

        [#17
            '', '',
            Paragraph('', style=text_style),
            Paragraph('Partial Payments', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('$0.00', style=text_style)
        ],

        [#18
            Paragraph('5', style=text_style),
            Paragraph('<b>Driver Education and Training Fund</b> (OCGA 15-21-179)', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('Full Payments', style=text_style),
            Paragraph('$0.00', style=text_style),
            Paragraph('1.5% of column (3) for May 6, 2013 or later offenses', style=text_style),
            Paragraph('$0.00', style=text_style),
        ],

        [#19
            '', '',
            Paragraph('', style=text_style),
            Paragraph('Full Payments', style=text_style),
            Paragraph('$0.00', style=text_style),
            Paragraph('5% of column (3) for pre May 6, 2013 offenses', style=text_style),
            Paragraph('$0.00', style=text_style)
        ],

        [#20
            '', '',
            Paragraph('', style=text_style),
            Paragraph('Partial Payments', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('$0.00', style=text_style),
        ],

        [#21
            Paragraph('SECTION 2 - INDIGENT DEFENSE', style=extend_style(text_style, textColor=colors.white)),
            '', '', '', '', '', ''
        ],

        [#22
            Paragraph('6', style=text_style),
            Paragraph('<b>Civil Action Surcharges</b> (OCGA 15-21A-6)', style=text_style),
            Paragraph('277', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('$15 x column (1)', style=text_style),
            Paragraph('$4155.00', style=text_style)
        ],

        [#23
            Paragraph('7', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('Full Payments', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('10% x column (3)', style=text_style),
            Paragraph('', style=text_style)
        ],

        [#24
            '',
            Paragraph('', style=text_style),
            Paragraph('21', style=text_style),
            Paragraph('Partial Payments', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('365.20', style=text_style)
        ],

        [#25
            '',
            Paragraph('<b>POPIDF-B</b> (OCGA 15-21-73 (a)(2)(B)) - <b>Bond Forfeitures</b>', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('Less than $1000', style=text_style),
            Paragraph('$0.00', style=text_style),
            Paragraph('10% x Column (3)', style=text_style),
            Paragraph('$0', style=text_style)
        ],

        [#26
            '',
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('Greater than $1000', style=text_style),
            Paragraph('$0.00', style=text_style),
            Paragraph('$100', style=text_style),
            Paragraph('$0.00', style=text_style)
        ],

        [#27
            Paragraph('8', style=text_style),
            Paragraph('<b>Safe Harbor Fund</b> (OCGA 15-21-208)', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('$2500 x column (1)', style=text_style),
            Paragraph('$0.00', style=text_style)
        ],

        [#28
            Paragraph('9', style=text_style),
            Paragraph('<b>State Indemnification Fund</b> (OCGA 16-5-21(c), 16-5-24(c), 16-10-24)', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('Full Payments', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('$300 or $2000 x column (1)', style=text_style),
            Paragraph('$0.00', style=text_style)
        ],

        [#29
            '', '',
            Paragraph('', style=text_style),
            Paragraph('Partial Payments', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('', style=text_style),
            Paragraph('$0.00', style=text_style)
        ],

        [#30
            Paragraph('GRAND TOTAL OF ALL COLLECTIONS', style=extend_style(text_style, textColor=colors.white)),
            '', '', '', '', '',
            Paragraph('$4877.70', style=text_style)
        ]
    ]

    table = Table(
        data,
        colWidths=(10*mm, 55*mm, None, 30*mm, 25*mm, 45*mm, None),
        rowHeights=_get_row_heights()
    )
    table.setStyle(extend_table_style(
        styles['iv-main-table'],
        [
            ('SPAN', (0,0), (2,0)),
            ('SPAN', (0,2), (1,2)),
            ('SPAN', (0,3), (1,3)),

            ('SPAN', (3,0), (4,0)),
            ('SPAN', (5,0), (6,0)),
            ('SPAN', (0,1), (2,1)),
            ('SPAN', (3,1), (4,1)),
            ('SPAN', (5,1), (6,1)),
            ('SPAN', (0,4), (6,4)),
            ('SPAN', (0,5), (0,9)),
            ('SPAN', (0,10), (0,12)),
            ('SPAN', (0,13), (0,14)),
            ('SPAN', (0,15), (0,17)),
            ('SPAN', (0,18), (0,20)),
            ('SPAN', (0,23), (0,26)),
            ('SPAN', (0,28), (0,29)),

            ('SPAN', (0,21), (6,21)),
            ('SPAN', (0,30), (5,30)),
            ('SPAN', (1,5), (1,7)),
            ('SPAN', (1,8), (1,9)),
            ('SPAN', (1,10), (1,12)),
            ('SPAN', (1,13), (1,14)),
            ('SPAN', (1,15), (1,17)),
            ('SPAN', (1,18), (1,20)),
            ('SPAN', (1,23), (1,24)),
            ('SPAN', (1,25), (1,26)),
            ('SPAN', (1,28), (1,29)),

            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('VALIGN', (0,5), (0,-2), 'TOP'),
            ('VALIGN', (1,5), (1,18), 'TOP'),
            ('VALIGN', (1,22), (1,28), 'TOP'),

            ('BACKGROUND', (0, 4), (0,4), colors.black),
            ('BACKGROUND', (0, 21), (0,21), colors.black),
            ('BACKGROUND', (0, 30), (0,30), colors.black),
            ('BACKGROUND', (4, 7), (5,7), colors.lightgrey),
            ('BACKGROUND', (4, 12), (5,12), colors.lightgrey),
            ('BACKGROUND', (4, 14), (5,14), colors.lightgrey),
            ('BACKGROUND', (4, 15), (4,15), colors.lightgrey),
            ('BACKGROUND', (4, 16), (4,16), colors.lightgrey),
            ('BACKGROUND', (4, 17), (5,17), colors.lightgrey),
            ('BACKGROUND', (4, 20), (5,20), colors.lightgrey),
            ('BACKGROUND', (3, 22), (4,22), colors.lightgrey),
            ('BACKGROUND', (4, 24), (5,24), colors.lightgrey),
            ('BACKGROUND', (3, 27), (4,27), colors.lightgrey),
            ('BACKGROUND', (4, 28), (4,28), colors.lightgrey),
            ('BACKGROUND', (4, 29), (5,29), colors.lightgrey),

            ('INNERGRID', (0,3), (-1,-1), 0.3, colors.black),
            ('LINEBELOW', (0,0), (6, 2), 0.3, colors.black),
            ('LINEBELOW', (6,30), (6,30), 0.3, colors.black),

            ('LINEABOVE', (0,10), (6,10), 1, colors.black),
            ('LINEABOVE', (0,13), (6,13), 1, colors.black),
            ('LINEABOVE', (0,15), (6,15), 1, colors.black),
            ('LINEABOVE', (0,18), (6,18), 1, colors.black),
            ('LINEABOVE', (0,23), (6,23), 1, colors.black),
            ('LINEABOVE', (0,27), (6,27), 1, colors.black),
            ('LINEABOVE', (0,28), (6,28), 1, colors.black),
        ]
        )
    )
    return table


def _get_row_heights():
    row_heights = [ROW_HEIGHT] * 31
    row_heights[3] = 15 * mm
    row_heights[4] = 4 * mm
    row_heights[10] = 9 * mm
    row_heights[11] = 9 * mm
    row_heights[18] = 9 * mm
    row_heights[19] = 9 * mm
    row_heights[21] = 4 * mm
    row_heights[22] = 9 * mm
    row_heights[27] = 9 * mm
    row_heights[30] = 4 * mm
    return row_heights
