import os
import shutil

from generate_abstract_of_court_record import generate_abstract_of_court_record

if __name__ == "__main__":
    buff = generate_abstract_of_court_record()

    with open(
        os.path.expanduser("~/Desktop/{}.pdf".format("abstract_of_court_record")), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
