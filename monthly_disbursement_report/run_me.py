import os
import shutil

from generate_monthly_disbursement_report import generate_monthly_disbursement_report

if __name__ == "__main__":
    buff = generate_monthly_disbursement_report()

    with open(
        os.path.expanduser("~/Desktop/{}.pdf".format("monthly_disbursement_report")), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")