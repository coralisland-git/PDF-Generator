import os
import shutil

from generate_cash_appearance_bond import generate_cash_appearance_bond

if __name__ == "__main__":
    buff = generate_cash_appearance_bond()
    with open(
        os.path.expanduser("~/Desktop/gscca_cash_appearance_bond.pdf"), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
