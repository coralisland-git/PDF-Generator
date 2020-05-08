import io
import os
import sys
from reportlab_styles import extend_style, styles, gutters, usable_width, usable_height

parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from reportlab.lib import colors
from reportlab.platypus import (
    BaseDocTemplate,
    PageTemplate,
    Frame,
    Table,
    Paragraph,
    Spacer,
    PageBreak
)
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter


def summary_section(data):
    return [
        Table(
            [
                [
                    Paragraph(
                        "DRIVER INFORMATION EXCHANGE",
                        extend_style(styles["heading"], fontSize=14),
                    )
                ]
            ],
            colWidths=[7.5 * inch],
            style=(
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ),
        ),
        Spacer(1, 8),
        Table(
            [
                [
                    Paragraph("<b>Motorist Report #:</b>", styles["trastop"]),
                    Paragraph(data["motorist_timestamp"], styles["trastop"]),
                    Paragraph("<b>Investigating Agency:</b>", styles["trastop"]),
                    Paragraph(data["investigating_agency"], styles["trastop"]),
                ],
                [
                    Paragraph("<b>Officer's Name/ID: </b>", styles["trastop"]),
                    Paragraph(
                        data["officer_name"] + " / " + data["badge_num"],
                        styles["trastop"],
                    ),
                    Paragraph("<b>Agency Report Number: </b>", styles["trastop"]),
                    Paragraph(data["arn"], styles["trastop"]),
                ],
                [
                    Paragraph("<b>County: </b>", styles["trastop"]),
                    Paragraph(data["county"], styles["trastop"]),
                    Paragraph("<b>City/Township: </b>", styles["trastop"]),
                    Paragraph(data["loc_city_township"], styles["trastop"]),
                ],
                [
                    Paragraph("<b>Crash Date: </b>", styles["trastop"]),
                    Paragraph(data["crash_date"], styles["trastop"]),
                    Paragraph("<b>Crash Location: </b>", styles["trastop"]),
                    Paragraph(data["crash_location"], styles["trastop"]),
                ]
            ],
            colWidths=[1.2 * inch, 2.55 * inch, 1.2 * inch, 2.55 * inch],
            style=(
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ),
        ),
    ]


def instruction_section(data):
    return [
        Table(
            [
                [
                    Paragraph(
                        "COMPLETE MOTORIST REPORT",
                        styles["heading-mini-instructions"],
                    )
                ],
                [
                    Paragraph(
                        "Please use the information for your unit number above to assist you in completing your Illinois Motorist Report, which can be found online at www.payquicket.com or in person at the %s, %s" % (
                            data["investigating_agency"], data["agency_address"]),
                        styles["trastop"],
                    )
                ]
            ],
            colWidths=[7.5 * inch],
            style=(
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ),
        ),
        Spacer(1, 5),
        Table(
            [
                [
                    Paragraph(
                        "PURCHASE COPY OF CRASH REPORT",
                        styles["heading-mini-instructions"],
                    )
                ],
                [
                    Paragraph(
                        "Please use the information from your unit number above to assist you in purchasing a copy of the complete Crash Report, which can be found online at www.payquicket.com.",
                        styles["trastop"],
                    )
                ]
            ],
            colWidths=[7.5 * inch],
            style=(
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ),
        ),
        Spacer(1, 5),
        Table(
            [
                [
                    Paragraph(
                        "LEGAL REQUIREMENTS",
                        styles["heading-mini-instructions"],
                    )
                ],
                [
                    Paragraph(
                        "The driver of any motor vehicle involved in a crash which results in injury, death, or damage to any one person's property in excess of $1,500 (or, $500 if any driver is not insured) must complete an IL Motorist Report and send to the Illinois Department of Transportation (IDOT) within 10 days after the crash. <br /> <br /> If the driver is physically incapable of completing the report, the owner or another occupant of the vehicle should do so. <br /> (See Sections 625 ILCS 5/7 - 100 through 5/7 - 216 of the Illinois Vehicle Code for complete statute.)",
                        styles["trastop"],
                    )
                ]
            ],
            colWidths=[7.5 * inch],
            style=(
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ),
        ),
        Spacer(1, 5),
        Table(
            [
                [
                    Paragraph(
                        "DUTY TO REPORT ACCIDENT (625 ILCS 5/11-406)",
                        styles["heading-mini-instructions"],
                    )
                ],
                [
                    Paragraph(
                        "Illinois statute requires the driver of a vehicle involved in a crash to complete an Illinois Motorist Report. Please go to the URL below to complete this electronically. If you are unable to do so, please call (217) 785-2736 for asssitance. <br /> <center><b>http://motoristreport.illinois.gov</b></center>",
                        styles["trastop"],
                    )
                ]
            ],
            colWidths=[7.5 * inch],
            style=(
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ),
        )
    ]


def unit_section(unit_num, unit):
    driver = unit["Driver"]
    vehicle = unit.get("Vehicle", {})
    vehicle_owner = unit.get("Vehicle", {}).get("Owner", {})
    return [
        Table(
            [
                [
                    Paragraph(
                        "<b>UNIT: %s </b>" % unit_num,
                        styles["trastop"]
                    )
                ]
            ],
            style=(
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("LINEBELOW", (0, 0), (-1, -1), 1, colors.black)
            ),
        ),
        Table(
            [
                [
                    Paragraph(
                        "<b>Driver's Name: </b> %s %s %s" % (driver["DrvrFirstName"], driver["DrvrMidName"], driver["DrvrLastName"]),
                        styles["trastop"]
                    ),
                ],
                [
                    Paragraph(
                        "<b>Driver's Address: </b> %s %s %s %s" % (driver["DrvrAddr"], driver["DrvrCity"], driver["DrvrState"], driver["DrvrZipCode"]),
                        styles["trastop"]
                    ),
                ],
                [
                    Paragraph(
                        "<b>Driver Phone: </b> %s" % driver["DrvrPhoneNbr"],
                        styles["trastop"]
                    ),
                ],
                [
                    Paragraph(
                        "<b>Vehicle Year, Make, Model: </b> %s, %s, %s" % (vehicle.get("VehcYr", ""), vehicle.get("MAKE", ""), vehicle.get("MODEL", "")),
                        styles["trastop"],
                    ),
                ],
                [
                    Paragraph(
                        "<b>Plate No./State: </b> %s/%s" % (vehicle.get("VehcPlateNbr", ""), vehicle.get("VehcPlateState", "")),
                        styles["trastop"]
                    ),
                ],
                [
                    Paragraph(
                        "<b>Driver's License No.: </b> %s" % unit["Driver"]["DrvrLicNbr"],
                        styles["trastop"]
                    ),
                ],
                [
                    Paragraph(
                        "<b>Vehicle Owner's Name: </b> %s %s %s" % (vehicle_owner.get("OwnFirstName", ""), vehicle_owner.get("OwnMidName", ""), vehicle_owner.get("OwnLastName", "")),
                        styles["trastop"]
                    ),
                ],
                [
                    Paragraph(
                        "<b>Vehicle Owner's Address: </b> %s %s %s %s" % (vehicle_owner.get("OwnAddr", ""), vehicle_owner.get("OwnCity", ""), vehicle_owner.get("OwnState", ""), vehicle_owner.get("OwnZipCode", "")),
                        styles["trastop"]
                    ),
                ],
                [
                    Paragraph(
                        "<b>Vehicle Owner's Insurance Company: </b> %s" % vehicle_owner.get("OwnINSRCo", ""),
                        styles["trastop"],
                    ),
                ],
                [
                    Paragraph(
                        "<b>Vehicle Owner's Policy No.: </b> %s" % vehicle_owner.get("OwnINSRPolicyNbr", ""),
                        styles["trastop"]
                    ),
                ],
                [
                    Paragraph(
                        "<b>Vehicle Owner's Phone Number: </b> %s" % vehicle_owner.get("OwnPhoneNbr", ""),
                        styles["trastop"],
                    ),
                ]
            ],
            style=(
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
            ),
        ),
    ]


def create_report(data):
    units = []
    for i, unit in enumerate(data["units"]):
        units.append(unit_section(str(i + 1), unit))

    index = 0
    length_of_units = len(units)
    summary_height = get_height_of_section(summary_section(data))
    instruction_height = get_height_of_section(instruction_section(data))
    units_height = 0
    page = summary_section(data)
    while index < length_of_units:
        first_column_unit = units[index]
        second_column_unit = None
        index += 1
        if index < length_of_units:
            second_column_unit = units[index]
        unit_table = Table(
            [
                [
                    first_column_unit,
                    second_column_unit
                ]
            ],
            colWidths=[3.75 * inch, 3.75 * inch],
            style=(
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("VALIGN", (0, 0), (-1, -1), "TOP")
            ),
        )
        units_height += unit_table.wrap(usable_width, 0)[1]
        if (summary_height + units_height + instruction_height) < usable_height:
            page.append(unit_table)
        else:
            units_height = unit_table.wrap(usable_width, 0)[1]
            page.extend(instruction_section(data))
            page.append(PageBreak())
            page.extend(summary_section(data))
            page.append(unit_table)
        index += 1

    page.extend(instruction_section(data))
    page.append(PageBreak())
    return page


def get_height_of_section(story):
    height = 0
    for flowable in story:
        height += flowable.wrap(usable_width, 0)[1]
    return height


def generate_driver_information_exchange_sheet(data):
    stream_buffer = io.BytesIO()
    f = Frame(gutters[0], gutters[2], usable_width, usable_height, showBoundary=0)
    main_template = PageTemplate(id="main_template", frames=[f])
    doc = BaseDocTemplate(stream_buffer, pagesize=letter)
    doc.addPageTemplates(main_template)
    doc.build(create_report(data))

    stream_buffer.seek(0)
    return stream_buffer
