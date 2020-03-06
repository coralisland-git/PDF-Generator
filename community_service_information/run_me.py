import os
import shutil

from generate_community_service_information import generate_community_service_information

if __name__ == "__main__":
    buff = generate_community_service_information()

    with open(
        os.path.expanduser("~/Desktop/{}.pdf".format("community_service_information")), "wb+"
    ) as output_file:
        shutil.copyfileobj(buff, output_file)

    print("completed")
