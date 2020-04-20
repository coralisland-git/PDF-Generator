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
    doc.build(story, canvasmaker=PageNumCanvas)
    #del doc

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
        [#1
            '',
            '',
            Paragraph('<b>(1)</b>', style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('<b>(2)</b>', style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('<b>(3)</b>', style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('<b>(4)</b>', style=extend_style(text_style, alignment=TA_CENTER)),
        ],
        [#2
            '',
            Paragraph('<b>Fund Name1</b>', style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('<b>Description</b>', style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('<b>No. of Cases</b>', style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('<b>Fund Amount Disbursed</b>', style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('<b>Total Fund Amount Disbursed</b>', style=extend_style(text_style, alignment=TA_CENTER)),
        ],

        [#3
            Paragraph('1', style=text_style),
            Paragraph('Peace Officer Annuity & benefit (deducted from base-line)', style=text_style),
            Paragraph('$4.01 - $ 25.00', style=text_style),
            Paragraph('46', style=text_style),
            Paragraph('$138', style=text_style),
            Paragraph('', style=text_style),
        ],
        [#4
            '', '',
            Paragraph('$25.01 - $50.00', style=text_style),
            Paragraph('52', style=text_style),
            Paragraph('208', style=text_style),
            Paragraph('', style=text_style),
        ],
        # [#7
        #     '', '',
        #     Paragraph('20', style=text_style),
        #     Paragraph('Partial Payments', style=text_style),
        #     Paragraph('', style=text_style),
        #     Paragraph('', style=text_style),
        # ],
        # [#8
        #     '',
        #     Paragraph('<b>POPIDF-A (f/k/a POPTF)</b> (OCGA 15-21-73(a)(2)(A) ) - <b>Bond Forfeitures</b>', style=text_style),
        #     Paragraph('', style=text_style),
        #     Paragraph('Less than $1000', style=text_style),
        #     Paragraph('', style=text_style),
        #     Paragraph('10% x Column (3)', style=text_style),
        # ],
        # [#9
        #     '', '',
        #     Paragraph('', style=text_style),
        #     Paragraph('Greater than $1000', style=text_style),
        #     Paragraph('$0.00', style=text_style),
        #     Paragraph('$100', style=text_style),
        #     Paragraph('$0.00', style=text_style)
        # ],
        # [#10
        #     Paragraph('2', style=text_style),
        #     Paragraph('<b>Georgia Crime Victims Emergency Fund</b> (OCGA 15-21-112 for conviction of OCGA 40-6-391 (DUI of alcohol/drugs))', style=text_style),
        #     Paragraph('', style=text_style),
        #     Paragraph('$26', style=text_style),
        #     Paragraph('$0.00', style=text_style),
        #     Paragraph('Column (1) x $26 for July 1, 2004 or later offenses', style=text_style),
        #     Paragraph('$0.00', style=text_style)
        # ],
        # [#11
        #     '', '',
        #     Paragraph('', style=text_style),
        #     Paragraph('$25', style=text_style),
        #     Paragraph('$0.00', style=text_style),
        #     Paragraph('Column (1) x $25 for pre July 1, 2004 offenses', style=text_style),
        #     Paragraph('$0.00', style=text_style)
        # ],
        # [#12
        #     '', '',
        #     Paragraph('', style=text_style),
        #     Paragraph('Partial Payments', style=text_style),
        #     Paragraph('', style=text_style),
        #     Paragraph('', style=text_style),
        #     Paragraph('$0.00', style=text_style)
        # ],
        #
        # [#13
        #     Paragraph('3', style=text_style),
        #     Paragraph('<b>Brain and Spinal Injury Trust Fund</b> (OCGA 15-21-149 and 15-21-151)', style=text_style),
        #     Paragraph('', style=text_style),
        #     Paragraph('Full Payments', style=text_style),
        #     Paragraph('$0.00', style=text_style),
        #     Paragraph('10% x Column (3)', style=text_style),
        #     Paragraph('$0.00', style=text_style)
        # ],
        #
        # [#14
        #     '', '',
        #     Paragraph('', style=text_style),
        #     Paragraph('Partial Payments', style=text_style),
        #     Paragraph('', style=text_style),
        #     Paragraph('', style=text_style),
        #     Paragraph('$0.00', style=text_style)
        # ],

        # [#15
        #     Paragraph('4', style=text_style),
        #     Paragraph('<b>Crime Lab Fee</b> (OCGA 42-8-34)', style=text_style),
        #     Paragraph('', style=text_style),
        #     Paragraph('Felony', style=text_style),
        #     Paragraph('', style=text_style),
        #     Paragraph('$50 x column (1)', style=text_style),
        #     Paragraph('$0.00', style=text_style)
        # ],
        #
        # [#16
        #     '', '',
        #     Paragraph('', style=text_style),
        #     Paragraph('Misdemeanor', style=text_style),
        #     Paragraph('', style=text_style),
        #     Paragraph('$25 x column (1)', style=text_style),
        #     Paragraph('$0.00', style=text_style)
        # ],
        #
        # [#17
        #     '', '',
        #     Paragraph('', style=text_style),
        #     Paragraph('Partial Payments', style=text_style),
        #     Paragraph('', style=text_style),
        #     Paragraph('', style=text_style),
        #     Paragraph('$0.00', style=text_style)
        # ],
        #
        # [#18
        #     Paragraph('5', style=text_style),
        #     Paragraph('<b>Driver Education and Training Fund</b> (OCGA 15-21-179)', style=text_style),
        #     Paragraph('', style=text_style),
        #     Paragraph('Full Payments', style=text_style),
        #     Paragraph('$0.00', style=text_style),
        #     Paragraph('1.5% of column (3) for May 6, 2013 or later offenses', style=text_style),
        #     Paragraph('$0.00', style=text_style),
        # ],
        #
        # [#19
        #     '', '',
        #     Paragraph('', style=text_style),
        #     Paragraph('Full Payments', style=text_style),
        #     Paragraph('$0.00', style=text_style),
        #     Paragraph('5% of column (3) for pre May 6, 2013 offenses', style=text_style),
        #     Paragraph('$0.00', style=text_style)
        # ],
    ]
    global table_row_num
    table_row_num = len(data)
    table = Table(
        data,
        colWidths=(10*mm, 55*mm, None, 30*mm, 25*mm, 45*mm),
        rowHeights=_get_row_heights()
    )
    table.setStyle(extend_table_style(
        styles['iv-main-table'],
        [
            ('SPAN', (1,2), (1,3)),
            ('SPAN', (0,2), (0,3)),

            # ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            # ('VALIGN', (0,5), (0,-2), 'TOP'),
            # ('VALIGN', (1,5), (1,18), 'TOP'),
            # ('VALIGN', (1,22), (1,27), 'TOP'),

            ('BACKGROUND', (0, table_row_num), (0,table_row_num), colors.black),

            ('INNERGRID', (0,1), (-1,-1), 0.3, colors.black),
            ('LINEBELOW', (0,0), (6, 2), 0.3, colors.black),
            ('LINEBELOW', (6,30), (6,30), 0.3, colors.black),

            ('LINEABOVE', (0,10), (6,10), 1, colors.black),
            ('LINEABOVE', (0,13), (6,13), 1, colors.black),
            ('LINEABOVE', (0,15), (6,15), 1, colors.black),
            ('LINEABOVE', (0,18), (6,18), 1, colors.black),
            ('LINEABOVE', (0,23), (6,23), 1, colors.black),
            # ('LINEABOVE', (0,27), (6,27), 1, colors.black),
            # ('LINEABOVE', (0,28), (6,28), 1, colors.black),
        ]
    )
    )
    return table


def _get_row_heights():
    row_heights = [ROW_HEIGHT] * table_row_num
    row_heights[1] = 10 * mm
    # row_heights[4] = 9 * mm
    # row_heights[10] = 9 * mm
    # row_heights[11] = 9 * mm
    # row_heights[18] = 9 * mm
    # row_heights[19] = 9 * mm
    # row_heights[22] = 9 * mm
    # row_heights[27] = 9 * mm
    # row_heights[30] = 4 * mm
    return row_heights
