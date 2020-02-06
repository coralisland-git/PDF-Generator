import os
import shutil

from generate_first_dui_conviction_court_affidavit import generate_first_dui_conviction_court_affidavit

if __name__ == "__main__":
    buff = generate_first_dui_conviction_court_affidavit()

    with open(
        os.path.expanduser("~/Desktop/{}.pdf".format("first_dui_conviction_court_affidavit")), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
