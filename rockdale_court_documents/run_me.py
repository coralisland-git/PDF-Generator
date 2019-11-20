import os
import shutil
import json

from rockdale_court_documents.generate_advisement_acknowledgement_waiver_plea import (
    generate_advisement_acknowledgement_waiver_plea,
)
from rockdale_court_documents.generate_fdo import generate_fdo

if __name__ == "__main__":
    from sample_data import fdo_data, advisement_acknowledgement_waiver_plea_data

    doc_result = generate_fdo(fdo_data)
    with open(os.path.expanduser("~/Desktop/fdo.pdf"), "wb+") as output_file:
        shutil.copyfileobj(doc_result["document"], output_file)
    with open(os.path.expanduser("~/Desktop/fdo.json"), "w+") as output_file:
        output_file.write(json.dumps(doc_result["metadata"], indent=4))

    doc_result = generate_advisement_acknowledgement_waiver_plea(advisement_acknowledgement_waiver_plea_data)
    with open(os.path.expanduser("~/Desktop/advisement_acknowledgement_waiver_plea_data.pdf"), "wb+") as output_file:
        shutil.copyfileobj(doc_result["document"], output_file)
    with open(os.path.expanduser("~/Desktop/advisement_acknowledgement_waiver_plea_data.json"), "w+") as output_file:
        output_file.write(json.dumps(doc_result["metadata"], indent=4))

    print("completed")
