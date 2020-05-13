import os
import shutil

from generate_fpc_c_and_d_order import generate_fpc_c_and_d_order

if __name__ == "__main__":
    buff = generate_fpc_c_and_d_order()

    with open(
        os.path.expanduser("~/Desktop/{}.pdf".format("fpc_c_and_d_order")), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
