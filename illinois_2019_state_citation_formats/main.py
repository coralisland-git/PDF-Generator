import json
import os
import shutil
import sys

from generate_pdf import generate_il_state_pdf

if __name__ == "__main__":
    parentPath = os.path.abspath("..")
    if parentPath not in sys.path:
        sys.path.insert(0, parentPath)

    citation_type = sys.argv[1]
    copy_type = sys.argv[2]
    json_path = sys.argv[3]
    file_saving_path = sys.argv[4]

    with open(os.path.abspath(json_path)) as f:
        pdf_data = json.load(f)

    boolean_true = ["T", "Y"]
    boolean_false = ["F", "N"]

    for k, v in pdf_data.iteritems():
        if not v:
            pdf_data[k] = ""
        if v in boolean_true:
            pdf_data[k] = True
        if v in boolean_false:
            pdf_data[k] = False

    violation_text = pdf_data["violation_section"]

    if citation_type == "traffic":
        if pdf_data["violation_recorded_speed"] or pdf_data["violation_speed_limit"]:
            violation_text += "<br />Speeding {violation_recorded_speed} MPH in a {violation_speed_limit} MPH zone".format(
                violation_recorded_speed=pdf_data["violation_recorded_speed"],
                violation_speed_limit=pdf_data["violation_speed_limit"],
            )
        with open(os.path.abspath(file_saving_path), "wb+") as output_file:
            pdf = generate_il_state_pdf(
                pdf_data, copy_type=copy_type, violation_text=violation_text
            )
            shutil.copyfileobj(pdf[0], output_file)
            print(
                "{"
                + '"width": {width}, "height": {height}'.format(
                    width=pdf[1][0] / 72, height=pdf[1][1] / 72
                )
                + "}"
            )
            
    if citation_type == "non_traffic":
        with open(os.path.abspath(file_saving_path), "wb+") as output_file:
            pdf = generate_il_state_pdf(
                pdf_data, copy_type=copy_type, violation_text=violation_text
            )
            shutil.copyfileobj(pdf[0], output_file)
            print(
                "{"
                + '"width": {width}, "height": {height}'.format(
                    width=pdf[1][0] / 72, height=pdf[1][1] / 72
                )
                + "}"
            )

    if citation_type == "overweight":
        with open(os.path.abspath(file_saving_path), "wb+") as output_file:
            pdf = generate_il_state_pdf(
                pdf_data,
                copy_type=copy_type,
                overweight_text=pdf_data["ticket_number"],
                extra_title=sys.argv[5],
            )
            shutil.copyfileobj(pdf[0], output_file)
            print(
                "{"
                + '"width": {width}, "height": {height}'.format(
                    width=pdf[1][0] / 72, height=pdf[1][1] / 72
                )
                + "}"
            )
