import os
import shutil

from generate_order_and_sentence import generate_order_and_sentence

if __name__ == "__main__":
    buff = generate_order_and_sentence()

    with open(
        os.path.expanduser("~/Desktop/order_and_sentence.pdf"), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
