import json
import os
import shutil
import sys

from illinois_2019_state_citation_formats.generate_pdf import generate_il_state_pdf

if __name__ == "__main__":
    citation_type = sys.argv[1]
    copy_type = sys.argv[2]
    json_path = sys.argv[3]
    file_saving_path = sys.argv[4]

    with open(os.path.abspath(json_path)) as f:
        pdf_data = json.load(f)

    for k, v in pdf_data.iteritems():
        if not v:
            pdf_data[k] = ""

    violation_text = pdf_data["violation_section"]

    if pdf_data["violation_recorded_speed"] or pdf_data["violation_speed_limit"]:
        violation_text += "<br />Speeding {violation_recorded_speed} MPH in a {violation_speed_limit} MPH zone".format(
            violation_recorded_speed=pdf_data["violation_recorded_speed"],
            violation_speed_limit=pdf_data["violation_speed_limit"],
        )

    if citation_type == "traffic":
        with open(os.path.abspath(file_saving_path), "wb+") as output_file:
            pdf = generate_il_state_pdf(
                pdf_data, copy_type=copy_type, violation_text=violation_text
            )
            shutil.copyfileobj(pdf[0], output_file)
            print(
                "{width} by {height}".format(
                    width=pdf[1][0] / 72, height=pdf[1][1] / 72
                )
            )

    # with open(os.path.expanduser("~/Desktop/non_traffic.pdf"), "wb+") as output_file:
    #    shutil.copyfileobj(generate_il_state_pdf(non_traffic_citation), output_file)

    # with open(os.path.expanduser("~/Desktop/overweight.pdf"), "wb+") as output_file:
    #    shutil.copyfileobj(
    #        generate_il_state_pdf(
    #            overweight_citation,
    #            copy_type="VIOLATOR",
    #            extra_title=Municipality().name.upper() + " PD"
    #        ),
    #        output_file
    #    )
