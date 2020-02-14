import os
import shutil

from generate_statement_continuation_form import generate_statement_continuation_form

if __name__ == "__main__":
    buff = generate_statement_continuation_form()

    with open(
        os.path.expanduser("~/Desktop/{}.pdf".format("statement_continuation_form")), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
