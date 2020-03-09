import os
import shutil

from generate_defendants_right_to_an_attorney import generate_defendants_right_to_an_attorney

if __name__ == "__main__":
    buff = generate_defendants_right_to_an_attorney()

    with open(
        os.path.expanduser("~/Desktop/{}.pdf".format("defendants_right_to_an_attorney")), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
