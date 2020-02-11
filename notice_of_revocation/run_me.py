import os
import shutil

from generate_notice_of_revocation import generate_notice_of_revocation

if __name__ == "__main__":
    buff = generate_notice_of_revocation()

    with open(
        os.path.expanduser("~/Desktop/{}.pdf".format("notice_of_revocation")), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
