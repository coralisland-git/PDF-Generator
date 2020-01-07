import json
import os
import shutil

from generate_check_request_form import generate_check_request_form

if __name__ == "__main__":
    from sample_data import check_request_form_data

    doc_result = generate_check_request_form(check_request_form_data)
    with open(os.path.expanduser("~/Desktop/check_request_form.pdf"), "wb+") as output_file:
        shutil.copyfileobj(doc_result["document"], output_file)
    with open(os.path.expanduser("~/Desktop/check_request_form.json"), "w+") as output_file:
        output_file.write(json.dumps(doc_result["metadata"], indent=4))

    print("completed")
