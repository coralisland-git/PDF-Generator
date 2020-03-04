import os
import shutil

from generate_probationers_right_to_counsel import generate_probationers_right_to_counsel

if __name__ == "__main__":
    buff_en, buff_sp = generate_probationers_right_to_counsel()

    with open(
        os.path.expanduser("{}.pdf".format("probationers_right_to_counsel_english")), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff_en, output_file)

    with open(
        os.path.expanduser("{}.pdf".format("probationers_right_to_counsel_spanish")), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff_sp, output_file)

    print("completed")
