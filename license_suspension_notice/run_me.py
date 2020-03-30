import os
import shutil

from generate_license_suspension_notice import generate_license_suspension_notice

if __name__ == "__main__":
    buff = generate_license_suspension_notice()

    with open(
        os.path.expanduser("~/Desktop/{}.pdf".format("license_suspension_notice")),
        "wb+",
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
