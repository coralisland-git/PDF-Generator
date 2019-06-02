import os
import shutil

from illinois_2019_state_citation_formats.generate_pdf import generate_il_state_pdf

if __name__ == "__main__":
    from sample_data import traffic_citation, non_traffic_citation, overweight_citation

    with open(os.path.expanduser("~/Desktop/traffic.pdf"), "wb+") as output_file:
        shutil.copyfileobj(generate_il_state_pdf(traffic_citation), output_file)

    with open(os.path.expanduser("~/Desktop/non_traffic.pdf"), "wb+") as output_file:
        shutil.copyfileobj(generate_il_state_pdf(non_traffic_citation), output_file)

    with open(os.path.expanduser("~/Desktop/overweight.pdf"), "wb+") as output_file:
        shutil.copyfileobj(generate_il_state_pdf(overweight_citation), output_file)

    print("completed")
