import cStringIO
import datetime
import shutil
from reportlab.lib.units import inch
import os
from dateutil.parser import parse

from reportlab.platypus import Paragraph, Spacer, Table, KeepTogether, Image, PageBreak

from env.constants import Municipality
from reportlab_styles import (
    styles,
    SimpleDocTemplate,
    letter,
    Frame,
    RotatedPara,
    usable_width,
    colors,
    mm,
    PageTemplate,
)

from reportlab.graphics.barcode import code128


def incident_private_notes(story, citation_info=None):
    if citation_info is None:
        citation_info = {}

    private_notes = citation_info.get("incident_private_notes", "")

    story.append(PageBreak())
    story.append(
        RotatedPara("OFFICER'S NOTES", style=styles["rotated_detail_incident"])
    )

    story.append(
        Table(
            [
                [
                    Paragraph(
                        "OFFICER'S NOTES: %s" % private_notes, styles["detail-mini-utc"]
                    )
                ]
            ]
        )
    )

    return


def generate_il_state_pdf(citation_info, copy_type="Internal"):

    buff = cStringIO.StringIO()

    filename = "{ticket_number}.pdf".format(
        ticket_number=citation_info["ticket_number"]
    )
    key = "/".join(["Citation", citation_info["case_number"], filename])
    story = [
        Paragraph(
            "ILLINOIS CITATION AND COMPLAINT", style=styles["detail-compact-bold"]
        ),
        Paragraph("%s PD" % Municipality().name.upper(), styles["detail-compact-bold"]),
    ]

    doc = SimpleDocTemplate(
        buff,
        leftPadding=0,
        rightPadding=0,
        bottomPadding=0,
        topPadding=0,
        wordWrap=None,
        pagesize=letter,
        leftMargin=0.10 * inch,
        rightMargin=0.075 * inch,
        topMargin=0.25 * inch,
        bottomMargin=0.1 * inch,
    )
    column_gap = 0.30 * inch

    f_left = Frame(
        doc.rightMargin * 2,
        doc.bottomMargin,
        doc.width / 2 - 2,
        doc.height,
        id="left",
        rightPadding=column_gap,
        showBoundary=0,
    )
    f_right = Frame(
        doc.leftMargin + doc.width / 2 + 2,
        doc.bottomMargin,
        doc.width / 2 - 2,
        doc.height,
        id="right",
        leftPadding=column_gap / 2,
        showBoundary=2,
    )

    def _bool_to_checkbox(value):
        img_fname = "closed_box.png" if value else "open_box.png"
        img_path = os.path.join(os.getcwd(), "images", img_fname)
        return "<img src='{img_path}' valign='middle' width='10' height='10'/>".format(
            img_path=img_path
        )

    def _barcode_code128(value, width):
        barcode128 = code128.Code128(value, barWidth=width * 0.01, quiet=0)
        return barcode128

    def complaint_info(citation_info=None):
        if citation_info is None:
            citation_info = {}
        complaint = {  #'': citation.get('', ''),
            "case_num": citation_info.get("case_number", ""),
            "agency_ref_number": citation_info.get(
                "complainant_agency_report_number", ""
            ),
            "ticket_number": citation_info.get("ticket_number", ""),
            "county": citation_info.get("municipality_county", ""),
            "township": citation_info.get("complainant_municipality_township", ""),
            "village": citation_info.get("village", ""),
            "ref_id": citation_info.get("ref_id", ""),
        }
        story.append(RotatedPara("COMPLAINT", style=styles["rotated_detail_complaint"]))
        barcode_width = usable_width * 0.225
        barcode_obj = _barcode_code128(citation_info["ticket_number"], barcode_width)
        barcode_table = Table(
            [[barcode_obj], [citation_info["ticket_number"]]],
            barcode_width,
            style=[("FONTSIZE", (0, 0), (-1, -1), 8), ('ALIGN', (0, 0), (0, -1), "CENTER")],
        )

        story.append(
            Table(
                [
                    [
                        barcode_table,
                        Paragraph(
                            "Ticket Number: <b>%s</b>" % complaint["ticket_number"],
                            styles["detail-mini-utc"],
                        ),
                    ],
                    [None, Paragraph("DCN", styles["detail-mini-utc"]), None],
                    [
                        None,
                        Paragraph(
                            "<b> %s COPY </b>" % copy_type, styles["detail-mini-utc"]
                        ),
                    ],
                ],
                style=[
                    ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    ("SPAN", (0, 0), (0, -1)),
                    ("SPAN", (1, 2), (-1, 2)),
                    ("SPAN", (1, 0), (-1, 0)),
                    ("VALIGN", (0, 0), (0, 0), "TOP"),
                    ("VALIGN", (1, 0), (1, 0), "TOP"),
                    ("VALIGN", (2, 0), (2, 0), "TOP"),
                    ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                ],
                colWidths=(50 * mm, 25 * mm, 25 * mm),
                rowHeights=(5 * mm, 5 * mm, 5 * mm),
                hAlign="LEFT",
            )
        )

        story.append(
            Table(
                [
                    [
                        Paragraph("CIRCUIT COURT CASE #:", styles["detail-mini-utc"]),
                        # None, None,
                    ],
                    [
                        Paragraph(
                            "Agency and Reference ID: <b>%s</b>"
                            % complaint["agency_ref_number"],
                            styles["detail-mini-utc-addons"],
                        )
                    ],
                    [
                        Paragraph(
                            "COUNTY OF: <b>%s</b>" % complaint["county"],
                            styles["detail-mini-utc"],
                        ),
                        None,
                        Paragraph(
                            "TOWNSHIP OF: <b>%s</b>" % complaint["township"],
                            styles["detail-mini-utc"],
                        ),
                        None,
                    ],
                    [
                        Paragraph(
                            "{cb}City/ Village of {municipality_name}, {state}".format(
                                cb=_bool_to_checkbox(
                                    citation_info["complainant_is_municipality"]
                                ),
                                municipality_name=Municipality().name,
                                state=Municipality().state,
                            ),
                            styles["detail-mini-utc-addons"],
                        ),
                        # Paragraph('{municipality_name}, {state}'.format(municipality_name=Municipality().name, state=Municipality().state), styles['detail-mini-utc-addons']),
                        None,
                        None,
                        Paragraph("VS.", styles["detail-mini-utc"]),
                    ],
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    ("SPAN", (0, 0), (1, 0)),
                    ("SPAN", (-1, 0), (-1, 0)),
                    ("SPAN", (1, -1), (2, -1)),
                    ("SPAN", (0, 3), (1, 3)),
                    ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                ],
                colWidths=(35 * mm, 20 * mm, 20 * mm, 25 * mm),
                rowHeights=(5 * mm, 5 * mm, 5 * mm, 5 * mm),
                hAlign="LEFT",
            )
        )

    def defendantInfo(citation_info=None):
        if citation_info is None:
            citation_info = {}
        defendant = {
            "apt": citation_info.get("defendant_address_apartment", ""),
            "city": citation_info.get("defendant_address_city", ""),
            "state": citation_info.get("defendant_address_state", ""),
            "street": citation_info.get("defendant_address_street", ""),
            "zip": citation_info.get("defendant_address_zip", ""),
            "dob": citation_info.get("defendant_date_of_birth", None),
            "lic_expiry": citation_info.get(
                "defendant_driver_license_expiration_date", ""
            ),
            "cdl": citation_info.get("defendant_driver_license_is_commercial", ""),
            "driver_license": citation_info.get("defendant_driver_license_number", ""),
            "driver_license_state": citation_info.get(
                "defendant_driver_license_state", ""
            ),
            "eyes": citation_info.get("defendant_eye_color", ""),
            "first_name": citation_info.get("defendant_first_name", ""),
            "hair": citation_info.get("defendant_hair_color", ""),
            "height": citation_info.get("defendant_height", ""),
            "last_name": citation_info.get("defendant_last_name", ""),
            "middle_name": citation_info.get("defendant_middle_initial", ""),
            "race": citation_info.get("defendant_race", ""),
            "sex": citation_info.get("defendant_sex", ""),
            "weight": citation_info.get("defendant_weight", ""),
        }

        story.append(RotatedPara("DEFENDANT", style=styles["rotated_detail_defendant"]))
        defendant["name"] = (
            defendant["last_name"]
            + ", "
            + defendant["first_name"]
            + " "
            + defendant["middle_name"]
        )
        defendant["dob_year"] = (
            datetime.datetime.strftime(defendant["dob"], "%Y")
            if defendant["dob"] is not None
            else ""
        )
        defendant["dob_month"] = (
            datetime.datetime.strftime(defendant["dob"], "%m")
            if defendant["dob"] is not None
            else ""
        )
        defendant["dob_date"] = (
            datetime.datetime.strftime(defendant["dob"], "%d")
            if defendant["dob"] is not None
            else ""
        )
        try:
            defendant_dob = "DOB: <b>%s</b>" % defendant["dob"].strftime("%m/%d/%Y")
        except:
            defendant_dob = "DOB: <b> </b>"

        story.append(
            Table(
                [
                    [
                        Paragraph(
                            "LAST NAME: %s" % defendant["last_name"],
                            styles["detail-mini-utc"],
                        ),
                        None,
                        None,
                        Paragraph("SID #: ", styles["detail-mini-utc"]),
                        None,
                    ],
                    [
                        Paragraph(
                            "FIRST NAME: %s" % defendant["first_name"],
                            styles["detail-mini-utc"],
                        ),
                        None,
                        None,
                        Paragraph(
                            "MIDDLE NAME: %s" % defendant["middle_name"],
                            styles["detail-mini-utc"],
                        ),
                        None,
                    ],
                    [],
                    [
                        Paragraph(
                            "ADDRESS: %s" % defendant["street"],
                            styles["detail-mini-utc"],
                        ),
                        None,
                        Paragraph("%s" % defendant["apt"], styles["detail-mini-utc"]),
                        None,
                        Paragraph(
                            "{cb_f} Female<br/>{cb_m} Male".format(
                                cb_f=_bool_to_checkbox(
                                    citation_info["defendant_sex"] == "F"
                                ),
                                cb_m=_bool_to_checkbox(
                                    citation_info["defendant_sex"] == "M"
                                ),
                            ),
                            styles["detail-mini-utc"],
                        ),
                    ],
                    [
                        None,
                        Paragraph(("STREET"), styles["detail-mini-utc-tiny"]),
                        # None,
                        Paragraph(("Apt#"), styles["detail-mini-utc-tiny"]),
                        None,
                        None,
                    ],
                    [
                        Paragraph(
                            "CITY: %s" % defendant["city"], styles["detail-mini-utc"]
                        ),
                        Paragraph(
                            "STATE: %s" % defendant["state"], styles["detail-mini-utc"]
                        ),
                        Paragraph(
                            "ZIP: %s" % defendant["zip"], styles["detail-mini-utc"]
                        ),
                    ],
                    [
                        Paragraph(
                            "DOB: %s" % defendant["dob"], styles["detail-mini-utc"]
                        ),
                        Paragraph(
                            "HEIGHT: %s" % defendant["height"],
                            styles["detail-mini-utc"],
                        ),
                        # None,
                        Paragraph(
                            "WEIGHT: %s" % defendant["weight"],
                            styles["detail-mini-utc"],
                        ),
                        # None,
                        Paragraph(
                            "EYES: %s" % defendant["eyes"], styles["detail-mini-utc"]
                        ),
                        # None,
                        Paragraph(
                            "HAIR: %s" % defendant["hair"], styles["detail-mini-utc"]
                        ),
                    ],
                    [
                        Paragraph(
                            "DR. LIC. : %s" % defendant["driver_license"],
                            styles["detail-mini-utc"],
                        ),
                        Paragraph(
                            "CDL: %s" % defendant["cdl"], styles["detail-mini-utc"]
                        ),
                        # None,
                        Paragraph(
                            "STATE: %s" % defendant["driver_license_state"],
                            styles["detail-mini-utc"],
                        ),
                        # None,
                        Paragraph(
                            "LIC EXPIRES: %s" % defendant["lic_expiry"],
                            styles["detail-mini-utc"],
                        ),
                    ],
                ],
                style=[
                    ("SPAN", (0, 0), (1, 0)),  # (col, row)
                    ("SPAN", (3, 0), (4, 0)),
                    ("SPAN", (0, 1), (1, 1)),
                    ("SPAN", (3, 1), (4, 1)),
                    ("SPAN", (0, 3), (1, 3)),
                    ("SPAN", (3, 7), (4, 7)),
                    ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                ],
                colWidths=(29 * mm, 20 * mm, 20 * mm, 17 * mm, 15 * mm),
                rowHeights=(
                    4 * mm,
                    4 * mm,
                    4 * mm,
                    6 * mm,
                    1 * mm,
                    4 * mm,
                    4 * mm,
                    4 * mm,
                ),
                hAlign="LEFT",
            )
        )

    def defendant_addon(citation_info=None):
        if citation_info is None:
            citation_info = {}

        bad_values = (None, "", " ")
        violation_date_obj = citation_info["violation_date"]
        violation_time_obj = citation_info["violation_time"]
        citation_info["violation_date"] = (
            datetime.datetime.strftime(violation_date_obj, "%Y-%m-%d")
            if citation_info["violation_date"] not in bad_values
            else ""
        )
        citation_info["violation_time"] = (
            datetime.datetime.strftime(
                datetime.datetime.combine(
                    violation_date_obj, citation_info["violation_time"]
                ),
                "%H:%M:%S",
            )
            if citation_info["violation_time"] not in bad_values
            else ""
        )
        citation_info["violation_date"] = violation_date_obj
        citation_info["violation_time"] = violation_time_obj

        story.append(
            Table(
                [
                    [
                        Paragraph(
                            "The undersigned states that on",
                            styles["detail-mini-utc-addons"],
                        ),
                        Paragraph(
                            "%s at %s"
                            % (
                                citation_info["violation_date"],
                                citation_info["violation_time"],
                            ),
                            styles["detail-mini-utc-addons"],
                        ),
                        # Paragraph(', styles['detail-mini-utc']), None, None
                        # Paragraph('%s' % citation_info['violation_date'], styles['detail-mini-utc']),  # requires date time module
                        # Paragraph('and', styles['detail-mini-utc-addons']),
                        # Paragraph('%s' % citation_info['violation_time'], styles['detail-mini-utc']),  # requires time module
                    ],
                    [
                        Paragraph(
                            "defendant did unlawfully operate:",
                            styles["detail-mini-utc-addons"],
                        ),
                        None,
                    ],
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    ("VALIGN", (1, 0), (1, 0), "BOTTOM"),
                    # ('VALIGN',(2,0),(2,0),'TOP'),
                    # ('VALIGN',(3,0),(3,0),'TOP')
                ],
                colWidths=(70 * mm, 34 * mm),
                rowHeights=(4 * mm),
                hAlign="LEFT",
            )
        )

    def vehicleInfo(citation_info):
        hazmat = citation_info["vehicle_has_hazardous_materials_indicator"]
        commercial = citation_info["vehicle_is_commercial"]
        large_pass = citation_info["vehicle_is_large_passenger_vehicle"]
        v_type = citation_info["vehicle_type"]
        other_codes = (
            v_type
            if v_type not in ["053", "081", "052", "084", "009", "086", "080", "043"]
            else ""
        )

        def vtype_is_x(x):
            return _bool_to_checkbox(x == v_type)

        veh_reg_date = (
            parse(citation_info["vehicle_registration_expiration_date"]).year
            if citation_info["vehicle_registration_expiration_date"]
            else ""
        )

        if citation_info is None:
            citation_info = {}
        vehicle = {
            "plate_number": citation_info.get("vehicle_plate", ""),
            "make": citation_info.get("vehicle_make", ""),
            "model": citation_info.get("vehicle_model", ""),
            "color": citation_info.get("vehicle_color", ""),
            "plate_type": citation_info.get("vehicle_type", ""),
            "plate_state": citation_info.get("vehicle_state", ""),
            "plate_exp": citation_info.get(
                "vehicle_registration_expiration_date", None
            ),
            "year": citation_info.get("vehicle_year", ""),
            "us_dot": citation_info.get("vehicle_united_states_dot_number", ""),
        }

        story.append(RotatedPara("VEHICLE", style=styles["rotated_detail_vehicle"]))

        def vtype_is_x(x):
            return _bool_to_checkbox(x == v_type)

        try:
            plate_exp = parse(vehicle["plate_exp"]).date().strftime("%m/%Y")
        except:
            plate_exp = ""

        # vehicle['plate_exp'] = datetime.datetime.strptime(vehicle['plate_exp'], "%Y-%m-%d") if vehicle['plate_exp'] is not None else ''
        # vehicle['plate_exp'] = datetime.datetime.strftime(vehicle['plate_exp'], "%m/%y") if vehicle['plate_exp'] is not None else ''

        story.append(
            Table(
                [
                    [
                        Paragraph(
                            "REG. NO. #: <b>%s</b>" % vehicle["plate_number"],
                            styles["detail-mini-utc"],
                        ),
                        None,
                        Paragraph(
                            "STATE: <b>%s</b>" % vehicle["plate_state"],
                            styles["detail-mini-utc"],
                        ),
                        Paragraph(
                            "MO/YEAR: <b>%s</b>" % plate_exp, styles["detail-mini-utc"]
                        ),
                        None,
                        Paragraph(
                            "US DOT#: <b>%s</b>" % vehicle["us_dot"],
                            styles["detail-mini-utc"],
                        ),
                        None,
                        None,
                    ],
                    [
                        Paragraph(
                            "MAKE: <b>%s</b>" % vehicle["make"],
                            styles["detail-mini-utc"],
                        ),
                        None,
                        Paragraph(
                            "YEAR: <b>%s</b>" % vehicle["year"],
                            styles["detail-mini-utc"],
                        ),
                        None,
                    ],
                    [
                        # unsure of what type is
                        Paragraph(
                            "TYPE: <b>%s</b>" % vehicle["model"],
                            styles["detail-mini-utc"],
                        ),
                        None,
                    ],
                    [
                        Paragraph(
                            "COLOR: <b>%s</b>" % vehicle["color"],
                            styles["detail-mini-utc"],
                        ),
                        None,
                        Paragraph("VEHICLE USE:", styles["detail-mini-utc"]),
                    ],
                    [
                        None,
                        None,
                        Paragraph(
                            "COMMERCIAL MOTOR VEHICLE", styles["detail-mini-utc"]
                        ),
                        None,
                        None,
                        Paragraph(
                            "YES{cb}".format(cb=_bool_to_checkbox(hazmat)),
                            styles["detail-mini-utc"],
                        ),
                        None,
                        Paragraph(
                            "NO{cb}".format(cb=_bool_to_checkbox(not hazmat)),
                            styles["detail-mini-utc"],
                        ),
                        None,
                    ],
                    [
                        None,
                        None,
                        Paragraph("PLACARDED HAZ. MATERIAL", styles["detail-mini-utc"]),
                        None,
                        None,
                        Paragraph(
                            "YES{cb}".format(cb=_bool_to_checkbox(commercial)),
                            styles["detail-mini-utc"],
                        ),
                        None,
                        Paragraph(
                            "NO{cb}".format(cb=_bool_to_checkbox(not commercial)),
                            styles["detail-mini-utc"],
                        ),
                    ],
                    [
                        None,
                        None,
                        Paragraph(
                            "COMMERCIAL MOTOR VEHICLE", styles["detail-mini-utc"]
                        ),
                        None,
                        None,
                        Paragraph(
                            "YES{cb}".format(cb=_bool_to_checkbox(hazmat)),
                            styles["detail-mini-utc"],
                        ),
                        None,
                        Paragraph(
                            "NO{cb}".format(cb=_bool_to_checkbox(not hazmat)),
                            styles["detail-mini-utc"],
                        ),
                    ],
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.red),
                    ("SPAN", (0, 0), (1, 0)),  # reg no
                    ("SPAN", (0, 1), (1, 1)),  # make
                    ("SPAN", (0, 2), (1, 2)),  # type
                    ("SPAN", (0, 3), (1, 3)),  # color
                    ("SPAN", (2, 0), (2, 0)),  # state
                    ("SPAN", (3, 0), (4, 0)),  # mo/year
                    ("SPAN", (2, 3), (3, 3)),  # vehicle use
                    ("SPAN", (5, 0), (8, 0)),  # us dot
                    ("SPAN", (-4, -3), (-2, -3)),  # yes
                    ("SPAN", (-2, -3), (-1, -3)),  # no
                    ("SPAN", (-4, -2), (-2, -2)),  # yes
                    ("SPAN", (-2, -2), (-1, -2)),  # no
                    ("SPAN", (-4, -1), (-2, -1)),  # yes
                    ("SPAN", (-2, -1), (-1, -1)),  # no
                    ("SPAN", (2, -3), (4, -3)),  # cmv
                    ("SPAN", (2, -2), (4, -2)),  # phm
                    ("SPAN", (2, -1), (4, -1)),  # 16+
                    ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                ],
                colWidths=(
                    15 * mm,
                    14 * mm,
                    17 * mm,
                    15 * mm,
                    8 * mm,
                    10 * mm,
                    8 * mm,
                    8 * mm,
                    5 * mm,
                ),
                rowHeights=(4 * mm, 4 * mm, 4 * mm, 4 * mm, 4 * mm, 4 * mm, 4 * mm),
                hAlign="LEFT",
            )
        )

    def violationplus(citation_info=None):
        if citation_info is None:
            citation_info = {}
        story.append(
            Table(
                [
                    [
                        Paragraph(
                            "Or, as a Pedestrian or Passenger, and upon a public highway, or other location , Specifically ",
                            styles["detail-mini-utc-addons"],
                        )
                    ],
                    [
                        Paragraph(
                            "{violation_location}".format(
                                violation_location=citation_info["violation_location"]
                            ),
                            styles["detail-mini-utc"],
                        )
                    ],
                    [
                        Paragraph(
                            "{cb} Urban District".format(
                                cb=_bool_to_checkbox(
                                    citation_info["violation_is_in_urban_district"]
                                )
                            ),
                            styles["detail-mini-utc-right"],
                        )
                    ],
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('SPAN', (0,0), (1,0)),
                    # ('SPAN', (-1,0), (-1,0)),
                    # ('SPAN', (1,-1), (-1,-1)),
                    ("BOX", (0, 0), (-1, -1), 0.25, colors.black)
                ],
                colWidths=(100 * mm),
                rowHeights=(5 * mm, 5 * mm, 5 * mm),
                hAlign="LEFT",
            )
        )

    def violationInfo(citation_info=None):
        if citation_info is None:
            citation_info = {}

        violation = {
            "v_type": citation_info.get("violation_type", None),
            "other": citation_info.get("other_violation_type", ""),
            "violation_date": citation_info.get("violation_date", None),
            "violation_time": citation_info.get("violation_time", None),
            "location": citation_info.get("location", ""),
            "code": citation_info.get("violation_code", ""),
            "description": citation_info.get("violation_description", ""),
            "violation_section": citation_info.get("violation_section", ""),
            "violation_description": citation_info.get("violation_description", ""),
            "speed": citation_info.get("violation_recorded_speed", None),
            "local_ordinance": citation_info.get("local_ordinance", ""),
        }

        bad_values = (None, "", " ")
        violation_datetime = datetime.datetime.combine(
            violation["violation_date"], violation["violation_time"]
        )
        violation["year"] = (
            datetime.datetime.strftime(violation_datetime, "%Y")
            if citation_info["violation_date"] not in bad_values
            else ""
        )
        violation["month"] = (
            datetime.datetime.strftime(violation_datetime, "%m")
            if citation_info["violation_date"] not in bad_values
            else ""
        )
        violation["date"] = (
            datetime.datetime.strftime(violation_datetime, "%d")
            if citation_info["violation_date"] not in bad_values
            else ""
        )
        violation["time"] = (
            datetime.time.strftime(violation_datetime.time(), "%I:%M:%S")
            if citation_info["violation_time"] not in bad_values
            else ""
        )

        bad_values = (None, "", " ")
        citation_info["violation_date"] = (
            datetime.datetime.strftime(violation_datetime, "%Y-%m-%d")
            if citation_info["violation_date"] not in bad_values
            else ""
        )

        story.append(RotatedPara("VIOLATION", style=styles["rotated_detail_violation"]))
        story.append(
            Table(
                [
                    [
                        None,
                        Paragraph(
                            "{cb} LOCAL ORDINANCE".format(
                                cb=_bool_to_checkbox(
                                    violation["v_type"].upper() == "LOCAL ORDINANCE"
                                )
                            ),
                            styles["detail-mini-utc"],
                        ),
                    ],
                    [
                        None,
                        Paragraph(
                            " <b>%s</b>" % violation["violation_section"],
                            styles["detail-mini-utc"],
                        ),
                    ],
                    [
                        None,
                        Paragraph(
                            "MPH: <b>%s</b>" % (violation["speed"] or ""),
                            styles["detail-mini-utc"],
                        ),
                    ],
                    [
                        None,
                        Paragraph(
                            "NATURE OF OFFENSE: <b>%s</b>"
                            % (
                                violation["violation_description"]
                                if violation["violation_description"]
                                else "(None)"
                            ),
                            styles["detail-mini-utc"],
                        ),
                    ],
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    ("VALIGN", (1, 3), (1, 3), "TOP"),
                    ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                ],
                colWidths=(1 * mm, 99 * mm),
                rowHeights=(5 * mm, 4 * mm, 4 * mm, 8 * mm),
                hAlign="LEFT",
            )
        )

    def incidentInfo(citation_info=None):
        if citation_info is None:
            citation_info = {}
        conditions_map = {
            "incident_road_conditions_include_conditions": "CONDITIONS",
            "incident_road_conditions_include_dry": "DRY",
            "incident_road_conditions_include_ice": "ICE",
            "incident_road_conditions_include_sand_mud_dirt": "SAND MUD DIRT",
            "incident_road_conditions_include_snow_or_slush": "SNOW OR SLUSH",
            "incident_road_conditions_include_unknown": "UNKNOWN",
            "incident_road_conditions_include_wet": "WET",
            "incident_road_conditions_includes_other": citation_info[
                "incident_road_conditions_includes_other"
            ],
        }
        conditions_list = conditions_map.keys()

        method_map = {
            "incident_method_includes_accident": "ACCIDENT",
            "incident_method_includes_aircraft": "AIRCRAFT",
            "incident_method_includes_assist_or_other_agency": "ASSIST OR OTHER AGENCY",
            "incident_method_includes_complaint_signed": "COMPLAINT SIGNED",
            "incident_method_includes_detail": "DETAIL",
            "incident_method_includes_hand_held_radar": "HAND HELD RADAR",
            "incident_method_includes_lidar": "LIDAR",
            "incident_method_includes_marked": "MARKED",
            "incident_method_includes_paced": "PACED",
            "incident_method_includes_patrol": "PATROL",
            "incident_method_includes_plain_car": "PLAIN CAR",
            "incident_method_includes_radar": "RADAR",
            "incident_method_includes_vascar": "VASCAR",
            "incident_method_includes_other": citation_info[
                "incident_method_includes_other"
            ],
        }
        method_list = method_map.keys()

        visibility_map = {
            "incident_visibility_conditions_include_clear": "CLEAR",
            "incident_visibility_conditions_include_day": "DAY",
            "incident_visibility_conditions_include_fog_smoke_haze": "FOG_SMOKE_HAZE",
            "incident_visibility_includes_night": "NIGHT",
            "incident_visibility_includes_other": citation_info[
                "incident_visibility_includes_other"
            ],
            "incident_visibility_includes_rain": "RAIN",
            "incident_visibility_includes_severe_cross_wind": "SEVERE_CROSS_WIND",
            "incident_visibility_includes_sleet_hail": "SLEET_HAIL",
            "incident_visibility_includes_snow": "SNOW",
            "incident_visibility_includes_unknown": "UNKNOWN",
        }
        visibility_list = visibility_map.keys()

        incident = {
            "accident_type": citation_info.get("incident_accident_type", ""),
            "report": citation_info.get("complainant_agency_report_number", ""),
            "method": ", ".join(
                [str(method_map[meth]) for meth in method_list if citation_info[meth]]
            ),
            "road_conditions": ", ".join(
                [
                    str(conditions_map[cond])
                    for cond in conditions_list
                    if citation_info[cond]
                ]
            ),
            "visibility": ", ".join(
                [
                    str(visibility_map[vis])
                    for vis in visibility_list
                    if citation_info[vis]
                ]
            ),
            "notations": citation_info.get("incident_accident_notes", ""),
            "complainant_agency_report_number": citation_info[
                "complainant_agency_report_number"
            ],
        }

        if citation_info.get("is_overweight", "") and citation_info.get(
            "incident_private_notes", ""
        ):
            incident["notations"] = citation_info.get("incident_private_notes", "")
        elif citation_info.get("incident_public_narrative", ""):
            incident["notations"] = citation_info.get("incident_public_narrative", "")

        story.append(RotatedPara("INCIDENT", style=styles["rotated_detail_incident"]))
        story.append(
            Table(
                [
                    [
                        Paragraph(
                            "ACCIDENT TYPE: %s" % incident["accident_type"],
                            styles["detail-mini-utc"],
                        ),
                        None,
                        Paragraph(
                            "REPORT #: %s"
                            % incident["complainant_agency_report_number"],
                            styles["detail-mini-utc"],
                        ),
                        None,
                    ],
                    [
                        Paragraph(
                            "METHOD: %s" % incident["method"], styles["detail-mini-utc"]
                        )
                    ],
                    [
                        Paragraph(
                            "ROAD CONDITIONS: %s" % incident["road_conditions"],
                            styles["detail-mini-utc"],
                        ),
                        None,
                        None,
                        None,
                    ],
                    [
                        Paragraph(
                            "VISIBILITY: %s" % incident["visibility"],
                            styles["detail-mini-utc"],
                        ),
                        None,
                        None,
                        None,
                    ],
                    [
                        Paragraph(
                            "NOTATIONS: %s" % incident["notations"],
                            styles["detail-mini-utc"],
                        ),
                        None,
                        None,
                        None,
                    ],
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('SPAN', (0,0), (1,0)),       #reg no
                    ("SPAN", (2, 0), (3, 0)),  # state
                    ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                ],
                colWidths=(50 * mm, 25 * mm, 20 * mm, 5 * mm),
                rowHeights=(4 * mm, 15 * mm, 10 * mm, 12 * mm, 4 * mm),
                hAlign="LEFT",
            )
        )

    def bondInfo(citation_info=None):
        if citation_info is None:
            citation_info = {}
        bond_map = {
            "bond_includes_bond_card": "BOND CARD",
            "bond_includes_cash_bond_full": "CASH_BOND FULL",
            "bond_includes_cash_bond_ten_percent": "CASH BOND TENPERCENT",
            "bond_includes_companion_case": "COMPANION CASE",
            "bond_includes_currency_bond": "CURRENCY BOND",
            "bond_includes_drivers_license_bond": "DRIVERS LICENSE BOND",
            "bond_includes_dui_bond": "DUI BOND",
            "bond_includes_electronic_bond": "ELECTRONIC BOND",
            "bond_includes_individual_bond": "INDIVIDUAL BOND",
            "bond_includes_none": "NONE",
            "bond_includes_notice_to_appear": "NOTICE TO APPEAR",
            "bond_includes_personal_recognizance": "PERSONAL RECOGNIZANCE",
            "bond_includes_promise_to_comply": "PROMISE TO COMPLY",
        }
        bond_list = bond_map.keys()

        bond = {
            "total_bond_posted": citation_info.get("total_bond_amount"),
            "bond_amount": citation_info.get("bond_amount", 0.00),
            "bond_information": ", ".join(
                [bond_map[bonds] for bonds in bond_list if citation_info[bonds]]
            ),
        }

        story.append(RotatedPara("BOND", style=styles["rotated_detail_bond"]))
        story.append(
            Table(
                [
                    [
                        Paragraph(
                            "TOTAL BOND POSTED: <b>%s</b>" % bond["total_bond_posted"],
                            styles["detail-mini-utc"],
                        ),
                        None,
                        None,
                        Paragraph(
                            "BOND AMOUNT: <b>%s</b>" % bond["bond_amount"],
                            styles["detail-mini-utc"],
                        ),
                    ],
                    [
                        Paragraph(
                            "BOND INFORMATION: %s" % bond["bond_information"],
                            styles["detail-mini-utc"],
                        ),
                        None,
                        None,
                        None,
                    ],
                    [
                        Paragraph(
                            "WITHOUT ADMITTING GUILT, I promise to comply with the terms of this Ticket and Release.",
                            styles["detail-mini-utc"],
                        )
                    ],
                    [
                        Paragraph("Signature X:", styles["detail-mini-utc"]),
                        None,
                        None,
                        None,
                    ],
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    ("SPAN", (0, 0), (1, 0)),  # reg no
                    ("SPAN", (0, 1), (2, 1)),
                    ("SPAN", (0, 2), (-1, 2)),
                    ("VALIGN", (0, 2), (0, 2), "TOP"),
                    ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                ],
                colWidths=(30 * mm, 10 * mm, 30 * mm, 30 * mm),
                rowHeights=(4 * mm, 7 * mm, 7 * mm, 4 * mm),
                hAlign="LEFT",
            )
        )

    def courtInfo(citation_info=None):
        if citation_info is None:
            citation_info = {}
        court = {
            "court_location": citation_info.get("hearing_court_address", ""),
            "court_date": citation_info.get("hearing_court_date", None),
            "court_time": citation_info.get("hearing_time", None),
            "court_appearance": citation_info.get("hearing_attendance_required", None),
        }
        court["date"] = (
            datetime.datetime.strftime(court["court_date"], "%m/%d/%Y")
            if court["court_date"] is not None
            else ""
        )
        court["time"] = (
            datetime.time.strftime(court["court_time"], "%I:%M %p")
            if court["court_time"] is not None
            else ""
        )

        story.append(
            RotatedPara(
                "Court Place Date", style=styles["rotated_detail_courtplacedate"]
            )
        )
        story.append(
            Table(
                [
                    [
                        Paragraph(
                            "CIRCUIT COURT LOCATION, DATE AND TIME:",
                            styles["detail-mini-utc"],
                        )
                    ],
                    [
                        Paragraph(
                            "Court location: %s " % court["court_location"],
                            styles["detail-mini-utc-addons"],
                        )
                    ],
                    [
                        Paragraph(
                            "DATE: %s" % court["date"], styles["detail-mini-utc"]
                        ),
                        None,
                        Paragraph(
                            "TIME: %s" % court["time"], styles["detail-mini-utc"]
                        ),
                        None,
                        None,
                    ],
                    [
                        Paragraph(
                            "{cb} COURT APPEARANCE REQUIRED".format(
                                cb=_bool_to_checkbox(court["court_appearance"])
                            ),
                            styles["detail-mini-utc"],
                        )
                    ],
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('ALIGN', (1,-1), (-1,-1),'LEFT'),
                    ("SPAN", (0, 0), (-1, 0)),
                    ("SPAN", (0, 1), (-1, 1)),
                    ("SPAN", (0, -1), (-1, -1)),
                    ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                ],
                colWidths=(18 * mm, 10 * mm, 20 * mm, 20 * mm, 32 * mm),
                rowHeights=(4 * mm, 4 * mm, 4 * mm, 5 * mm),
                hAlign="LEFT",
            )
        )

    def officer_sign(citation_info=None):
        if citation_info is None:
            citation_info = {}
        signature_path = None
        officer = {"badge_number": "testnumber"}
        # TODO: How does .NET handle signatures?
        # if (
        #     officer.get("signature_link", None) is not None
        #     and officer.get("signature_link", None) != ""
        # ):
        #     (
        #         signature_filename,
        #         signature_stream,
        #     ) = db.auth_user.signature_link.retrieve(officer["signature_link"])
        #     temp_path = os.path.join(request.folder, "temp", signature_filename)
        #     shutil.copyfileobj(signature_stream, open(temp_path, "wb"))
        #     signature_path = temp_path

        signatureImage = ""
        if signature_path is not None:
            signatureImage = Image(
                open(signature_path, "rb"), width=60, height=20, kind="proportional"
            )
        story.append(Spacer(1 * mm, 1 * mm))
        story.append(
            Table(
                [[Paragraph("SEE INSTRUCTIONS BELOW", styles["detail-compact-bold"])]],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    ("BOX", (0, 0), (-1, -1), 0.25, colors.black)
                ],
                colWidths=(100 * mm),
                hAlign="LEFT",
            )
        )

        story.append(
            Table(
                [
                    [
                        Paragraph(
                            "Under penalties as provided by law for false certification pursuant to Section 1-109 of the Code of Civil Procedure and perjury pursuant to Section 32-2 of the Criminal Code",
                            styles["detail-mini-utc-left"],
                        )
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
                ],
            )
        )

        signature_table = Table(
            [[signatureImage]],
            [usable_width * 0.003, usable_width * 0.4, usable_width * 0.3],
            style=[
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                # ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
                # ('LINEBELOW', (0, 0), (0, 0), 0.8, colors.black),
                # ('LINEBELOW', (-1, 0), (-1, 0), 0.8, colors.black)
            ],
        )
        citation_info["violation_date_day"] = (
            citation_info["violation_date"].split("-")[2]
            if citation_info["violation_date"] is not None
            else ""
        )
        citation_info["violation_date_month"] = (
            citation_info["violation_date"].split("-")[1]
            if citation_info["violation_date"] is not None
            else ""
        )
        citation_info["violation_date_year"] = (
            citation_info["violation_date"].split("-")[0]
            if citation_info["violation_date"] is not None
            else ""
        )
        # try:
        #     defendant_dob = 'DOB: <b>%s</b>' % defendant['dob'].strftime('%m/%d/%Y')
        # except:
        #     defendant_dob = 'DOB: <b> </b>'
        story.append(
            Table(
                [
                    [
                        Paragraph(
                            "<b>%s</b>" % citation_info["violation_date_month"],
                            styles["detail-mini-utc-left"],
                        ),
                        Paragraph(
                            "<b>%s</b>" % citation_info["violation_date_day"],
                            styles["detail-mini-utc-left"],
                        ),
                        Paragraph(
                            "<b>%s</b>" % citation_info["violation_date_year"],
                            styles["detail-mini-utc-left"],
                        ),
                        # Paragraph('', styles['detail-mini-utc-left']),
                        signature_table,
                        Paragraph(
                            " <b>%s</b>" % officer["badge_number"],
                            styles["detail-mini-utc-left"],
                        ),
                    ],
                    [
                        Paragraph("MONTH ", styles["detail-mini-utc-left"]),
                        Paragraph("DAY", styles["detail-mini-utc-left"]),
                        Paragraph("YEAR", styles["detail-mini-utc-left"]),
                        Paragraph("OFFICER SIGNATURE", styles["detail-mini-utc-left"]),
                        Paragraph("ID", styles["detail-mini-utc-left"]),
                    ],
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    ("LINEABOVE", (0, 1), (-1, -1), 0.25, colors.black),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
                ],
                colWidths=(17 * mm, 15 * mm, 15 * mm, 40 * mm, 15 * mm),
                rowHeights=(5 * mm),
                hAlign="LEFT",
            )
        )

    def complaint_nocourt(citation_info=None):
        if citation_info is None:
            citation_info = {}
        story.append(
            Table(
                [
                    [
                        [
                            Paragraph(
                                "Read These Instructions Carefully",
                                styles["detail-compact-bold"],
                            )
                        ]
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ],
            )
        )
        story.append(
            Table(
                [
                    [
                        [
                            Paragraph(
                                "Your ticket has been marked  {cb}  NO COURT APPEARANCE REQUIRED. You have the following options:".format(
                                    cb=_bool_to_checkbox(
                                        not citation_info["hearing_attendance_required"]
                                    )
                                ),
                                styles["detail-mini-utc-left"],
                            )
                        ]
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ],
            )
        )
        story.append(
            Table(
                [
                    [
                        [
                            Paragraph(
                                '1. If you wish to plead "GUILTY", complete the "PLEA OF <br/> GUILTY AND WAIVER" provided and follow those instructions.<br/> Mail the guilty plea with full payment of fine and costs. <br/>',
                                styles["detail-mini-utc-left"],
                            )
                        ]
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ],
            )
        )
        story.append(Spacer(5 * mm, 5 * mm))

        story.append(
            Table(
                [
                    [
                        [
                            Paragraph(
                                "Fine and Costs<br/> The fine and costs where court appearances are <br/> not required are:<br/>",
                                styles["detail-mini-utc-left"],
                            )
                        ]
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ],
            )
        )
        story.append(
            Table(
                [
                    [
                        None,
                        [
                            Paragraph(
                                "(a) $120.00 for all complaints, except (b)  and (c) below;<br/> (b) $60.00 for seat belt violations cited under 625 ILCS 5/12-603.1;<br/> (c) $140.00 for speeding more than 20 mph but not more than 25 mph over the limit.<br/>",
                                styles["detail-mini-utc-left"],
                            )
                        ],
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ],
                colWidths=(15 * mm, 80 * mm),
                rowHeights=(25 * mm),
                hAlign="LEFT",
            )
        )
        story.append(
            Table(
                [
                    [
                        [
                            Paragraph(
                                "Note: Payment must be by cash, money order, certified check, bank draft, or traveler's check unless otherwise  authorized by the clerk of the court. (DO NOT SEND CASH IN THE MAIL; use cash only if paying in person.)",
                                styles["detail-mini-utc-left"],
                            )
                        ]
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ],
            )
        )
        story.append(Spacer(5 * mm, 5 * mm))
        story.append(Spacer(5 * mm, 5 * mm))

        story.append(
            Table(
                [
                    [
                        [
                            Paragraph(
                                "Bond Information - Failure to Appear",
                                styles["detail-mini-utc-center"],
                            )
                        ]
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ],
            )
        )
        story.append(
            Table(
                [
                    [
                        [
                            Paragraph(
                                'The type of bond that you posted is noted in the "Bond" section. The result of your failure to appear or pay this  ticket is determined by the bond type identified below and whether your ticket is marked "Court Appearance Required"  or "No Court Appearance Required".',
                                styles["detail-mini-utc-left"],
                            )
                        ]
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ],
            )
        )
        story.append(
            Table(
                [[[Paragraph("FULL CASH BOND: ", styles["detail-mini-utc-left"])]]],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ],
            )
        )
        story.append(
            Table(
                [
                    [
                        [
                            Paragraph(
                                "No Court Appearance Required: A judgement may be entered against you for fine, penalties and costs as provided in the NOTICE. ",
                                styles["detail-mini-utc-left"],
                            )
                        ]
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ],
            )
        )
        story.append(
            Table(
                [
                    [
                        [
                            Paragraph(
                                " <b> Notice of Consent for Entry of Judgment </b> <br/> If a driver's license, cash bail, bond certificate or an individual bond was posted or if you were released on a Notice to Appear or Promise to Comply and you were charged with an offense which does not require a court appearance, YOU ARE HEREBY NOTIFIED THAT: ",
                                styles["detail-mini-utc-center"],
                            )
                        ]
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ],
            )
        )
        story.append(
            Table(
                [
                    [
                        [
                            Paragraph(
                                "In the event that you fail to appear in court or answer the charge on the date set for your appearance, or any date to which the case is continued, or you do not submit a written plea of guilty to the clerk at least three (3) days before the date, you thereby consent to the entry of a judgment of conviction against you in the amount of the applicable fine, penalties, and costs. The cash bail or other security deposited will be used to pay the fines, penalties,and costs. If you are an Illinois Driver and you fail to pay in full any judgment imposed, a notice will be sent to the Secretary of State and your driver's license will not be renewed, reissued, or reclassified, until full payment is received.",
                                styles["detail-mini-utc-center"],
                            )
                        ]
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ],
            )
        )

    def courtcomm_nocourt(citation_info=None):
        if citation_info is None:
            citation_info = {}
        story.append(
            Table(
                [[[Paragraph("GUILTY PLEA ", styles["detail-compact-bold"])]]],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ],
            )
        )
        story.append(
            Table(
                [
                    [
                        [
                            Paragraph(
                                "If you intend to plead GUILTY to the ticket and No Court Appearance is Required.",
                                styles["detail-mini-utc-left"],
                            )
                        ]
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ],
            )
        )
        story.append(
            Table(
                [
                    [
                        [
                            Paragraph(
                                '1. Complete this form. <br/>2. Mail this form, together with the fine and costs to the Clerk of the Court, Traffic Section. You must mail this completed form, with all fine and costs, no earlier than ten (10) work days after the ticket was issued (noted on the top half, below "Defendant" section, of the ticket), and no later than three (3) work days before the court appearance date noted on the bottom half of the ticket in the "Court Place/Date" section or as may have been provided by the clerk of the court. <br/>',
                                styles["detail-mini-utc-left"],
                            )
                        ]
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ],
            )
        )
        story.append(
            Table(
                [
                    [
                        [
                            Paragraph(
                                "Fine and Costs<br/> The fine and costs where court appearances are not required are:",
                                styles["detail-mini-utc-left"],
                            )
                        ]
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ],
            )
        )
        story.append(
            Table(
                [
                    [
                        None,
                        [
                            Paragraph(
                                "(a) $120.00 for all complaints, except (b)  and (c) below;<br/> (b) $60.00 for seat belt violations cited under 625 ILCS 5/12-603.1;<br/> (c) $140.00 for speeding more than 20 mph but not more than 25 mph over the limit.<br/>",
                                styles["detail-mini-utc-left"],
                            )
                        ],
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ],
                colWidths=(15 * mm, 80 * mm),
                rowHeights=(25 * mm),
                hAlign="LEFT",
            )
        )
        story.append(
            Table(
                [
                    [
                        [
                            Paragraph(
                                "Note: Payment must be by cash, money order, certified check, bank draft, or traveler's check unless otherwise authorized by the clerk of the court. (DO NOT SEND CASH IN THE MAIL; use cash only if paying in person.)",
                                styles["detail-mini-utc-left"],
                            )
                        ]
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
                ],
            )
        )
        story.append(
            Table(
                [
                    [
                        [
                            Paragraph(
                                "PLEA OF GUILTY AND WAIVER",
                                styles["detail-compact-bold"],
                            )
                        ]
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
                ],
            )
        )
        story.append(
            Table(
                [
                    [
                        [
                            Paragraph(
                                "I, the undersigned, do hereby plead guilty to the charge  noted on this ticket. I understand my right to a trial, that my signature to this plea of guilty will have the same force and effect as a judgment of court and that this record will be sent to the Secretary of State of this state (or of the State where I received my license to drive). I hereby PLEAD GUILTY to the said offense on this ticket, GIVE UP my right to trial, and agree to pay the penalty required. ",
                                styles["detail-mini-utc-left"],
                            )
                        ]
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
                ],
            )
        )
        story.append(
            Table(
                [
                    [
                        [
                            Paragraph(
                                "Defendant's Signature", styles["detail-mini-utc-left"]
                            )
                        ],
                        [Paragraph("Date ", styles["detail-mini-utc-left"])],
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                    ("LINEABOVE", (0, 0), (-1, -1), 0.25, colors.black)
                ],
            )
        )
        story.append(
            Table(
                [
                    [
                        [Paragraph("Mailing Address", styles["detail-mini-utc-left"])],
                        [Paragraph("Street", styles["detail-mini-utc-left"])],
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                    ("LINEABOVE", (0, 0), (-1, -1), 0.25, colors.black)
                ],
            )
        )
        story.append(
            Table(
                [
                    [
                        [Paragraph("City", styles["detail-mini-utc-left"])],
                        [Paragraph("State", styles["detail-mini-utc-left"])],
                        [Paragraph("Zip", styles["detail-mini-utc-left"])],
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    ("LINEABOVE", (0, 0), (-1, -1), 0.25, colors.black),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ],
                # colWidths=(50*mm, 50*mm,50*mm), rowHeights=(4*mm),
                # hAlign='LEFT'
            )
        )

    def violator_nocourt(citation_info=None):  # wrapper
        return complaint_nocourt(citation_info)

    def violator_courtreq(citation_info=None):
        if citation_info is None:
            citation_info = {}
        story.append(
            Table(
                [
                    [
                        [
                            Paragraph(
                                "Read These Instructions Carefully",
                                styles["detail-compact-bold"],
                            )
                        ]
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ],
                rowHeights=(10 * mm),
                hAlign="LEFT",
            )
        )
        story.append(Spacer(2 * mm, 2 * mm))
        story.append(
            Table(
                [
                    [
                        [
                            Paragraph(
                                "Your ticket has been marked {cb} COURT APPEARANCE REQUIRED.You are required to come to court on  the date, time and place noted in the COURT PLACE/DATE section on the ticket.".format(
                                    cb=_bool_to_checkbox(
                                        not citation_info["hearing_attendance_required"]
                                    )
                                ),
                                styles["detail-mini-utc-left"],
                            )
                        ]
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ],
            )
        )
        story.append(Spacer(2 * mm, 2 * mm))
        story.append(
            Table(
                [
                    [
                        [
                            Paragraph(
                                "Bond Information - Failure to Appear",
                                styles["detail-mini-utc-center"],
                            )
                        ]
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ],
            )
        )
        story.append(Spacer(2 * mm, 2 * mm))
        story.append(
            Table(
                [
                    [
                        [
                            Paragraph(
                                'The type of bond that you posted is noted in the "Bond"section. The result of your failure to appear or pay this ticket is determined by the bond type identified below and whether your ticket is marked "Court Appearance Required" or "No Court Appearance Required". ',
                                styles["detail-mini-utc-center"],
                            )
                        ]
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ],
            )
        )
        story.append(Spacer(2 * mm, 2 * mm))
        story.append(
            Table(
                [
                    [
                        [
                            Paragraph(
                                "PROMISE TO COMPLY <br/> A notice of suspension of your driving privileges will be sent to your licensing state; or, a judgment may be entered against you for fine, penalties, and costs as provided in the NOTICE; Or, the court may issue a warrant for your arrest. ",
                                styles["detail-mini-utc-left"],
                            )
                        ]
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ],
            )
        )
        story.append(Spacer(2 * mm, 2 * mm))
        story.append(
            Table(
                [
                    [
                        [
                            Paragraph(
                                "Notice of Consent for Entry of Judgment ",
                                styles["detail-mini-utc-center"],
                            )
                        ]
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ],
            )
        )
        story.append(Spacer(2 * mm, 2 * mm))

        story.append(
            Table(
                [
                    [
                        [
                            Paragraph(
                                " If a driver's license, cash bail, bond certificate or an individual bond was posted or if you were released on a Notice to Appear or Promise to Comply and you were charged with an offense which does not require a court appearance, YOU ARE HEREBY NOTIFIED THAT: ",
                                styles["detail-mini-utc-left"],
                            )
                        ]
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ],
            )
        )
        story.append(Spacer(2 * mm, 2 * mm))
        story.append(
            Table(
                [
                    [
                        [
                            Paragraph(
                                "In the event that you fail to appear in court or answer the charge on the date set for your appearance, or any date to which the case is continued, or you do not submit a written plea of guilty to the clerk at least three (3) days before the date, you thereby consent to the entry of a judgment of conviction against you in the amount of the applicable fine, penalties, and costs. The cash bail or other security deposited will be used to pay the fines, penalties,and costs. If you are an Illinois Driver and you fail to pay in full any judgment imposed, a notice will be sent to the Secretary of State and your driver's license will not be renewed, reissued, or reclassified, until full payment is received.",
                                styles["detail-mini-utc-left"],
                            )
                        ]
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ],
            )
        )

    def complaint_courtreq(citation_info=None):
        if citation_info is None:
            citation_info = {}
        story.append(
            Table(
                [
                    [
                        [
                            Paragraph(
                                "Read These Instructions Carefully",
                                styles["detail-compact-bold"],
                            )
                        ]
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ],
                rowHeights=(10 * mm),
                hAlign="LEFT",
            )
        )
        story.append(Spacer(2 * mm, 2 * mm))
        story.append(
            Table(
                [
                    [
                        [
                            Paragraph(
                                "Your ticket has been marked {cb} COURT APPEARANCE REQUIRED.You are required to come to court on the date, time and place noted in the COURT PLACE/DATE section on the ticket.".format(
                                    cb=_bool_to_checkbox(
                                        not citation_info["hearing_attendance_required"]
                                    )
                                ),
                                styles["detail-mini-utc-left"],
                            )
                        ]
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ],
            )
        )
        story.append(Spacer(2 * mm, 2 * mm))
        story.append(
            Table(
                [
                    [
                        [
                            Paragraph(
                                "Bond Information - Failure to Appear",
                                styles["detail-mini-utc-center"],
                            )
                        ]
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ],
            )
        )
        story.append(Spacer(2 * mm, 2 * mm))
        story.append(
            Table(
                [
                    [
                        [
                            Paragraph(
                                'The type of bond that you posted is noted in the "Bond" section. The result of your failure to appear or pay this ticket is determined by the bond type identified below and whether your ticket is marked "Court Appearance Required" or "No Court Appearance Required". ',
                                styles["detail-mini-utc-center"],
                            )
                        ]
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ],
            )
        )
        story.append(Spacer(2 * mm, 2 * mm))
        story.append(
            Table(
                [
                    [
                        [
                            Paragraph(
                                "PROMISE TO COMPLY <br/> A notice of suspension of your driving privileges will be sent to your licensing state; or, a judgment may be entered against you for fine, penalties, and costs as provided in the NOTICE; Or, the court may issue a warrant for your arrest. ",
                                styles["detail-mini-utc-left"],
                            )
                        ]
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ],
            )
        )
        story.append(Spacer(2 * mm, 2 * mm))
        story.append(
            Table(
                [
                    [
                        [
                            Paragraph(
                                "Notice of Consent for Entry of Judgment ",
                                styles["detail-mini-utc-center"],
                            )
                        ]
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
                ],
            )
        )
        story.append(Spacer(2 * mm, 2 * mm))

        story.append(
            Table(
                [
                    [
                        [
                            Paragraph(
                                " If a driver's license, cash bail, bond certificate or an individual bond was posted or if you were released on a Notice to Appear or Promise to Comply and you were charged with an offense which does not require a court appearance, YOU ARE HEREBY NOTIFIED THAT: ",
                                styles["detail-mini-utc-left"],
                            )
                        ]
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
                ],
            )
        )
        story.append(Spacer(2 * mm, 2 * mm))
        story.append(
            Table(
                [
                    [
                        [
                            Paragraph(
                                "In the event that you fail to appear in court or answer the charge on the date set for your appearance, or any date to which the case is continued, or you do not submit a written plea of guilty to the clerk at least three (3) days beforethe date, you thereby consent to the entry of a judgment of conviction against you in the amount of the applicable fine, penalties, and costs. The cash bail or other security deposited will be used to pay the fines, penalties,and costs. If you are an Illinois Driver and you fail to pay in full any judgment imposed, a notice will be sent to the Secretary of State and your driver's license will not be renewed, reissued, or reclassified, until full payment is received.",
                                styles["detail-mini-utc-left"],
                            )
                        ]
                    ]
                ],
                style=[
                    # ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
                ],
            )
        )

    complaint_info(citation_info)
    defendantInfo(citation_info)
    defendant_addon(citation_info)
    vehicleInfo(citation_info)
    violationplus(citation_info)
    violationInfo(citation_info)
    incidentInfo(citation_info)
    bondInfo(citation_info)
    courtInfo(citation_info)
    officer_sign(citation_info)

    incident_private_notes(story, citation_info)

    if copy_type is None:
        pass
    elif copy_type == "VIOLATOR":
        if citation_info["hearing_attendance_required"] is False:
            violator_nocourt(citation_info)
        else:
            violator_courtreq(citation_info)

    elif copy_type == "COURT COMMUNICATION":
        courtcomm_nocourt(citation_info)

    elif copy_type == "COMPLAINT":
        if citation_info["hearing_attendance_required"] is False:
            complaint_nocourt(citation_info)
        else:
            complaint_courtreq(citation_info)
    else:
        pass

    story.append(KeepTogether(Spacer(0, 0.002 * mm)))

    main_template = PageTemplate(id="main_template", frames=[f_left, f_right])
    doc.addPageTemplates([main_template])
    doc.build(story)

    buff.seek(0)

    return buff
