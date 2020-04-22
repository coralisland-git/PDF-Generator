import os
import sys
import json
import shutil
from driver_exchange_information import generate_driver_information_exchange_sheet

def create_driver_exchange(path_to_json, pdf_save_path):
    with open(os.path.abspath(path_to_json)) as f:
        json_representation = json.load(f)
    pdfBuffer = generate_driver_information_exchange_sheet(json_representation)
    with open(os.path.abspath(pdf_save_path), "wb+") as output_file:
        shutil.copyfileobj(pdfBuffer, output_file)
    return pdf_save_path


if __name__ == "__main__":	
    parentPath = os.path.abspath("..")
    if parentPath not in sys.path:
        sys.path.insert(0, parentPath)

    successful = False
    return_message = "Unable to create PDF with given arguments"
    if sys.argv.count >= 3:
        try:
            return_message = create_driver_exchange(sys.argv[1], sys.argv[2])
            successful = True
        except:
            e = sys.exc_info()[0]
            return_message = e
            successful = False

    response = {
        "successful": successful,
        "message": return_message
    }
    print(json.dumps(response))
