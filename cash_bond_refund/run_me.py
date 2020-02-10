###### run_me.py ######
import os
import shutil

from generate_cash_bond_refund import generate_cash_bond_refund

if __name__ == "__main__":
    buff = generate_cash_bond_refund()

    with open(
        os.path.expanduser("~/Desktop/{}.pdf".format("cash_bond_refund")), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
