import os
import shutil

from generate_municipal_court_caseload_report import generate_municipal_court_caseload_report

if __name__ == "__main__":
    buff = generate_municipal_court_caseload_report()

    with open(
        os.path.expanduser("~/Desktop/{}.pdf".format("municipal_court_caseload_report")), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
