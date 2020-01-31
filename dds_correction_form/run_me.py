from generate_dds_correction_form import generate_dds_correction_form
import json
import os
import shutil

if __name__ == "__main__":
    from sample_data import dds_correction_form_data

    doc_result = generate_dds_correction_form(dds_correction_form_data)
    with open(os.path.expanduser("~/Desktop/dds_correction_form.pdf"), "wb+") as output_file:
        shutil.copyfileobj(doc_result["document"], output_file)
    with open(os.path.expanduser("~/Desktop/dds_correction_form.json"), "w+") as output_file:
        output_file.write(json.dumps(doc_result["metadata"], indent=4))

    print("completed")
