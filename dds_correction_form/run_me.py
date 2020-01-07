import os
import shutil

from generate_dds_correction_form import generate_dds_correction_form

if __name__ == "__main__":
    buff = generate_dds_correction_form()
    with open(
        os.path.expanduser("~/Desktop/dds_correction_form.pdf"), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
