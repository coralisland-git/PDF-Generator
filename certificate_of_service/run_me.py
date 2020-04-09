import os
import shutil

from generate_certificate_of_service import generate_certificate_of_service
from sample_data import certificate_service_data

if __name__ == "__main__":
    buff = generate_certificate_of_service(certificate_service_data)

    with open(
        os.path.expanduser("~/Desktop/{}.pdf".format("certificate_of_service")), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
