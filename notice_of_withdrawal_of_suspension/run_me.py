from generate_notice_of_withdrawal_of_suspension import generate_notice_of_withdrawal_of_suspension
import json
import os
import shutil

if __name__ == "__main__":
    from sample_data import notice_data

    doc_result = generate_notice_of_withdrawal_of_suspension(notice_data)
    with open(os.path.expanduser("~/Desktop/notice_of_withdrawal_of_suspension.pdf"), "wb+") as output_file:
        shutil.copyfileobj(doc_result["document"], output_file)
    with open(os.path.expanduser("~/Desktop/notice_of_withdrawal_of_suspension.json"), "w+") as output_file:
        output_file.write(json.dumps(doc_result["metadata"], indent=4))

    print("completed")
