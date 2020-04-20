import os
import shutil

from generate_detention_order import generate_detention_order

if __name__ == "__main__":
    buff = generate_detention_order()
    with open(
        os.path.expanduser("~/Desktop/fund_calculations.pdf"), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
