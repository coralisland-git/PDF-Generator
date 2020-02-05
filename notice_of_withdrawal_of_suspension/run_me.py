import os
import shutil

from generate_notice_of_withdrawal_of_suspension import generate_notice_of_withdrawal_of_suspension

if __name__ == "__main__":
    buff = generate_notice_of_withdrawal_of_suspension()

    with open(
        os.path.expanduser("~/Desktop/notice_of_withdrawal_of_suspension.pdf"), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
