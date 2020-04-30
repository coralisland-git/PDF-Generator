import os
import shutil

from generate_sentence_recommendation import generate_sentence_recommendation

if __name__ == "__main__":
    buff = generate_sentence_recommendation()

    with open(
        os.path.expanduser("~/Desktop/{}.pdf".format("sentence_recommendation")), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
