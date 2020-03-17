import os
import shutil

from generate_judicial_correction_services import generate_judicial_correction_services

if __name__ == "__main__":
    buff = generate_judicial_correction_services()

    with open(
        os.path.expanduser("~/Desktop/{}.pdf".format("judicial_correction_services")), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
