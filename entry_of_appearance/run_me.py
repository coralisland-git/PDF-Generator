import os
import shutil

from generate_entry_of_appearance import generate_entry_of_appearance

if __name__ == "__main__":
    buff = generate_entry_of_appearance()

    with open(
        os.path.expanduser("~/Desktop/{}.pdf".format("entry_of_appearance")), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
