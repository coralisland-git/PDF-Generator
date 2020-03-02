import os
import shutil

from generate_plea_sentence_recommendation_form import generate_plea_sentence_recommendation_form

if __name__ == "__main__":
    buff = generate_plea_sentence_recommendation_form()

    with open(
        os.path.expanduser("~/Desktop/{}.pdf".format("plea_sentence_recommendation_form")), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
