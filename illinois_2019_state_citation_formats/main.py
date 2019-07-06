import json
import os
import shutil
import sys
from datetime import datetime

from generate_pdf import generate_il_state_pdf

if __name__ == "__main__":
    parentPath = os.path.abspath("..")
    if parentPath not in sys.path:
        sys.path.insert(0, parentPath)

    copy_type = sys.argv[1]
    json_path = sys.argv[2]
    file_saving_path = sys.argv[3]

    with open(os.path.abspath(json_path)) as f:
        pdf_data = json.load(f)

    boolean_true = ["T", "Y"]
    boolean_false = ["F", "N"]
    boolean_keys = [
        "bond_includes_bond_card",
        "bond_includes_cash_bond_full",
        "bond_includes_cash_bond_ten_percent",
        "bond_includes_companion_case",
        "bond_includes_currency_bond",
        "bond_includes_drivers_license_bond",
        "bond_includes_dui_bond",
        "bond_includes_electronic_bond",
        "bond_includes_individual_bond",
        "bond_includes_none",
        "bond_includes_notice_to_appear",
        "bond_includes_personal_recognizance",
        "bond_includes_promise_to_comply",
        "complainant_is_municipality",
        "complainant_is_tollway",
        "complainant_is_township_road",
        "defendant_address_street_num_half",
        "defendant_driver_license_is_commercial",
        "defendant_name_is_alias",
        "hearing_attendance_required",
        "incident_method_includes_accident",
        "incident_method_includes_aircraft",
        "incident_method_includes_assist_or_other_agency",
        "incident_method_includes_complaint_signed",
        "incident_method_includes_detail",
        "incident_method_includes_hand_held_radar",
        "incident_method_includes_lidar",
        "incident_method_includes_marked",
        "incident_method_includes_other",
        "incident_method_includes_paced",
        "incident_method_includes_patrol",
        "incident_method_includes_plain_car",
        "incident_method_includes_radar",
        "incident_method_includes_vascar",
        "incident_road_conditions_include_conditions",
        "incident_road_conditions_include_dry",
        "incident_road_conditions_include_ice",
        "incident_road_conditions_include_sand_mud_dirt",
        "incident_road_conditions_include_snow_or_slush",
        "incident_road_conditions_include_unknown",
        "incident_road_conditions_include_wet",
        "incident_road_conditions_includes_other",
        "incident_visibility_conditions_include_clear",
        "incident_visibility_conditions_include_day",
        "incident_visibility_conditions_include_fog_smoke_haze",
        "incident_visibility_includes_night",
        "incident_visibility_includes_other",
        "incident_visibility_includes_rain",
        "incident_visibility_includes_severe_cross_wind",
        "incident_visibility_includes_sleet_hail",
        "incident_visibility_includes_snow",
        "incident_visibility_includes_unknown",
        "is_overweight",
        "is_traffic",
        "vehicle_has_hazardous_materials_indicator",
        "vehicle_is_commercial",
        "vehicle_is_large_passenger_vehicle",
        "violation_is_in_urban_district",
        "violation_street_num_half",
        "weights_functioning_auxiliary_power_unit"
    ]
    date_key_to_skip_converting = 'vehicle_registration_expiration_date'

    for k, v in pdf_data.iteritems():
        if not v:
            pdf_data[k] = ""
        if 'date' in k and v and k != date_key_to_skip_converting:
            try:
                pdf_data[k] = datetime.strptime(v, '%Y-%m-%d').strftime('%m/%d/%Y')
            except ValueError:
                pass
        if 'time' in k and v:
            try:
                pdf_data[k] = datetime.strptime(v, '%H:%M:%S').strftime('%I:%M %p')
            except ValueError:
                pass

    for key in boolean_keys:
        bool_string = pdf_data.get(key, '')
        if bool_string in boolean_true:
            pdf_data[key] = True
        elif bool_string in boolean_false:
            pdf_data[key] = False

    violation_text = pdf_data["violation_section"]

    with open(os.path.abspath(file_saving_path), "wb+") as output_file:
        pdf = generate_il_state_pdf(
            pdf_data,
            copy_type=copy_type,
            violation_text=violation_text
        )
        shutil.copyfileobj(pdf[0], output_file)
        print(
            "{"
            + '"width": {width}, "height": {height}'.format(
                width=pdf[1][0] / 72, height=pdf[1][1] / 72
            )
            + "}"
        )
