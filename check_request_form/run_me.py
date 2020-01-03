import os
import shutil

from generate_check_request_form import generate_check_request_form

if __name__ == "__main__":
    buff = generate_check_request_form()
    with open(
        os.path.expanduser("~/Desktop/check_request_form.pdf"), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
