import os
import shutil

from generate_county_drug_abuse_treatment_and_education_fund import generate_county_drug_abuse_treatment_and_education_fund
if __name__ == "__main__":
    buff = generate_county_drug_abuse_treatment_and_education_fund()

    with open(
        os.path.expanduser("~/Desktop/{}.pdf".format("county_drug_abuse_treatment_and_education_fund")), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
