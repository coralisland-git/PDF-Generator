import os
import shutil

from generate_plea_proceeding_rawr import generate_plea_proceeding_rawr

if __name__ == "__main__":
    buff = generate_plea_proceeding_rawr()

    with open(
        os.path.expanduser("~/Desktop/{}.pdf".format("plea_proceeding_rawr")), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
