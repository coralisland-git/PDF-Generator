# This Python file uses the following encoding: utf-8

import cStringIO

from reportlab_styles import *


def generate_retirement_fund_remittance_form(pdf_dict):
    buff = cStringIO.StringIO()
    doc = BaseDocTemplate(buff, pagesize=letter)
    f = Frame(
        gutters[0],
        gutters[2],
        usable_width,
        usable_height,
        showBoundary=0,
        topPadding=50,
        leftPadding=20,
        rightPadding=20
    )

    story = _create_story(pdf_dict)

    main_template = PageTemplate(id="main_template", frames=[f])
    doc.addPageTemplates([main_template])
    doc.build(story, canvasmaker=PageNumCanvas)
    #del doc

    buff.seek(0)
    return buff


def _create_story(doc_data):
    story = []

    header_table = _create_header()
    story.append(header_table)

    title = Paragraph(
        """
        SHERIFFS’ RETIREMENT FUND OF GEORGIA<br />
        3000 HWY 42 N<br />
        MCDONOUGH, GA 30253<br />
        770-914-1076
        """,
        style=extend_style(styles['body'], alignment=TA_CENTER, spaceBefore=10)
    )
    story.append(title)

    general_info_table = _create_general_info_table(doc_data)
    story.append(general_info_table)

    paragraph = Paragraph(
        '''Indicate below; the Court reporting, the number of cases and amount due at $2.00 each for fines collected or bonds
        forfeited of $5.00 or more for any <b>criminal or quasi-criminal case</b>:
        ''',
        extend_style(styles['body-smaller-font'], spaceBefore=20)
    )
    story.append(paragraph)

    document_body = _create_document_body_table(doc_data)
    story.append(document_body)

    paragraph = Paragraph(
        """
        To the best of my knowledge this is a correct amount for the period stated due the Sheriffs' Retirement Fund of Georgia as
        required by official Georgia Code Title 47-16-60 and 47-16-61 as amended.
        """,
        extend_style(styles['body-smaller-font'], spaceBefore=20)
    )
    story.append(paragraph)

    signature = _create_signature_table(doc_data)
    story.append(signature)

    paragraph = Paragraph(
        """
        <b>NOTE</b>: If there were no cases or money collected; please indicate by placing a zero (0) in the proper blank.
        """,
        style=extend_style(styles['body-smaller-font'], spaceBefore=20)
    )
    story.append(paragraph)

    return story


def _create_signature_table(doc_data):
    data = [
        [
            '',
            '',
            Paragraph(
                "Date: <u>{}</u>".format(doc_data['generated_on']),
                style=styles["body-smaller-font"]
            )
        ],
        [
            Paragraph(
                """
                Signature of Remitter and Title<br />
                CHIEF MAGISTRATE JUDGE PHINIA ATEN
                """,
                style=extend_style(
                    styles["body-smaller-font"],
                    leftIndent=50
                )
            )
        ]
    ]

    table = Table(data, colWidths=[300, None], spaceBefore=25)
    table.setStyle(extend_table_style(
        styles["iv-main-table"],
        [
            ('LINEBELOW', (0, 0), (0, 0), 0.5, colors.black)
        ]
        )
    )
    return table


def _create_document_body_table(doc_data):
    data = [
        [
            Paragraph(
                '<b>MAGISTRATE</b>: # OF CASES <u>{}</u> AMT. DUE $<u>{}</u>'.
                format(
                    doc_data['number_of_criminal_magistrate_cases'],
                    doc_data['criminal_magistrate_amount_due']
                ),
                style=styles["body-smaller-font"]
            ),
            Paragraph(
                '<b>OTHER</b>: # OF CASES <u>{}</u> AMT. DUE $<u>{}</u>'.
                format(doc_data['number_of_criminal_other_cases'],
                       doc_data['criminal_other_amount_due']
                ),
                style=styles["body-smaller-font"]
            )
        ],
        [
            Paragraph(
                """
                Indicate below; the Court reporting,
                the number of cases and amount due at $1.00 each for <u><b>civil proceedings</b></u>:
                """,
                style=styles["body-smaller-font"]
            ),
            ''
        ],
        [
            Paragraph(
                '<b>MAGISTRATE</b>: # OF CASES <u>{}</u> AMT. DUE $<u>{}</u>'.
                format(
                    doc_data['number_of_civil_magistrate_cases'],
                    doc_data['civil_magistrate_amount_due']
                ),
                style=styles["body-smaller-font"]
            ),
            Paragraph(
               '<b>OTHER</b>: # OF CASES <u>{}</u> AMT. DUE $<u>{}</u>'.
               format(doc_data['number_of_civil_other_cases'],
                      doc_data['civil_other_amount_due']
                ),
               style=styles["body-smaller-font"]
            )
        ],
        [
            Paragraph(
                'PLEASE INDICATE IF THE ABOVE CONTAIN ANY PARTIAL PAYMENTS.',
                style=styles["body-smaller-font"]
            ),
            ''
        ],
        [
            Paragraph(
                'Check Number <u>{}</u>{}Check Amount $<u>{}</u>'.
                format(
                    doc_data['check_number'],
                    "&nbsp;" * 5,
                    doc_data['check_amount']
                ),
                style=styles["body-smaller-font"]
            )
        ]
    ]

    table = Table(data, rowHeights=[30, 30, 30, 30, 30], spaceBefore=10)
    table.setStyle(extend_table_style(
        styles["iv-main-table"],
        [
            ('SPAN', (0, 1), (1, 1)),
            ('SPAN', (0, 3), (1, 3))
        ]
        )
    )
    return table


def _create_general_info_table(doc_data):
    data = [
        [
            Paragraph(
                'Name of Court: <u>MAGISTRATE COURT OF ROCKDALE COUNTY</u>',
                style=styles["body-smaller-font"]
            ),
            '',
            Paragraph(
                'County: <u>ROCKDALE</u>',
                style=styles["body-smaller-font"]
            )
        ],
        [
            Paragraph(
                'Mailing Address: <u>945 COURT STREET, CONYERS, GA 30012</u>',
                style=styles["body-smaller-font"]
            ),
            '', ''
        ],
        [
            Paragraph(
                'Period of Time Covered by this Report:',
                      style=styles["body-smaller-font"]
            ),
            '',
            Paragraph(
                    'From: <u>{}</u>'.format(doc_data["date_range_from"]), style=styles["body-smaller-font"]
            )
        ],
        [
            '', '',
            Paragraph(
                'To: <u>{}</u>'.format(doc_data['date_range_to']),
                style=styles["body-smaller-font"]
            )
        ]
    ]

    tabble = Table(data, spaceBefore=20, rowHeights=[15, 30, 15, 15]) #colWidths=(None, 0, None))
    tabble.setStyle(extend_table_style(
        styles["iv-main-table"],
        [
            ('SPAN', (0, 0), (1, 0)),
            ('SPAN', (0, 1), (1, 1)),
            ('SPAN', (0, 2), (1, 2)),
            ('LEFTPADDING', (0, 0), (0, 2), 20)
        ]
    ))

    return tabble


def _create_header():
    data = [
        [
            Paragraph('J. Terry Norris', styles["body-smaller-font"]),
            '',
            Paragraph('Lisa Petty', styles["body-smaller-font"])
        ],
        [
            Paragraph('Secretary/Treasurer', styles["body-smaller-font"]),
            '',
            Paragraph('Assistant Secretary/Treasurer', styles["body-smaller-font"])
        ]
    ]

    table = Table(data)
    table.setStyle(extend_table_style(styles["iv-main-table"]))

    return table
