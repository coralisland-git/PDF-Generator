from generate_refund_request import generate_refund_request_english, generate_refund_request_spanish
import json
import os
import shutil

if __name__ == "__main__":
    from sample_data import refund_request_data

    doc_result = generate_refund_request_english(refund_request_data)
    with open(os.path.expanduser("~/Desktop/refund_request_en.pdf"), "wb+") as output_file:
        shutil.copyfileobj(doc_result["document"], output_file)
    with open(os.path.expanduser("~/Desktop/refund_request_en.json"), "w+") as output_file:
        output_file.write(json.dumps(doc_result["metadata"], indent=4))
    doc_result = generate_refund_request_spanish(refund_request_data)
    with open(os.path.expanduser("~/Desktop/refund_request_es.pdf"), "wb+") as output_file:
        shutil.copyfileobj(doc_result["document"], output_file)
    with open(os.path.expanduser("~/Desktop/refund_request_es.json"), "w+") as output_file:
        output_file.write(json.dumps(doc_result["metadata"], indent=4))

    print("completed")
