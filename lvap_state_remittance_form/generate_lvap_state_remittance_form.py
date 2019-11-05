# This Python file uses the following encoding: utf-8
import cStringIO
from datetime import datetime

from reportlab.lib.units import mm

from reportlab_styles import *


GENERAL_TABLE_BIG_ROW_HEIGHT = 7 * mm
GENERAL_TABLE_SMALL_ROW_HEIGHT = 4 * mm
GENERAL_TABLE_FIRST_COL_WIDTH = 65 * mm
PAYMENT_TABLE_FIRST_COL_WIDTH = 90 * mm
PAYMENT_TABLE_ROW_HEIGHT = 10 * mm
SIGNATURE_TABLE_FIRST_COL_WIDTH = 100 * mm
SIGNATURE_TABLE_LAST_COL_WIDTH = 80 * mm
SIGNATURE_TABLE_ROW_HEIGHT = 4 * mm


def generate_lvap_state_remittance_form(pdf_dict):
    buff = cStringIO.StringIO()
    doc = BaseDocTemplate(buff, pagesize=letter)

    f = Frame(
        gutters[0],
        gutters[2],
        usable_width,
        usable_height,
        topPadding=50,
        leftPadding=20,
        rightPadding=50,
        showBoundary=0
    )
    main_template = PageTemplate(id="main_template", frames=[f])
    doc.addPageTemplates(main_template)

    story = _create_story(pdf_dict)
    doc.build(story, canvasmaker=PageNumCanvas)
    #del doc

    buff.seek(0)
    return buff


def _create_story(doc_data):
    story = []

    story.append(
        Paragraph(
            "<strong>Georgia Criminal Justice Coordinating Council<br />Local Victim Assistance Program –Surcharge Report</strong>",
            style=extend_style(styles["heading"], leading=14)
        )
    )

    story.append(
        Paragraph(
            """
            Please mail all reports to:<br />
            <b>Criminal Justice Coordinating Council<br />
            104 Marietta Street<br />
            Suite 440<br />
            Atlanta, Ga. 30303</b>
            """,
            style=extend_style(styles["body"], leading=14, spaceBefore=30)
        )
    )

    general_info_table = _create_general_info_table(doc_data)
    story.append(general_info_table)

    story.append(
        Paragraph("Agencies/ Organizations/Program who were paid the LVAP Surcharge Collected for the Period",
                  style=extend_style(styles["body"], spaceBefore=30))
    )

    payment_info_table = _create_payment_info_table(doc_data)
    story.append(payment_info_table)

    signature_table = _cretae_signature_table(doc_data)
    story.append(signature_table)

    story.append(
        Paragraph("Reports must be filed monthly and are due to the address stated above by the 15th of the following month in which the report covers.",
                  style=extend_style(styles["body"], firstLineIndent=24, spaceBefore=20))
    )

    story.append(
        Paragraph("The 2000 Georgia General Assembly enacted legislation to amend Article 8, Chapter 21 of Title 5 of the Official Code of Georgia to require the court officer in charge of collecting monies arising from fines pursuant to this Code Section and Code Section §15-21-133 to file a monthly financial report to the Criminal Justice Council. This report should state the amount of 5% fines collected and the agencies, organizations, or programs, which directly receive these funds in the same period from the said officer.",
                  style=extend_style(style=styles["body"], firstLineIndent=24, spaceBefore=20)
        )
      )

    return story


def _create_general_info_table(doc_data):
    data = [
        [
            Paragraph("County/City Reporting:", style=styles['body']),
            Paragraph("<b>{}</b>".format(doc_data["county/city"]), style=extend_style(styles['body'], leftIndent=0)),
            ""
        ],
        [
            '',
            Paragraph("(County Name/City Name)", style=styles['note']),
            ""
        ],
        [
            Paragraph("Court name and ORI Number:", style=styles['body']),
            Paragraph("<b>{}{}{}</b>".format(doc_data["court_name"], "&nbsp;"*10, doc_data["ori_number"]),
                      style=extend_style(styles['body'], leftIndent=0)
            ),
            ""
        ],
        [
            Paragraph(
                "(Juvenile, Magistrate, Municipal, Probate, State or Superior Court) Complete a separate form for each court served and Court ORI #",
                style=extend_style(styles['note'], alignment=TA_RIGHT)
            ),
            ""
        ],
        [
            Paragraph("Time Period of Report:", style=styles['body']),
            Paragraph("From: <u><b>{}</b></u>".format(_format_date(doc_data["date_range_from"])),
                      style=extend_style(styles['body'], leftIndent=0)),
            Paragraph("To: <u><b>{}</b></u>".format(_format_date(doc_data["date_range_to"])),
                          style=extend_style(styles['body'], leftIndent=0))
        ],
        [
            "",
            Paragraph("(i.e. {} thru {})".format(_format_short_date(doc_data["date_range_from"]), _format_short_date(doc_data["date_range_to"])),
                      style=extend_style(styles['note'], alignment=TA_CENTER)),
            ""
        ],
        [
            Paragraph("Total Amount of LVAP Surcharges Collected for the period:", style=styles['body']),
            "",
            Paragraph("<b>${}</b>".format(doc_data["total_amount"]), style=extend_style(styles['body'], leftIndent=0))
        ],
        [
            Paragraph("<u>(This amount is calculated by total applicable fines multiplied by 5%. This amount should equal the sum of the surcharge paid out below.)</u>",
                      style=extend_style(styles['note'], alignment=TA_CENTER, )),
            "", ""
        ]
    ]

    table = Table(
        data,
        spaceBefore=20,
        colWidths=(GENERAL_TABLE_FIRST_COL_WIDTH, None, None),
        rowHeights=[
            GENERAL_TABLE_BIG_ROW_HEIGHT,
            GENERAL_TABLE_SMALL_ROW_HEIGHT,
            GENERAL_TABLE_BIG_ROW_HEIGHT,
            GENERAL_TABLE_SMALL_ROW_HEIGHT,
            GENERAL_TABLE_BIG_ROW_HEIGHT,
            GENERAL_TABLE_SMALL_ROW_HEIGHT,
            GENERAL_TABLE_BIG_ROW_HEIGHT,
            GENERAL_TABLE_SMALL_ROW_HEIGHT
        ]
    )
    table.setStyle(extend_table_style(
        styles["iv-main-table"],
        [
            ('LINEBELOW', (1, 0), (2, 0), 0.5, colors.black),
            ('LINEBELOW', (1, 2), (1, 2), 0.5, colors.black),
            ('LINEBELOW', (2, 2), (2, 2), 0.5, colors.black),
            ('LINEBELOW', (2, 6), (2, 6), 0.5, colors.black),
            ('SPAN', (1, 1), (2, 1)),
            ('SPAN', (1, 2), (2, 2)),
            ('SPAN', (0, 3), (2, 3)),
            ('SPAN', (1, 5), (2, 5)),
            ('SPAN', (0, 6), (1, 6)),
            ('SPAN', (0, 7), (2, 7)),
        ]
    ))

    return table


def _create_payment_info_table(doc_data):
    data = [
        [
            Paragraph("<u>Name of Agencies Paid</u>", style=styles["body"]),
            Paragraph("<u>Amount</u>", style=styles["body"]),
            Paragraph("<u>Check Number</u>", style=styles["body"])
        ],
        [
            Paragraph("<u><b>Rockdale County Board of Commissioners</b></u>", style=styles["body"]),
            Paragraph("<u><b>${}</b></u>".format(doc_data["total_amount"]), style=styles["body"]),
            black_line_short
        ]
    ]

    table = Table(
        data,
        colWidths=(PAYMENT_TABLE_FIRST_COL_WIDTH, None, None),
        rowHeights=[PAYMENT_TABLE_ROW_HEIGHT, PAYMENT_TABLE_ROW_HEIGHT]
    )
    table.setStyle(styles["iv-main-table"])

    return table


def _cretae_signature_table(doc_data):
    data = [
        [
            Paragraph("<u>{}</u>".format("&nbsp;"*61), style=styles["body"]), "",
            Paragraph("<u>{}</u>".format(_format_date(doc_data["order_date"])), style=styles["body"])
        ],
        [
            Paragraph("Signature of Authorized Court Officer", style=styles["body"]),
            "",
            Paragraph("Date", style=styles["body"])
        ]
    ]

    table = Table(
        data,
        colWidths=(SIGNATURE_TABLE_FIRST_COL_WIDTH, None, SIGNATURE_TABLE_LAST_COL_WIDTH),
        rowHeights=[SIGNATURE_TABLE_ROW_HEIGHT, SIGNATURE_TABLE_ROW_HEIGHT],
        spaceBefore=40
    )
    table.setStyle(styles["iv-main-table"])

    return table


def _format_date(date_as_string):
    date = datetime.strptime(date_as_string, "%m/%d/%Y")
    formated_date = date.strftime("%B %d, %Y")
    return formated_date


def _format_short_date(date_as_string):
    date = datetime.strptime(date_as_string, "%m/%d/%Y")
    formated_date = date.strftime("%B %d")
    return formated_date
