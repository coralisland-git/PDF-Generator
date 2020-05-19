import os
import sys
import json
import shutil
import traceback
from driver_exchange_information import generate_driver_information_exchange_sheet


def create_driver_exchange(path_to_json, pdf_save_path):
    with open(os.path.abspath(path_to_json)) as f:
        json_representation = json.load(f)
    pdf_buffer = generate_driver_information_exchange_sheet(json_representation)
    with open(os.path.abspath(pdf_save_path), "wb+") as output_file:
        shutil.copyfileobj(pdf_buffer, output_file)
    return pdf_save_path


if __name__ == "__main__":
    successful = False
    return_message = "Unable to create PDF with given arguments"
    if len(sys.argv) >= 3:
        try:
            return_message = create_driver_exchange(sys.argv[1], sys.argv[2])
            successful = True
        except:
            exception_type, exception_value, exception_traceback = sys.exc_info()
            return_message = traceback.format_exception(
                exception_type, exception_value, exception_traceback
            )
            successful = False

    response = {"successful": successful, "message": return_message}
    print(json.dumps(response))
