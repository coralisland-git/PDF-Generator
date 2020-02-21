import os
import shutil

from generate_dvd_request_form import generate_dvd_request_form

if __name__ == "__main__":
    buff = generate_dvd_request_form()

    with open(
        os.path.expanduser("~/Desktop/{}.pdf".format("DVD Request Form")), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
