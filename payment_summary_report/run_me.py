import os
import shutil

from generate_payment_summary_report import generate_payment_summary_report

if __name__ == "__main__":
    buff = generate_payment_summary_report()

    with open(
        os.path.expanduser("~/Desktop/{}.pdf".format("payment_summary_report")), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
