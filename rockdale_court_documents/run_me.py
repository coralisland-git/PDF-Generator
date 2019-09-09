import os
import shutil

from rockdale_court_documents.generate_advisement_acknowledgement_waiver_plea import (
    generate_advisement_acknowledgement_waiver_plea,
)
from rockdale_court_documents.generate_fdo import generate_fdo

if __name__ == "__main__":
    from sample_data import fdo_data, advisement_acknowledgement_waiver_plea_data

    with open(os.path.expanduser("~/Desktop/fdo.pdf"), "wb+") as output_file:
        shutil.copyfileobj(generate_fdo(fdo_data), output_file)

    with open(
        os.path.expanduser("~/Desktop/advisement_acknowledgement_waiver_plea_data.pdf"),
        "wb+",
    ) as output_file:
        shutil.copyfileobj(
            generate_advisement_acknowledgement_waiver_plea(
                advisement_acknowledgement_waiver_plea_data
            ),
            output_file,
        )

    print("completed")
