import json
import os
import shutil

from generate_order_and_sentence import generate_order_and_sentence

if __name__ == "__main__":
    from sample_data import order_and_sentence_data

    doc_result = generate_order_and_sentence(order_and_sentence_data)
    with open(os.path.expanduser("~/Desktop/order_and_sentence.pdf"), "wb+") as output_file:
        shutil.copyfileobj(doc_result["document"], output_file)
    with open(os.path.expanduser("~/Desktop/order_and_sentence.json"), "w+") as output_file:
        output_file.write(json.dumps(doc_result["metadata"], indent=4))

    print("completed")
