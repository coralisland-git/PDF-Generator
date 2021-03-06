# This Python file uses the following encoding: utf-8
import cStringIO
from datetime import datetime
from document_specific_styles import *


GENERAL_TABLE_BIG_ROW_HEIGHT = 7 * mm
GENERAL_TABLE_SMALL_ROW_HEIGHT = 4 * mm
GENERAL_TABLE_FIRST_COL_WIDTH = 65 * mm
PAYMENT_TABLE_FIRST_COL_WIDTH = 90 * mm
PAYMENT_TABLE_ROW_HEIGHT = 10 * mm
SIGNATURE_TABLE_FIRST_COL_WIDTH = 100 * mm
SIGNATURE_TABLE_LAST_COL_WIDTH = 80 * mm
SIGNATURE_TABLE_ROW_HEIGHT = 10 * mm
SIGNATURE_TABLE_ANOTAITON_ROW_HEIGHT = 5 * mm
SIGNATURE_TABLE_CHECK_ROW_HEIGHT = 6 * mm


def generate_local_victim_remittance_report(pdf_dict):
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
            "<strong>LOCAL VICTIM ASSISTANCE FUND REMITTANCE REPORT</strong>",
            style=extend_style(styles["heading"], leading=14)
        )
    )

    story.append(
        Paragraph(
            """
            Please mail all reports to:<br />
            <b>Attn: Gwen Patterson <br />
            Dekalb County Finance Dept<br />
            1300 Commerce Drive<br />
            Decatur, Ga. 30303</b>
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

    signature_table = create_signature_table(doc_data)
    story.append(signature_table)

    story.append(
        Paragraph("The 2006 Georgia General Assembly enacted legislation to amend Article 8 of Chapter 21 of Title 5 of "
                  "the Official Code of Georgia to require the court officer in charge of collecting moneys arising from "
                  "fines pursuant to this Code Section and Code Section §15-21-133 to file a monthly financial report to"
                  " the Criminal Justice Council. This report should state the amount of 5% fines collected and the "
                  "agencies, organizations, or programs, which directly received these funds in the same period from the "
                  "said officer. Inquries should be directed to the Criminal Justice Coordinating Council, 503 Oak Place, "
                  "Suite 540, Atlanta, Georgia 30349, (404) 559-4949",
                 style=extend_style(style=styles["body"], spaceBefore=20))
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
            Paragraph("Court name", style=styles['body']),
            Paragraph("<b>{}{}{}</b>".format(doc_data["court_name"], "&nbsp;"*10, ""),
                      style=extend_style(styles['body'], leftIndent=0)
            ),
            ""
        ],
        [
            Paragraph(
                "(Juvenile, Magistrate, Municipal, Probate, State or Superior Court) Complete a separate form for each court served",
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
            Paragraph("", style=styles["body"]),
            Paragraph("<u>Number of Cases</u>", style=styles["body"]),
            Paragraph("<u>Amount Distributed</u>", style=styles["body"])
        ],
        [
            Paragraph("<u><b>Local Victim Assistance Fund</b></u>", style=styles["body"]),
            Paragraph("<u><b>{}</b></u>".format(doc_data["cases_count"]), style=styles["body"]),
            Paragraph("<u><b>${}</b></u>".format(doc_data["amount_distributed"]), style=styles["body"]),
        ]
    ]

    table = Table(
        data,
        colWidths=(80 * mm, 50 * mm, 50 * mm),
        rowHeights=[PAYMENT_TABLE_ROW_HEIGHT, PAYMENT_TABLE_ROW_HEIGHT]
    )
    table.setStyle(styles["iv-main-table"])

    return table


def create_signature_table(doc_data):
    data = [
        [
            Paragraph("<u>{}</u>".format(doc_data["check_number"] + "&nbsp;" * (35 - len(doc_data["check_number"])*2)),
                      style=styles["check_body"]),
            "",
            Paragraph("<u>{}</u>".format("$" + doc_data["check_amount"] + "&nbsp;" * (35 - len(doc_data["check_number"])*2)),
                      style=styles["check_body"]),
        ],
        [
            Paragraph("Check Number", style=styles["check_body"]),
            "",
            Paragraph("Check Amount", style=styles["check_body"]),
        ],
        [None],
        [
            Paragraph("<u>{}</u>".format("&nbsp;" * 75), style=styles["body"]),
            "",
            Paragraph("<u>{}</u>".format(_format_date(doc_data["order_date"])), style=styles["body"]),
        ],
        [
            Paragraph("Signature of Individual Filling Report/Title", style=styles["body"]),
            "",
            Paragraph("Date", style=styles["body"])
        ],
        [
            Paragraph("<u>{}</u>".format(doc_data["printed_name"] + get_remain_space(doc_data["printed_name"])),
                      style=styles["body"]),
            "",
            Paragraph("<u>{}</u>".format(doc_data["phone_number"] + get_remain_space(doc_data["phone_number"])),
                      style=styles["body"]),
        ],
        [
            Paragraph("Printed Name of Individual Filling Report", style=styles["body"]),
            "",
            Paragraph("Contact's Phone Number", style=styles["body"])
        ],
        [
            Paragraph("<u>{}</u>".format(doc_data["email"] + get_remain_space(doc_data["email"])),
                      style=styles["body"]),
            "",
            ""
        ],
        [
            Paragraph("Contact's E-Mail Address", style=styles["body"]),
            "",
            ""
        ],
    ]

    table = Table(
        data,
        colWidths=(SIGNATURE_TABLE_FIRST_COL_WIDTH, None, SIGNATURE_TABLE_LAST_COL_WIDTH),
        rowHeights=[SIGNATURE_TABLE_ROW_HEIGHT, SIGNATURE_TABLE_ANOTAITON_ROW_HEIGHT, SIGNATURE_TABLE_CHECK_ROW_HEIGHT,
                    SIGNATURE_TABLE_ANOTAITON_ROW_HEIGHT, SIGNATURE_TABLE_ANOTAITON_ROW_HEIGHT,
                    SIGNATURE_TABLE_ROW_HEIGHT, SIGNATURE_TABLE_ANOTAITON_ROW_HEIGHT, SIGNATURE_TABLE_ROW_HEIGHT,
                    SIGNATURE_TABLE_ANOTAITON_ROW_HEIGHT],
        spaceBefore=20
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


def get_remain_space(str):
    return "&nbsp;" * (75 - len(str)*2)
