import os
import shutil

from generate_general_notice import generate_general_notice

if __name__ == "__main__":
    buff = generate_general_notice()

    with open(
        os.path.expanduser("~/Desktop/{}.pdf".format("general_notice")), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
