import json
import os
import shutil
import sys

from datetime import datetime, date, time
from illinois_2019_state_citation_formats.generate_pdf import generate_il_state_pdf

if __name__ == "__main__":
    citation_type = sys.argv[1]
    copy_type = sys.argv[2]
    # pdf_data = json.loads(sys.argv[3])

    # test code
    from sample_data import traffic_citation

    for k, v in traffic_citation.iteritems():
        if isinstance(v, datetime) or isinstance(v, date):
            traffic_citation[k] = v.strftime("%Y-%m-%d")
        if isinstance(v, time):
            traffic_citation[k] = v.strftime("%H:%M:%S")

    pdf_data = json.loads(json.dumps(traffic_citation))

    violation_text = "Chapter...Act...Section<br />Input Area<br />More Lines" # needs change

    if citation_type == "traffic":
        with open(os.path.expanduser("~/Desktop/traffic.pdf"), "wb+") as output_file:
            shutil.copyfileobj(
                generate_il_state_pdf(
                    pdf_data, copy_type=copy_type, violation_text=violation_text
                ),
                output_file,
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
