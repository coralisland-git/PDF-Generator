import os
import shutil

from generate_application_for_aoc import generate_application_for_aoc

if __name__ == "__main__":
    buff = generate_application_for_aoc()

    with open(
        os.path.expanduser("~/Desktop/{}.pdf".format("application_for_aoc")), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
