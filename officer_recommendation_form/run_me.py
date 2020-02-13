import os
import shutil

from generate_officer_recommendation_form import generate_officer_recommendation_form

if __name__ == "__main__":
    buff = generate_officer_recommendation_form()

    with open(
        os.path.expanduser("~/Desktop/{}.pdf".format("officer_recommendation_form")), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
