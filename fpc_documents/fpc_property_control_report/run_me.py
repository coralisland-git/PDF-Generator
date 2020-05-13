import os
import shutil

from generate_fpc_property_control_report import generate_fpc_property_control_report

if __name__ == "__main__":
    buff = generate_fpc_property_control_report()

    with open(
        os.path.expanduser("~/Desktop/{}.pdf".format("fpc_property_control_report")),
        "wb+",
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
