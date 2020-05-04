import io
import os
import sys

parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from reportlab.platypus import (
    BaseDocTemplate,
    PageTemplate,
    Frame,
    Table,
    Paragraph,
    Spacer,
)
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab_styles import extend_style, styles, gutters, usable_width, usable_height


def generate_driver_information_exchange_sheet(data):
    def summary_section():
        story.append(
            Table(
                [
                    [
                        Paragraph(
                            "DRIVER INFORMATION EXCHANGE",
                            extend_style(styles["heading"], fontSize=14),
                        )
                    ]
                ],
                style=(
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ),
            )
        )
        story.append(Spacer(1, 12))
        story.append(Spacer(1, 12))
        story.append(
            Table(
                [
                    [
                        Paragraph("<b>Motorist Report #:</b>", styles["trastop"]),
                        Paragraph(data["motorist_timestamp"], styles["trastop"]),
                        Paragraph("<b>Investigating Agency:</b>", styles["trastop"]),
                        Paragraph(data["investigating_agency"], styles["trastop"]),
                    ]
                ],
                colWidths=[1.2 * inch, 2 * inch, 1.2 * inch, 2 * inch],
                style=(
                    ("LEFTPADDING", (0, 0), (-1, -1), 0.5),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0.5),
                ),
            )
        )
        story.append(
            Table(
                [
                    [
                        Paragraph("<b>Officer's Name/ID: </b>", styles["trastop"]),
                        Paragraph(
                            data["officer_name"] + " / " + data["badge_num"],
                            styles["trastop"],
                        ),
                        Paragraph("<b>Agency Report Number: </b>", styles["trastop"]),
                        Paragraph(data["arn"], styles["trastop"]),
                    ]
                ],
                colWidths=[1.2 * inch, 2 * inch, 1.2 * inch, 2 * inch],
                style=(
                    ("LEFTPADDING", (0, 0), (-1, -1), 0.5),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0.5),
                ),
            )
        )
        story.append(
            Table(
                [
                    [
                        Paragraph("<b>County: </b>", styles["trastop"]),
                        Paragraph(data["county"], styles["trastop"]),
                        Paragraph("<b>City/Township: </b>", styles["trastop"]),
                        Paragraph(data["loc_city_township"], styles["trastop"]),
                    ]
                ],
                colWidths=[1.2 * inch, 2 * inch, 1.2 * inch, 2 * inch],
                style=(
                    ("LEFTPADDING", (0, 0), (-1, -1), 0.5),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0.5),
                ),
            )
        )
        story.append(
            Table(
                [
                    [
                        Paragraph("<b>Crash Date: </b>", styles["trastop"]),
                        Paragraph(data["crash_date"], styles["trastop"]),
                        Paragraph("<b>Crash Location: </b>", styles["trastop"]),
                        Paragraph(data["crash_location"], styles["trastop"]),
                    ]
                ],
                colWidths=[1.2 * inch, 2 * inch, 1.2 * inch, 2 * inch],
                style=(
                    ("LEFTPADDING", (0, 0), (-1, -1), 0.5),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0.5),
                ),
            )
        )
        story.append(Spacer(1, 12))
        story.append(Spacer(1, 12))

    def unit_section(unit_num, unit):
        story.append(
            Table(
                [
                    [
                        Paragraph(
                            "<b>UNIT: " + unit_num + "</b>",
                            extend_style(styles["boxed"], fontSize=14),
                        )
                    ]
                ],
                style=(
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ),
            )
        )

        story.append(
            Table(
                [
                    [
                        Paragraph("<b>Driver's Name: </b>", styles["trastop"]),
                        Paragraph(
                            unit["Driver"]["DrvrFirstName"]
                            + " "
                            + unit["Driver"]["DrvrMidName"]
                            + " "
                            + unit["Driver"]["DrvrLastName"],
                            styles["trastop"],
                        ),
                        Paragraph("<b>Driver's Address: </b>", styles["trastop"]),
                        Paragraph(
                            unit["Driver"]["DrvrAddr"]
                            + " "
                            + unit["Driver"]["DrvrCity"]
                            + " "
                            + unit["Driver"]["DrvrState"]
                            + " "
                            + unit["Driver"]["DrvrZipCode"],
                            styles["trastop"],
                        ),
                    ]
                ],
                colWidths=[1.2 * inch, 2 * inch, 1.2 * inch, 2 * inch],
                style=(
                    ("LEFTPADDING", (0, 0), (-1, -1), 0.5),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0.5),
                ),
            )
        )

        story.append(
            Table(
                [
                    [
                        Paragraph("<b>Driver Phone: </b>", styles["trastop"]),
                        Paragraph(unit["Driver"]["DrvrPhoneNbr"], styles["trastop"]),
                        Paragraph(
                            "<b>Vehicle Year, Make, Model: </b>", styles["trastop"]
                        ),
                        Paragraph(
                            unit.get("Vehicle", {}).get("VehcYr", "")
                            + ", "
                            + unit.get("Vehicle", {}).get("MAKE", "")
                            + ", "
                            + unit.get("Vehicle", {}).get("MODEL", ""),
                            styles["trastop"],
                        ),
                    ]
                ],
                colWidths=[1.2 * inch, 2 * inch, 1.2 * inch, 2 * inch],
                style=(
                    ("LEFTPADDING", (0, 0), (-1, -1), 0.5),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0.5),
                ),
            )
        )
        story.append(
            Table(
                [
                    [
                        Paragraph("<b>Plate No. /State: </b>", styles["trastop"]),
                        Paragraph(
                            unit.get("Vehicle", {}).get("VehcPlateNbr", "")
                            + " /"
                            + unit.get("Vehicle", {}).get("VehcPlateState", ""),
                            styles["trastop"],
                        ),
                        Paragraph("<b>Driver's License No.: </b>", styles["trastop"]),
                        Paragraph(unit["Driver"]["DrvrLicNbr"], styles["trastop"]),
                    ]
                ],
                colWidths=[1.2 * inch, 2 * inch, 1.2 * inch, 2 * inch],
                style=(
                    ("LEFTPADDING", (0, 0), (-1, -1), 0.5),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0.5),
                ),
            )
        )
        story.append(
            Table(
                [
                    [
                        Paragraph("<b>Vehicle Owner's Name: </b>", styles["trastop"]),
                        Paragraph(
                            unit.get("Vehicle", {})
                            .get("Owner", {})
                            .get("OwnFirstName", "")
                            + " "
                            + unit.get("Vehicle", {})
                            .get("Owner", {})
                            .get("OwnMidName", "")
                            + " "
                            + unit.get("Vehicle", {})
                            .get("Owner", {})
                            .get("OwnLastName", ""),
                            styles["trastop"],
                        ),
                        Paragraph(
                            "<b>Vehicle Owner's Address: </b>", styles["trastop"]
                        ),
                        Paragraph(
                            unit.get("Vehicle", {}).get("Owner", {}).get("OwnAddr", "")
                            + " "
                            + unit.get("Vehicle", {})
                            .get("Owner", {})
                            .get("OwnCity", "")
                            + " "
                            + unit.get("Vehicle", {})
                            .get("Owner", {})
                            .get("OwnState", "")
                            + " "
                            + unit.get("Vehicle", {})
                            .get("Owner", {})
                            .get("OwnZipCode", ""),
                            styles["trastop"],
                        ),
                    ]
                ],
                colWidths=[1.2 * inch, 2 * inch, 1.2 * inch, 2 * inch],
                style=(
                    ("LEFTPADDING", (0, 0), (-1, -1), 0.5),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0.5),
                ),
            )
        )
        story.append(
            Table(
                [
                    [
                        Paragraph(
                            "<b>Vehicle Owner's Insurance Company: </b>",
                            styles["trastop"],
                        ),
                        Paragraph(
                            unit.get("Vehicle", {})
                            .get("Owner", {})
                            .get("OwnINSRCo", ""),
                            styles["trastop"],
                        ),
                        Paragraph(
                            "<b>Vehicle Owner's Policy No.: </b>", styles["trastop"]
                        ),
                        Paragraph(
                            unit.get("Vehicle", {})
                            .get("Owner", {})
                            .get("OwnINSRPolicyNbr", ""),
                            styles["trastop"],
                        ),
                    ]
                ],
                colWidths=[1.2 * inch, 2 * inch, 1.2 * inch, 2 * inch],
                style=(
                    ("LEFTPADDING", (0, 0), (-1, -1), 0.5),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0.5),
                ),
            )
        )
        story.append(
            Table(
                [
                    [
                        Paragraph(
                            "<b>Vehicle Owner's Phone Number: </b>", styles["trastop"],
                        ),
                        Paragraph(
                            unit.get("Vehicle", {})
                            .get("Owner", {})
                            .get("OwnPhoneNbr", ""),
                            styles["trastop"],
                        ),
                        None,
                        None,
                    ]
                ],
                colWidths=[1.2 * inch, 2 * inch, 1.2 * inch, 2 * inch],
                style=(
                    ("LEFTPADDING", (0, 0), (-1, -1), 0.5),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0.5),
                ),
            )
        )
        story.append(Spacer(1, 12))
        story.append(Spacer(1, 12))

    def instruction_section():
        story.append(
            Table(
                [
                    [
                        Paragraph(
                            "COMPLETE MOTORIST REPORT",
                            extend_style(styles["heading"], fontSize=14),
                        )
                    ]
                ],
                style=(
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ),
            )
        )

        story.append(
            Paragraph(
                "Please use the information for your unit number above to assist you in completing your Illinois Motorist Report, which can be found online at www.payquicket.com or in person at the %s, %s"
                % (data["investigating_agency"], data["agency_address"]),
                styles["detail"],
            )
        )

        story.append(Spacer(1, 12))

        story.append(
            Table(
                [
                    [
                        Paragraph(
                            "PURCHASE COPY OF CRASH REPORT",
                            extend_style(styles["heading"], fontSize=14),
                        )
                    ]
                ],
                style=(
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ),
            )
        )
        story.append(
            Paragraph(
                "Please use the information from your unit number above to assist you in purchasing a copy of the complete Crash Report, which can be found online at www.payquicket.com.",
                styles["detail"],
            )
        )
        story.append(Spacer(1, 12))

        story.append(
            Table(
                [
                    [
                        Paragraph(
                            "LEGAL REQUIREMENTS",
                            extend_style(styles["heading"], fontSize=14),
                        )
                    ]
                ],
                style=(
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ),
            )
        )
        story.append(
            Paragraph(
                "The driver of any motor vehicle involved in a crash which results in injury, death, or damage to any one person's property in excess of $1,500 (or, $500 if any driver is not insured) must complete an IL Motorist Report and send to the Illinois Department of Transportation (IDOT) within 10 days after the crash. <br /> <br /> If the driver is physically incapable of completing the report, the owner or another occupant of the vehicle should do so. <br /> (See Sections 625 ILCS 5/7 - 100 through 5/7 - 216 of the Illinois Vehicle Code for complete statute.)",
                styles["detail"],
            )
        )
        story.append(Spacer(1, 12))

        story.append(
            Table(
                [
                    [
                        Paragraph(
                            "DUTY TO REPORT ACCIDENT (625 ILCS 5/11-406)",
                            extend_style(styles["heading"], fontSize=14),
                        )
                    ]
                ],
                style=(
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ),
            )
        )
        story.append(
            Paragraph(
                "Illinois statute requires the driver of a vehicle involved in a crash to complete an Illinois Motorist Report. Please go to the URL below to complete this electronically. If you are unable to do so, please call (217) 785-2736 for asssitance. <br /> <center><b>http://motoristreport.illinois.gov</b></center>",
                styles["detail"],
            )
        )
        story.append(Spacer(1, 12))

    story = []
    summary_section()
    units = data["units"]
    for i, unit in enumerate(units):
        unit_section(str(i + 1), unit)
    instruction_section()

    streamBuffer = io.BytesIO()
    f = Frame(gutters[0], gutters[2], usable_width, usable_height, showBoundary=0)
    main_template = PageTemplate(id="main_template", frames=[f])
    doc = BaseDocTemplate(streamBuffer, pagesize=letter)
    doc.addPageTemplates(main_template)
    doc.build(story)

    streamBuffer.seek(0)
    return streamBuffer
