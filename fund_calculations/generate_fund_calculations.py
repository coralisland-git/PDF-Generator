# This Python file uses the following encoding: utf-8
import cStringIO

from document_specific_styles import *

ROW_HEIGHT = 6 * mm
table_row_num = 0


def generate_fund_calculations(pdf_dict):
    buff = cStringIO.StringIO()
    doc = BaseDocTemplate(buff, pagesize=letter)
    f = Frame(gutters[0], gutters[2], usable_width, usable_height, showBoundary=0, topPadding=15, )

    story = _create_story(pdf_dict)

    main_template = PageTemplate(id="main_template", frames=[f])
    doc.addPageTemplates([main_template])
    doc.build(story, canvasmaker=FirstPageOnlyDatePageNumCanvas)
    # del doc

    buff.seek(0)
    return buff


def _create_story(pdf_dict):
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

    doc_body = _create_main_table(pdf_dict["main-table"])
    story.append(doc_body)

    bottom_table = _create_bottom_table(pdf_dict["secondary-table"])
    story.append(bottom_table)

    return story


def _create_main_table(section_list):
    data = [
        [  # 0
            '', '', '', '', ''
        ],
        [  # 1
            Paragraph('<b>Fund Name</b>', style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('<b>Description</b>', style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('<b>No. of Cases</b>', style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('<b>Fund Amount Disbursed</b>', style=extend_style(text_style, alignment=TA_CENTER)),
            Paragraph('<b>Total Fund Amount Disbursed</b>', style=extend_style(text_style, alignment=TA_CENTER)),
        ],
    ]


    total_state_funds = 0.0
    for section in section_list:
        total_section_funds = 0.0
        for index, row in enumerate(section["data"], start=1):
            # print (type(row.get('fund-amt', 0.0)), row.get('fund-amt', 0.0))
            funds = row.get('fund-amt', 0.0)
            funds = 0.0 if not funds else funds
            total_section_funds += funds
            section_data = [
                Paragraph(section['sect-desc'], style=text_style),
                Paragraph(row['description'], style=text_style),
                Paragraph(oformat(row.get('num-cases', 0)), style=text_style),
                Paragraph(oformat(row.get('fund-amt', 0)), style=text_style),
            ]
            if index == len(section["data"]):
                section_data.append(
                    Paragraph(oformat(total_section_funds), style=text_style),
                )
            else:
                section_data.append(
                    Paragraph("", style=text_style),
                )
            data.append(section_data)
        total_state_funds += total_section_funds
    data.append( [  # 41
        Paragraph('TOTAL STATE FUNDS', style=extend_style(
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
        Paragraph('%s' % total_state_funds, style=text_style)
    ],)

    global table_row_num
    table_row_num = len(data)
    table = Table(
        data,
        colWidths=(55 * mm, None, 30 * mm, 25 * mm, 45 * mm),
        rowHeights=_get_row_heights()
    )
    table.setStyle(extend_table_style(
        styles['iv-main-table'],
        [
            ('SPAN', (0, 2), (0, 6)),

            ('SPAN', (0, 7), (0, 9)),
            ('SPAN', (0, 10), (0, 11)),

            ('SPAN', (0, 12), (0, 13)),
            ('SPAN', (0, 14), (0, 15)),

            ('SPAN', (0, 16), (0, 18)),

            ('SPAN', (0, 19), (0, 20)),

            ('SPAN', (0, 21), (0, 26)),

            ('SPAN', (0, 27), (0, 28)),

            ('SPAN', (0, 29), (0, 30)),

            ('SPAN', (0, 31), (0, 32)),

            ('SPAN', (0, 33), (0, 34)),

            ('SPAN', (0, 35), (0, 36)),

            ('SPAN', (0, 37), (0, 38)),

            # ('SPAN', (0, 39), (0, 40)),

            ('SPAN', (0, 39), (3, 39)),
            #
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('VALIGN', (0, 2), (0, -2), 'TOP'),
            ('VALIGN', (1, 5), (1, 18), 'TOP'),
            ('VALIGN', (1, 22), (1, 27), 'TOP'),

            ('BACKGROUND', (0, table_row_num), (0, table_row_num), colors.black),

            ('INNERGRID', (0, 1), (-1, -1), 0.3, colors.black),

            ('LINEABOVE', (0, 1), (5, 1), 1, colors.black),
            ('LINEBELOW', (0, 6), (5, 6), 1, colors.black),
            ('LINEBELOW', (0, 11), (5, 11), 1, colors.black),
            ('LINEBELOW', (0, 15), (5, 15), 1, colors.black),
            ('LINEBELOW', (0, 18), (5, 18), 1, colors.black),
            ('LINEBELOW', (0, 20), (5, 20), 1, colors.black),
            ('LINEBELOW', (0, 26), (5, 26), 1, colors.black),
            ('LINEBELOW', (0, 28), (5, 28), 1, colors.black),
            ('LINEBELOW', (0, 30), (5, 30), 1, colors.black),
            ('LINEBELOW', (0, 32), (5, 32), 1, colors.black),
            ('LINEBELOW', (0, 34), (5, 34), 1, colors.black),
            ('LINEBELOW', (0, 36), (5, 36), 1, colors.black),
            ('LINEBELOW', (0, 38), (5, 38), 1, colors.black),
            ('LINEBELOW', (0, 39), (5, 39), 1, colors.black),
            ('LINEBELOW', (0, 40), (5, 40), 1, colors.black),
            #
            # ('BOX', (0, 1), (-1, -1), 1, colors.black),
        ]
    )
    )
    return table


def _create_bottom_table(data_mapper):
    i, j = (20, 70)
    first = data_mapper["first-col"]
    second = data_mapper["second-col"]
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
                        Paragraph('%s' % oformat(first["base-fines"]),
                                  style=extend_style(text_style, alignment=TA_RIGHT)),
                        Paragraph('BASE - FINES',
                                  style=extend_style(text_style, alignment=TA_LEFT)),
                    ]
                ],
                style=styles['iv-main-table'],
                colWidths=(i * mm, j * mm)

            ),
            Table(
                [
                    [
                        Paragraph('%s' % oformat(second['total-disbursements']),
                                  style=extend_style(text_style, alignment=TA_RIGHT)),
                        Paragraph('TOTAL DISBURSEMENTS',
                                  style=extend_style(text_style, alignment=TA_LEFT)),
                    ]
                ],
                style=styles['iv-main-table'],
                colWidths=(i * mm, j * mm)

            ),
        ],
        [  # 2
            Table(
                [
                    [
                        Paragraph('%s' % oformat(first['state-surcharges-only']),
                                  style=extend_style(text_style, alignment=TA_RIGHT)),
                        Paragraph('STATE SURCHARGES ONLY',
                                  style=extend_style(text_style, alignment=TA_LEFT)),
                    ]
                ],
                style=styles['iv-main-table'],
                colWidths=(i * mm, j * mm)

            ),
            Table(
                [
                    [
                        Paragraph('%s' % oformat(second["total-state-fees"]),
                                  style=extend_style(text_style, alignment=TA_RIGHT)),
                        Paragraph('TOTAL STATE FEES (surcharges and others)',
                                  style=extend_style(text_style, alignment=TA_LEFT)),
                    ]
                ],
                style=styles['iv-main-table'],
                colWidths=(i * mm, j * mm)

            )
        ],
        [  # 3
            Table(
                [
                    [
                        Paragraph('%s' % oformat(first["proc-fees"]),
                                  style=extend_style(text_style, alignment=TA_RIGHT)),
                        Paragraph('PROC - FEES',
                                  style=extend_style(text_style, alignment=TA_LEFT)),
                    ]
                ],
                style=styles['iv-main-table'],
                colWidths=(i * mm, j * mm)

            ),
            Table(
                [
                    [
                        Paragraph('%s' % oformat(second["proc-fees"]),
                                  style=extend_style(text_style, alignment=TA_RIGHT)),
                        Paragraph('PROC - FEES',
                                  style=extend_style(text_style, alignment=TA_LEFT)),
                    ]
                ],
                style=styles['iv-main-table'],
                colWidths=(i * mm, j * mm)

            )
        ],
        [  # 4
            Table(
                [
                    [
                        Paragraph('%s' % oformat(first["other-charges"]),
                                  style=extend_style(text_style, alignment=TA_RIGHT)),
                        Paragraph('OTHER CHARGES',
                                  style=extend_style(text_style, alignment=TA_LEFT)),
                    ]
                ],
                style=styles['iv-main-table'],
                colWidths=(i * mm, j * mm)

            ),
            Table(
                [
                    [
                        Paragraph('%s' % oformat(second["other-charges"]),
                                  style=extend_style(text_style, alignment=TA_RIGHT)),
                        Paragraph('OTHER CHARGES',
                                  style=extend_style(text_style, alignment=TA_LEFT)),
                    ]
                ],
                style=styles['iv-main-table'],
                colWidths=(i * mm, j * mm)

            )
        ],
        [  # 5
            Table(
                [
                    [
                        Paragraph('%s' % oformat(first["adm-fees"]),
                                  style=extend_style(text_style, alignment=TA_RIGHT)),
                        Paragraph('ADM FEES',
                                  style=extend_style(text_style, alignment=TA_LEFT)),
                    ]
                ],
                style=styles['iv-main-table'],
                colWidths=(i * mm, j * mm)

            ),
            Table(
                [
                    [
                        Paragraph('%s' % oformat(second["adm-fees"]),
                                  style=extend_style(text_style, alignment=TA_RIGHT)),
                        Paragraph('ADM FEES',
                                  style=extend_style(text_style, alignment=TA_LEFT)),
                    ]
                ],
                style=styles['iv-main-table'],
                colWidths=(i * mm, j * mm)

            )
        ],
        [  # 6
            Table(
                [
                    [
                        Paragraph('%s' % oformat(first["tech-fees"]),
                                  style=extend_style(text_style, alignment=TA_RIGHT)),
                        Paragraph('TECH FEES',
                                  style=extend_style(text_style, alignment=TA_LEFT)),
                    ]
                ],
                style=styles['iv-main-table'],
                colWidths=(i * mm, j * mm)

            ),
            Table(
                [
                    [
                        Paragraph('%s' % oformat(second["tech-fees"]),
                                  style=extend_style(text_style, alignment=TA_RIGHT)),
                        Paragraph('TECH FEES',
                                  style=extend_style(text_style, alignment=TA_LEFT)),
                    ]
                ],
                style=styles['iv-main-table'],
                colWidths=(i * mm, j * mm)

            )
        ],
        [
            # 7
            Table(
                [
                    [
                        Paragraph('<b>%s</b>' % oformat(first["total-disbursements"]),
                                  style=extend_style(text_style, alignment=TA_RIGHT)),
                        Paragraph('<b>TOTAL DISBURSEMENTS</b>',
                                  style=extend_style(text_style, alignment=TA_LEFT)),
                    ]
                ],
                style=styles['iv-main-table'],
                colWidths=(i * mm, j * mm)

            ),
            Table(
                [
                    [
                        Paragraph('<b>%s</b>' % oformat(second["net-disbursements"]),
                                  style=extend_style(text_style, alignment=TA_RIGHT)),
                        Paragraph('<b>NET DISBURSEMENTS</b>      (City General Fund)',
                                  style=extend_style(text_style, alignment=TA_LEFT)),
                    ]
                ],
                style=styles['iv-main-table'],
                colWidths=(i * mm, j * mm)

            )
        ]
    ]
    table = Table(
        data,
        colWidths=(90 * mm, 90 * mm),
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


def oformat(data):
    if data is None or data == "":
        return ""
    else:
        return "{:.2f}".format(data)
