import os
import shutil

from generate_report_of_conviction import report_of_conviction

if __name__ == "__main__":
    buff = report_of_conviction()

    with open(
        os.path.expanduser("~/Desktop/report_of_conviction.pdf"), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
