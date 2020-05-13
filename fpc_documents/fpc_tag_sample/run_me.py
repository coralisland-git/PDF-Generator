import os
import shutil

from generate_fpc_tag_sample import generate_fpc_tag_sample

if __name__ == "__main__":
    buff = generate_fpc_tag_sample()

    with open(
        os.path.expanduser("~/Desktop/{}.pdf".format("fpc_tag_sample")), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
