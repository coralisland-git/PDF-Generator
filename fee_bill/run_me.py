import os
import shutil

from generate_fee_bill import generate_fee_bill

if __name__ == "__main__":
    buff = generate_fee_bill()

    with open(
        os.path.expanduser("~/Desktop/fee_bill.pdf"), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
