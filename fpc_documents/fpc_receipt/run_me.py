import os
import shutil

from generate_fpc_receipt import generate_fpc_receipt

if __name__ == "__main__":
    buff = generate_fpc_receipt()

    with open(
        os.path.expanduser("~/Desktop/{}.pdf".format("fpc_receipt")), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
