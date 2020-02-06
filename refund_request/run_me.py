import os
import shutil

from generate_refund_request import generate_refund_request_english, generate_refund_request_spanish

if __name__ == "__main__":
    buff = generate_refund_request_english()  # < - To switch between spanish/english switch this function

    with open(
        os.path.expanduser("~/Desktop/refund_request.pdf"), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
