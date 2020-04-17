import os
import shutil

from generate_fund_calculations import generate_fund_calculations
from sample_data import funds_calculation_data

if __name__ == "__main__":
    buff = generate_fund_calculations(ignition_data)

    with open(
        os.path.expanduser("~/Desktop/{}.pdf".format("ignition_interlock_exemption")),
        "wb+",
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
