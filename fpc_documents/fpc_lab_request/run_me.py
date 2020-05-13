import os
import shutil

from generate_fpc_lab_request import generate_fpc_lab_request

if __name__ == "__main__":
    buff = generate_fpc_lab_request()

    with open(
        os.path.expanduser("~/Desktop/{}.pdf".format("fpc_lab_request")), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
