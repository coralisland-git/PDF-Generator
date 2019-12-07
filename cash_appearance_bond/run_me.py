import os
import shutil

from generate_cash_appearance_bond_report import (
    generate_cash_appearance_bond_report
)


if __name__ == "__main__":
    buff = generate_cash_appearance_bond_report()
    with open(
        os.path.expanduser("~/Desktop/cash_appearance_bond_report.pdf"),
        "wb+",
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
