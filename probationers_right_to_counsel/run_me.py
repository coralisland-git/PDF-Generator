import os
import shutil

from generate_probationers_right_to_counsel import generate_probationers_right_to_counsel

if __name__ == "__main__":
    buff = generate_probationers_right_to_counsel()

    with open(
        os.path.expanduser("{}.pdf".format("probationers_right_to_counsel")), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
